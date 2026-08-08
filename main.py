import os
import json
import time
import numpy as np
import requests
from datetime import datetime, timezone, timedelta
from pycoingecko import CoinGeckoAPI

# ============================================================
# Инициализация
# ============================================================
api_key = os.environ.get('COINGECKO_API_KEY')
cg = CoinGeckoAPI(api_key=api_key)

GIST_ID    = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

# Один запрос за 90 дней даёт оба таймфрейма:
# • 14-дневная бета  — последние 336 часовых бакетов (как раньше)
# • 90-дневная бета  — все ~2160 бакетов (новый таймфрейм)
DAYS_WINDOW      = 90
BUCKET_SECONDS   = 3600
MIN_MATCHED_14D  = 24    # минимум синхронных точек для 14d-беты
MIN_MATCHED_90D  = 120   # минимум для 90d-беты (5 дней)
REQUEST_GAP_SEC  = 1.0
MAX_RETRIES      = 3
RETRY_BACKOFF    = 3.0
RANK_LOOKBACK_H  = 24    # горизонт сравнения ранга (часы)

TOKENS = {
    'ETH': 'ethereum',
    'SUI': 'sui', 'LINK': 'chainlink', 'NEAR': 'near', 'AAVE': 'aave',
    'XRP': 'ripple', 'ADA': 'cardano', 'YFI': 'yearn-finance', 'TAO': 'bittensor',
    'FET': 'fetch-ai', 'ENA': 'ethena',
    # GRAM = ex-TON (ребрендинг 07.2026). CoinGecko id НЕ меняем: id у CG
    # постоянные при переименовании, и он сохраняет всю 90д-историю.
    'GRAM': 'the-open-network',
    'AVAX': 'avalanche-2', 'ONDO': 'ondo-finance', 'RENDER': 'render-token',
    'TRX': 'tron', 'SOL': 'solana', 'BCH': 'bitcoin-cash', 'HYPE': 'hyperliquid',
    'SKY': 'sky',
    'HBAR': 'hedera-hashgraph', 'XLM': 'stellar', 'ALGO': 'algorand',
    # BNB добавлен 2026-07-29. 24 альта + BTC = 25 вызовов/прогон (~18k/мес).
    'BNB': 'binancecoin',
    # Добавлены 2026-08-07. Итого 28 альтов + BTC = 29 market_chart
    # + 1 /coins/markets (ранги) = 30 вызовов/прогон (~21.6k/мес).
    'ZEC': 'zcash', 'XMR': 'monero', 'UNI': 'uniswap',
    # LIT на Binance = Lighter (перп LITUSDT, подтверждено 2026-08-07).
    # НЕ Litentry: тот id дал ранг #1183 и диапазон $0.06-1.26 при цене $2.33 —
    # детектор расхождения источников (инв. 11) поймал разные активы.
    # CG id не подтверждён по API: если бот даст NO DATA — найти точный id
    # через api.coingecko.com/api/v3/search?query=lighter и заменить строку.
    'LIT': 'lighter'
}

# ============================================================
# Вспомогательные функции
# ============================================================

def fetch_with_retry(coin_id):
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            data = cg.get_coin_market_chart_by_id(
                id=coin_id, vs_currency='usd', days=DAYS_WINDOW)
            if not data or 'prices' not in data or len(data['prices']) < 5:
                raise ValueError("Пустой или некорректный ответ CoinGecko")
            return data, None
        except Exception as e:
            last_err = str(e)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (2 ** (attempt - 1)))
    return None, last_err


