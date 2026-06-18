import os
import json
import time
import numpy as np
import requests
from datetime import datetime, timezone
from pycoingecko import CoinGeckoAPI

# ============================================================
# Инициализация
# ============================================================
api_key = os.environ.get('COINGECKO_API_KEY')
cg = CoinGeckoAPI(api_key=api_key)

GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

DAYS_WINDOW = 14          # глубина истории (дней) — не менялась, как договорились
BUCKET_SECONDS = 3600     # размер тайм-бакета для синхронизации BTC <-> альт (1 час)
MIN_MATCHED_CANDLES = 24  # минимум синхронных точек, чтобы регрессия имела смысл
REQUEST_GAP_SEC = 1.0     # пауза между запросами к CoinGecko
MAX_RETRIES = 3           # попыток на каждый запрос при ошибке/рейт-лимите
RETRY_BACKOFF_BASE = 3.0  # секунд, растёт экспоненциально (3s, 6s, 12s)

TOKENS = {
    'SUI': 'sui', 'LINK': 'chainlink', 'NEAR': 'near', 'AAVE': 'aave',
    'XRP': 'ripple', 'ADA': 'cardano', 'YFI': 'yearn-finance', 'TAO': 'bittensor',
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TON': 'the-open-network',
    'AVAX': 'avalanche-2', 'ONDO': 'ondo-finance', 'RENDER': 'render-token',
    'TRX': 'tron', 'SOL': 'solana', 'BCH': 'bitcoin-cash', 'HYPE': 'hyperliquid',
    'SKY': 'sky'
}


# ============================================================
# Вспомогательные функции
# ============================================================

def fetch_market_chart_with_retry(coin_id):
    """Запрос к CoinGecko с retry/backoff на случай rate-limit / временных сбоев."""
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=DAYS_WINDOW)
            if not data or 'prices' not in data or len(data['prices']) < 5:
                raise ValueError("Пустой или некорректный ответ CoinGecko (нет 'prices')")
            return data, None
        except Exception as e:
            last_err = str(e)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF_BASE * (2 ** (attempt - 1)))
    return None, last_err


