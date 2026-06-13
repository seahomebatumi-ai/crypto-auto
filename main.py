import os
import json
import time
import requests
from pycoingecko import CoinGeckoAPI
import numpy as np

# Инициализация
cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

TOKENS = {
    'SUI': 'sui', 'ONDO': 'ondo', 'LINK': 'chainlink', 'RENDER': 'render', 
    'NEAR': 'near', 'YFI': 'yearn-finance', 'AAVE': 'aave', 'AVAX': 'avalanche-2', 
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TAO': 'bittensor', 'TON': 'the-open-network', 
    'XRP': 'ripple', 'ADA': 'cardano'
}

def get_beta(coin_id):
    time.sleep(1.5) # Защита от лимитов CoinGecko
    try:
        data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
        prices = np.array([p[1] for p in data['prices']])
        returns = np.diff(prices) / prices[:-1]
        
        pos = returns[returns > 0]
        neg = returns[returns < 0]
        
        return {
            "up": float(np.mean(pos) * 100 if len(pos) > 0 else 1.0),
            "down": float(np.mean(neg) * 100 if len(neg) > 0 else -1.0),
            "status": "OK"
        }
    except Exception:
        return {"up": 1.0, "down": -1.0, "status": "FAIL"}

def main():
    analysis_data = []
    all_ok = True
    
    for symbol, coin_id in TOKENS.items():
        res = get_beta(coin_id)
        analysis_data.append({
            "symbol": symbol, 
            "up": res['up'], 
            "down": res['down'],
            "status": res['status']
        })
        if res['status'] == "FAIL": all_ok = False

    # Формируем структуру с общим статусом
    final_data = {
        "analysis_data": analysis_data,
        "global_status": "OK" if all_ok else "PARTIAL_FAIL",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Отправка в Gist
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    payload = {"files": {"coeffs.json": {"content": json.dumps(final_data)}}}
    
    res = requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=payload)
    print(f"Update finished with status: {res.status_code}")

if __name__ == "__main__":
    main()
