import os
import json
import time
import requests
import numpy as np
from datetime import datetime, timedelta
from pycoingecko import CoinGeckoAPI

# Инициализация
api_key = os.environ.get('COINGECKO_API_KEY')
cg = CoinGeckoAPI(api_key=api_key)

GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

TOKENS = {
    'SUI': 'sui', 'LINK': 'chainlink', 'NEAR': 'near', 'AAVE': 'aave', 
    'XRP': 'ripple', 'ADA': 'cardano', 'YFI': 'yearn-finance', 'TAO': 'bittensor',
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TON': 'the-open-network', 
    'AVAX': 'avalanche-2', 'ONDO': 'ondo-finance', 'RENDER': 'render-token',
    'TRX': 'tron', 'SOL': 'solana', 'BCH': 'bitcoin-cash', 'HYPE': 'hyperliquid',
    'SKY': 'sky'
}

BUCKET_MS = 3600 * 1000  # 1 час в миллисекундах

def fetch_with_retry(func, *args, **kwargs):
    """Механизм повторов при сбоях API"""
    for i in range(3):
        try:
            return func(*args, **kwargs)
        except Exception:
            time.sleep(2 * (i + 1))
    return func(*args, **kwargs)

def bucket_prices_by_time(price_list):
    """Приводит данные к часовым бакетам: {timestamp_hour: price}"""
    buckets = {}
    for ts_ms, price in price_list:
        bucket = (ts_ms // BUCKET_MS) * BUCKET_MS
        buckets[bucket] = price
    return buckets

def fit_stats(x, y):
    if len(x) < 5: return None, None
    A = np.vstack([x, np.ones(len(x))]).T
    beta, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = beta * x + intercept
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    return float(beta), float(r2)

def get_asymmetric_beta(coin_id, b_buckets):
    try:
        data = fetch_with_retry(cg.get_coin_market_chart_by_id, id=coin_id, vs_currency='usd', days=14)
        c_buckets = bucket_prices_by_time(data['prices'])
        
        # Freshness check: данные не старше 24ч
        last_ts = max(c_buckets.keys())
        if datetime.now().timestamp() * 1000 - last_ts > 86400000:
            raise ValueError("Data too old")

        # АЛГОРИТМ ВЫРАВНИВАНИЯ (Timestamp Alignment)
        common_ts = sorted(set(b_buckets.keys()) & set(c_buckets.keys()))
        if len(common_ts) < 10: raise ValueError("Insufficient overlap")

        b_aligned = np.array([b_buckets[ts] for ts in common_ts])
        c_aligned = np.array([c_buckets[ts] for ts in common_ts])
        
        # Расчет доходности по выровненным данным
        b_r = np.diff(b_aligned) / b_aligned[:-1]
        c_r = np.diff(c_aligned) / c_aligned[:-1]
        
        up_mask = b_r > 0
        down_mask = b_r < 0
        
        up_beta, up_r2 = fit_stats(b_r[up_mask], c_r[up_mask])
        down_beta, down_r2 = fit_stats(b_r[down_mask], c_r[down_mask])
        
        c_prices = np.array(list(c_buckets.values()))
        curr_price, min_p, max_p = c_prices[-1], np.min(c_prices), np.max(c_prices)
        price_pos = ((curr_price - min_p) / (max_p - min_p)) * 100 if max_p != min_p else 0
        
        return {
            "beta": {
                "up_beta": up_beta, "up_r2": up_r2,
                "down_beta": down_beta, "down_r2": down_r2,
                "price_pos": float(price_pos),
                "volatility": float(np.std(c_r)),
                "min_price": float(min_p),
                "max_price": float(max_p),
                "error": False
            },
            "debug": {"candles_used": len(common_ts)}
        }
    except Exception as e:
        return {
            "beta": {"up_beta": None, "up_r2": None, "down_beta": None, "down_r2": None, "price_pos": 0, "volatility": 0, "min_price": 0, "max_price": 0, "error": True},
            "debug": {"candles_used": 0, "error": str(e)}
        }

def main():
    try:
        # Предварительная бакетизация BTC (делаем один раз)
        b_data = fetch_with_retry(cg.get_coin_market_chart_by_id, id='bitcoin', vs_currency='usd', days=14)
        b_buckets = bucket_prices_by_time(b_data['prices'])
        
        results = []
        debug_info = {"timestamp": datetime.utcnow().isoformat(), "details": {}}
        
        for s, i in TOKENS.items():
            res = get_asymmetric_beta(i, b_buckets)
            results.append({"symbol": s, **res["beta"]})
            debug_info["details"][s] = res["debug"]
        
        payload = {
            "files": {
                "coeffs.json": {"content": json.dumps({"analysis_data": results})},
                "debug.json": {"content": json.dumps(debug_info, indent=4)}
            }
        }
        
        response = requests.patch(
            f"https://api.github.com/gists/{GIST_ID}", 
            headers={"Authorization": f"token {GIST_TOKEN}", "Content-Type": "application/json"}, 
            json=payload
        )
        
        if not response.ok: print(f"Ошибка GitHub Gist: {response.status_code}")
            
    except Exception as e: print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
