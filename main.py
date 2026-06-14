import os, json, time, requests
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

TOKENS = {'SUI': 'sui', 'ONDO': 'ondo', 'LINK': 'chainlink', 'RENDER': 'render', 'NEAR': 'near', 'YFI': 'yearn-finance', 'AAVE': 'aave', 'AVAX': 'avalanche-2', 'FET': 'fetch-ai', 'ENA': 'ethena', 'TAO': 'bittensor', 'TON': 'the-open-network', 'XRP': 'ripple', 'ADA': 'ada'}

def get_asymmetric_beta(coin_id):
    # Увеличили паузу до 2.5с для стабильной работы с API CoinGecko
    time.sleep(2.5)
    try:
        # Изменили период с 30 на 14 дней
        c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=14)
        b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
        
        c_ret = np.diff([p[1] for p in c_data['prices']]) / [p[1] for p in c_data['prices']][:-1]
        b_ret = np.diff([p[1] for p in b_data['prices']]) / [p[1] for p in b_data['prices']][:-1]
        
        # Бета роста
        up_mask = b_ret > 0
        up_beta = np.mean(c_ret[up_mask]) / np.mean(b_ret[up_mask]) if sum(up_mask) > 5 else 1.2
        
        # Бета падения
        down_mask = b_ret < 0
        down_beta = np.mean(c_ret[down_mask]) / np.mean(b_ret[down_mask]) if sum(sub_mask := down_mask) > 5 else 1.5
        
        return {"up_beta": float(up_beta), "down_beta": float(down_beta)}
    except:
        return {"up_beta": 1.2, "down_beta": 1.5}

def main():
    data = [{"symbol": s, **get_asymmetric_beta(i)} for s, i in TOKENS.items()]
    requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers={"Authorization": f"token {GIST_TOKEN}"}, 
                   json={"files": {"coeffs.json": {"content": json.dumps({"analysis_data": data})}}})

if __name__ == "__main__":
    main()
