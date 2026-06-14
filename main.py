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
    time.sleep(1.5) # Защита от лимитов
    try:
        # Изменено на btc для корректной корреляции
        data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='btc', days=30)
        prices = np.array([p[1] for p in data['prices']])
        returns = np.diff(prices) / prices[:-1]
        
        pos = returns[returns > 0]
        neg = returns[returns < 0]
        
        return {
            "up": float(np.mean(pos) * 100 if len(pos) > 0 else 0.0),
            "down": float(np.mean(neg) * 100 if len(neg) > 0 else 0.0),
            "status": "OK"
        }
    except Exception:
        return {"up": 0.0, "down": 0.0, "status": "FAIL"}

def main():
    analysis_data = []
    
    for symbol, coin_id in TOKENS.items():
        res = get_beta(coin_id)
        analysis_data.append({
            "symbol": symbol, 
            "up": res['up'], 
            "down": res['down'],
            "status": res['status']
        })

    # Вычисляем средние значения для обработки FAIL
    valid_data = [d for d in analysis_data if d['status'] == "OK"]
    avg_up = np.mean([d['up'] for d in valid_data]) if valid_data else 0.5
    avg_down = np.mean([d['down'] for d in valid_data]) if valid_data else -0.5

    # Заполняем FAIL значения средними
    for d in analysis_data:
        if d['status'] == "FAIL":
            d['up'] = avg_up
            d['down'] = avg_down

    final_data = {
        "analysis_data": analysis_data,
        "global_status": "OK",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    payload = {"files": {"coeffs.json": {"content": json.dumps(final_data)}}}
    
    res = requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=payload)
    print(f"Update finished with status: {res.status_code}")

if __name__ == "__main__":
    main()
