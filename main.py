import os
import json
import time
import requests
import numpy as np
from datetime import datetime
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

def get_asymmetric_beta(coin_id, b_prices, b_ret):
    time.sleep(0.6) 
    try:
        c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=14)
        c_prices = np.array([p[1] for p in c_data['prices']])
        c_ret = np.diff(c_prices) / c_prices[:-1]
        
        # Новый расчет для аналитики
        volatility = np.std(c_ret)
        min_price = float(np.min(c_prices))
        max_price = float(np.max(c_prices))
        
        min_len = min(len(c_ret), len(b_ret))
        c_r = c_ret[-min_len:]
        b_r = b_ret[-min_len:]
        
        up_mask = b_r > 0
        down_mask = b_r < 0
        
        up_beta = np.mean(c_r[up_mask]) / np.mean(b_r[up_mask]) if sum(up_mask) > 5 else None
        down_beta = np.mean(c_r[down_mask]) / np.mean(b_r[down_mask]) if sum(down_mask) > 5 else None
        
        return {
            "beta": {
                "up_beta": up_beta, 
                "down_beta": down_beta, 
                "volatility": float(volatility),
                "min_price": min_price,
                "max_price": max_price,
                "error": False
            },
            "debug": {"candles_used": min_len}
        }
    except Exception as e:
        return {
            "beta": {"up_beta": None, "down_beta": None, "volatility": 0, "min_price": 0, "max_price": 0, "error": True},
            "debug": {"candles_used": 0, "error": str(e)}
        }

def main():
    try:
        b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
        b_prices = np.array([p[1] for p in b_data['prices']])
        b_ret = np.diff(b_prices) / b_prices[:-1]
        
        results = []
        debug_info = {"timestamp": datetime.utcnow().isoformat(), "details": {}}
        
        for s, i in TOKENS.items():
            res = get_asymmetric_beta(i, b_prices, b_ret)
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
        
        if not response.ok:
            print(f"Ошибка GitHub Gist: {response.status_code}")
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
