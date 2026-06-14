import os, json, time, requests
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

# Наш список 12 подтвержденных монет
TOKENS = {
    'SUI': 'sui', 'LINK': 'chainlink', 'NEAR': 'near', 'AAVE': 'aave', 
    'XRP': 'ripple', 'ADA': 'cardano', 'YFI': 'yearn-finance', 'TAO': 'bittensor',
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TON': 'the-open-network', 'AVAX': 'avalanche-2'
}

def get_asymmetric_beta(coin_id):
    time.sleep(3.0) 
    c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=14)
    b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
    
    # Извлекаем цены
    c_prices = [p[1] for p in c_data.get('prices', [])]
    b_prices = [p[1] for p in b_data.get('prices', [])]
    
    # СИНХРОНИЗАЦИЯ: делаем массивы одинаковой длины
    min_len = min(len(c_prices), len(b_prices))
    c_prices = c_prices[-min_len:]
    b_prices = b_prices[-min_len:]
    
    # Расчет процентных изменений
    c_ret = np.diff(c_prices) / np.array(c_prices[:-1])
    b_ret = np.diff(b_prices) / np.array(b_prices[:-1])
    
    # Расчет коэффициентов
    up_mask = b_ret > 0
    down_mask = b_ret < 0
    
    if sum(up_mask) < 5 or sum(down_mask) < 5: 
        raise Exception(f"Недостаточно данных для {coin_id}")
        
    up_beta = np.mean(c_ret[up_mask]) / np.mean(b_ret[up_mask])
    down_beta = np.mean(c_ret[down_mask]) / np.mean(b_ret[down_mask])
    
    return {"up_beta": float(up_beta), "down_beta": float(down_beta)}

def main():
    results = []
    for s, i in TOKENS.items():
        print(f"Обработка {s}...")
        results.append({"symbol": s, **get_asymmetric_beta(i)})
    
    # Обновляем Gist - формат данных для калькулятора остается прежним!
    response = requests.patch(
        f"https://api.github.com/gists/{GIST_ID}", 
        headers={"Authorization": f"token {GIST_TOKEN}"}, 
        json={"files": {"coeffs.json": {"content": json.dumps({"analysis_data": results})}}}
    )
    
    if response.status_code == 200:
        print("Данные успешно обновлены.")
    else:
        print(f"Ошибка GitHub {response.status_code}")
        raise Exception("Не удалось обновить Gist")

if __name__ == "__main__":
    main()
