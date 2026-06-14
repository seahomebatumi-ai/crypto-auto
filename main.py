import os, json, requests, time
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

def get_asymmetric_beta(coin_id):
    # Берем данные
    c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=14)
    b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
    
    if not c_data or 'prices' not in c_data:
        raise Exception(f"Ошибка: данные для {coin_id} не получены")

    c_prices = [p[1] for p in c_data['prices']]
    b_prices = [p[1] for p in b_data['prices']]
    
    # Синхронизация по минимальной длине (чтобы избежать ошибки индексов)
    min_len = min(len(c_prices), len(b_prices))
    c_ret = np.diff(c_prices[-min_len:]) / np.array(c_prices[-min_len-1:-1])
    b_ret = np.diff(b_prices[-min_len:]) / np.array(b_prices[-min_len-1:-1])
    
    up_mask = b_ret > 0
    down_mask = b_ret < 0
    
    # Расчет бет
    up_beta = np.mean(c_ret[up_mask]) / np.mean(b_ret[up_mask])
    down_beta = np.mean(c_ret[down_mask]) / np.mean(b_ret[down_mask])
    
    return {"symbol": "RENDER", "up_beta": float(up_beta), "down_beta": float(down_beta)}

def main():
    # Прогоняем полноценный расчет
    result = get_asymmetric_beta('render-token')
    
    # Записываем результат в том же формате, что и основной бот
    payload = {
        "files": {
            "coeffs.json": {"content": json.dumps({"analysis_data": [result]})},
            "debug.json": None,
            "test_results.json": None
        }
    }
    
    response = requests.patch(
        f"https://api.github.com/gists/{GIST_ID}", 
        headers={"Authorization": f"token {GIST_TOKEN}"}, 
        json=payload
    )
    
    if response.status_code == 200:
        print("Тест Render с расчетом бет выполнен успешно.")
    else:
        raise Exception(f"Ошибка GitHub {response.status_code}")

if __name__ == "__main__":
    main()
