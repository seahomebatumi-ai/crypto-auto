import os, json, time, requests
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

# ВАЖНО: используем 'render-token' вместо старого 'render'
TOKENS = {
    'SUI': 'sui', 'LINK': 'chainlink', 'NEAR': 'near', 'AAVE': 'aave', 
    'XRP': 'ripple', 'ADA': 'cardano', 'YFI': 'yearn-finance', 'TAO': 'bittensor',
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TON': 'the-open-network', 
    'AVAX': 'avalanche-2', 'ONDO': 'ondo-finance', 'RENDER': 'render-token'
}

def get_asymmetric_beta(coin_id):
    # Добавляем паузу, чтобы API не блокировало запросы
    time.sleep(5) 
    
    # Запрос данных
    c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=14)
    b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
    
    if not c_data or 'prices' not in c_data:
        raise Exception(f"Ошибка API: данные для {coin_id} не получены")

    c_prices = np.array([float(p[1]) for p in c_data['prices']])
    b_prices = np.array([float(p[1]) for p in b_data['prices']])
    
    # Расчет корреляций
    min_len = min(len(c_prices), len(b_prices))
    c_ret = np.diff(c_prices[-min_len:]) / c_prices[-min_len-1:-1]
    b_ret = np.diff(b_prices[-min_len:]) / b_prices[-min_len-1:-1]
    
    up_beta = np.mean(c_ret[b_ret > 0]) if np.any(b_ret > 0) else 0.0
    down_beta = np.mean(c_ret[b_ret < 0]) if np.any(b_ret < 0) else 0.0
    
    return {
        "up_beta": float(np.nan_to_num(up_beta, nan=0.0)),
        "down_beta": float(np.nan_to_num(down_beta, nan=0.0))
    }

def main():
    results = []
    for s, i in TOKENS.items():
        try:
            print(f"Считаем {s}...")
            results.append({"symbol": s, **get_asymmetric_beta(i)})
        except Exception as e:
            print(f"Ошибка на {s}: {e}")
    
    # Отправка в Gist
    payload = {
        "files": {
            "coeffs.json": {"content": json.dumps({"analysis_data": results, "timestamp": time.time()})},
            "debug.json": None,
            "test_results.json": None
        }
    }
    
    response = requests.patch(f"https://api.github.com/gists/{GIST_ID}", 
                              headers={"Authorization": f"token {GIST_TOKEN}"}, json=payload)
    
    if response.status_code == 200:
        print("Данные успешно обновлены в Gist!")
    else:
        print(f"Ошибка GitHub {response.status_code}: {response.text}")

if __name__ == "__main__":
    main()
