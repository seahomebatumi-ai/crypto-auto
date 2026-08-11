#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
СТЕНД БЭКТЕСТА СКОРИНГА  —  SYSTEM_MAP §10 п.1
==============================================================================
Отвечает на ОДИН вопрос: сортирует ли scoreCandidate внимание лучше, чем монетка.
НЕ даёт права крутить веса (это было бы переобучение) — только вердикт
«работает / шум / инвертирован».

ГЛАВНЫЙ ИНВАРИАНТ СТЕНДА: ноль копий продакшн-математики.
  • scoreCandidate + has/clamp01/sigmaDay/volRegime + EFF_TREND/PACE_Z/VOL_ABNORMAL
    вырезаются ИЗ HTML при каждом запуске и исполняются настоящим движком (node).
  • cur/min/max/volatility/eff14/r7/r14/r30/vol7/vol_ratio считаются кодом,
    вырезанным ИЗ get_token_betas бота (AST), включая window_stats/window_vol/
    volume_expansion — теми же функциями, что писали coeffs.json.
Правка любого из двух файлов автоматически меняет стенд. Расхождению взяться неоткуда.

РЕЖИМЫ
  --selftest              офлайн: синтетика с известным ответом (проверка стенда)
  --fetch --years 2       разовая закачка CoinGecko в кэш (нужен COINGECKO_API_KEY)
  --run                   прогон по кэшу
  --run --quality-const   чувствительность: ранг/оборот берутся СЕГОДНЯШНИЕ
                          (в них зашит взгляд в будущее — только для сравнения)