def fetch_market_info():
    """Ранг капитализации + FDV/MC — ОДИН вызов /coins/markets (тот же, что был).
    FDV бесплатен: market_cap и fully_diluted_valuation уже приходят в ответе.
    Возвращает {coin_id: {"rank": int|None, "fdv_mc": float|None}}.
    Любой сбой -> {} (фронт рисует серый / не рисует FDV — инвариант 9)."""
    ids = ",".join(TOKENS.values())
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            data = cg.get_coins_markets(vs_currency='usd', ids=ids,
                                        per_page=250, page=1)
            out = {}
            for item in (data or []):
                cid = item.get('id')
                if not cid:
                    continue
                entry = {}
                r = item.get('market_cap_rank')
                if isinstance(r, int) and r > 0:
                    entry["rank"] = r
                # FDV/MC. None штатен: у монет без max supply (ETH, XMR)
                # CoinGecko отдаёт fully_diluted_valuation = null.
                mc  = item.get('market_cap')
                fdv = item.get('fully_diluted_valuation')
                try:
                    if mc and fdv and float(mc) > 0 and float(fdv) > 0:
                        ratio = float(fdv) / float(mc)
                        # Отсекаем мусор: FDV < MC невозможен экономически,
                        # >100x = ошибка данных о supply, а не сигнал.
                        if 0.95 <= ratio <= 100.0:
                            entry["fdv_mc"] = round(ratio, 3)
                except (TypeError, ValueError):
                    pass
                if entry:
                    out[cid] = entry
            return out
        except Exception:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (2 ** (attempt - 1)))
    return {}


def prev_ranks_from_history(history_points, now_utc):
    """Ранги из ближайшей точки истории СТАРШЕ RANK_LOOKBACK_H часов.
    Нет такой точки (история короче / сброшена) -> {} -> фронт серый."""
    cutoff = now_utc - timedelta(hours=RANK_LOOKBACK_H)
    for point in reversed(history_points):
        try:
            t = datetime.fromisoformat(str(point.get("t")))
        except Exception:
            continue
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        if t <= cutoff:
            out = {}
            for sym, v in (point.get("coins") or {}).items():
                if isinstance(v, dict) and isinstance(v.get("r"), int):
                    out[sym] = v["r"]
            return out
    return {}


