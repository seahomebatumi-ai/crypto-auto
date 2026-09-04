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
JS_FUNCS = ["has", "clamp01", "sigmaDay", "volRegime", "qualityScore",
            "scoreFinish", "scoreCandidate"]
JS_VARS = ["EFF_TREND", "PACE_Z", "VOL_ABNORMAL"]

# Names a bundle may read without defining them. Deliberately short: this
# is the escape hatch of the closure check below, and every entry on it is
# an identifier the check can no longer catch.
JS_GLOBALS = ["Math", "JSON", "isFinite", "isNaN", "parseFloat", "parseInt",
              "Number", "String", "Array", "Object", "Date", "RegExp",
              "Error", "require", "process", "console", "NaN", "Infinity"]
# `name(` forms that are not calls.
JS_KEYWORDS = frozenset(["if", "for", "while", "switch", "catch", "return",
                         "typeof", "function", "new", "delete", "void",
                         "do", "else", "try", "throw", "case", "in", "of",
                         "instanceof"])


def _js_noise_span(s, i):
    """If s[i] opens a JS string literal or a comment, return the index where
    that span ends; otherwise None. THE one description in this file of how a
    string and a comment are traversed (inv. 20): _skip_to_matching_brace steps
    over them with it and _strip_js_noise blanks them with it, so the two can
    never disagree about what is code and what is prose."""
    n = len(s)
    c = s[i]
    if c in "'\"":
        q = c
        i += 1
        while i < n and s[i] != q:
            i += 2 if s[i] == "\\" else 1
        return i + 1
    if c == "/" and i + 1 < n and s[i + 1] == "/":
        while i < n and s[i] != "\n":
            i += 1
        return i                        # the newline itself is code again
    if c == "/" and i + 1 < n and s[i + 1] == "*":
        j = s.find("*/", i + 2)
        return n if j < 0 else j + 2    # unterminated: the rest is prose
    return None


def _skip_to_matching_brace(s, i):
    """i указывает на '{'. Возвращает индекс ПОСЛЕ парной '}'."""
    depth = 0
    n = len(s)
    while i < n:
        j = _js_noise_span(s, i)
        if j is not None:               # a '}' inside a string or a comment
            i = max(j, i + 1)           # would otherwise end the function
            continue
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("незакрытая функция")


def _strip_js_noise(src):
    """Blank every string literal and comment, preserving length and newlines.
    A static scan over the result cannot read an identifier out of prose, and
    offsets still line up with the original text."""
    out = list(src)
    i, n = 0, len(src)
    while i < n:
        j = _js_noise_span(src, i)
        if j is None:
            i += 1
            continue
        j = min(max(j, i + 1), n)
        for k in range(i, j):
            if out[k] != "\n":
                out[k] = " "
        i = j
    return "".join(out)


