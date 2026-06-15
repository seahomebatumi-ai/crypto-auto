import os, json, time, requests
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

# Обновленный список монет с добавленными TRX, SOL, BCH, HYPE
TOKENS = {
    'SUI': 'sui', 'LINK': 'chainlink', 'NEAR': 'near', 'AAVE': 'aave', 
    'XRP': 'ripple', 'ADA': 'cardano', 'YFI': 'yearn-finance', 'TAO': 'bittensor',
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TON': 'the-open-network', 
    'AVAX': 'avalanche-2', 'ONDO': 'ondo-finance', 'RENDER': 'render-token',
    'TRX': 'tron', 'SOL': 'solana', 'BCH': 'bitcoin-cash', 'HYPE': 'hyperliquid'
}

def get_asymmetric_beta(coin_id, b_prices, b_ret):
    time.sleep(2.5)
    try:
        c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=14)
        c_prices = np.array([p[1] for p in c_data['prices']])
        c_ret = np.diff(c_prices) / c_prices[:-1]
        
        # Подгоняем длину, если данные CoinGecko немного отличаются
        min_len = min(len(c_ret), len(b_ret))
        c_r = c_ret[-min_len:]
        b_r = b_ret[-min_len:]
        
        up_mask = b_r > 0
        up_beta = np.mean(c_r[up_mask]) / np.mean(b_r[up_mask]) if sum(up_mask) > 5 else 1.2
        
        down_mask = b_r < 0
        down_beta = np.mean(c_r[down_mask]) / np.mean(b_r[down_mask]) if sum(down_mask) > 5 else 1.5
        
        return {"up_beta": float(up_beta), "down_beta": float(down_beta)}
    except:
        return {"up_beta": 1.2, "down_beta": 1.5}

def main():
    # Предварительно берем Биткоин
    b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
    b_prices = np.array([p[1] for p in b_data['prices']])
    b_ret = np.diff(b_prices) / b_prices[:-1]
    
    # ВОЗВРАЩАЕМ СТРУКТУРУ analysis_data
    data = [{"symbol": s, **get_asymmetric_beta(i, b_prices, b_ret)} for s, i in TOKENS.items()]
    
    payload = {"files": {"coeffs.json": {"content": json.dumps({"analysis_data": data})}}}
    
    requests.patch(f"https://api.github.com/gists/{GIST_ID}", 
                   headers={"Authorization": f"token {GIST_TOKEN}", "Content-Type": "application/json"}, 
                   json=payload)

if __name__ == "__main__":
    main()
