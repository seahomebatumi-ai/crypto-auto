import os
import json
import time
import requests
import numpy as np
from pycoingecko import CoinGeckoAPI

# Инициализация с ключом из GitHub Secrets
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
    # С демо-ключом пауза 0.6с — это безопасно и быстро
    time.sleep(0.6) 
    try:
        c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=14)
        c_prices = np.array([p[1] for p in c_data['prices']])
        c_ret = np.diff(c_prices) / c_prices[:-1]
        
        min_len = min(len(c_ret), len(b_ret))
        c_r = c_ret[-min_len:]
        b_r = b_ret[-min_len:]
        
        up_mask = b_r > 0
        down_mask = b_r < 0
        
        up_beta = np.mean(c_r[up_mask]) / np.mean(b_r[up_mask]) if sum(up_mask) > 5 else None
        down_beta = np.mean(c_r[down_mask]) / np.mean(b_r[down_mask]) if sum(down_mask) > 5 else None
        
        return {"up_beta": up_beta, "down_beta": down_beta, "error": False}
    except Exception as e:
        print(f"Ошибка при обработке {coin_id}: {e}")
        return {"up_beta": None, "down_beta": None, "error": True}

def main():
    try:
        b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
        b_prices = np.array([p[1] for p in b_data['prices']])
        b_ret = np.diff(b_prices) / b_prices[:-1]
        
        data = [{"symbol": s, **get_asymmetric_beta(i, b_prices, b_ret)} for s, i in TOKENS.items()]
        
        payload = {"files": {"coeffs.json": {"content": json.dumps({"analysis_data": data})}}}
        
        response = requests.patch(
            f"https://api.github.com/gists/{GIST_ID}", 
            headers={"Authorization": f"token {GIST_TOKEN}", "Content-Type": "application/json"}, 
            json=payload
        )
        
        if not response.ok:
            print(f"Ошибка GitHub Gist: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