def bucket_prices(price_list):
    """[[ts_ms, price], ...] -> {bucket_index: price}  (часовые бакеты)"""
    buckets = {}
    for ts_ms, price in price_list:
        b = int(ts_ms // (BUCKET_SECONDS * 1000))
        buckets[b] = price
    return buckets


def fit_stats(x, y):
    """OLS y = beta*x + c -> (beta, R2)"""
    if len(x) < 5:
        return None, None
    A = np.vstack([x, np.ones(len(x))]).T
    beta, c = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = beta * x + c
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0
    return float(beta), float(r2)


def paired_hourly_returns(btc_buckets, coin_buckets, keys):
    """Часовые возвраты ТОЛЬКО между соседними бакетами (k-1 -> k).
    Возвраты через дыры в данных (пропуск >1 часа) отбрасываются,
    чтобы не смешивать горизонты и не искажать бету/R2."""
    key_set = set(keys)
    b_r, c_r = [], []
    for k in keys:
        if (k - 1) in key_set:
            b_prev = btc_buckets[k - 1]
            c_prev = coin_buckets[k - 1]
            if b_prev > 0 and c_prev > 0:
                b_r.append(btc_buckets[k] / b_prev - 1.0)
                c_r.append(coin_buckets[k] / c_prev - 1.0)
    return np.array(b_r), np.array(c_r)


def safe_corr(x, y):
    """Пирсоновская корреляция с защитой от вырожденных рядов."""
    if len(x) < 5 or float(np.std(x)) == 0.0 or float(np.std(y)) == 0.0:
        return None
    c = float(np.corrcoef(x, y)[0, 1])
    return c if np.isfinite(c) else None


def asymmetric_beta(b_r, c_r):
    """Up-бета и down-бета из выровненных часовых ВОЗВРАТОВ."""
    if len(b_r) < 5:
        return None, None, None, None
    up_b,   up_r2   = fit_stats(b_r[b_r > 0], c_r[b_r > 0])
    down_b, down_r2 = fit_stats(b_r[b_r < 0], c_r[b_r < 0])
    return up_b, up_r2, down_b, down_r2


def get_token_betas(coin_id, btc_buckets, cutoff_14d):
    """
    Считает 14d-бету и 90d-бету за один запрос к CoinGecko.
    cutoff_14d — минимальный bucket_index, соответствующий 14 дням назад.
    """
    time.sleep(REQUEST_GAP_SEC)

    debug = {"candles_total": 0, "matched_90d": 0, "matched_14d": 0,
             "returns_90d": 0, "returns_14d": 0, "error": None}

    def err_result(msg):
        debug["error"] = msg
        empty = dict(up_beta=None, up_r2=None, down_beta=None, down_r2=None,
                     up_beta_90=None, up_r2_90=None, down_beta_90=None, down_r2_90=None,
                     corr_90=None,
                     price_pos=0, volatility=0, min_price=0, max_price=0, error=True)
        return empty, debug

    c_data, err = fetch_with_retry(coin_id)
    if c_data is None:
        return err_result(err)

    try:
        c_prices = np.array([p[1] for p in c_data['prices']])
        debug["candles_total"] = len(c_prices)

        # Собственные метрики монеты (по всем 90 дням, не зависят от BTC)
        cur   = c_prices[-1]
        min_p = float(np.min(c_prices))
        max_p = float(np.max(c_prices))
        price_pos  = ((cur - min_p) / (max_p - min_p) * 100) if max_p != min_p else 0
        volatility = float(np.std(np.diff(c_prices) / c_prices[:-1])) if len(c_prices) > 1 else 0

        coin_buckets = bucket_prices(c_data['prices'])
        common_90    = sorted(set(btc_buckets) & set(coin_buckets))
        debug["matched_90d"] = len(common_90)

        # -- 90-дневная бета + корреляция BTC/ALT --
        up_b90 = ur90 = dn_b90 = dr90 = corr90 = None
        if len(common_90) >= MIN_MATCHED_90D:
            b_r90, c_r90 = paired_hourly_returns(btc_buckets, coin_buckets, common_90)
            debug["returns_90d"] = len(b_r90)
            up_b90, ur90, dn_b90, dr90 = asymmetric_beta(b_r90, c_r90)
            corr90 = safe_corr(b_r90, c_r90)

        # -- 14-дневная бета (срез последних 14 дней из тех же данных) --
        common_14 = [k for k in common_90 if k >= cutoff_14d]
        debug["matched_14d"] = len(common_14)

        up_b = ur = dn_b = dr = None
        has_error_14 = len(common_14) < MIN_MATCHED_14D
        if not has_error_14:
            b_r14, c_r14 = paired_hourly_returns(btc_buckets, coin_buckets, common_14)
            debug["returns_14d"] = len(b_r14)
            up_b, ur, dn_b, dr = asymmetric_beta(b_r14, c_r14)
        else:
            debug["error"] = f"Мало 14d-точек: {len(common_14)}"

        return (
            dict(up_beta=up_b,   up_r2=ur,   down_beta=dn_b,   down_r2=dr,
                 up_beta_90=up_b90, up_r2_90=ur90,
                 down_beta_90=dn_b90, down_r2_90=dr90,
                 corr_90=corr90,
                 price_pos=float(price_pos), volatility=volatility,
                 min_price=min_p, max_price=max_p, error=has_error_14),
            debug
        )

    except Exception as e:
        return err_result(str(e))


# ============================================================
# Главный прогон
# ============================================================
def main():
    try:
        b_data, err = fetch_with_retry('bitcoin')
        if b_data is None:
            print(f"Критическая ошибка BTC: {err}")
            return

        btc_buckets  = bucket_prices(b_data['prices'])
        cutoff_14d   = int((time.time() - 14 * 24 * 3600) * 1000 // (BUCKET_SECONDS * 1000))
        now_utc      = datetime.now(timezone.utc)
        generated_at = now_utc.isoformat()

        # 90д-статистика самого BTC (тот же ответ, доп. запросов НЕТ).
        btc_p     = np.array([p[1] for p in b_data['prices']])
        btc_min   = float(np.min(btc_p))
        btc_max   = float(np.max(btc_p))
        btc_pos   = ((float(btc_p[-1]) - btc_min) / (btc_max - btc_min) * 100) \
                    if btc_max != btc_min else 0.0
        btc_vol   = float(np.std(np.diff(btc_p) / btc_p[:-1])) if len(btc_p) > 1 else 0.0
        btc_stats = {"min_price": btc_min, "max_price": btc_max,
                     "price_pos": float(btc_pos), "volatility": btc_vol}

        results    = []
        debug_info = {"timestamp": generated_at, "details": {}}

        for symbol, coin_id in TOKENS.items():
            beta_data, dbg = get_token_betas(coin_id, btc_buckets, cutoff_14d)
            results.append({"symbol": symbol, **beta_data})
            debug_info["details"][symbol] = dbg

        # --- Ранг по капитализации + FDV/MC: 1 вызов на весь список ---
        market_info = fetch_market_info()
        debug_info["ranks_fetched"] = sum(
            1 for v in market_info.values() if v.get("rank") is not None)
        debug_info["fdv_fetched"] = sum(
            1 for v in market_info.values() if v.get("fdv_mc") is not None)
        for row in results:
            info = market_info.get(TOKENS.get(row["symbol"])) or {}
            row["rank"] = info.get("rank")
            row["rank_prev"] = None   # заполняется ниже из history.json
            row["fdv_mc"] = info.get("fdv_mc")   # None штатен (нет max supply)

        # --- История бет: компактная запись по каждому токену ---
        # Дописываем одну точку на прогон. Храним только беты и R2 (без min/max/vol),
        # чтобы файл рос медленно. Старые записи обрезаем (хранится ~30 дней = 720 точек).
        # Читаем существующую историю из Gist, дописываем новую точку
        history_points = []
        try:
            existing = requests.get(
                f"https://api.github.com/gists/{GIST_ID}",
                headers={"Authorization": f"token {GIST_TOKEN}"},
                timeout=30
            )
            if existing.ok:
                files = existing.json().get("files", {})
                if "history.json" in files:
                    hf = files["history.json"]
                    # GitHub API обрезает файлы >1 МБ (truncated=true):
                    # тогда content неполный, json.loads падает и история
                    # сбрасывалась. Читаем полную версию через raw_url.
                    if hf.get("truncated") and hf.get("raw_url"):
                        raw = requests.get(hf["raw_url"], timeout=30).text
                    else:
                        raw = hf.get("content", "[]")
                    history_points = json.loads(raw)
                    if not isinstance(history_points, list):
                        history_points = []
        except Exception as e:
            print(f"История: не удалось прочитать прошлую ({e}), начинаем заново")
            history_points = []

        # Ранг 24ч назад — из уже прочитанной истории (доп. запросов НЕТ)
        prev_ranks = prev_ranks_from_history(history_points, now_utc)
        for row in results:
            row["rank_prev"] = prev_ranks.get(row["symbol"])

        # Снимок для истории: беты (как раньше) + ранг «r».
        # Поля опциональные — старые читатели history.json не ломаются.
        history_snapshot = {"t": generated_at, "coins": {}}
        for row in results:
            entry = {}
            if not row.get("error"):
                entry = {
                    "ub":  round(row["up_beta"], 3)    if row["up_beta"]    is not None else None,
                    "ur":  round(row["up_r2"], 3)      if row["up_r2"]      is not None else None,
                    "db":  round(row["down_beta"], 3)  if row["down_beta"]  is not None else None,
                    "dr":  round(row["down_r2"], 3)    if row["down_r2"]    is not None else None,
                    "ub90": round(row["up_beta_90"], 3)   if row["up_beta_90"]   is not None else None,
                    "db90": round(row["down_beta_90"], 3) if row["down_beta_90"] is not None else None,
                }
            if row.get("rank") is not None:
                entry["r"] = row["rank"]
            if entry:
                history_snapshot["coins"][row["symbol"]] = entry

        history_points.append(history_snapshot)
        # Обрезаем до последних 720 точек (~30 дней при часовом прогоне)
        if len(history_points) > 720:
            history_points = history_points[-720:]

        payload = {
            "files": {
                "coeffs.json": {"content": json.dumps({
                    "generated_at": generated_at,
                    "btc": btc_stats,
                    "analysis_data": results
                })},
                "debug.json": {"content": json.dumps(debug_info, indent=4)},
                "history.json": {"content": json.dumps(history_points)}
            }
        }

        r = requests.patch(
            f"https://api.github.com/gists/{GIST_ID}",
            headers={"Authorization": f"token {GIST_TOKEN}",
                     "Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        if not r.ok:
            print(f"Ошибка Gist: {r.status_code} {r.text}")

    except Exception as e:
        print(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
