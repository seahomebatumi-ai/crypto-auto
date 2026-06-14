import os, json, time, requests
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

TOKENS = {
    'SUI': 'sui', 'LINK': 'chainlink', 'NEAR': 'near', 'AAVE': 'aave', 
    'XRP': 'ripple', 'ADA': 'cardano', 'YFI': 'yearn-finance', 'TAO': 'bittensor',
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TON': 'the-open-network', 
    'AVAX': 'avalanche-2', 'ONDO': 'ondo-finance', 'RENDER': 'render-token'
}

def get_beta(coin_id, b_prices):
    time.sleep(2)
    c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=14)
    c_prices = np.array([float(p[1]) for p in c_data['prices']])
    
    min_len = min(len(c_prices), len(b_prices))
    c_ret = np.diff(c_prices[-min_len:]) / c_prices[-min_len-1:-1]
    b_ret = np.diff(b_prices[-min_len:]) / b_prices[-min_len-1:-1]
    
    up_beta = np.mean(c_ret[b_ret > 0]) if np.any(b_ret > 0) else 0.0
    down_beta = np.mean(c_ret[b_ret < 0]) if np.any(b_ret < 0) else 0.0
    
    return float(np.nan_to_num(up_beta, nan=0.0)), float(np.nan_to_num(down_beta, nan=0.0))

def main():
    b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
    b_prices = np.array([float(p[1]) for p in b_data['prices']])
    
    results = []
    for symbol, coin_id in TOKENS.items():
        u_b, d_b = get_beta(coin_id, b_prices)
        results.append({"symbol": symbol, "up_beta": u_b, "down_beta": d_b})
    
    payload = {"files": {"coeffs.json": {"content": json.dumps({"analysis_data": results})}}}
    
    requests.patch(f"https://api.github.com/gists/{GIST_ID}", 
                   headers={"Authorization": f"token {GIST_TOKEN}", "Content-Type": "application/json"}, 
                   json=payload)

if __name__ == "__main__":
    main()