def bucket_prices_by_time(price_list, bucket_seconds=BUCKET_SECONDS):
    """
    Превращает [[ts_ms, price], ...] в {bucket_index: price}.
    Бакетизация по времени — ключевой фикс: раньше ряды BTC и альта
    выравнивались по индексу/длине массива, что давало рассинхрон,
    если у CoinGecko где-то была пропущена или сдвинута точка.
    Теперь сопоставление идёт по фактическому времени свечи.
    """
    buckets = {}
    for ts_ms, price in price_list:
        bucket = int(ts_ms // (bucket_seconds * 1000))
        buckets[bucket] = price  # данные идут хронологически, последняя точка в бакете побеждает
    return buckets


def fit_stats(x, y):
    """OLS-регрессия y = beta*x + intercept, возвращает (beta, R^2)."""
    if len(x) < 5:
        return None, None
    A = np.vstack([x, np.ones(len(x))]).T
    beta, intercept = np.linalg.lstsq(A, y, rcond=None)[0]

    y_pred = beta * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

    return float(beta), float(r2)


def get_asymmetric_beta(coin_id, btc_buckets):
    """
    Считает up/down beta и R^2 для одной монеты относительно BTC.
    btc_buckets — уже посчитанный {bucket_index: price} для BTC (считается один раз в main()).
    """
    time.sleep(REQUEST_GAP_SEC)

    debug = {"candles_total_coin": 0, "candles_matched": 0, "error": None}

    c_data, err = fetch_market_chart_with_retry(coin_id)
    if c_data is None:
        debug["error"] = err
        return {
            "beta": {
                "up_beta": None, "up_r2": None, "down_beta": None, "down_r2": None,
                "price_pos": 0, "volatility": 0, "min_price": 0, "max_price": 0,
                "error": True
            },
            "debug": debug
        }

    try:
        c_prices_full = np.array([p[1] for p in c_data['prices']])
        debug["candles_total_coin"] = len(c_prices_full)

        # --- Собственные метрики монеты (не требуют синхронизации с BTC) ---
        curr_price = c_prices_full[-1]
        min_p, max_p = float(np.min(c_prices_full)), float(np.max(c_prices_full))
        price_pos = ((curr_price - min_p) / (max_p - min_p)) * 100 if max_p != min_p else 0

        own_returns = np.diff(c_prices_full) / c_prices_full[:-1]
        volatility = float(np.std(own_returns)) if len(own_returns) > 1 else 0.0

        # --- Синхронизация с BTC по времени (ключевой фикс) ---
        coin_buckets = bucket_prices_by_time(c_data['prices'])
        common_keys = sorted(set(btc_buckets.keys()) & set(coin_buckets.keys()))
        debug["candles_matched"] = len(common_keys)

        if len(common_keys) < MIN_MATCHED_CANDLES:
            debug["error"] = f"Недостаточно синхронных точек с BTC: {len(common_keys)}"
            return {
                "beta": {
                    "up_beta": None, "up_r2": None, "down_beta": None, "down_r2": None,
                    "price_pos": float(price_pos), "volatility": volatility,
                    "min_price": min_p, "max_price": max_p, "error": True
                },
                "debug": debug
            }

        btc_aligned = np.array([btc_buckets[k] for k in common_keys])
        coin_aligned = np.array([coin_buckets[k] for k in common_keys])

        b_r = np.diff(btc_aligned) / btc_aligned[:-1]
        c_r = np.diff(coin_aligned) / coin_aligned[:-1]

        up_mask = b_r > 0
        down_mask = b_r < 0

        up_beta, up_r2 = fit_stats(b_r[up_mask], c_r[up_mask])
        down_beta, down_r2 = fit_stats(b_r[down_mask], c_r[down_mask])

        return {
            "beta": {
                "up_beta": up_beta, "up_r2": up_r2,
                "down_beta": down_beta, "down_r2": down_r2,
                "price_pos": float(price_pos),
                "volatility": volatility,
                "min_price": min_p,
                "max_price": max_p,
                "error": False
            },
            "debug": debug
        }

    except Exception as e:
        debug["error"] = str(e)
        return {
            "beta": {"up_beta": None, "up_r2": None, "down_beta": None, "down_r2": None,
                      "price_pos": 0, "volatility": 0, "min_price": 0, "max_price": 0, "error": True},
            "debug": debug
        }


def main():
    try:
        b_data, err = fetch_market_chart_with_retry('bitcoin')
        if b_data is None:
            print(f"Критическая ошибка: не удалось получить данные BTC ({err})")
            return

        btc_buckets = bucket_prices_by_time(b_data['prices'])

        results = []
        generated_at = datetime.now(timezone.utc).isoformat()
        debug_info = {"timestamp": generated_at, "details": {}}

        for symbol, coin_id in TOKENS.items():
            res = get_asymmetric_beta(coin_id, btc_buckets)
            results.append({"symbol": symbol, **res["beta"]})
            debug_info["details"][symbol] = res["debug"]

        # "generated_at" добавлен на верхний уровень coeffs.json — это нужно для
        # будущей проверки свежести данных в калькуляторе (текущий формат
        # analysis_data не меняется, совместимость с фронтендом сохранена)
        coeffs_payload = {
            "generated_at": generated_at,
            "analysis_data": results
        }

        payload = {
            "files": {
                "coeffs.json": {"content": json.dumps(coeffs_payload)},
                "debug.json": {"content": json.dumps(debug_info, indent=4)}
            }
        }

        response = requests.patch(
            f"https://api.github.com/gists/{GIST_ID}",
            headers={"Authorization": f"token {GIST_TOKEN}", "Content-Type": "application/json"},
            json=payload
        )

        if not response.ok:
            print(f"Ошибка GitHub Gist: {response.status_code} {response.text}")

    except Exception as e:
        print(f"Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