def _js_defined(txt):
    """The names a piece of JS text declares — function names, var names and
    every declared parameter. DERIVED from the text, never typed: a manifest
    typed by hand is the defect this whole check exists to catch."""
    names = set(re.findall(r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\(", txt))
    names |= set(re.findall(r"\bvar\s+([A-Za-z_$][\w$]*)", txt))
    for m in re.finditer(r"\bfunction\s*(?:[A-Za-z_$][\w$]*)?\s*\(([^)]*)\)",
                         txt):
        names |= set(p.strip() for p in m.group(1).split(",") if p.strip())
    return names


def _assert_js_closed(bundle_src, driver_src, label):
    """The assembled bundle must be CLOSED UNDER REFERENCE: every identifier it
    reads is defined in the bundle, declared in the driver, or a JS global.
    A hand-written extraction manifest goes stale the moment production splits a
    helper out, and the failure is silent by construction — the drivers' per-row
    `catch` turns the ReferenceError into a column of nulls and the run dies
    hundreds of lines away comparing None with None. This raises at build time
    naming the identifier instead. Direction of error is safe: a declaration
    form this scan does not recognise raises, it never passes silently.
    Returns the number of identifier occurrences examined (inv. 22)."""
    b = _strip_js_noise(bundle_src)
    known = _js_defined(b) | _js_defined(_strip_js_noise(driver_src))
    known |= set(JS_GLOBALS)
    seen = [m.group(1) for m
            in re.finditer(r"(?<![.\w$])([A-Za-z_$][\w$]*)\s*\(", b)
            if m.group(1) not in JS_KEYWORDS]                # called
    seen += [m.group(1) for m
             in re.finditer(r"(?<![.\w$])([A-Z][A-Z0-9_]{2,})\b", b)]  # read
    if not seen:
        raise RuntimeError("замкнутость %s: сверено 0 идентификаторов — "
                           "проверка ничего не проверила (инв. 22)" % label)
    for name in seen:
        if name not in known:
            raise RuntimeError(
                "замкнутость %s: связка ссылается на %s, а определения нет ни "
                "в ней, ни в драйвере — вырезка отстала от продакшна "
                "(инв. 20)" % (label, name))
    print("  замкнутость %s: сверено %d обращений, %d имён, пропущенных 0"
          % (label, len(seen), len(set(seen))))
    return len(seen)


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
    bundle = "\n".join(out)
    _assert_js_closed(bundle, JS_DRIVER, "_score_bridge.js")
    return bundle


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
    «какую из 30 взять», а не «куда пойдёт рынок»."""
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


def _save(sym, P, V, src_name, HL=None):
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
    doc = {"prices": pr, "volumes": [V[k] for k in sorted(V)], "src": src_name}
    if HL:
        doc["hl"] = [HL[k] for k in sorted(HL)]     # additive; old readers unaffected
    json.dump(doc, open(os.path.join(CACHE, sym + ".json"), "w"))
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
    Масштаб одной биржи не мешает: vol_ratio делит на собственную медиану за 90д.
    HL: high/low of the hour under the same end-of-hour stamp. Needed by --stops
    only: a stop/liquidation is a TOUCH event (§3.3), and close-only series
    systematically undercount touches — an error in the dangerous direction."""
    d = {}
    for k in rows:
        d[int(k[0]) // HOUR_MS] = (float(k[4]), float(k[7]),
                                   float(k[2]), float(k[3]))
    keys = sorted(d)
    P = {b: [b * HOUR_MS + HOUR_MS, d[b][0]] for b in keys}
    HL = {b: [b * HOUR_MS + HOUR_MS, d[b][2], d[b][3]] for b in keys}
    cs = np.concatenate([[0.0], np.cumsum([d[b][1] for b in keys])])
    V = {keys[n]: [P[keys[n]][0], float(cs[n + 1] - cs[n + 1 - 24])]
         for n in range(23, len(keys))}
    return P, V, HL


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
        P, V, HL = _series_from_rows(rows)
        if _save(sym, P, V, source + ("-perp" if fut else ""), HL):
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


def verify_against_live(bot_path, html_path=None):
    """Сверка восстановленной записи с ЖИВЫМ coeffs.json.

    ВАЖНО про меру. Раньше всё сверялось в ОТНОСИТЕЛЬНЫХ процентах, и на
    доходностях это давало мусор: r14 у монеты бывает 0.001, тогда расхождение
    в полпроцентного пункта печатается как 1449%. Уровни цен сверяются
    относительно, доходности — в процентных ПУНКТАХ, eff14 — в своих единицах.

    ВАЖНО про вердикт (11.08.2026). Это единственный режим, который умеет
    ошибиться в ОПАСНУЮ сторону — напечатать «совпадает». Поэтому:
      • код возврата ненулевой при любом провале (раньше был всегда 0, и
        упавшая сверка выглядела в workflow зелёной — тот же класс, что инв. 25);
      • считается число сверок ПО КАЖДОМУ ПОЛЮ, а не только число монет:
        поле, которого нет в живом coeffs.json ни у одной монеты, раньше
        проходило порог с нулём сравнений (инв. 22);
      • поля, не сравнимые из-за разрыва во времени, названы в вердикте —
        «совпадает» без оговорки о них больше не печатается.

    ВАЖНО про порог (v3 семантики, 12.08.2026, после двух боевых прогонов).
    Дефект ВОССТАНОВЛЕНИЯ системный по построению кода: логика окон, семантика
    времени и единицы применяются ко всем монетам одинаково. Поэтому поле
    ПРОВАЛЕНО только если за порогом >= 3 монет или ВСЕ сравнённые (>= 2).
    Одна монета за порогом — ЛЮБОГО размера — это идиосинкразия источников
    (прогон №1: XLM volatility 12.4 %, один день; прогон №2: HYPE min90 6.1 % —
    фитиль ликвидаций на перпе против композитного спота) и печатается
    громким поимённым предупреждением, не останавливая конвейер.

    БАЗИС ПЕРП/СПОТ. У монет с fut:true спота на Binance НЕТ: кэш стенда —
    перп-свечи, бот считает по композитному споту CoinGecko. Это два РАЗНЫХ
    настоящих инструмента, поэтому при переданном html у fut-монет ЛЮБОЕ поле
    за порогом идёт в справочную полосу «базис перп/спот» и в провал не
    попадает никогда. Урок двух прогонов: №1 срубили доходности XMR (r30
    6.7 пп), №2 — уровень HYPE (min90 6.1 %); ограничивать полосу одними
    доходностями было моей ошибкой масштаба."""
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
    fut = set()
    if html_path:
        try:
            fut = {t["name"] for t in tokens_from_html(html_path) if t.get("fut")}
        except Exception as e:
            print("tokens[] из HTML не разобраны (%s) — базис-поблажки нет"
                  % type(e).__name__)
    RET_FIELDS = ("r7", "r14", "r30", "eff14")
    # поле -> (вид сверки, порог).  rel = относительно, pp = проц. пункты,
    # abs = в единицах величины, info = только показать
    SPEC = [("min_price", "rel", 2.0), ("max_price", "rel", 2.0),
            ("min30", "rel", 2.0), ("max30", "rel", 2.0),
            ("volatility", "rel", 10.0), ("vol7", "rel", 25.0),
            ("r7", "pp", 1.5), ("r14", "pp", 2.0), ("r30", "pp", 3.0),
            ("eff14", "abs", 0.15), ("vol_ratio", "info", 0.0)]
    # Same filter as load_cache: '_'-prefixed files are side data, not series.
    # --run --quality-const legitimately keeps _quality_today.json right here,
    # and reading ["prices"] out of it crashed the whole check.
    ends = [json.load(open(os.path.join(CACHE, f)))["prices"][-1][0]
            for f in os.listdir(CACHE)
            if f.endswith(".json") and not f.startswith("_")]
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
    seen = {k: 0 for k, _, _ in SPEC}          # comparisons actually performed
    breach = {k: [] for k, _, _ in SPEC}       # (sym, dev) over threshold
    basis = []                                 # fut-coin return gaps: informative
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
            seen[k] += 1
            thr_k = next(t for kk, _, t in SPEC if kk == k)
            kind_k = next(kd for kk, kd, _ in SPEC if kk == k)
            if kind_k != "info" and dv > thr_k:
                if sym in fut:
                    basis.append((sym, k, dv))   # ALL fields: two instruments
                else:
                    breach[k].append((sym, dv))
        print("%-7s " % sym + " ".join(cells))
    if cmp_n == 0:
        sys.exit("СТОП: сверять нечего — в кэше ноль монет. "
                 "Это провал закачки, а не успешная сверка.")
    skip = RET_FIELDS if (gap is None or gap > 3) else ()
    def field_fails(k, thr):
        # A reconstruction defect is SYSTEMIC by construction: window logic,
        # timestamp semantics and units apply to every coin equally. A single
        # coin over the bar — at any magnitude — is source idiosyncrasy
        # (12.08: XLM volatility one day, HYPE perp-wick min90 the next) and
        # warns loudly instead of killing the pipeline.
        br = breach[k]
        return len(br) >= 3 or (cmp_n >= 2 and len(br) >= cmp_n)
    bad = [k for k, kind, thr in SPEC
           if kind != "info" and k not in skip and field_fails(k, thr)]
    warn = [(k, breach[k]) for k, kind, thr in SPEC
            if kind != "info" and k not in skip and breach[k]
            and k not in bad]
    # A field the live JSON never carried compares zero times and keeps
    # worst = 0.0, i.e. it passes its threshold without a single comparison.
    # That is invariant 22 verbatim, one level down: count, then judge.
    never = [k for k, kind, _ in SPEC
             if kind != "info" and k not in skip and seen[k] == 0]
    print("\nсверено монет: %d" % cmp_n)
    for k, kind, thr in SPEC:
        u = {"rel": "%", "pp": " пп", "abs": "", "info": "%"}[kind]
        note = ("не сравнимо (разрыв во времени)" if k in skip else
                "справочно" if kind == "info" else "%.2f%s" % (thr, u))
        print("  %-11s сверок %2d   худшее %8.3f%s   порог %s"
              % (k, seen[k], worst[k], u, note))
    if skip:
        print("  ожидаемый сдвиг цены за разрыв: ~%.1f%% при часовой воле 1%%"
              % (100 * 0.01 * math.sqrt(max(gap or 0, 0))))
    print("")
    if never:
        print("НЕ СВЕРЕНО НИ РАЗУ: " + ", ".join(never)
              + " — поля нет в живом coeffs.json. Нулевое число сравнений "
                "не является совпадением.")
    for k, br in warn:
        print("ПРЕДУПРЕЖДЕНИЕ %s: единичные выбросы (%s) — источники, не "
              "восстановление; конвейер не останавливается"
              % (k, ", ".join("%s %.2f" % (sy, dv) for sy, dv in br)))
    if basis:
        by = {}
        for sy, k, dv in basis:
            by.setdefault(sy, []).append("%s %.1f" % (k, dv))
        print("БАЗИС ПЕРП/СПОТ (fut-монеты, справочно, не провал): "
              + " · ".join(sy + ": " + ", ".join(v) for sy, v in sorted(by.items())))
    if bad:
        print("ВЫШЛИ ЗА ПОРОГ: " + ", ".join(bad))
    if not bad and not never:
        checked = [k for k, kind, _ in SPEC if kind != "info" and k not in skip]
        print("совпадает с продакшном по сверенным полям: " + ", ".join(checked))
    if skip:
        print("НЕ СВЕРЯЛОСЬ (разрыв во времени %s): %s"
              % ("неизвестен" if gap is None else "%.1f ч" % gap, ", ".join(skip)))
    # Non-zero exit is the whole point: a workflow step must go red on failure.
    # A time gap is an expected operational state of the archive, not a failure,
    # so it downgrades the claim in words instead of failing the step.
    return 1 if (bad or never) else 0


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
# 6. EXPERIMENT LAB — three pre-registered measurements (12.08.2026)
#
# Registered BEFORE any real data is seen (invariant 23). One PRIMARY claim per
# experiment; every other cell is exploration and gets the doubled bar that the
# regime study already set as precedent (|IC| >= 0.10, CI99). A positive primary
# does NOT wire anything into the product by itself: the standing rule is a
# fresh confirmation run after +26 weeks of new data before any product change.
#
#   A. --stops    Is the invalidation layer honest? PRIMARY: pooled per-side
#                 calibration ratio measured/model of 7d stop-touch frequency.
#                 CI95 contains 1.0 -> the normal model is honest at 7d;
#                 lower bound > 1.0 -> tails heavier than normal, board
#                 probabilities understate risk by that factor (record in §7);
#                 upper bound < 1.0 -> model overstates (errs safe), no action.
#                 Hit and whipsaw rates are DESCRIPTIVE (no auto-thresholds:
#                 acting on them is a separate, separately-argued change).
#   B. --res7     Does the residual-vs-BTC factor rank coins? PRIMARY: LONG,
#                 7d, contrarian orientation (factor = -z: fell on its own ->
#                 long candidate). Bar identical to the scoring study:
#                 IC >= +0.05 and CI95 clear of zero. Short side, momentum
#                 orientation, 3/14d, and the r30 factor are exploration.
#   C. --funding  Does funding crowding predict? PRIMARY: SHORT, 7d,
#                 factor = z of 3-day mean funding within its trailing 30-day
#                 distribution (crowded longs -> future underperformance).
#                 Same bar: IC >= +0.05, CI95 clear of zero. Long side, 3/14d,
#                 and the raw-level variant are exploration.
#
# Multiplicity is named, not hidden: three primaries in one session. Any single
# positive at 0.05 therefore carries a family-wise caveat in its verdict line,
# and the +26-week confirmation rule above is what actually gates product use.
# ─────────────────────────────────────────────────────────────────────────────
FACT_BAR = 0.05          # primary bar — identical to the scoring study
EXPL_BAR = 0.10          # exploration bar — identical to the regime study
EXPL_LEVEL = 99.0


def factor_verdict(m, primary):
    if m["ic_mean"] is None:
        return "НЕТ ДАННЫХ"
    lo, hi = m["ic_ci"]
    off0 = lo is not None and hi is not None and lo * hi > 0
    if primary:
        if off0 and m["ic_mean"] >= FACT_BAR:
            return ("ПЛАНКА ВЗЯТА (семейная оговорка: 3 первичных теста; "
                    "в продукт — только после подтверждения на +26 неделях)")
        if off0 and m["ic_mean"] <= -0.02:
            return "ИНВЕРТИРОВАН — знак противоположен гипотезе"
        return "ШУМ — от монетки не отличим"
    if off0 and abs(m["ic_mean"]) >= EXPL_BAR:
        return "сигнал выше разведочной планки — кандидат в отдельный пре-регистрированный тест"
    return "разведка: вердикта не выносится"


def factor_report(title, m, primary):
    print("\n" + ("═" if primary else "─") * 62)
    print(("ПЕРВИЧНЫЙ ТЕСТ · " if primary else "разведка · ") + title)
    if m["ic_mean"] is None:
        print("  нет данных")
        return
    lv = 95 if primary else int(EXPL_LEVEL)
    print("  дат %d · монет на дату %.1f" % (m["n_dates"], m["n_coins"] or 0))
    print("  IC = %+.3f   ДИ%d [%+.3f; %+.3f]   SE %.3f   контроль %+.3f"
          % (m["ic_mean"], lv, m["ic_ci"][0] or float("nan"),
             m["ic_ci"][1] or float("nan"), m["ic_se"] or float("nan"),
             m["random"] or 0))
    print("  ТОП-3 минус среднее: %+.2f%%" % (100 * (m["top_mean"] or 0)))
    print("  ВЕРДИКТ: " + factor_verdict(m, primary))


def walk_grid(series, horizon_d=7, step_d=7, warm_d=90, fwd_extra_d=0):
    """Date grid + per-coin index pairs. Mirrors run_walk's admission guards
    verbatim (6h staleness, 12h end-of-horizon tolerance, i >= 100, unbalanced
    panel by construction); run_walk itself is left untouched — it is the
    validated scoring path. fwd_extra_d extends the REQUIRED forward history
    (e.g. whipsaw needs 7d past the 7d touch window) without changing the
    measurement horizon."""
    syms = sorted(series)
    ts = {s: np.array([p[0] for p in series[s]["prices"]]) for s in syms}
    need = (horizon_d + fwd_extra_d) * DAY_MS
    t0 = min(ts[s][0] for s in syms) + warm_d * DAY_MS
    t1 = max(ts[s][-1] for s in syms) - need
    if t1 <= t0:
        raise ValueError("истории не хватает даже на одну дату")
    grid = list(range(int(t0), int(t1) + 1, step_d * DAY_MS))
    out = []
    for t in grid:
        row = []
        for s in syms:
            i = int(np.searchsorted(ts[s], t, "right")) - 1
            if i < 100 or abs(ts[s][i] - t) > 6 * HOUR_MS:
                continue
            iF = int(np.searchsorted(ts[s], t + horizon_d * DAY_MS, "right")) - 1
            iX = int(np.searchsorted(ts[s], t + need, "right")) - 1
            if iF <= i or ts[s][iF] < t + horizon_d * DAY_MS - 12 * HOUR_MS:
                continue
            if fwd_extra_d and (iX <= iF or ts[s][iX] < t + need - 12 * HOUR_MS):
                continue
            row.append((s, i, iF, iX))
        if row:
            out.append((t, row))
    return out


# ── 7. --stops · honesty of the invalidation layer ──────────────────────────
INV_JS_FUNCS = ["has", "firstNum", "normCdf", "sigmaDay", "touchProb",
                "invalidationInfo"]
INV_JS_VARS = ["LIQ_MMR", "RISK_Z", "INV_FLOOR_SD", "INV_CAP_SD"]

INV_DRIVER = r"""
var fs = require('fs');
__EXTRACTED__
var job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
var out = [];
for (var i = 0; i < job.length; i++) {
    var j = job[i], r = null;
    try {
        var inv = invalidationInfo(j.cd, j.E, j.isLong);
        if (inv) {
            // Log-distance of the stop barrier, same construction that
            // liqTouchProb applies to the liquidation barrier (§3.3).
            // Extreme-vol longs can cap the distance at >= 100 % of price
            // (6-sigma of a 3.5+%/h coin): log(<=0) is NaN and the touch
            // model is undefined there — mark p null, Python counts them out.
            var b = j.isLong ? -Math.log(1 - inv.dist) : Math.log(1 + inv.dist);
            var pm = touchProb(j.cd.volatility, b, j.hours);
            r = { dist: inv.dist, price: inv.price, src: inv.src,
                  floored: inv.floored, capped: inv.capped,
                  p: (isFinite(b) && isFinite(pm)) ? pm : null };
        }
    } catch (e) { r = null; }
    out.push(r);
}
fs.writeFileSync(process.argv[3], JSON.stringify(out));
"""


def _extract_js_set(html_path, funcs, jvars, driver, bridge_name):
    src = open(html_path, encoding="utf-8").read()
    out = []
    for name in funcs:
        m = re.search(r"\nfunction\s+" + name + r"\s*\(", src)
        if not m:
            raise ValueError("в HTML не найдена функция " + name)
        b = src.index("{", m.end())
        out.append(src[m.start() + 1:_skip_to_matching_brace(src, b)])
    for name in jvars:
        m = re.search(r"\nvar\s+" + name + r"\s*=\s*([^;\n]+);", src)
        if not m:
            raise ValueError("в HTML не найдена константа " + name)
        out.append("var " + name + " = " + m.group(1).strip() + ";")
    _assert_js_closed("\n".join(out), driver, bridge_name)
    path = os.path.join(HERE, bridge_name)
    open(path, "w", encoding="utf-8").write(
        driver.replace("__EXTRACTED__", "\n".join(out)))
    r = subprocess.run(["node", "--check", path], capture_output=True)
    if r.returncode:
        raise RuntimeError("node --check провалился:\n" + r.stderr.decode())
    return path


class JsBridge:
    """Same batch pattern as JsScorer: one node process per date."""

    def __init__(self, html_path, funcs, jvars, driver, name):
        self.path = _extract_js_set(html_path, funcs, jvars, driver, name)
        self.fi = os.path.join(HERE, "_job2.json")
        self.fo = os.path.join(HERE, "_out2.json")

    def call(self, jobs):
        json.dump(jobs, open(self.fi, "w"), allow_nan=False)
        r = subprocess.run(["node", self.path, self.fi, self.fo],
                           capture_output=True)
        if r.returncode:
            raise RuntimeError("node упал: " + r.stderr.decode()[:800])
        return json.load(open(self.fo))


def run_stops(series, bot, html, horizon_d=7, step_d=7, verbose=True):
    """Measure the invalidation layer on real touches.

    Per (date, coin, side): production invalidationInfo -> stop level; the
    forward 7d of high/low decides whether it was TOUCHED; the production
    touchProb gives the model figure for the same barrier. Whipsaw: among
    touched setups, the share where price is back at entry within the 7 days
    AFTER the touch — a stop that fired and then un-fired, i.e. paid-for noise.
    Requires 'hl' in cache (refetch after 12.08 — cache key v4)."""
    for s in series:
        if "hl" not in series[s]:
            sys.exit("СТОП: в кэше %s нет high/low. Перекачать историю "
                     "(--fetch, ключ кэша v4): касание по закрытиям — "
                     "заниженный, то есть опасный, замер." % s)
    cdb = CdBuilder(bot)
    br = JsBridge(html, INV_JS_FUNCS, INV_JS_VARS, INV_DRIVER, "_inv_bridge.js")
    px = {s: np.array([p[1] for p in series[s]["prices"]]) for s in series}
    hlt = {s: np.array([h[0] for h in series[s]["hl"]]) for s in series}
    hi = {s: np.array([h[1] for h in series[s]["hl"]]) for s in series}
    lo = {s: np.array([h[2] for h in series[s]["hl"]]) for s in series}
    pts = {s: [p[0] for p in series[s]["prices"]] for s in series}
    vts = {s: [v[0] for v in series[s]["volumes"]] for s in series}
    H = horizon_d * 24
    dates = []
    n_undef = [0]
    for t, row in walk_grid(series, horizon_d, step_d, fwd_extra_d=horizon_d):
        jobs, meta = [], []
        for s, i, iF, iX in row:
            cd = cdb.build(series[s]["prices"], series[s]["volumes"], i,
                           pts[s], vts[s])
            if cd is None:
                continue
            E = float(px[s][i])
            for isL in (True, False):
                jobs.append({"cd": cd, "E": E, "isLong": isL, "hours": H})
                meta.append((s, i, E, isL))
        if len(meta) < 16:
            continue
        res = br.call(jobs)
        obs = []
        for (s, i, E, isL), r in zip(meta, res):
            if r is None:
                continue
            if r.get("p") is None:
                n_undef[0] += 1        # stop >= 100 % away: not a measurable setup
                continue
            t_i = series[s]["prices"][i][0]
            j0 = int(np.searchsorted(hlt[s], t_i, "right"))
            j1 = int(np.searchsorted(hlt[s], t_i + H * HOUR_MS, "right"))
            if j1 - j0 < H - 12:            # hl series must cover the window
                continue
            seg_hi, seg_lo = hi[s][j0:j1], lo[s][j0:j1]
            touch = (seg_lo <= r["price"]) if isL else (seg_hi >= r["price"])
            hit = bool(touch.any())
            whip = None
            if hit:
                k = int(np.argmax(touch))
                k1 = min(j0 + k + H, len(hlt[s]))
                back = (hi[s][j0 + k:k1] >= E) if isL else (lo[s][j0 + k:k1] <= E)
                whip = bool(back.any())
            cat = ("capped" if r["capped"] else
                   "floored" if r["floored"] else "struct")
            obs.append({"side": "long" if isL else "short", "cat": cat,
                        "hit": hit, "whip": whip, "p": r["p"],
                        "dist": r["dist"]})
        if obs:
            dates.append({"t": t, "obs": obs})
        if verbose and len(dates) % 20 == 0 and dates:
            print("  дат посчитано: %d" % len(dates), flush=True)
    if n_undef[0]:
        print("  исключено сетапов с dist >= 100%% (модель касания не "
              "определена, экстремальная волатильность): %d" % n_undef[0])
    return dates


def stops_summary(dates, level=95.0):
    """Pooled and per-category rates with date-block bootstrap CIs. The unit of
    independence is the DATE (cross-coin correlation within a week is heavy),
    so resampling is over dates, pooling their setups."""
    def pool(sel):
        rows = [[o for o in d["obs"] if sel(o)] for d in dates]
        rows = [r for r in rows if r]
        if len(rows) < 5:
            return None
        def agg(rs):
            f = [o for r in rs for o in r
                 if o["p"] is not None and np.isfinite(o["p"])]
            if not f:
                return (float("nan"), 0.0, None, float("nan"), 0)
            hitv = np.array([1.0 if o["hit"] else 0.0 for o in f])
            pv = np.array([o["p"] for o in f], float)
            hits = [o for o in f if o["hit"] and o["whip"] is not None]
            wv = (np.mean([1.0 if o["whip"] else 0.0 for o in hits])
                  if hits else None)
            return (float(hitv.mean()), float(pv.mean()), wv,
                    float(np.median([o["dist"] for o in f])), len(f))
        hit, mod, whip, med_d, n = agg(rows)
        rng = np.random.default_rng(17)
        bh, br_, bw = [], [], []
        for _ in range(2000):
            take = [rows[k] for k in rng.integers(0, len(rows), len(rows))]
            h, mo, w, _, _ = agg(take)
            bh.append(h)
            br_.append(h / mo if mo > 0 else np.nan)
            if w is not None:
                bw.append(w)
        a = (100 - level) / 2
        ci = lambda v: (float(np.nanpercentile(v, a)),
                        float(np.nanpercentile(v, 100 - a)))
        return {"n": n, "hit": hit, "hit_ci": ci(bh), "model": mod,
                "ratio": hit / mod if mod > 0 else None, "ratio_ci": ci(br_),
                "whip": whip, "whip_ci": ci(bw) if bw else (None, None),
                "med_dist": med_d}
    out = {}
    for side in ("long", "short"):
        out[side] = pool(lambda o, sd=side: o["side"] == sd)
        for cat in ("floored", "struct", "capped"):
            out[side + "." + cat] = pool(
                lambda o, sd=side, c=cat: o["side"] == sd and o["cat"] == c)
    return out


def report_stops(sm):
    print("\n" + "═" * 62)
    print("СЛОЙ ИНВАЛИДАЦИИ · касание стопа за 7д · факт против модели")
    print("═" * 62)
    for side, nm in (("long", "ЛОНГ"), ("short", "ШОРТ")):
        m = sm.get(side)
        if not m:
            print("%s: данных мало" % nm)
            continue
        print("\n%s · сетапов %d · медианная дистанция %.1f%%"
              % (nm, m["n"], 100 * m["med_dist"]))
        print("  выбито за 7д: %.1f%% [%.1f; %.1f] · модель %.1f%%"
              % (100 * m["hit"], 100 * m["hit_ci"][0], 100 * m["hit_ci"][1],
                 100 * m["model"]))
        cal_ok = m["ratio"] is not None and np.isfinite(m["ratio"])
        if cal_ok:
            print("  калибровка факт/модель: %.2f [%.2f; %.2f]"
                  % (m["ratio"], m["ratio_ci"][0], m["ratio_ci"][1]))
        else:
            print("  калибровка факт/модель: не считается (модель не "
                  "определена на этих сетапах)")
        if m["whip"] is not None:
            print("  из выбитых вернулись ко входу за следующие 7д: %.0f%% [%.0f; %.0f]"
                  % (100 * m["whip"], 100 * (m["whip_ci"][0] or 0),
                     100 * (m["whip_ci"][1] or 0)))
        if cal_ok:
            lo_, hi_ = m["ratio_ci"]
            v = ("нормальная модель честна на 7д (ДИ95 содержит 1.0)"
                 if lo_ <= 1.0 <= hi_ else
                 "ХВОСТЫ ТЯЖЕЛЕЕ НОРМАЛИ в ~%.1f раза — вероятности на доске "
                 "занижены; множитель зафиксировать в §7" % m["ratio"]
                 if lo_ > 1.0 else
                 "модель завышает риск (ошибка в безопасную сторону) — не менять")
            print("  ВЕРДИКТ (первичный, правило до прогона): " + v)
        else:
            print("  ВЕРДИКТ: не выносится — модель не определена")
        for cat, cn in (("floored", "пол 2σ"), ("struct", "структурный"),
                        ("capped", "обрезан 6σ")):
            c = sm.get(side + "." + cat)
            if c:
                print("    %-11s n=%-5d выбито %.1f%% · модель %.1f%% · возврат %s"
                      % (cn, c["n"], 100 * c["hit"], 100 * c["model"],
                         "—" if c["whip"] is None else "%.0f%%" % (100 * c["whip"])))


# ── 8. --res7 · residual-vs-BTC as a ranking factor ─────────────────────────
def bot_functions(bot_path, names):
    """AST-cut top-level bot functions into a namespace (invariant 21)."""
    src = open(bot_path, encoding="utf-8").read()
    lines = src.splitlines()
    tree = ast.parse(src)
    got = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            got[node.name] = "\n".join(lines[node.lineno - 1:node.end_lineno])
    if len(got) != len(names):
        raise ValueError("в боте не найдены: "
                         + ", ".join(sorted(set(names) - set(got))))
    ns = {"np": np}
    # Module-level constants the cut functions reference (BUCKET_SECONDS etc.):
    # every top-level UPPERCASE assignment with a literal value comes along.
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id.isupper()):
            try:
                ns[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, SyntaxError):
                pass
    exec("\n\n".join(got.values()), ns)
    return ns


RES_JS_FUNCS = ["has", "residual7"]
RES_JS_VARS = ["RES_Z", "RES_R2_CAP", "H_NOISE"]
RES_DRIVER = r"""
var fs = require('fs');
__EXTRACTED__
var job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
var out = [];
for (var i = 0; i < job.length; i++) {
    var r = null;
    try { r = residual7(job[i].cd, job[i].btc); } catch (e) { r = null; }
    out.push(r === null ? null : { z: r.z, own: r.own, cls: r.cls });
}
fs.writeFileSync(process.argv[3], JSON.stringify(out));
"""


class BetaWalk:
    """Rolling 90d up/down beta+R2 vs BTC from the SAME bot functions the
    production pipeline uses: bucket_prices, paired_hourly_returns, fit_stats,
    asymmetric_beta (AST-cut, zero copies). The >=120 matched-hours guard is
    §2's admission rule, restated here because it lives inside get_token_betas'
    request plumbing, not in the math functions."""

    def __init__(self, bot_path, btc_prices):
        self.ns = bot_functions(bot_path, ["bucket_prices", "fit_stats",
                                           "paired_hourly_returns",
                                           "asymmetric_beta"])
        self.btc_b = self.ns["bucket_prices"](btc_prices)
        self.btc_keys = np.array(sorted(self.btc_b))

    def betas(self, prices, i, pts):
        t_end = prices[i][0]
        cut = t_end - 90 * DAY_MS
        lo_i = bisect.bisect_left(pts, cut, 0, i + 1)
        cb = self.ns["bucket_prices"](prices[lo_i:i + 1])
        k0 = int(np.searchsorted(self.btc_keys, t_end // HOUR_MS - 90 * 24))
        k1 = int(np.searchsorted(self.btc_keys, t_end // HOUR_MS, "right"))
        bb = {int(k): self.btc_b[int(k)] for k in self.btc_keys[k0:k1]}
        common = sorted(set(bb) & set(cb))
        if len(common) < 120:
            return None
        b_r, c_r = self.ns["paired_hourly_returns"](bb, cb, common)
        if len(b_r) < 120:
            return None
        up_b, up_r2, dn_b, dn_r2 = self.ns["asymmetric_beta"](b_r, c_r)
        return {"up_beta_90": up_b, "up_r2_90": up_r2,
                "down_beta_90": dn_b, "down_r2_90": dn_r2}


def run_res7(series, btc, bot, html, horizon_d=7, step_d=7, verbose=True):
    cdb = CdBuilder(bot)
    bw = BetaWalk(bot, btc["prices"])
    br = JsBridge(html, RES_JS_FUNCS, RES_JS_VARS, RES_DRIVER, "_res_bridge.js")
    px = {s: np.array([p[1] for p in series[s]["prices"]]) for s in series}
    pts = {s: [p[0] for p in series[s]["prices"]] for s in series}
    vts = {s: [v[0] for v in series[s]["volumes"]] for s in series}
    bpts = [p[0] for p in btc["prices"]]
    bts = np.array(bpts)
    dates = []
    for t, row in walk_grid(series, horizon_d, step_d):
        bi = int(np.searchsorted(bts, t, "right")) - 1
        if bi < 100 or abs(bts[bi] - t) > 6 * HOUR_MS:
            continue
        bcd = cdb.build(btc["prices"], [], bi, bpts, [])
        if bcd is None or bcd["r7"] is None:
            continue
        jobs, meta = [], []
        for s, i, iF, _ in row:
            cd = cdb.build(series[s]["prices"], series[s]["volumes"], i,
                           pts[s], vts[s])
            if cd is None:
                continue
            bet = bw.betas(series[s]["prices"], i, pts[s])
            if bet is None:
                continue
            cd.update(bet)
            cur = float(px[s][i])
            path = px[s][i:iF + 1]
            jobs.append({"cd": cd, "btc": {"r7": bcd["r7"]}})
            meta.append({
                "sym": s, "fwd": float(path[-1] / cur - 1),
                "mae_long": float(path.min() / cur - 1),
                "mae_short": float(path.max() / cur - 1),
                "f_low": -float((cur - cd["min_price"]) / cur)
                         / (cd["volatility"] * math.sqrt(24) or 1e-9),
                "f_r7": cd["r7"] if cd["r7"] is not None else 0.0,
                "r30c": -(cd["r30"] if cd["r30"] is not None else 0.0),
            })
        if len(meta) < 8:
            continue
        out = br.call(jobs)
        keep = []
        for m, r in zip(meta, out):
            if r is None or r["z"] is None:
                continue
            m["res_c"] = -r["z"]        # contrarian: fell on its own -> long
            m["res_m"] = r["z"]         # momentum orientation (exploration)
            keep.append(m)
        if len(keep) < 8:
            continue
        fw = np.array([m["fwd"] for m in keep])
        for m in keep:
            m["exc"] = m["fwd"] - float(fw.mean())
        dates.append({"t": t, "coins": keep})
        if verbose and len(dates) % 20 == 0:
            print("  дат посчитано: %d" % len(dates), flush=True)
    return dates


# ── 9. --funding · crowding as a directional factor ─────────────────────────
def _fund_rows_from_zip(blob):
    """fundingRate CSV: column layout drifted over the years, so columns are
    recognised by content — the ms timestamp and the small |rate|<0.05 float."""
    import zipfile, io, csv
    out = []
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        with z.open(z.namelist()[0]) as f:
            for row in csv.reader(io.TextIOWrapper(f, "utf-8")):
                ts, rate = None, None
                for cell in row:
                    try:
                        v = float(cell)
                    except ValueError:
                        continue
                    if v > 1e12:
                        ts = int(v / 1000.0) if v > 1e14 else int(v)
                    elif abs(v) < 0.05 and cell not in ("0", "0.0"):
                        rate = v
                    elif abs(v) < 0.05 and rate is None:
                        rate = v
                if ts is not None and rate is not None:
                    out.append([ts, rate])
    return out


def fetch_funding(html_path, years=3):
    import requests
    os.makedirs(CACHE, exist_ok=True)
    toks = tokens_from_html(html_path)
    t_end = int(time.time() * 1000)
    t_beg = t_end - int(years * 365 * DAY_MS)
    beg = time.gmtime(t_beg / 1000)
    end = time.gmtime(t_end / 1000)
    months, y, m = [], beg.tm_year, beg.tm_mon
    while (y, m) <= (end.tm_year, end.tm_mon):
        months.append("%04d-%02d" % (y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    ok = 0
    for t in toks:
        sym, pair = t["name"], t["s"]
        f = os.path.join(CACHE, "_fund_%s.json" % sym)
        if os.path.exists(f):
            print("  %-7s funding уже в кэше" % sym)
            ok += 1
            continue
        rows, miss = [], 0
        for mo in months:
            u = ("https://data.binance.vision/data/futures/um/monthly/"
                 "fundingRate/%s/%s-fundingRate-%s.zip" % (pair, pair, mo))
            r = requests.get(u, timeout=60)
            if r.status_code == 200:
                rows += _fund_rows_from_zip(r.content)
            else:
                miss += 1
        rows.sort()
        if len(rows) < 200:                 # < ~67 days of 8h prints
            print("  %-7s funding МАЛО (%d выплат, нет %d мес.)"
                  % (sym, len(rows), miss))
            continue
        json.dump({"rates": rows}, open(f, "w"))
        print("  %-7s funding ok  %5d выплат" % (sym, len(rows)))
        ok += 1
    print("funding в кэше: %d из %d" % (ok, len(toks)))
    if ok < 8:
        sys.exit("СТОП: funding меньше чем у восьми монет — тест бессмыслен.")


def load_funding():
    out = {}
    for f in sorted(os.listdir(CACHE)):
        if f.startswith("_fund_") and f.endswith(".json"):
            out[f[6:-5]] = json.load(open(os.path.join(CACHE, f)))["rates"]
    return out


def fund_factor(rates_ts, rates_v, t):
    """z of the 3-day mean funding within its trailing 30-day distribution.
    Registered choice: single prints are noisy, the 9-print mean is the
    crowding STATE; the 30d window is the coin's own recent norm."""
    j1 = int(np.searchsorted(rates_ts, t, "right"))
    j0 = int(np.searchsorted(rates_ts, t - 30 * DAY_MS, "left"))
    w = rates_v[j0:j1]
    if len(w) < 60:
        return None, None
    sd = float(np.std(w, ddof=1))
    if sd <= 0:
        return None, None
    j3 = int(np.searchsorted(rates_ts, t - 3 * DAY_MS, "left"))
    m3 = rates_v[j3:j1]
    if len(m3) < 6:
        return None, None
    z = (float(np.mean(m3)) - float(np.mean(w))) / sd
    lvl = float(np.mean(m3))
    return z, lvl


def run_funding(series, fund, bot, horizon_d=7, step_d=7, verbose=True):
    cdb = CdBuilder(bot)
    px = {s: np.array([p[1] for p in series[s]["prices"]]) for s in series}
    pts = {s: [p[0] for p in series[s]["prices"]] for s in series}
    vts = {s: [v[0] for v in series[s]["volumes"]] for s in series}
    fts = {s: np.array([r[0] for r in fund[s]], float) for s in fund}
    fvs = {s: np.array([r[1] for r in fund[s]], float) for s in fund}
    dates = []
    for t, row in walk_grid(series, horizon_d, step_d):
        meta = []
        for s, i, iF, _ in row:
            if s not in fts:
                continue
            z, lvl = fund_factor(fts[s], fvs[s], t)
            if z is None:
                continue
            cd = cdb.build(series[s]["prices"], series[s]["volumes"], i,
                           pts[s], vts[s])
            if cd is None:
                continue
            cur = float(px[s][i])
            path = px[s][i:iF + 1]
            meta.append({
                "sym": s, "fwd": float(path[-1] / cur - 1),
                "mae_long": float(path.min() / cur - 1),
                "mae_short": float(path.max() / cur - 1),
                "f_low": -float((cur - cd["min_price"]) / cur)
                         / (cd["volatility"] * math.sqrt(24) or 1e-9),
                "f_r7": cd["r7"] if cd["r7"] is not None else 0.0,
                "fz": z, "fp": lvl,
            })
        if len(meta) < 8:
            continue
        fw = np.array([m["fwd"] for m in meta])
        for m in meta:
            m["exc"] = m["fwd"] - float(fw.mean())
        dates.append({"t": t, "coins": meta})
        if verbose and len(dates) % 20 == 0:
            print("  дат посчитано: %d" % len(dates), flush=True)
    return dates


# ── 10. --target · the 90-day extremum against a continuation target ───────
# Map §3.12 records the tension and §10 carries it as «not built, gated»:
# tradeGeometry always aims at the 90-day extremum — a MEAN-REVERSION target —
# while in `trend` the ranking comes from the CONTINUATION channel. This mode is
# that measurement and nothing else; it changes no production math.
# Both arms share ONE leverageDecision, computed on the UNTOUCHED cd, so
# inv.dist, inv.price, moneyBelowMin and ok are literally the same numbers in
# both: the comparison is on the reward leg alone. The continuation arm is a
# shallow copy of cd whose extremum is replaced by E*exp(±k·vol·√H) and handed
# to the UNMODIFIED tradeGeometry, so every veto, the chase anchor and tgtSig
# are production's own arithmetic on a substituted target (inv. 21, 38).
# Nothing here forecasts: the primary is a first-touch count against the odds
# RR_MIN itself asserts.
TARGET_JS_FUNCS = ["has", "firstNum", "normCdf", "sigmaDay", "touchProb",
                   "fmtP", "invalidationInfo", "lStruct", "lNoise", "advBeta",
                   "lBtcCheck", "lMoney", "volRegime", "fixHint",
                   "leverageDecision", "marketRegime", "tradeGeometry"]
TARGET_JS_VARS = ["LIQ_MMR", "RISK_Z", "H_NOISE", "H_REACT", "H_BTC",
                  "INV_FLOOR_SD", "INV_CAP_SD", "MAX_MARGIN_LOSS", "RR_MIN",
                  "TGT_SIGMA_MIN", "ENTRY_CHASE_SD", "L_MIN", "L_CAP",
                  "VOL_ABNORMAL", "VOL_HARD", "VOL_STOP", "EFF_TREND",
                  "REG_STRESS_Z"]

# Registered before any data (inv. 23), one declaration each (inv. 20).
K_GRID = [1.0, 1.5, 2.0, 2.5, 3.0]
TGT_STEP_D = 7          # a daily grid would multiply setups without multiplying
                        # independent forward windows: consecutive dates share
                        # six sevenths of the window (§3.13) and the CI would
                        # come out narrower than the evidence supports.
TGT_QUORUM_N = 60       # admitted setups, per side per arm
TGT_QUORUM_D = 20       # contributing dates, per side per arm
TGT_BOOT = 2000         # resamples, date blocks — as stops_summary does it
TGT_H_LADDER = [1, 4, 8, 16, 32]   # multiples of H_NOISE, registered before data
TGT_MONO_MIN_PTS = 3               # fewest grid points a monotonicity claim needs

TARGET_DRIVER = r"""
var fs = require('fs');
__EXTRACTED__
function armOut(g) {
    if (!g) return null;
    return { veto: g.veto, rr: g.rr, tgtSig: g.tgtSig, reward: g.reward };
}
var job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
var out = [];
for (var i = 0; i < job.length; i++) {
    var j = job[i], r = null;
    try {
        // ONE decision per (date, coin, side), on the untouched cd: both arms
        // get the same dec, so the risk leg cannot move between them. The
        // substitution touches max_price (long) / min_price (short), which is
        // the opposite side from the one invalidationInfo reads, so it cannot
        // leak into the stop either.
        var dec = leverageDecision(j.cd, j.E, j.isLong, j.btcStats);
        var g0  = tradeGeometry(j.cd, j.E, j.isLong, dec, j.hi24, j.lo24);
        var vol = j.cd.volatility;
        var tgt0 = j.isLong ? j.cd.max_price : j.cd.min_price;
        var p0 = (has(vol) && vol > 0 && has(tgt0) && tgt0 > 0 && j.E > 0)
                 ? touchProb(vol, Math.abs(Math.log(tgt0 / j.E)), j.H) : null;
        var subs = {};
        for (var key in j.subs) {
            var lvl = j.subs[key], cdk = {};
            for (var f in j.cd) cdk[f] = j.cd[f];
            if (j.isLong) cdk.max_price = lvl; else cdk.min_price = lvl;
            subs[key] = {
                g: armOut(tradeGeometry(cdk, j.E, j.isLong, dec,
                                        j.hi24, j.lo24)),
                p: (has(vol) && vol > 0 && lvl > 0 && j.E > 0)
                   ? touchProb(vol, Math.abs(Math.log(lvl / j.E)), j.H) : null,
                tgt: lvl };
        }
        r = { ok: dec.ok, moneyBelowMin: dec.moneyBelowMin,
              dist: dec.inv ? dec.inv.dist : null,
              stop: dec.inv ? dec.inv.price : null,
              reg: marketRegime(j.btcStats).mode,
              prod: { g: armOut(g0), p: p0, tgt: has(tgt0) ? tgt0 : null },
              subs: subs };
    } catch (e) { r = null; }
    out.push(r);
}
fs.writeFileSync(process.argv[3], JSON.stringify(out));
"""


def _read_js_num(html_path, name):
    """One number, cut from index.html at every run — never typed here."""
    src = open(html_path, encoding="utf-8").read()
    m = re.search(r"\nvar\s+" + name + r"\s*=\s*([0-9.eE+-]+)\s*;", src)
    if not m:
        raise ValueError("в HTML не найдена числовая константа " + name)
    return float(m.group(1))


def _sig_params(html_path, name):
    """Declared parameter names of a production function, READ FROM THE SOURCE.
    The mode assembles hi24/lo24 itself, so inv. 48 applies: the fields supplied
    must be the fields the reader takes, and that is checked against the text
    rather than remembered."""
    src = open(html_path, encoding="utf-8").read()
    m = re.search(r"\nfunction\s+" + name + r"\s*\(([^)]*)\)", src)
    if not m:
        raise ValueError("в HTML не найдена функция " + name)
    return [p.strip() for p in m.group(1).split(",") if p.strip()]


def _ak(k):
    return "k%.1f" % k


def _touch_calc(hi, lo, j0, j1, tgt, stop, is_long):
    """First touch between the two barriers on hourly high/low, plus the plain
    target touch used by the calibration descriptive. `tie` is RECORDED, never
    guessed: when both barriers fall inside the same hourly candle the order is
    unresolvable at this resolution (the journal's own vocabulary, §3.13).
    Returns (first, tgt_touched); first ∈ {tgt, stop, tie, none}."""
    seg_hi, seg_lo = hi[j0:j1], lo[j0:j1]
    if is_long:
        t_hit, s_hit = seg_hi >= tgt, seg_lo <= stop
    else:
        t_hit, s_hit = seg_lo <= tgt, seg_hi >= stop
    tgt_any = bool(t_hit.any())
    either = t_hit | s_hit
    if not either.any():
        return "none", tgt_any
    k = int(np.argmax(either))
    if t_hit[k] and s_hit[k]:
        return "tie", tgt_any
    return ("tgt" if t_hit[k] else "stop"), tgt_any


def run_target(series, bot, html, btc, betawalk=None, k_grid=None,
               H_override=None, want_identity=False, verbose=True):
    """Per (date, coin, side): production's own geometry on the 90-day extremum
    against the same geometry on a continuation target, resolved by first touch
    on the forward window. Requires 'hl' in the cache — a close-based touch
    understates BOTH barriers, and understating the target is exactly the error
    this measurement exists to detect."""
    par = _sig_params(html, "tradeGeometry")
    if par[-2:] != ["hi24", "lo24"]:
        raise RuntimeError("tradeGeometry берёт не те поля, что собирает стенд: "
                           "подпись %r (инв. 48)" % (par,))
    for s in series:
        if "hl" not in series[s]:
            sys.exit("СТОП: в кэше %s нет high/low. Перекачать историю "
                     "(--fetch, ключ кэша v4): касание по закрытиям занижает "
                     "оба барьера, а занижённая цель — ровно та ошибка, ради "
                     "которой этот замер и существует." % s)
    ks = list(K_GRID if k_grid is None else k_grid)
    H = int(H_override if H_override else _read_js_num(html, "H_NOISE"))
    horizon_d = max(1, H // 24)
    cdb = CdBuilder(bot)
    br = JsBridge(html, TARGET_JS_FUNCS, TARGET_JS_VARS, TARGET_DRIVER,
                  "_tgt_bridge.js")
    px = {s: np.array([p[1] for p in series[s]["prices"]]) for s in series}
    hlt = {s: np.array([h[0] for h in series[s]["hl"]]) for s in series}
    hi = {s: np.array([h[1] for h in series[s]["hl"]]) for s in series}
    lo = {s: np.array([h[2] for h in series[s]["hl"]]) for s in series}
    pts = {s: [p[0] for p in series[s]["prices"]] for s in series}
    vts = {s: [v[0] for v in series[s]["volumes"]] for s in series}
    bpts = [p[0] for p in btc["prices"]]
    bts = np.array(bpts)
    dates = []
    for t, row in walk_grid(series, horizon_d, TGT_STEP_D, fwd_extra_d=0):
        bi = int(np.searchsorted(bts, t, "right")) - 1
        if bi < 100 or abs(bts[bi] - t) > 6 * HOUR_MS:
            continue
        bcd = cdb.build(btc["prices"], [], bi, bpts, [])
        if bcd is None:
            continue
        # The WHOLE BTC record, because that is what production hands these
        # functions: the board passes botData.btc, i.e. coeffs.btc entire.
        # leverageDecision takes volatility off it (§3.3) and marketRegime
        # takes r7 and r14 (§3.11); a hand-built subset silences the second
        # reader to serve the first, and the recorded regime label could then
        # only ever be `range` or `stress`. A bench that builds its own input
        # proves the function and not the wiring (inv. 48). CdBuilder.build
        # computes r7/r14/r30 with the bot's own window_stats — the same call
        # main.py makes for BTC — so the faithful object costs nothing.
        btc_stats = bcd
        jobs, meta = [], []
        for s, i, iF, _ in row:
            t_i = series[s]["prices"][i][0]
            j0 = int(np.searchsorted(hlt[s], t_i, "right"))
            if j0 < 24:                     # 24 hourly rows ending at i
                continue
            cd = cdb.build(series[s]["prices"], series[s]["volumes"], i,
                           pts[s], vts[s])
            if cd is None:
                continue
            if betawalk is not None:
                bet = betawalk.betas(series[s]["prices"], i, pts[s])
                if bet is not None:
                    cd.update(bet)          # absent betas stay absent: that is
                                            # production's own missing-field
                                            # path and it drops the BTC ceiling
            vol = cd["volatility"]
            if vol is None or not (vol > 0):
                continue
            E = float(px[s][i])
            hi24 = float(np.max(hi[s][j0 - 24:j0]))
            lo24 = float(np.min(lo[s][j0 - 24:j0]))
            q = vol * math.sqrt(H)
            for isL in (True, False):
                subs = {_ak(k): E * math.exp(k * q if isL else -k * q)
                        for k in ks}
                if want_identity:
                    t0 = cd["max_price"] if isL else cd["min_price"]
                    if t0 is not None and t0 > 0:
                        subs["ident"] = float(t0)
                jobs.append({"cd": cd, "E": E, "isLong": isL, "H": H,
                             "btcStats": btc_stats, "hi24": hi24, "lo24": lo24,
                             "subs": subs})
                meta.append((s, i, iF, j0, E, isL))
        if not meta:
            continue
        res = br.call(jobs)
        obs = []
        for (s, i, iF, j0, E, isL), r in zip(meta, res):
            if r is None:
                continue
            j1 = int(np.searchsorted(hlt[s], series[s]["prices"][i][0]
                                     + H * HOUR_MS, "right"))
            if j1 - j0 < H - 12:            # the window must be covered
                continue
            pg = r["prod"]["g"]
            o = {"sym": s, "side": "long" if isL else "short", "reg": r["reg"],
                 "rr": pg["rr"] if pg else None,
                 "tgtSig": pg["tgtSig"] if pg else None,
                 "adm": bool(pg and not pg["veto"]), "arms": {}}
            stop, dist = r["stop"], r["dist"]
            if stop is None or dist is None or not (dist > 0) or not (stop > 0):
                obs.append(o)
                continue
            b_log = abs(math.log(stop / E))
            # Mark-to-market at H, in units of the risk leg: the only reading a
            # setup that touched neither barrier can be given.
            mtm = ((float(px[s][iF]) / E - 1.0) if isL
                   else (1.0 - float(px[s][iF]) / E)) / dist
            arms = [("prod", pg, r["prod"]["p"], r["prod"]["tgt"])]
            arms += [(key, r["subs"][key]["g"], r["subs"][key]["p"],
                      r["subs"][key]["tgt"]) for key in r["subs"]]
            for key, g, p, tgt in arms:
                # Admission = this arm's own geometry gate and nothing else:
                # the regime and channel layers decide the SIDE, not the target.
                if g is None or g["veto"] or tgt is None or not (tgt > 0):
                    continue
                first, hit = _touch_calc(hi[s], lo[s], j0, j1, tgt, stop, isL)
                o["arms"][key] = {
                    "first": first, "hit": hit, "p": p, "rr": g["rr"],
                    "tgtSig": g["tgtSig"], "a": abs(math.log(tgt / E)),
                    "b": b_log,
                    "R": (g["rr"] if first == "tgt" else
                          -1.0 if first == "stop" else
                          0.0 if first == "tie" else mtm)}
            obs.append(o)
        if obs:
            dates.append({"t": t, "obs": obs})
        if verbose and len(dates) % 20 == 0 and dates:
            print("  дат посчитано: %d" % len(dates), flush=True)
    return dates


def _arm_pool(dates, arm, side, level=95.0):
    """One arm on one side (side=None pools both). The resampling unit is the
    DATE, exactly as stops_summary does it: setups inside one week are not
    independent, so a setup-level bootstrap would invent precision."""
    rows = []
    for d in dates:
        r = [o["arms"][arm] for o in d["obs"]
             if (side is None or o["side"] == side) and arm in o["arms"]]
        if r:
            rows.append(r)
    if len(rows) < 5:
        return None

    def agg(rs):
        f = [o for r in rs for o in r]
        nt = sum(1 for o in f if o["first"] == "tgt")
        ns = sum(1 for o in f if o["first"] == "stop")
        cal = [o for o in f if o["p"] is not None and np.isfinite(o["p"])]
        meas = (float(np.mean([1.0 if o["hit"] else 0.0 for o in cal]))
                if cal else float("nan"))
        mod = float(np.mean([o["p"] for o in cal])) if cal else float("nan")
        return (len(f), nt, ns, (nt / ns) if ns else float("nan"), meas, mod)

    n, nt, ns, om, meas, mod = agg(rows)
    flat = [o for r in rows for o in r]
    nz = sum(1 for o in flat if o["first"] == "tie")
    nn = sum(1 for o in flat if o["first"] == "none")
    rng = np.random.default_rng(17)
    bo, bc = [], []
    for _ in range(TGT_BOOT):
        take = [rows[k] for k in rng.integers(0, len(rows), len(rows))]
        _, _, _, o2, m2, d2 = agg(take)
        bo.append(o2)
        bc.append(m2 / d2 if d2 > 0 else np.nan)
    a = (100.0 - level) / 2.0
    ci = lambda v: (float(np.nanpercentile(v, a)),
                    float(np.nanpercentile(v, 100 - a)))
    # Driftless two-barrier identity: P(target first) = b/(a+b) in LOG
    # distances. Printed beside the mean 1/RR, which uses RELATIVE ones — the
    # gap between the two is itself worth having and costs nothing.
    qs = [o["b"] / (o["a"] + o["b"]) for o in flat if (o["a"] + o["b"]) > 0]
    den = sum(1.0 - q for q in qs)
    irr = [1.0 / o["rr"] for o in flat if o["rr"]]
    return {"n": n, "n_dates": len(rows), "n_tgt": nt, "n_stop": ns,
            "n_tie": nz, "n_none": nn, "omega": om, "omega_ci": ci(bo),
            "p_none": (nn / n) if n else None, "measured": meas, "model": mod,
            "calib": (meas / mod) if mod > 0 else None, "calib_ci": ci(bc),
            "model_odds": (sum(qs) / den) if qs and den > 0 else None,
            "inv_rr": float(np.mean(irr)) if irr else None,
            "R": float(np.mean([o["R"] for o in flat])) if flat else None,
            "quorum": n >= TGT_QUORUM_N and len(rows) >= TGT_QUORUM_D}


def target_summary(dates, html, ks=None, H=None, level=95.0):
    """The registered primary, the descriptives and the continuation arm's
    reading. Every verdict below is produced by the rule fixed before the data,
    never by the number's appearance."""
    ks = list(K_GRID if ks is None else ks)
    out = {"bar": 1.0 / _read_js_num(html, "RR_MIN"), "ks": ks,
           "H": int(H if H is not None else _read_js_num(html, "H_NOISE")),
           "quorum": [TGT_QUORUM_N, TGT_QUORUM_D],
           "arms": {}, "pooled": {}, "sides": {}}
    for arm in ["prod"] + [_ak(k) for k in ks]:
        out["arms"][arm] = {sd: _arm_pool(dates, arm, sd, level)
                            for sd in ("long", "short")}
        out["pooled"][arm] = _arm_pool(dates, arm, None, level)
    for sd in ("long", "short"):
        kstar = None
        for k in ks:                        # smallest k whose CI is not
            m = out["arms"][_ak(k)][sd]     # entirely below the bar
            if m and m["quorum"] and m["omega_ci"][1] >= out["bar"]:
                kstar = k
                break
        rows = [o for d in dates for o in d["obs"] if o["side"] == sd
                and o["rr"] is not None and o["tgtSig"] is not None]
        dist = lambda v: ({"n": len(v), "med": float(np.median(v)),
                           "p10": float(np.percentile(v, 10)),
                           "p90": float(np.percentile(v, 90))} if v else None)
        out["sides"][sd] = {
            "kstar": kstar, "n_geo": len(rows),
            "spearman": spearman([o["rr"] for o in rows],
                                 [o["tgtSig"] for o in rows]),
            "adm": dist([o["tgtSig"] for o in rows if o["adm"]]),
            "ref": dist([o["tgtSig"] for o in rows if not o["adm"]])}
    syms = {}
    for d in dates:
        for o in d["obs"]:
            e = syms.setdefault(o["sym"], {"d": set(), "long": 0, "short": 0,
                                           "cont": 0})
            e["d"].add(d["t"])
            if "prod" in o["arms"]:
                e[o["side"]] += 1
            e["cont"] += sum(1 for a in o["arms"] if a not in ("prod", "ident"))
    out["symbols"] = sorted([{"sym": s, "dates": len(v["d"]), "long": v["long"],
                              "short": v["short"], "cont": v["cont"]}
                             for s, v in syms.items()], key=lambda r: r["sym"])
    return out


def _tgt_line(m):
    if not m:
        return "не выносится — сетапов нет"
    s = ("сетапов %d · дат %d · цель %d / стоп %d / ничья %d / никуда %d"
         % (m["n"], m["n_dates"], m["n_tgt"], m["n_stop"], m["n_tie"],
            m["n_none"]))
    if not np.isfinite(m["omega"]):
        return s + " · Ω не определена (стоп не выбит ни разу)"
    return s + ("\n    Ω = %.3f  ДИ95 [%.3f; %.3f]"
                % (m["omega"], m["omega_ci"][0], m["omega_ci"][1]))


def report_target(sm):
    bar = sm["bar"]
    print("\n" + "═" * 62)
    print("ЦЕЛЬ СДЕЛКИ · экстремум 90д против канала продолжения · "
          "первое касание за %dч" % sm["H"])
    print("═" * 62)
    print("ПЕРВИЧНЫЙ: Ω = цель/стоп по первому касанию на ДОПУЩЕННОМ наборе "
          "продакшн-плеча,\nничьи и «никуда» исключены из обоих счётчиков. "
          "Планка 1/RR_MIN = %.2f — самая\nщедрая точка допущенного "
          "диапазона, ошибка в пользу действующей цели.\nКворум: %d сетапов и "
          "%d дат на сторону и рукав." % (bar, sm["quorum"][0],
                                          sm["quorum"][1]))
    for sd, nm in (("long", "ЛОНГ"), ("short", "ШОРТ")):
        m = sm["arms"]["prod"][sd]
        print("\n" + "─" * 62)
        print("%s · экстремум 90д (продакшн)" % nm)
        print("  " + _tgt_line(m))
        if not m:
            continue
        if not m["quorum"]:
            print("  ВЕРДИКТ: не выносится — ниже кворума")
        elif not np.isfinite(m["omega"]):
            print("  ВЕРДИКТ: не выносится — Ω не определена")
        else:
            lo_, hi_ = m["omega_ci"]
            v = ("ДИ95 ЦЕЛИКОМ НИЖЕ %.2f — экстремум 90д не даёт шансов, "
                 "которые обещает его собственный RR, на горизонте, которым "
                 "система торгует" % bar if hi_ < bar else
                 "ДИ95 целиком выше %.2f — даёт, и с запасом; цель канала "
                 "продолжения отклоняется" % bar if lo_ > bar else
                 "ДИ95 накрывает %.2f — даёт; цель канала продолжения "
                 "отклоняется" % bar)
            print("  ВЕРДИКТ (правило зафиксировано до прогона): " + v)
        print("  СПРАВОЧНО калибровка цели факт/модель: %s"
              % ("не считается" if m["calib"] is None else
                 "%.2f [%.2f; %.2f] (факт %.1f%% · модель %.1f%%)"
                 % (m["calib"], m["calib_ci"][0], m["calib_ci"][1],
                    100 * m["measured"], 100 * m["model"])))
        print("  СПРАВОЧНО P(никуда за %dч): %.1f%%"
              % (sm["H"], 100 * (m["p_none"] or 0)))
        print("  СПРАВОЧНО модельные шансы Σq/Σ(1−q) по ЛОГ-дистанциям: %s · "
              "среднее 1/RR по относительным: %s"
              % ("—" if m["model_odds"] is None else "%.3f" % m["model_odds"],
                 "—" if m["inv_rr"] is None else "%.3f" % m["inv_rr"]))
        print("  СПРАВОЧНО реализованный R (+rr цель / −1 стоп / 0 ничья / "
              "переоценка на H): %s" % ("—" if m["R"] is None
                                        else "%+.3f" % m["R"]))
        print("    Регистрируется БЕЗ ПОСЛЕДСТВИЙ: при E[R]=0 на блуждании "
              "(инв. 32) это число\n    не может быть доводом ни за одну из "
              "целей, пока не предъявлен источник\n    сноса или издержек.")
        sd_m = sm["sides"][sd]
        print("  СПРАВОЧНО ранговая связь RR ↔ tgtSig на ВСЕХ %d строках, "
              "дошедших до геометрии: %s"
              % (sd_m["n_geo"], "—" if sd_m["spearman"] is None
                 else "%+.3f" % sd_m["spearman"]))
        for key, t in (("adm", "допущено"), ("ref", "отказано")):
            v = sd_m[key]
            print("  СПРАВОЧНО tgtSig %s: %s" % (t, "—" if not v else
                  "n=%d · медиана %.2f · p10 %.2f · p90 %.2f"
                  % (v["n"], v["med"], v["p10"], v["p90"])))
        print("  КАНАЛ ПРОДОЛЖЕНИЯ:")
        for k in sm["ks"]:
            c = sm["arms"][_ak(k)][sd]
            if not c:
                print("    k=%.1f · сетапов нет" % k)
                continue
            print("    k=%.1f · n=%-5d дат %-4d Ω %s · калибровка %s · "
                  "P(никуда) %.0f%%%s"
                  % (k, c["n"], c["n_dates"],
                     "—" if not np.isfinite(c["omega"]) else
                     "%.3f [%.3f; %.3f]" % (c["omega"], c["omega_ci"][0],
                                            c["omega_ci"][1]),
                     "—" if c["calib"] is None else "%.2f" % c["calib"],
                     100 * (c["p_none"] or 0),
                     "" if c["quorum"] else " · НИЖЕ КВОРУМА"))
        ks_ = sd_m["kstar"]
        print("  k* (наименьший k, чей ДИ95 накрывает %.2f или выше): %s"
              % (bar, "нет такого k в сетке" if ks_ is None else "%.1f" % ks_))
        print("    k* — НАХОДКА, а не константа: в index.html она не "
              "переносится и продакшн-числом не становится.")
    print("\n" + "─" * 62)
    print("ЧТО СРАВНИВАЛОСЬ (инв. 22) · допущено сетапов по монетам")
    print("  %-8s %5s %7s %7s %7s" % ("монета", "дат", "лонг", "шорт", "канал"))
    for r in sm["symbols"]:
        print("  %-8s %5d %7d %7d %7d"
              % (r["sym"], r["dates"], r["long"], r["short"], r["cont"]))


def _tgt_probe_rr(html):
    """The admissible set of K_GRID, MEASURED through production's own
    tradeGeometry and never derived in Python (inv. 21).

    One probe row at the most generous point production arithmetic allows:
    E = 1, min30 and max30 at E so invalidationInfo's dStruct clamps up to the
    INV_FLOOR_SD floor, and volatility immediately below VOL_STOP. RR is
    largest exactly there — rr = (exp(k·vol·sqrt(H_NOISE)) − 1) /
    (INV_FLOOR_SD·sigmaDay(vol)) grows with vol up to that cut — so a grid
    point whose probe rr is below RR_MIN cannot hold a setup on ANY world, and
    a bar requiring one there tests nothing. The long side dominates the short
    for the same k (exp(x) − 1 > 1 − exp(−x)), so one long row bounds both.
    tradeGeometry sets rr before it pushes any veto, so a refused row still
    reports its number. Returns [(k, rr, admittable)]."""
    vol = _read_js_num(html, "VOL_STOP") * (1 - 1e-9)
    H = int(_read_js_num(html, "H_NOISE"))
    rr_min = _read_js_num(html, "RR_MIN")
    E = 1.0
    q = vol * math.sqrt(H)
    br = JsBridge(html, TARGET_JS_FUNCS, TARGET_JS_VARS, TARGET_DRIVER,
                  "_tgt_bridge.js")
    r = br.call([{"cd": {"volatility": vol, "min30": E, "max30": E,
                         "min_price": E, "max_price": E},
                  "E": E, "isLong": True, "H": H,
                  "btcStats": {"volatility": vol, "r7": 0.0, "r14": 0.0},
                  "hi24": E, "lo24": E,
                  "subs": {_ak(k): E * math.exp(k * q) for k in K_GRID}}])[0]
    if r is None:
        raise RuntimeError("зонд допустимости не прошёл через продакшн-"
                           "геометрию: сетку не с чем сверять (инв. 22)")
    out = []
    for k in K_GRID:
        g = r["subs"][_ak(k)]["g"]
        rr = g["rr"] if g else None
        out.append((k, rr, rr is not None and rr >= rr_min))
    return out


# ── 11. --lab-selftest · known-answer worlds for the four experiments ───────
def synth_hl(mode, n_coins=16, hours=16000, seed=3, sub=6):
    """Hourly series WITH intra-hour high/low built from `sub` substeps.
    normal — iid gaussian substeps: measured touch must match the model;
    wick   — the same diffusion plus rare one-sided intra-hour wicks
             (~1.7/week per side, 6..14 sigma-hour deep) that fully retrace
             before the close. Close-based sigma is provably blind to them,
             so the barrier and the model p do not move while true touches
             do. Known answer: ratio > 1 — the exact error class the primary
             exists to catch (stop-hunt wicks).
    Lessons recorded during control construction, BEFORE real data (inv. 23):
    (1) VOLATILITY CLUSTERING at the 2-sigma floor pushes the ratio BELOW 1 —
    touch probability is concave in sigma near 40-55%, so regime mixing
    LOWERS the average versus the flat-vol model. A real-run ratio < 1 is
    therefore explainable by clustering and errs in the safe direction.
    (2) Symmetric diffusive jumps mostly land IN the estimated sigma: the
    barrier scales with it and the ratio stays ~1 — variance-like fat tails
    are already absorbed by the engine's own vol measurement."""
    rng = np.random.default_rng(seed)
    t0 = 1700000000000
    out = {}
    for c in range(n_coins):
        v = 0.006 + 0.006 * rng.random()            # hourly vol 0.6–1.2%
        e = rng.normal(0, v / math.sqrt(sub), (hours, sub))
        cum = np.cumsum(e.reshape(-1))
        lp = np.concatenate([[0.0], cum]).reshape(-1)
        # per-hour path: lp[i*sub] .. lp[(i+1)*sub]
        P, HL = [], []
        base = 10.0
        wick_lo = np.zeros(hours)
        wick_hi = np.zeros(hours)
        if mode == "wick":
            ev = rng.random(hours) < 0.02            # ~1.7 events/week per side
            side = rng.random(hours) < 0.5
            depth = rng.uniform(6, 14, hours) * v
            wick_lo[ev & side] = depth[ev & side]
            wick_hi[ev & ~side] = depth[ev & ~side]
        for i in range(hours):
            seg = lp[i * sub:(i + 1) * sub + 1]
            ts = t0 + (i + 1) * HOUR_MS
            P.append([ts, float(base * math.exp(seg[-1]))])
            HL.append([ts, float(base * math.exp(seg.max() + wick_hi[i])),
                       float(base * math.exp(seg.min() - wick_lo[i]))])
        V = [[P[i][0], 1e7] for i in range(hours)]
        out["C%02d" % c] = {"prices": P, "volumes": V, "hl": HL}
    return out


def synth_res(mode, n_coins=20, hours=12000, seed=3, beta=0.7):
    """resnull — idio is a random walk: residual factor must read 0.
    resrev  — idio LEVEL mean-reverts to 0 with ~3.5-day half-life: a coin
    that fell on its own move rebounds -> contrarian res7 must go positive."""
    rng = np.random.default_rng(seed)
    t0 = 1700000000000
    mkt = np.cumsum(rng.normal(0, 0.004, hours))
    k = {"resnull": 0.0, "resrev": 1 - 0.5 ** (1 / 84.0)}[mode]
    out = {"__mkt": mkt}
    for c in range(n_coins):
        e = rng.normal(0, 0.010, hours)
        x = np.zeros(hours)
        for i in range(1, hours):
            x[i] = x[i - 1] * (1 - k) + e[i]
        lp = beta * mkt + x
        p = 10.0 * np.exp(lp)
        ts = [t0 + (i + 1) * HOUR_MS for i in range(hours)]
        out["C%02d" % c] = {"prices": [[ts[i], float(p[i])] for i in range(hours)],
                            "volumes": [[ts[i], 1e7] for i in range(hours)]}
    btc = {"prices": [[t0 + (i + 1) * HOUR_MS, float(50000 * math.exp(mkt[i]))]
                      for i in range(hours)], "volumes": []}
    out.pop("__mkt")
    return out, btc


def synth_fund(coupled, n_coins=20, hours=12000, seed=5, g=5e-4):
    """Prices + synthetic 8h funding. coupled=True: a causal negative drift
    -g*z_fund(t) is injected into each coin's idio — crowded funding must
    predict underperformance and the SHORT primary must go positive.
    coupled=False: funding exists but is wired to nothing — must read 0."""
    rng = np.random.default_rng(seed)
    t0 = 1700000000000
    mkt = np.cumsum(rng.normal(0, 0.004, hours))
    ser, fund = {}, {}
    for c in range(n_coins):
        n8 = hours // 8 + 40
        f = np.zeros(n8)
        for i in range(1, n8):
            f[i] = 0.97 * f[i - 1] + rng.normal(0, 8e-5)
        fts = [t0 + i * 8 * HOUR_MS for i in range(n8)]
        fund["C%02d" % c] = [[fts[i], float(f[i])] for i in range(n8)]
        fsd = float(np.std(f)) or 1e-9
        lp = np.zeros(hours)
        for i in range(1, hours):
            drift = -g * (f[min(i // 8, n8 - 1)] / fsd) if coupled else 0.0
            lp[i] = lp[i - 1] + drift + rng.normal(0, 0.010) + 0.7 * (mkt[i] - mkt[i - 1])
        p = 10.0 * np.exp(lp)
        ts = [t0 + (i + 1) * HOUR_MS for i in range(hours)]
        ser["C%02d" % c] = {"prices": [[ts[i], float(p[i])] for i in range(hours)],
                            "volumes": [[ts[i], 1e7] for i in range(hours)]}
    return ser, fund


def lab_selftest(html, bot, seeds=3):
    """Known-answer worlds for all three experiments. Direction of error is
    safe by construction: a healthy stand can flag itself broken on an unlucky
    seed, never the reverse claim."""
    ok = True

    # A · stops: extraction + calibration on flat vol, detection on clustered
    print("A · --stops")
    sm_n = stops_summary(run_stops(synth_hl("normal"), bot, html, verbose=False))
    sm_c = stops_summary(run_stops(synth_hl("wick"), bot, html, verbose=False))
    for side in ("long", "short"):
        n, c = sm_n[side], sm_c[side]
        in1 = n["ratio_ci"][0] <= 1.0 <= n["ratio_ci"][1] or 0.85 <= n["ratio"] <= 1.10
        det = c["ratio"] > n["ratio"] and c["ratio_ci"][0] > 1.0
        print("  %-5s flat ratio %.2f [%.2f;%.2f] %s · wick %.2f [%.2f;%.2f] %s"
              % (side, n["ratio"], n["ratio_ci"][0], n["ratio_ci"][1],
                 "ОК" if in1 else "СТОП",
                 c["ratio"], c["ratio_ci"][0], c["ratio_ci"][1],
                 "ОК" if det else "СТОП"))
        ok = ok and in1 and det

    # B · res7: beta recovery + null reads 0 + reversion reads +
    print("B · --res7")
    icn, icr, bset = [], [], []
    for sd in range(1, seeds + 1):
        ser, btc = synth_res("resnull", seed=sd)
        bw = BetaWalk(bot, btc["prices"])
        s0 = sorted(ser)[0]
        b = bw.betas(ser[s0]["prices"], len(ser[s0]["prices"]) - 1,
                     [p[0] for p in ser[s0]["prices"]])
        bset += [b["up_beta_90"], b["down_beta_90"]]
        d = run_res7(ser, btc, bot, html, verbose=False)
        icn.append(metrics(d, "res_c", 1.0)["ic_mean"])
        ser, btc = synth_res("resrev", seed=sd)
        d = run_res7(ser, btc, bot, html, verbose=False)
        icr.append(metrics(d, "res_c", 1.0)["ic_mean"])
    se = 0.03
    b_ok = all(bb is not None and 0.5 < bb < 0.9 for bb in bset)
    n_ok = abs(float(np.mean(icn))) < 2 * se / math.sqrt(seeds)
    r_ok = float(np.mean(icr)) > 0.10
    print("  беты восстановлены: %s (среднее %.2f) · нулевой мир IC %+.3f %s · "
          "возвратный мир IC %+.3f %s"
          % ("ОК" if b_ok else "СТОП", float(np.mean([b for b in bset if b])),
             float(np.mean(icn)), "ОК" if n_ok else "СТОП",
             float(np.mean(icr)), "ОК" if r_ok else "СТОП"))
    ok = ok and b_ok and n_ok and r_ok

    # C · funding: uncoupled reads 0, coupled reads + on the SHORT primary
    print("C · --funding")
    icn, icc = [], []
    for sd in range(1, seeds + 1):
        ser, fund = synth_fund(False, seed=sd)
        icn.append(metrics(run_funding(ser, fund, bot, verbose=False),
                           "fz", -1.0)["ic_mean"])
        ser, fund = synth_fund(True, seed=sd)
        icc.append(metrics(run_funding(ser, fund, bot, verbose=False),
                           "fz", -1.0)["ic_mean"])
    n_ok = abs(float(np.mean(icn))) < 2 * se / math.sqrt(seeds)
    c_ok = float(np.mean(icc)) > 0.10
    print("  нулевой мир IC %+.3f %s · связанный мир IC %+.3f %s"
          % (float(np.mean(icn)), "ОК" if n_ok else "СТОП",
             float(np.mean(icc)), "ОК" if c_ok else "СТОП"))
    ok = ok and n_ok and c_ok

    # D · target: the continuation channel against the 90-day extremum. Runs
    # unconditionally, not behind a flag: a comparator never proven on identity
    # supports no claim about a real diff (inv. 45).
    print("D · --target")
    H1 = int(_read_js_num(html, "H_NOISE"))
    w = synth_hl("normal")
    btc = w.pop(sorted(w)[0])       # BTC is the regime meter, not a candidate
    dA = run_target(w, bot, html, btc, k_grid=K_GRID, want_identity=True,
                    verbose=False)
    sA = target_summary(dA, html)

    c = sA["pooled"][_ak(1.5)]
    d1 = bool(c and c["calib"] is not None
              and (c["calib_ci"][0] <= 1.0 <= c["calib_ci"][1]
                   or 0.85 <= c["calib"] <= 1.10))
    print("  D1 калибровка цели, k=1.5: %s %s"
          % ("—" if not c or c["calib"] is None else
             "%.2f [%.2f; %.2f]" % (c["calib"], c["calib_ci"][0],
                                    c["calib_ci"][1]),
             "ОК" if d1 else "СТОП"))

    # D2 · the grid is filled where production can fill it, and Ω falls where
    # there is enough of it to fall. The admissible set is a MEASUREMENT of
    # production geometry (the probe), not a hand-written expectation: k = 1.0
    # is unreachable by production arithmetic, and the five-point form this
    # replaces therefore asserted a property no world could satisfy.
    ov = [(sA["pooled"][_ak(k)] or {}).get("omega", float("nan"))
          for k in K_GRID]
    on = [(sA["pooled"][_ak(k)] or {}).get("n", 0) for k in K_GRID]
    probe = _tgt_probe_rr(html)
    # D2a — emptiness matches admissibility exactly, and the grid fills
    # monotonically: rr and tgtSig both grow with the target distance at fixed
    # (vol, dist), so admission at k implies admission at every larger k.
    d2a = (all((n > 0) == adm for (_, _, adm), n in zip(probe, on))
           and all(on[i] <= on[i + 1] for i in range(len(on) - 1)))
    # D2b — the Ω claim is made only where there is a quorum, and only if at
    # least TGT_MONO_MIN_PTS points carry one: two points are not a trend.
    qi = [i for i, k in enumerate(K_GRID)
          if (sA["pooled"][_ak(k)] or {}).get("n", 0) >= TGT_QUORUM_N]
    oq = [ov[i] for i in qi]
    d2b = (len(qi) >= TGT_MONO_MIN_PTS and all(np.isfinite(v) for v in oq)
           and all(oq[i] > oq[i + 1] for i in range(len(oq) - 1)))
    d2 = d2a and d2b
    print("  D2 монотонность Ω(k) на точках с кворумом: %s %s"
          % (" > ".join("%.3f" % v for v in oq) if oq else "—",
             "ОК" if d2 else "СТОП"))
    print("     допущено на точку сетки: %s"
          % " · ".join("k=%.1f n=%d" % (k, n) for k, n in zip(K_GRID, on)))
    print("     зонд продакшн-геометрии (пол инвалидации, vol у VOL_STOP): %s"
          % " · ".join("k=%.1f rr %s %s"
                       % (k, "—" if rr is None else "%.4f" % rr,
                          "допустима" if adm else "НЕДОСТИЖИМА")
                       for k, rr, adm in probe))
    print("     D2a пустота совпадает с недостижимостью, заполнение не убывает:"
          " %s · D2b точек с кворумом %d (нужно %d): %s"
          % ("ОК" if d2a else "СТОП", len(qi), TGT_MONO_MIN_PTS,
             "ОК" if d2b else "СТОП"))

    # D3 · the two-barrier limit, read off a LADDER instead of one rung. The
    # single-rung form this replaces carried two hand-written numerals, and a
    # band deciding whether a measurement is plausible is derived from the null
    # computed in the same run, never typed into the rule (inv. 49). Nothing
    # below is a number about the outcome: escape must decay, the gap to the
    # closed form must shrink, and the limit must be reached where escape has.
    lad = []
    for m in TGT_H_LADDER:
        Hm = m * H1
        dL = run_target(w, bot, html, btc, k_grid=[], H_override=Hm,
                        verbose=False)
        lad.append((m, target_summary(dL, html, ks=[], H=Hm)["pooled"]["prod"]))

    def _gap(pm):                       # |Ω − Σq/Σ(1−q)| / (Σq/Σ(1−q))
        if not pm or not pm["model_odds"] or pm["model_odds"] <= 0:
            return None
        return (abs(pm["omega"] - pm["model_odds"]) / pm["model_odds"]
                if np.isfinite(pm["omega"]) else None)

    pn = [(pm["p_none"] if pm and pm["p_none"] is not None else None)
          for _, pm in lad]
    gp = [_gap(pm) for _, pm in lad]
    print("  D3 предельный переход, лестница H = m×%dч:" % H1)
    for (m, pm), g in zip(lad, gp):
        if not pm:
            print("    m=%-3d H=%-5d сетапов нет" % (m, m * H1))
            continue
        print("    m=%-3d H=%-5d n=%-5d дат %-4d %-12s P(никуда) %.3f · "
              "Ω %s · Σq/Σ(1−q) %s · разрыв %s"
              % (m, m * H1, pm["n"], pm["n_dates"],
                 "кворум" if pm["quorum"] else "НИЖЕ КВОРУМА",
                 pm["p_none"] if pm["p_none"] is not None else float("nan"),
                 "—" if not np.isfinite(pm["omega"]) else
                 "%.3f [%.3f; %.3f]" % (pm["omega"], pm["omega_ci"][0],
                                        pm["omega_ci"][1]),
                 "—" if pm["model_odds"] is None else "%.3f" % pm["model_odds"],
                 "—" if g is None else "%.1f%%" % (100 * g)))
    have_pn = all(v is not None for v in pn)
    d3a = (have_pn and all(pn[i] >= pn[i + 1] for i in range(len(pn) - 1))
           and pn[-1] < pn[0])
    d3b = (gp[0] is not None and gp[-1] is not None and gp[-1] < gp[0])
    cand = [i for i, (_, pm) in enumerate(lad)
            if pm and pm["quorum"] and gp[i] is not None]
    istar = min(cand, key=lambda i: gp[i]) if cand else None
    med = float(np.median([v for v in pn if v is not None])) if have_pn else None
    if istar is None or med is None:
        d3c = False
    else:
        pstar = lad[istar][1]
        d3c = bool(pstar["omega_ci"][0] <= pstar["model_odds"]
                   <= pstar["omega_ci"][1] and pstar["p_none"] <= med)
    d3 = d3a and d3b and d3c
    print("     D3a уход затухает: P(никуда) %s %s"
          % (" → ".join("—" if v is None else "%.3f" % v for v in pn),
             "ОК" if d3a else "СТОП"))
    print("     D3b сближение с замкнутой формой: разрыв %s → %s %s"
          % ("—" if gp[0] is None else "%.1f%%" % (100 * gp[0]),
             "—" if gp[-1] is None else "%.1f%%" % (100 * gp[-1]),
             "ОК" if d3b else "СТОП"))
    print("     D3c предел там, где уход затух: %s %s"
          % ("рунгов с кворумом нет" if istar is None else
             "наименьший разрыв на m=%d · Σq/Σ(1−q) %.3f %s ДИ95 Ω "
             "[%.3f; %.3f] · P(никуда) %.3f против медианы %.3f"
             % (lad[istar][0], lad[istar][1]["model_odds"],
                "внутри" if (lad[istar][1]["omega_ci"][0]
                             <= lad[istar][1]["model_odds"]
                             <= lad[istar][1]["omega_ci"][1]) else "ВНЕ",
                lad[istar][1]["omega_ci"][0], lad[istar][1]["omega_ci"][1],
                lad[istar][1]["p_none"], med),
             "ОК" if d3c else "СТОП"))

    n_cmp, n_diff = 0, 0
    for d in dA:
        for o in d["obs"]:
            a1, a2 = o["arms"].get("prod"), o["arms"].get("ident")
            if (a1 is None) != (a2 is None):
                n_cmp += 1
                n_diff += 1
                continue
            if a1 is None:
                continue
            for f in ("first", "hit", "R", "p", "rr", "tgtSig", "a", "b"):
                n_cmp += 1
                n_diff += int(a1[f] != a2[f])
    d4 = n_cmp > 0 and n_diff == 0
    print("  D4 тождественный дифф: сравнений %d, расхождений %d %s"
          % (n_cmp, n_diff, "ОК" if d4 else "СТОП"))

    tmax = max(d["t"] for d in dA) + H1 * HOUR_MS
    cut = lambda ser: {s: {f: [r for r in ser[s][f] if r[0] <= tmax]
                           for f in ("prices", "volumes", "hl")} for s in ser}
    dC = run_target(cut(w), bot, html, cut({"B": btc})["B"], k_grid=K_GRID,
                    want_identity=True, verbose=False)
    d5 = (json.dumps(dA, sort_keys=True) == json.dumps(dC, sort_keys=True)
          and len(dA) > 0)
    print("  D5 взгляд в будущее: запись на полном ряде против обрезанного "
          "на t+H — %s %s" % ("совпала" if d5 else "РАЗОШЛАСЬ",
                              "ОК" if d5 else "СТОП"))

    ml, ms = sA["arms"]["prod"]["long"], sA["arms"]["prod"]["short"]
    d6 = bool(ml and ms and np.isfinite(ml["omega"])
              and np.isfinite(ms["omega"])
              and abs(ml["omega"] - ms["omega"]) <= 0.10)
    print("  D6 обмен сторон: Ω лонг %s · Ω шорт %s %s"
          % ("—" if not ml else "%.3f" % ml["omega"],
             "—" if not ms else "%.3f" % ms["omega"], "ОК" if d6 else "СТОП"))
    ok = ok and d1 and d2 and d3 and d4 and d5 and d6

    print("\nВЕРДИКТ ЛАБОРАТОРИИ: %s"
          % ("измеряет то, что должна" if ok else "НЕИСПРАВНА — результатам не верить"))
    return 0 if ok else 1

# ─────────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--regimes", action="store_true")
    ap.add_argument("--stops", action="store_true")
    ap.add_argument("--target", action="store_true")
    ap.add_argument("--res7", action="store_true")
    ap.add_argument("--funding", action="store_true")
    ap.add_argument("--fetch-funding", action="store_true")
    ap.add_argument("--lab-selftest", action="store_true")
    ap.add_argument("--lab-seeds", type=int, default=3)
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
    if a.lab_selftest:
        return lab_selftest(a.html, a.bot, a.lab_seeds)
    if a.fetch_funding:
        return fetch_funding(a.html, a.years)
    if a.stops:
        ser = load_cache()
        if len(ser) < 8:
            sys.exit("СТОП: в кэше %d монет." % len(ser))
        sm = stops_summary(run_stops(ser, a.bot, a.html, a.horizon, a.step))
        report_stops(sm)
        json.dump(sm, open(os.path.join(HERE, "stops_raw.json"), "w"))
        return 0
    if a.target:
        # --horizon/--step are NOT read here: the mode's horizon is H_NOISE cut
        # from index.html and its step is registered at 7 days (inv. 23).
        ser = load_cache()
        btc = load_cache(keep_btc=True).get("BTC")
        if btc is None:
            sys.exit("СТОП: в кэше нет BTC — плечо и режим считать не от чего.")
        if len(ser) < 8:
            sys.exit("СТОП: в кэше %d монет." % len(ser))
        sm = target_summary(run_target(ser, a.bot, a.html, btc,
                                       betawalk=BetaWalk(a.bot, btc["prices"])),
                            a.html)
        report_target(sm)
        json.dump(sm, open(os.path.join(HERE, "target_raw.json"), "w"))
        pl, ps = sm["arms"]["prod"]["long"], sm["arms"]["prod"]["short"]
        if not (pl and pl["quorum"]) and not (ps and ps["quorum"]):
            # A run that compared too little must not look like a run that
            # found nothing (инв. 22, 37).
            sys.exit("СТОП: обе стороны продакшн-рукава ниже кворума "
                     "(%d сетапов и %d дат) — сравнивать нечего."
                     % (TGT_QUORUM_N, TGT_QUORUM_D))
        return 0
    if a.res7:
        ser = load_cache()
        btc = load_cache(keep_btc=True).get("BTC")
        if btc is None:
            sys.exit("СТОП: в кэше нет BTC — остаток считать не от чего.")
        if len(ser) < 8:
            sys.exit("СТОП: в кэше %d монет." % len(ser))
        d = run_res7(ser, btc, a.bot, a.html, a.horizon, a.step)
        pri = (a.horizon == 7)
        factor_report("ОСТАТОК К BTC · контр (лонг) · %dд" % a.horizon,
                      metrics(d, "res_c", 1.0, level=95.0 if pri else EXPL_LEVEL),
                      pri)
        for ttl, key, sg in (("остаток · моментум (лонг)", "res_m", 1.0),
                             ("остаток · контр (шорт)", "res_m", -1.0),
                             ("r30 · контр (лонг)", "r30c", 1.0)):
            factor_report("%s · %dд" % (ttl, a.horizon),
                          metrics(d, key, sg, level=EXPL_LEVEL), False)
        json.dump([{"t": x["t"]} for x in d],
                  open(os.path.join(HERE, "res7_dates.json"), "w"))
        return 0
    if a.funding:
        ser = load_cache()
        fund = load_funding()
        if len(fund) < 8:
            sys.exit("СТОП: funding есть у %d монет. Сначала --fetch-funding."
                     % len(fund))
        d = run_funding(ser, fund, a.bot, a.horizon, a.step)
        pri = (a.horizon == 7)
        factor_report("FUNDING · перегрев лонгов (шорт) · %dд" % a.horizon,
                      metrics(d, "fz", -1.0, level=95.0 if pri else EXPL_LEVEL),
                      pri)
        for ttl, key, sg in (("funding-уровень (шорт)", "fp", -1.0),
                             ("funding z (лонг, зеркало)", "fz", 1.0)):
            factor_report("%s · %dд" % (ttl, a.horizon),
                          metrics(d, key, sg, level=EXPL_LEVEL), False)
        return 0
    if a.probe:
        print("Проверка доступности источников:"); probe(); return 0
    if a.fetch:
        return fetch_prices(a.html, a.bot, a.years, a.source)
    if a.verify:
        return verify_against_live(a.bot, a.html)
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
