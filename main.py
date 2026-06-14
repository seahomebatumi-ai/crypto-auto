import os, json, time, requests
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

# Полный список из 14 монет
TOKENS = {
    'SUI': 'sui', 'LINK': 'chainlink', 'NEAR': 'near', 'AAVE': 'aave', 
    'XRP': 'ripple', 'ADA': 'cardano', 'YFI': 'yearn-finance', 'TAO': 'bittensor',
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TON': 'the-open-network', 
    'AVAX': 'avalanche-2', 'ONDO': 'ondo-finance', 'RENDER': 'render'
}

def get_asymmetric_beta(coin_id):
    time.sleep(3.0) 
    c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=14)
    b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
    
    if not c_data or 'prices' not in c_data or not b_data or 'prices' not in b_data:
        raise Exception(f"Нет данных для {coin_id}")

    c_prices = [p[1] for p in c_data['prices']]
    b_prices = [p[1] for p in b_data['prices']]
    
    c_ret = np.diff(c_prices) / np.array(c_prices[:-1])
    b_ret = np.diff(b_prices) / np.array(b_prices[:-1])
    
    up_mask = b_ret > 0
    down_mask = b_ret < 0
    
    if sum(up_mask) < 5 or sum(down_mask) < 5: 
        raise Exception(f"Мало данных для {coin_id}")
        
    up_beta = np.mean(c_ret[up_mask]) / np.mean(b_ret[up_mask])
    down_beta = np.mean(c_ret[down_mask]) / np.mean(b_ret[down_mask])
    
    return {"up_beta": float(up_beta), "down_beta": float(down_beta)}

def main():
    results = []
    for s, i in TOKENS.items():
        results.append({"symbol": s, **get_asymmetric_beta(i)})
    
    response = requests.patch(
        f"https://api.github.com/gists/{GIST_ID}", 
        headers={"Authorization": f"token {GIST_TOKEN}"}, 
        json={"files": {"coeffs.json": {"content": json.dumps({"analysis_data": results})}}}
    )
    
    if response.status_code == 200:
        print("Полный список из 14 монет успешно обновлен.")
    else:
        raise Exception(f"Ошибка GitHub {response.status_code}")

if __name__ == "__main__":
    main()