==============================================================================
"""

import os, re, ast, sys, json, time, math, argparse, subprocess, textwrap, bisect
import numpy as np

HOUR_MS = 3600 * 1000
DAY_MS = 86400 * 1000

HERE = os.path.dirname(os.path.abspath(__file__))
DEF_HTML = os.path.join(HERE, "Скрипт_Код_CriptoCalculator.html")
DEF_BOT = os.path.join(HERE, "Код_для_Bota_на_GitHub.py")
CACHE = os.path.join(HERE, "cache")

# ─────────────────────────────────────────────────────────────────────────────
# 1. ВЫРЕЗКА JS: scoreCandidate и его зависимости — из HTML, без копий
# ─────────────────────────────────────────────────────────────────────────────
JS_FUNCS = ["has", "clamp01", "sigmaDay", "volRegime", "scoreCandidate"]
JS_VARS = ["EFF_TREND", "PACE_Z", "VOL_ABNORMAL"]


def _skip_to_matching_brace(s, i):
    """i указывает на '{'. Возвращает индекс ПОСЛЕ парной '}'.
    Пропускает строки '..' ".." и комментарии // /* */ — иначе '}' внутри
    строки развалила бы вырезку."""
    depth = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c in "'\"":
            q = c
            i += 1
            while i < n and s[i] != q:
                i += 2 if s[i] == "\\" else 1
            i += 1
            continue
        if c == "/" and i + 1 < n and s[i + 1] == "/":
            while i < n and s[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and s[i + 1] == "*":
            i = s.find("*/", i + 2) + 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("незакрытая функция")


def extract_js(html_path):
    src = open(html_path, encoding="utf-8").read()
    out = []
    for name in JS_FUNCS:
        m = re.search(r"\nfunction\s+" + name + r"\s*\(", src)
        if not m:
            raise ValueError("в HTML не найдена функция " + name)
        b = src.index("{", m.end())
        out.append(src[m.start() + 1:_skip_to_matching_brace(src, b)])
    for name in JS_VARS:
        m = re.search(r"\nvar\s+" + name + r"\s*=\s*([^;\n]+);", src)
        if not m:
            raise ValueError("в HTML не найдена константа " + name)
        out.append("var " + name + " = " + m.group(1).strip() + ";")
    return "\n".join(out)


JS_DRIVER = r"""
var fs = require('fs');
var cachedFunding = {};
__EXTRACTED__
var job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
var out = [];
for (var i = 0; i < job.length; i++) {
    var j = job[i];
    cachedFunding = {};
    if (j.fr !== null && j.fr !== undefined) cachedFunding[j.sym] = j.fr;
    var r = null;
    try { r = scoreCandidate(j.cd, j.sym, j.cur, j.p24, j.qv, j.isLong); } catch (e) { r = null; }
    out.push(r === null ? null : r.score);
}
fs.writeFileSync(process.argv[3], JSON.stringify(out));
"""


class JsScorer:
    """Пакетный вызов настоящего scoreCandidate одним процессом node."""

    def __init__(self, html_path):
        self.path = os.path.join(HERE, "_score_bridge.js")
        open(self.path, "w", encoding="utf-8").write(
            JS_DRIVER.replace("__EXTRACTED__", extract_js(html_path)))
        r = subprocess.run(["node", "--check", self.path], capture_output=True)
        if r.returncode:
            raise RuntimeError("node --check провалился:\n" + r.stderr.decode())

    def score(self, jobs):
        fi = os.path.join(HERE, "_job.json")
        fo = os.path.join(HERE, "_out.json")
        json.dump(jobs, open(fi, "w"), allow_nan=False)
        r = subprocess.run(["node", self.path, fi, fo], capture_output=True)
        if r.returncode:
            raise RuntimeError("node упал: " + r.stderr.decode()[:800])
        return json.load(open(fo))


# ─────────────────────────────────────────────────────────────────────────────
# 2. ВЫРЕЗКА PYTHON: блок метрик монеты — из get_token_betas бота, без копий
# ─────────────────────────────────────────────────────────────────────────────
def extract_bot_block(bot_path):
    src = open(bot_path, encoding="utf-8").read()
    lines = src.splitlines()
    tree = ast.parse(src)

    fns = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in (
                "window_stats", "window_vol", "volume_expansion"):
            fns[node.name] = "\n".join(lines[node.lineno - 1:node.end_lineno])
    if len(fns) != 3:
        raise ValueError("в боте не найдены window_stats/window_vol/volume_expansion")

    gtb = next(n for n in tree.body
               if isinstance(n, ast.FunctionDef) and n.name == "get_token_betas")
    tryn = next(n for n in gtb.body if isinstance(n, ast.Try))
    stop = next(st for st in tryn.body
                if isinstance(st, ast.Assign)
                and getattr(st.targets[0], "id", "") == "coin_buckets")
    block = textwrap.dedent(
        "\n".join(lines[tryn.body[0].lineno - 1:stop.lineno - 1]))

    ns = {"np": np}
    exec("\n\n".join(fns.values()), ns)
    return compile(block, "<bot-block>", "exec"), ns


class CdBuilder:
    """Собирает запись coeffs.json на момент t тем же кодом, что и бот."""

    def __init__(self, bot_path):
        self.code, self.ns = extract_bot_block(bot_path)

    def build(self, prices, volumes, i, pts=None, vts=None):
        """prices/volumes: списки [ts_ms, value] по возрастанию; i — индекс «сейчас».
        pts/vts — заранее посчитанные метки времени (иначе прогон квадратичен
        по длине истории). Кэшировать их по id(list) НЕЛЬЗЯ: Python переиспользует
        id освобождённых объектов, и на втором посеве кэш отдал бы чужой ряд.
        Берётся ровно скользящее окно 90 дней, как у бота из /market_chart?days=90."""
        t_end = prices[i][0]
        cut = t_end - 90 * DAY_MS
        if pts is None:
            pts = [p[0] for p in prices]
        lo = bisect.bisect_left(pts, cut, 0, i + 1)
        seg = prices[lo:i + 1]
        if len(seg) < 200:
            return None
        segv = None
        if volumes:
            if vts is None:
                vts = [v[0] for v in volumes]
            segv = volumes[bisect.bisect_left(vts, cut):bisect.bisect_right(vts, t_end)]

        g = dict(self.ns)
        g.update({"c_data": {"prices": seg, "total_volumes": segv},
                  "debug": {}, "np": np})
        exec(self.code, g)
        return {
            "min_price": g["min_p"], "max_price": g["max_p"],
            "price_pos": float(g["price_pos"]), "volatility": g["volatility"],
            "r7": g["r7"], "r14": g["r14"], "r30": g["r30"],
            "min30": g["mn30"], "max30": g["mx30"], "vol7": g["vol7"],
            "eff14": g["eff14"], "vol_ratio": g["vratio"],
            "rank": None, "rank_prev": None, "fdv_mc": None,
        }


# ─────────────────────────────────────────────────────────────────────────────
# 3. ДВИЖОК ПРОГОНА
# ─────────────────────────────────────────────────────────────────────────────
def spearman(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    if len(a) < 4:
        return None
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean()
    rb -= rb.mean()
    d = math.sqrt(float((ra ** 2).sum()) * float((rb ** 2).sum()))
    return float((ra * rb).sum() / d) if d > 0 else None


def block_bootstrap_ci(x, n=4000, block=3, seed=7, level=95.0):
    """ДИ среднего по ряду дат. Блоки — против автокорреляции соседних недель."""
    x = np.asarray([v for v in x if v is not None], float)
    if len(x) < 5:
        return (None, None)
    rng = np.random.default_rng(seed)
    nb = int(math.ceil(len(x) / block))
    means = np.empty(n)
    for k in range(n):
        st = rng.integers(0, max(1, len(x) - block + 1), nb)
        means[k] = np.concatenate([x[s:s + block] for s in st])[:len(x)].mean()
    a = (100.0 - level) / 2.0
    return (float(np.percentile(means, a)), float(np.percentile(means, 100 - a)))


def run_walk(series, cdb, scorer, horizon_d=7, step_d=7, warm_d=90,
             quality_const=None, verbose=True):
    """series: {sym: {'prices': [[ts,p]...], 'volumes': [[ts,v]...]}} — часовой шаг.
    Возвращает список наблюдений по датам."""
    syms = sorted(series)
    ts = {s: np.array([p[0] for p in series[s]["prices"]]) for s in syms}
    px = {s: np.array([p[1] for p in series[s]["prices"]]) for s in syms}
    pts = {s: [p[0] for p in series[s]["prices"]] for s in syms}
    vts = {s: [v[0] for v in series[s]["volumes"]] for s in syms}

    # Панель НЕСБАЛАНСИРОВАНА, и это штатно: LIT торгуется с августа 2026.
    # Границы по max(начало)/min(конец) обрезали бы весь прогон до истории самой
    # молодой монеты — сетка строится по объединению, а на каждую дату монета
    # входит, только если у неё есть 90 дней позади и полный горизонт впереди.
    t0 = min(ts[s][0] for s in syms) + warm_d * DAY_MS
    t1 = max(ts[s][-1] for s in syms) - horizon_d * DAY_MS
    if t1 <= t0:
        raise ValueError("истории не хватает даже на одну дату")
    grid = list(range(int(t0), int(t1) + 1, step_d * DAY_MS))

    dates = []
    for t in grid:
        jobs, meta = [], []
        for s in syms:
            i = int(np.searchsorted(ts[s], t, "right")) - 1
            if i < 100 or abs(ts[s][i] - t) > 6 * HOUR_MS:
                continue
            j24 = int(np.searchsorted(ts[s], t - DAY_MS, "right")) - 1
            iF = int(np.searchsorted(ts[s], t + horizon_d * DAY_MS, "right")) - 1
            # Ряд оборвался внутри горизонта -> доходность вышла бы за более
            # короткий срок и тихо попала в общую выборку. Такую монету не берём.
            if iF <= i or ts[s][iF] < t + horizon_d * DAY_MS - 12 * HOUR_MS:
                continue
            cd = cdb.build(series[s]["prices"], series[s]["volumes"], i, pts[s], vts[s])
            if cd is None:
                continue
            if quality_const:
                cd["rank"] = quality_const.get(s, {}).get("rank")
                cd["rank_prev"] = cd["rank"]
            cur = float(px[s][i])
            p24 = float(px[s][i] / px[s][j24] - 1) * 100 if j24 >= 0 and px[s][j24] > 0 else None
            qv = (quality_const or {}).get(s, {}).get("qv")
            path = px[s][i:iF + 1]
            meta.append({
                "sym": s, "cur": cur,
                "fwd": float(path[-1] / cur - 1),
                "mae_long": float(path.min() / cur - 1),
                "mae_short": float(path.max() / cur - 1),
                # факторы-одиночки для сравнения с композитом
                "f_low": -float((cur - cd["min_price"]) / cur) / (cd["volatility"] * math.sqrt(24) or 1e-9),
                "f_r7": cd["r7"] if cd["r7"] is not None else 0.0,
            })
            # Абляция «без штрафов»: eff14 и p24 сняты, поэтому множители
            # «падает прямой линией» и «нож ещё летит» физически не могут
            # сработать. Сама функция НЕ трогается — отсутствие полей это
            # штатный путь продакшна (инвариант 9).
            cdA = dict(cd); cdA["eff14"] = None
            for cdx, pl, is_long in ((cd, p24, True), (cd, p24, False),
                                     (cdA, None, True)):
                jobs.append({"cd": cdx, "sym": s, "cur": cur, "p24": pl,
                             "qv": qv, "isLong": is_long, "fr": None})
        if len(meta) < 8:
            continue
        sc = scorer.score(jobs)
        for k, m in enumerate(meta):
            m["long"] = sc[3 * k]
            m["short"] = sc[3 * k + 1]
            m["long_nopen"] = sc[3 * k + 2]
        fw = np.array([m["fwd"] for m in meta])
        for m in meta:
            m["exc"] = m["fwd"] - float(fw.mean())
        dates.append({"t": t, "coins": meta})
        if verbose and len(dates) % 10 == 0:
            print("  дат посчитано: %d" % len(dates), flush=True)
    return dates


def metrics(dates, key="long", sgn=1.0, topn=3, level=95.0):
    """sgn = +1 лонг (хотим рост), −1 шорт (хотим падение).
    Цель — ИЗБЫТОЧНАЯ доходность к среднему по списку: счёт решает задачу
    «какую из 28 взять», а не «куда пойдёт рынок»."""
    mkey = "mae_long" if sgn > 0 else "mae_short"
    ic, top, base_low, base_r7, rnd, rndtop, ncoins = [], [], [], [], [], [], []
    rng = np.random.default_rng(11)
    mae_b = {0: [], 1: [], 2: []}
    for d in dates:
        cs = [c for c in d["coins"] if c.get(key) is not None]
        if len(cs) < 8:
            continue
        y = np.array([sgn * c["exc"] for c in cs])
        s = np.array([c[key] for c in cs])
        ic.append(spearman(s, y)); ncoins.append(len(cs))
        base_low.append(spearman(np.array([c["f_low"] for c in cs]), y))
        base_r7.append(spearman(np.array([-c["f_r7"] for c in cs]), y))
        p = rng.permutation(s)
        rnd.append(spearman(p, y))
        o = np.argsort(-s)
        top.append(float(y[o[:topn]].mean() - y.mean()))
        op = np.argsort(-p)
        rndtop.append(float(y[op[:topn]].mean() - y.mean()))
        q = max(1, len(cs) // 3)
        for b, idx in enumerate((o[:q], o[q:len(cs) - q], o[len(cs) - q:])):
            mae_b[b] += [cs[i][mkey] for i in idx]
    icv = [v for v in ic if v is not None]
    mn = lambda a: float(np.mean([v for v in a if v is not None])) if a else None
    return {
        "n_dates": len(icv), "n_coins": mn(ncoins),
        "ic_mean": mn(icv), "ic_ci": block_bootstrap_ci(icv, level=level),
        "ic_se": float(np.std(icv, ddof=1) / math.sqrt(len(icv))) if len(icv) > 2 else None,
        "top_mean": mn(top), "top_ci": block_bootstrap_ci(top),
        "base_low": mn(base_low), "base_r7": mn(base_r7),
        "random": mn(rnd), "random_top": mn(rndtop),
        "mae": {b: float(np.median(v)) if v else None for b, v in mae_b.items()},
    }


def verdict(m):
    """Правило РЕГИСТРИРУЕТСЯ ДО прогона. Менять его после — подгонка."""
    if m["ic_mean"] is None:
        return "НЕТ ДАННЫХ"
    lo, hi = m["ic_ci"]
    if lo is not None and lo > 0 and m["ic_mean"] >= 0.05:
        return "РАБОТАЕТ — счёт сортирует внимание лучше монетки"
    if hi is not None and hi < 0 and m["ic_mean"] <= -0.02:
        return "ИНВЕРТИРОВАН — счёт вреден, гасить"
    return "ШУМ — от монетки не отличим"


def report(title, m):
    print("\n" + "═" * 62)
    print(title)
    print("═" * 62)
    print("дат (независимых наблюдений): %d · монет на дату в среднем %.1f"
          % (m["n_dates"], m["n_coins"] or float("nan")))
    if m["ic_mean"] is None:
        print("нет данных")
        return
    print("IC (ранговая связь счёт↔будущее): %+.3f  ДИ95 [%+.3f; %+.3f]  SE %.3f"
          % (m["ic_mean"], m["ic_ci"][0] or float("nan"),
             m["ic_ci"][1] or float("nan"), m["ic_se"] or float("nan")))
    print("   контроль: перемешанный счёт %+.3f (обязан быть ≈0)" % m["random"])
    print("   фактор «у мин90» как сигнал этой стороны  %+.3f" % (m["base_low"] or float("nan")))
    print("   фактор «упал за 7д» как сигнал этой стороны %+.3f" % (m["base_r7"] or float("nan")))
    print("ТОП-3 минус среднее по списку: %+.2f%%  ДИ95 [%+.2f%%; %+.2f%%]  (случайный выбор %+.2f%%)"
          % (100 * m["top_mean"], 100 * (m["top_ci"][0] or float("nan")),
             100 * (m["top_ci"][1] or float("nan")), 100 * m["random_top"]))
    print("медиана худшей просадки внутри окна: топ %+.1f%% · середина %+.1f%% · низ %+.1f%%"
          % tuple(100 * (m["mae"][b] or float("nan")) for b in (0, 1, 2)))
    print("ВЕРДИКТ: " + verdict(m))


# ─────────────────────────────────────────────────────────────────────────────
# 3b. РЕЖИМ РЫНКА — правило зарегистрировано ДО прогона (одобрено 11.08.2026)
# ─────────────────────────────────────────────────────────────────────────────
# ТРЕНД = наклон 90-дневной регрессии BTC значимо отличается от нуля.
#         Иначе — ДИАПАЗОН.
# Реализация: МНК log(цена) по номеру дня на 90 ДНЕВНЫХ закрытиях, ошибка
# наклона по Ньюи–Уэсту (поправка на автокорреляцию остатков), лаг по
# автоматическому правилу L = floor(4*(n/100)^(2/9)) = 3. |t| > 1.96 -> тренд.
# Почему по дневным, а не по 2160 часовым: на часовых остатки так
# автокоррелированы, что наивный t-стат объявил бы трендом почти каждую дату,
# и деление выродилось бы. Лаг взят по стандартному правилу, а не подобран.
#
# ПЛАНКА ВЕРДИКТА ПОДНЯТА: проверок теперь две вместо одной, поэтому
# требуется |IC| >= 0.10 (вдвое против исходных 0.05) И доверительный
# интервал 99% (поправка Бонферрони), не задевающий ноль.
# ГЛАВНАЯ проверка одна: ЛОНГ, горизонт 7 дней. Всё остальное — разведка
# без вердикта, потому что каждая лишняя ячейка удешевляет любую находку.
REG_T = 1.96
REG_BAR = 0.10
REG_LEVEL = 99.0


def _hac_slope_t(y, L=3):
    """Наклон и его t-статистика с ошибкой Ньюи–Уэста."""
    n = len(y)
    X = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X.dot(b)
    xi = X * e[:, None]
    S = xi.T.dot(xi)
    for l in range(1, L + 1):
        w = 1.0 - l / (L + 1.0)
        G = xi[l:].T.dot(xi[:-l])
        S = S + w * (G + G.T)
    XtXi = np.linalg.inv(X.T.dot(X))
    V = XtXi.dot(S).dot(XtXi)
    se = math.sqrt(max(V[1, 1], 1e-30))
    return float(b[1]), float(b[1] / se)


def _trend_stat(logp):
    """ТРЕНД vs ДИАПАЗОН по 90 дневным закрытиям BTC.

    Почему НЕ наивная регрессия уровня по времени: цена — процесс со
    случайным блужданием, и МНК по её уровню порождает «значимый» наклон
    из ничего. Замер на синтетике: чистое блуждание объявлялось трендом
    в 70% случаев даже с поправкой Ньюи–Уэста, деление вырождалось.
    Правильно сформулированный тот же вопрос — значим ли снос: наклон
    оценивается по ДОХОДНОСТЯМ (они почти независимы), t = μ·√n/σ.
    Под нулевой гипотезой даёт положенные ~5% ложных срабатываний.

    Замена сделана ДО касания реальных данных, по синтетическому контролю,
    а не после того, как результат не понравился."""
    r = np.diff(logp)
    n = len(r)
    sd = float(np.std(r, ddof=1))
    if n < 30 or sd <= 0:
        return None, None
    mu = float(np.mean(r))
    return mu, mu * math.sqrt(n) / sd


def btc_regimes(btc, times):
    """Метка режима на каждую дату прогона."""
    ts = np.array([p[0] for p in btc["prices"]])
    px = np.array([p[1] for p in btc["prices"]])
    out = {}
    for t in times:
        i = int(np.searchsorted(ts, t, "right")) - 1
        lo = int(np.searchsorted(ts, t - 90 * DAY_MS, "left"))
        if i - lo < 1200:
            continue
        seg_t, seg_p = ts[lo:i + 1], px[lo:i + 1]
        day = seg_t // DAY_MS
        last = {}
        for k in range(len(seg_t)):
            last[int(day[k])] = float(seg_p[k])   # закрытие каждых суток UTC
        if len(last) < 60:
            continue
        y = np.log(np.array([last[d] for d in sorted(last)]))
        mu, tst = _trend_stat(y)
        if tst is None:
            continue
        out[t] = ("тренд" if abs(tst) > REG_T else "диапазон",
                  tst, "вверх" if mu > 0 else "вниз")
    return out


def report_regime(title, m, primary):
    lo, hi = m["ic_ci"]
    print("\n" + "─" * 62)
    print(title)
    print("  дат %d · монет на дату %.1f" % (m["n_dates"], m["n_coins"] or 0))
    print("  IC = %+.3f   ДИ%d%% [%+.3f; %+.3f]   SE %.3f"
          % (m["ic_mean"], int(REG_LEVEL), lo or float("nan"),
             hi or float("nan"), m["ic_se"] or float("nan")))
    print("  контроль перемешиванием %+.3f · различимо |IC| ≳ %.3f"
          % (m["random"], 2 * (m["ic_se"] or 0)))
    if primary:
        off0 = lo is not None and hi is not None and lo * hi > 0
        if off0 and abs(m["ic_mean"]) >= REG_BAR:
            v = "СИГНАЛ ЕСТЬ — планка взята"
        elif off0:
            v = ("эффект отличим от нуля, но ниже планки %.2f — "
                 "не основание для действия" % REG_BAR)
        else:
            v = "шум — от монетки не отличим"
        print("  ВЕРДИКТ (планка |IC| ≥ %.2f и ДИ%d%% мимо нуля): %s"
              % (REG_BAR, int(REG_LEVEL), v))
    else:
        print("  разведка, вердикта не выносится")


def run_regimes(html, bot, horizon=7, step=7):
    ser = load_cache()
    btc = load_cache(keep_btc=True).get("BTC")
    if btc is None:
        sys.exit("СТОП: в кэше нет BTC — режим определять не по чему.")
    if len(ser) < 8:
        sys.exit("СТОП: в кэше %d монет." % len(ser))
    d = run_walk(ser, CdBuilder(bot), JsScorer(html), horizon, step)
    reg = btc_regimes(btc, [x["t"] for x in d])
    for x in d:
        x["reg"] = reg.get(x["t"], (None,))[0]
    n = {k: sum(1 for x in d if x["reg"] == k) for k in ("тренд", "диапазон")}
    ups = sum(1 for x in d if reg.get(x["t"], (None, 0, ""))[2] == "вверх"
              and x["reg"] == "тренд")
    print("\n" + "═" * 62)
    print("ДЕЛЕНИЕ ПО РЕЖИМУ BTC · горизонт %dд" % horizon)
    print("═" * 62)
    print("тренд %d дат (из них вверх %d, вниз %d) · диапазон %d дат"
          % (n["тренд"], ups, n["тренд"] - ups, n["диапазон"]))
    if min(n.values()) < 20:
        print("ВНИМАНИЕ: деление вырожденное, меньшая часть — %d дат. "
              "Сравнивать нечего." % min(n.values()))
    for key, sg, nm, primary in (("long", 1.0, "ЛОНГ", True),
                                 ("short", -1.0, "ШОРТ", False)):
        for r in ("тренд", "диапазон"):
            sub = [x for x in d if x["reg"] == r]
            if len(sub) < 10:
                continue
            m = metrics(sub, key, sg, level=REG_LEVEL)
            report_regime("%s · режим «%s»%s" % (nm, r, "" if primary else " (разведка)"),
                          m, primary)
    json.dump([{"t": x["t"], "reg": x["reg"]} for x in d],
              open(os.path.join(HERE, "regimes.json"), "w"))
def tokens_from_html(html_path):
    """Список пар — из фронта, а не из отдельной копии (инвариант 2: список монет
    живёт в одном месте). Разбирается настоящим node, а не регуляркой."""
    src = open(html_path, encoding="utf-8").read()
    m = re.search(r"\nvar\s+tokens\s*=\s*\[", src)
    if not m:
        raise ValueError("в HTML не найден массив tokens[]")
    i = src.index("[", m.end() - 1)
    d = 0
    while i < len(src):
        if src[i] == "[":
            d += 1
        elif src[i] == "]":
            d -= 1
            if d == 0:
                break
        i += 1
    js = os.path.join(HERE, "_tokens.js")
    open(js, "w", encoding="utf-8").write(
        "var tokens = " + src[src.index("[", m.end() - 1):i + 1]
        + ";\nconsole.log(JSON.stringify(tokens));\n")
    out = subprocess.run(["node", js], capture_output=True)
    if out.returncode:
        raise RuntimeError("не разобрать tokens[]: " + out.stderr.decode()[:400])
    return json.loads(out.stdout)


def _save(sym, P, V, src_name):
    """Общий выход обеих качалок + гарды. Часовой шаг обязателен: вся математика
    бота часовая (√336, √168, Vol в %/час) — дневной ряд молча дал бы бред."""
    pr = [P[k] for k in sorted(P)]
    if len(pr) < 2600:                      # < ~110 дней: даже на прогрев не хватит
        print("  %-7s МАЛО ИСТОРИИ (%d ч) — пропуск" % (sym, len(pr)))
        return False
    ts = [p[0] for p in pr]
    step = float(np.median(np.diff(ts))) / HOUR_MS
    if not (0.8 < step < 1.5):
        sys.exit("СТОП: %s — шаг %.2f ч, не часовой. Стенд недействителен." % (sym, step))
    span = (ts[-1] - ts[0]) / HOUR_MS + 1
    gaps = 1.0 - len(pr) / span
    if gaps > 0.05:
        print("  %-7s ДЫР %.1f%% — пропуск" % (sym, 100 * gaps))
        return False
    json.dump({"prices": pr, "volumes": [V[k] for k in sorted(V)], "src": src_name},
              open(os.path.join(CACHE, sym + ".json"), "w"))
    print("  %-7s ok  %5d ч  дыр %.1f%%  (%s)" % (sym, len(pr), 100 * gaps, src_name))
    return True


HOSTS = [
    ("vision", "архив data.binance.vision",
     "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1h/BTCUSDT-1h-2025-06.zip"),
    ("dataapi", "зеркало data-api.binance.vision",
     "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=1"),
    ("binance", "боевой api.binance.com",
     "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=1"),
    ("fapi", "боевой fapi.binance.com",
     "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1h&limit=1"),
    ("cg", "api.coingecko.com",
     "https://api.coingecko.com/api/v3/ping"),
]


def probe(verbose=True):
    """20 секунд на диагноз. Binance закрывает публичные данные для США (HTTP 451),
    а раннеры GitHub стоят именно там — прогон 10.08 умер ровно на этом и не сказал
    об этом ни слова, потому что код глотал код ответа. Больше не глотает."""
    import requests
    alive = []
    for key, name, url in HOSTS:
        try:
            r = requests.get(url, timeout=20)
            code, note = r.status_code, ""
            if code == 451:
                note = " — доступ закрыт по географии (раннер в США)"
            elif code == 200:
                alive.append(key)
        except Exception as e:
            code, note = "нет связи", " — " + type(e).__name__
        if verbose:
            print("  %-32s %s%s" % (name, code, note))
    return alive


def _rows_from_zip(blob):
    """CSV из архива Binance: те же 12 колонок, что и у REST. У свежих файлов
    появилась строка заголовка, а метки времени переехали в микросекунды —
    обе разновидности распознаются по содержимому, а не по дате файла."""
    import zipfile, io, csv
    out = []
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        with z.open(z.namelist()[0]) as f:
            for row in csv.reader(io.TextIOWrapper(f, "utf-8")):
                if not row:
                    continue
                try:
                    t = float(row[0])
                except ValueError:
                    continue                      # строка заголовка
                if t > 1e14:                      # микросекунды -> миллисекунды
                    t /= 1000.0
                out.append([int(t), row[1], row[2], row[3], row[4], row[5],
                            0, row[7]])
    return out


def _vision_rows(pair, is_fut, t_beg, t_end):
    import requests
    base = ("https://data.binance.vision/data/futures/um" if is_fut
            else "https://data.binance.vision/data/spot")
    beg = time.gmtime(t_beg / 1000)
    end = time.gmtime(t_end / 1000)
    months, y, m = [], beg.tm_year, beg.tm_mon
    while (y, m) <= (end.tm_year, end.tm_mon):
        months.append("%04d-%02d" % (y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    rows, miss = [], 0
    for mo in months:
        u = "%s/monthly/klines/%s/1h/%s-1h-%s.zip" % (base, pair, pair, mo)
        r = requests.get(u, timeout=60)
        if r.status_code == 200:
            rows += _rows_from_zip(r.content)
        else:
            miss += 1
    # Текущий месяц выкладывается посуточно — добираем его дневными файлами.
    for d in range(0, 40):
        ts = t_end - d * DAY_MS
        if ts < t_beg:
            break
        day = time.strftime("%Y-%m-%d", time.gmtime(ts / 1000))
        if day[:7] != months[-1]:
            break
        u = "%s/daily/klines/%s/1h/%s-1h-%s.zip" % (base, pair, pair, day)
        r = requests.get(u, timeout=60)
        if r.status_code == 200:
            rows += _rows_from_zip(r.content)
    return rows, miss


def _rest_rows(host, path, pair, t_beg, t_end):
    import requests
    rows, cur = [], t_beg
    while cur < t_end:
        r = requests.get(host + path, timeout=30, params={
            "symbol": pair, "interval": "1h",
            "startTime": cur, "endTime": t_end, "limit": 1000})
        if r.status_code in (429, 418):
            time.sleep(30); continue
        if r.status_code != 200:
            return None, r.status_code
        j = r.json()
        if not j:
            break
        rows += [[int(k[0]), k[1], k[2], k[3], k[4], k[5], 0, k[7]] for k in j]
        cur = int(j[-1][0]) + HOUR_MS
        time.sleep(0.25)
    return rows, 200


def _series_from_rows(rows):
    """Цена = закрытие часа, помеченное КОНЦОМ часа: на метке t она уже известна.
    Оборот — скользящая сумма за 24 ч, то же, что CoinGecko кладёт в total_volumes.
    Масштаб одной биржи не мешает: vol_ratio делит на собственную медиану за 90д."""
    d = {}
    for k in rows:
        d[int(k[0]) // HOUR_MS] = (float(k[4]), float(k[7]))
    keys = sorted(d)
    P = {b: [b * HOUR_MS + HOUR_MS, d[b][0]] for b in keys}
    cs = np.concatenate([[0.0], np.cumsum([d[b][1] for b in keys])])
    V = {keys[n]: [P[keys[n]][0], float(cs[n + 1] - cs[n + 1 - 24])]
         for n in range(23, len(keys))}
    return P, V


def fetch_prices(html_path, bot_path, years=3, source="auto"):
    os.makedirs(CACHE, exist_ok=True)
    print("Проверка доступности источников:")
    alive = probe()
    if source == "auto":
        source = next((k for k in ("vision", "dataapi", "binance", "cg") if k in alive), None)
        if source is None:
            sys.exit("СТОП: ни один источник не отвечает — прогон невозможен.")
    print("Источник: %s\n" % source)
    if source == "cg":
        return fetch_cg(bot_path, min(years, 1.0))

    toks = tokens_from_html(html_path) + [{"name": "BTC", "s": "BTCUSDT"}]
    t_end = int(time.time() * 1000)
    t_beg = t_end - int(years * 365 * DAY_MS)
    ok = 0
    for t in toks:
        sym, pair, fut = t["name"], t["s"], bool(t.get("fut"))
        if os.path.exists(os.path.join(CACHE, sym + ".json")):
            print("  %-7s уже в кэше" % sym); ok += 1; continue
        rows, why = [], ""
        for is_fut in ((True,) if fut else (False, True)):
            if source == "vision":
                rows, miss = _vision_rows(pair, is_fut, t_beg, t_end)
                why = "нет %d месячных файлов" % miss
                # Дневные файлы архива выкладываются на следующие сутки, поэтому
                # он всегда отстаёт примерно на день. Дотягиваем хвост зеркалом,
                # иначе сверка сравнивает два разных момента времени.
                if rows:
                    tail = max(int(r[0]) for r in rows) + HOUR_MS
                    if t_end - tail > 2 * HOUR_MS:
                        add, code = _rest_rows("https://data-api.binance.vision",
                                               "/api/v3/klines", pair, tail, t_end)
                        if add:
                            rows += add
                        else:
                            why += ", хвост не добран (HTTP %s)" % code
            else:
                host = (("https://fapi.binance.com", "/fapi/v1/klines") if is_fut else
                        (("https://data-api.binance.vision", "/api/v3/klines")
                         if source == "dataapi" else
                         ("https://api.binance.com", "/api/v3/klines")))
                rows, code = _rest_rows(host[0], host[1], pair, t_beg, t_end)
                rows, why = rows or [], "HTTP %s" % code
            if len(rows) >= 2600:
                break
        if len(rows) < 2600:
            print("  %-7s НЕТ ДАННЫХ (%s, строк %d)" % (sym, why, len(rows)))
            continue
        P, V = _series_from_rows(rows)
        if _save(sym, P, V, source + ("-perp" if fut else "")):
            ok += 1
    print("монет в кэше: %d из %d" % (ok, len(toks)))
    if ok < 8:
        sys.exit("СТОП: монет меньше восьми — прогон бессмыслен.")


def fetch_cg(bot_path, years=1):
    """ЗАПАСНОЙ источник — бесплатный тариф Demo (10 000 вызовов/мес, история
    365 дней, часовой шаг только кусками ≤90 дней). Годится для сверки с ботом,
    не для основного прогона: 365 дней = ~39 дат, а этого мало (см. мощность)."""
    import requests
    src = open(bot_path, encoding="utf-8").read()
    tokens = ast.literal_eval(re.search(r"TOKENS\s*=\s*(\{.*?\n\})", src, re.S).group(1))
    tokens["BTC"] = "bitcoin"
    key = os.environ.get("COINGECKO_API_KEY")
    years = min(years, 1.0)                 # жёсткий потолок тарифа Demo
    os.makedirs(CACHE, exist_ok=True)
    now = int(time.time())
    chunks = [(now - (k + 1) * 90 * 86400, now - k * 90 * 86400)
              for k in range(int(math.ceil(years * 365 / 90)))][::-1]
    calls = 0
    for sym, cid in tokens.items():
        if os.path.exists(os.path.join(CACHE, sym + ".json")):
            print("  %-7s уже в кэше" % sym); continue
        P, V = {}, {}
        for (a, b) in chunks:
            r = requests.get(
                "https://api.coingecko.com/api/v3/coins/%s/market_chart/range" % cid,
                params={"vs_currency": "usd", "from": a, "to": b},
                headers=({"x-cg-demo-api-key": key} if key else {}), timeout=30)
            calls += 1
            if r.status_code == 429:
                time.sleep(65); continue
            if r.status_code != 200:
                print("  %-7s чанк -> %d" % (sym, r.status_code)); time.sleep(2); continue
            j = r.json()
            for ts, p in j.get("prices", []):
                P[int(ts) // HOUR_MS] = [int(ts), float(p)]
            for ts, v in j.get("total_volumes", []):
                V[int(ts) // HOUR_MS] = [int(ts), float(v)]
            time.sleep(2.5)
        _save(sym, P, V, "coingecko-demo")
    print("вызовов CoinGecko: %d (месячный лимит Demo — 10 000)" % calls)


def verify_against_live(bot_path):
    """Сверка восстановленной записи с ЖИВЫМ coeffs.json.

    ВАЖНО про меру. Раньше всё сверялось в ОТНОСИТЕЛЬНЫХ процентах, и на
    доходностях это давало мусор: r14 у монеты бывает 0.001, тогда расхождение
    в полпроцентного пункта печатается как 1449%. Уровни цен сверяются
    относительно, доходности — в процентных ПУНКТАХ, eff14 — в своих единицах."""
    import requests
    live = requests.get(
        "https://gist.githubusercontent.com/seahomebatumi-ai/"
        "3f50574a29bc37434c18cc8480779ccb/raw/coeffs.json", timeout=30).json()
    ref = {d["symbol"]: d for d in live["analysis_data"]} if isinstance(
        live.get("analysis_data"), list) else live["analysis_data"]
    gen = live.get("generated_at", "")
    try:
        g = time.mktime(time.strptime(gen[:19], "%Y-%m-%dT%H:%M:%S"))
        g -= time.timezone
    except Exception:
        g = None
    cdb = CdBuilder(bot_path)
    # поле -> (вид сверки, порог).  rel = относительно, pp = проц. пункты,
    # abs = в единицах величины, info = только показать
    SPEC = [("min_price", "rel", 2.0), ("max_price", "rel", 2.0),
            ("min30", "rel", 2.0), ("max30", "rel", 2.0),
            ("volatility", "rel", 10.0), ("vol7", "rel", 25.0),
            ("r7", "pp", 1.5), ("r14", "pp", 2.0), ("r30", "pp", 3.0),
            ("eff14", "abs", 0.15), ("vol_ratio", "info", 0.0)]
    ends = [json.load(open(os.path.join(CACHE, f)))["prices"][-1][0]
            for f in os.listdir(CACHE) if f.endswith(".json")]
    gap = None
    if g and ends:
        gap = (g - max(ends) / 1000.0) / 3600.0
        print("coeffs.json собран %s · кэш кончается %s · разрыв %.1f ч" % (
            gen[:16], time.strftime("%Y-%m-%dT%H:%M", time.gmtime(max(ends) / 1000)), gap))
        if gap > 3:
            print("РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ: доходности r7/r14/r30/eff14 считаются "
                  "на разные моменты и НЕ СРАВНИМЫ. Смотреть только уровни и "
                  "волатильность; для доходностей показан сдвиг в сигмах.")
    print("уровни и скорости — в относительных %, доходности — в проц. пунктах")
    print("%-7s " % "монета" + " ".join("%-9s" % k for k, _, _ in SPEC))
    worst = {k: 0.0 for k, _, _ in SPEC}
    cmp_n = 0
    for sym, ser in sorted(load_cache().items()):
        r = ref.get(sym)
        if not r:
            continue
        cd = cdb.build(ser["prices"], ser["volumes"], len(ser["prices"]) - 1)
        if cd is None:
            continue
        cmp_n += 1
        cells = []
        for k, kind, _ in SPEC:
            a, b = cd.get(k), r.get(k)
            if a is None or b is None or not isinstance(b, (int, float)):
                cells.append("   —     "); continue
            if kind == "pp":
                dv = abs(a - b) * 100.0; cells.append("%7.2f пп" % dv)
            elif kind == "abs":
                dv = abs(a - b); cells.append("%9.3f" % dv)
            else:
                dv = 100 * abs(a - b) / max(1e-12, abs(b)); cells.append("%8.2f%% " % dv)
            worst[k] = max(worst[k], dv)
        print("%-7s " % sym + " ".join(cells))
    if cmp_n == 0:
        sys.exit("СТОП: сверять нечего — в кэше ноль монет. "
                 "Это провал закачки, а не успешная сверка.")
    skip = ("r7", "r14", "r30", "eff14") if (gap is None or gap > 3) else ()
    bad = [k for k, kind, thr in SPEC
           if kind != "info" and k not in skip and worst[k] > thr]
    print("\nсверено монет: %d" % cmp_n)
    for k, kind, thr in SPEC:
        u = {"rel": "%", "pp": " пп", "abs": "", "info": "%"}[kind]
        note = ("не сравнимо (разрыв во времени)" if k in skip else
                "справочно" if kind == "info" else "%.2f%s" % (thr, u))
        print("  %-11s худшее %8.3f%s   порог %s" % (k, worst[k], u, note))
    if skip:
        print("  ожидаемый сдвиг цены за разрыв: ~%.1f%% при часовой воле 1%%"
              % (100 * 0.01 * math.sqrt(max(gap or 0, 0))))
    print("\n%s" % ("восстановление совпадает с продакшном" if not bad else
                    "ВЫШЛИ ЗА ПОРОГ: " + ", ".join(bad)))


def load_cache(keep_btc=False):
    out = {}
    for f in sorted(os.listdir(CACHE)):
        if f.endswith(".json") and not f.startswith("_"):
            out[f[:-5]] = json.load(open(os.path.join(CACHE, f)))
    if not keep_btc:
        out.pop("BTC", None)      # BTC — измеритель режима, не кандидат в сделку
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 5. САМОПРОВЕРКА: синтетика с ИЗВЕСТНЫМ ответом
# ─────────────────────────────────────────────────────────────────────────────
def synth(mode, n_coins=28, hours=8760, seed=3):
    """noise — чистое блуждание (ответ: IC≈0)
       revert — возврат к среднему (ответ: IC>0 у лонга)
       trend  — импульс (ответ: IC<0 у лонга)"""
    rng = np.random.default_rng(seed)
    t0 = 1700000000000
    mkt = np.cumsum(rng.normal(0, 0.004, hours))
    out = {}
    for c in range(n_coins):
        lp = np.zeros(hours)
        idio = rng.normal(0, 0.010, hours)
        k = {"noise": 0.0, "revert": 0.004, "trend": -0.0015}[mode]
        run, cnt = 0.0, 0
        for i in range(1, hours):
            run += lp[i - 1]
            cnt += 1
            if i > 720:
                run -= lp[i - 721]
                cnt -= 1
            anchor = run / cnt if i > 24 else 0.0
            lp[i] = lp[i - 1] - k * (lp[i - 1] - anchor) + idio[i] + 0.7 * (mkt[i] - mkt[i - 1])
        p = 10.0 * np.exp(lp)
        ts = [t0 + i * HOUR_MS for i in range(hours)]
        out["C%02d" % c] = {"prices": [[ts[i], float(p[i])] for i in range(hours)],
                            "volumes": [[ts[i], float(1e7 * (1 + 0.3 * rng.random()))]
                                        for i in range(hours)]}
    return out


def selftest(html, bot, n_seeds=10):
    scorer = JsScorer(html)
    cdb = CdBuilder(bot)
    print("Т1 · вырезка кода: JS-мост собран, node --check пройден; блок бота разобран AST — ОК")

    # Т2 — отсутствие взгляда в будущее
    s = synth("noise", n_coins=2, hours=3000)
    key = list(s)[0]
    pr, vo = s[key]["prices"], s[key]["volumes"]
    i = 2600
    a = cdb.build(pr, vo, i)
    b = cdb.build(pr[:i + 1], [v for v in vo if v[0] <= pr[i][0]], i)
    same = json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    print("Т2 · взгляд в будущее: запись на дату t из полного ряда и из обрезанного %s"
          % ("совпадает — ОК" if same else "РАСХОДИТСЯ — СТОП"))
    if not same:
        sys.exit(1)

    # Т3 — счёт реагирует на вход как задумано
    probe = {"min_price": 10.0, "max_price": 20.0, "price_pos": 0, "volatility": 0.01,
             "r7": -0.05, "r14": -0.08, "r30": -0.20, "min30": 10.0, "max30": 15.0,
             "vol7": 0.011, "eff14": -0.2, "vol_ratio": 1.0,
             "rank": None, "rank_prev": None, "fdv_mc": None}
    jj = [{"cd": probe, "sym": "X", "cur": 10.2, "p24": -1.0, "qv": None, "isLong": True, "fr": None},
          {"cd": probe, "sym": "X", "cur": 19.5, "p24": -1.0, "qv": None, "isLong": True, "fr": None}]
    r = scorer.score(jj)
    print("Т3 · монотонность: у минимума %.1f · у максимума %.1f — %s"
          % (r[0], r[1], "ОК" if r[0] > r[1] else "СТОП"))

    # Т4 — Монте-Карло по мирам с ИЗВЕСТНЫМ ответом.
    # Один посев не доказывает ничего: при SE(IC) ≈ 0.026 любая из статистик
    # уходит на 2 SE примерно в каждом двадцатом прогоне. Судим по РАСПРЕДЕЛЕНИЮ.
    exp = {"noise": "0", "revert": "+", "trend": "\u2212"}
    acc = {}
    for mode in ("noise", "revert", "trend"):
        rows = []
        for sd in range(1, n_seeds + 1):
            d = run_walk(synth(mode, seed=sd), cdb, scorer, verbose=False)
            mL = metrics(d, "long")
            rows.append({"ctl": mL["base_low"], "full": mL["ic_mean"],
                         "nopen": metrics(d, "long_nopen")["ic_mean"],
                         "rnd": mL["random"], "se": mL["ic_se"], "nd": mL["n_dates"]})
        acc[mode] = rows
        f = lambda k: np.array([r[k] for r in rows], float)
        good = int((f("ctl") > 0).sum() if exp[mode] == "+"
                   else (f("ctl") < 0).sum() if exp[mode] == "\u2212"
                   else (np.abs(f("ctl")) < 2 * f("se")).sum())
        print("\nМИР \u00ab%s\u00bb  (эталонный фактор обязан дать \u00ab%s\u00bb), посевов %d"
              % (mode, exp[mode], n_seeds))
        print("  эталон \u00abблизость к мин90\u00bb  IC = %+.3f \u00b1 %.3f   нужный знак %d/%d"
              % (f("ctl").mean(), f("ctl").std(ddof=1), good, n_seeds))
        print("  перемешанный счёт (нуль)   IC = %+.3f \u00b1 %.3f" % (f("rnd").mean(), f("rnd").std(ddof=1)))
        print("  scoreCandidate целиком     IC = %+.3f \u00b1 %.3f" % (f("full").mean(), f("full").std(ddof=1)))
        print("  он же без двух штрафов     IC = %+.3f \u00b1 %.3f" % (f("nopen").mean(), f("nopen").std(ddof=1)))

    g = lambda m, k: np.array([r[k] for r in acc[m]], float)
    se = float(np.mean(g("noise", "se")))
    ok_null = abs(g("noise", "ctl").mean()) < se and abs(g("noise", "rnd").mean()) < se
    ok_pow = g("revert", "ctl").mean() > 0.10 and g("trend", "ctl").mean() < -0.10
    print("\n" + "\u2550" * 62)
    print("ИТОГ САМОПРОВЕРКИ")
    print("\u2550" * 62)
    print("нулевой мир не даёт ложного сигнала: %s" % ("ДА" if ok_null else "НЕТ"))
    print("миры со знаком распознаются верно:   %s" % ("ДА" if ok_pow else "НЕТ"))
    print("мощность: SE(IC) \u2248 %.3f при %d датах \u2192 отличим |IC| \u2273 %.3f"
          % (se, int(np.mean(g("noise", "nd"))), 2 * se))
    print("ВЕРДИКТ СТЕНДА: %s" % ("измеряет то, что должен"
                                  if (ok_null and ok_pow) else "НЕИСПРАВЕН \u2014 результатам не верить"))
    return 0 if (ok_null and ok_pow) else 1


# ─────────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--regimes", action="store_true")
    ap.add_argument("--years", type=float, default=3)
    ap.add_argument("--source", default="auto",
                    choices=["auto", "vision", "dataapi", "binance", "cg"])
    ap.add_argument("--horizon", type=int, default=7)
    ap.add_argument("--step", type=int, default=7)
    ap.add_argument("--quality-const", action="store_true")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--html", default=DEF_HTML)
    ap.add_argument("--bot", default=DEF_BOT)
    a = ap.parse_args()

    if a.regimes:
        return run_regimes(a.html, a.bot, a.horizon, a.step)
    if a.probe:
        print("Проверка доступности источников:"); probe(); return 0
    if a.fetch:
        return fetch_prices(a.html, a.bot, a.years, a.source)
    if a.verify:
        return verify_against_live(a.bot)
    if a.selftest:
        return selftest(a.html, a.bot, a.seeds)
    if a.run:
        qc = None
        if a.quality_const:
            qc = json.load(open(os.path.join(CACHE, "_quality_today.json")))
        ser = load_cache()
        if len(ser) < 8:
            sys.exit("СТОП: в кэше %d монет. Сначала должна отработать закачка "
                     "(--fetch), прогон на пустом кэше смысла не имеет." % len(ser))
        d = run_walk(ser, CdBuilder(a.bot), JsScorer(a.html),
                     a.horizon, a.step, quality_const=qc)
        for side in ("long", "short"):
            report("РЕАЛЬНЫЕ ДАННЫЕ · %s · горизонт %dд%s"
                   % (side.upper(), a.horizon,
                      " · ранг/оборот сегодняшние" if qc else ""),
                   metrics(d, side, 1.0 if side == "long" else -1.0))
        json.dump(d, open(os.path.join(HERE, "run_raw.json"), "w"))
        return 0
    ap.print_help()


if __name__ == "__main__":
    sys.exit(main() or 0)
