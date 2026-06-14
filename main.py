import os, json, time, requests
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

def run_render_production():
    # 1. Запрос данных для RENDER (используем точный ID)
    c_data = cg.get_coin_market_chart_by_id(id='render-token', vs_currency='usd', days=14)
    b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
    
    # 2. Математика (расчет реальной beta)
    c_prices = np.array([float(p[1]) for p in c_data['prices']])
    b_prices = np.array([float(p[1]) for p in b_data['prices']])
    
    min_len = min(len(c_prices), len(b_prices))
    c_ret = np.diff(c_prices[-min_len:]) / c_prices[-min_len-1:-1]
    b_ret = np.diff(b_prices[-min_len:]) / b_prices[-min_len-1:-1]
    
    up_mask = b_ret > 0
    down_mask = b_ret < 0
    
    # Расчет с защитой от пустых массивов
    up_beta = np.mean(c_ret[up_mask]) if np.any(up_mask) else 0.0
    down_beta = np.mean(c_ret[down_mask]) if np.any(down_mask) else 0.0
    
    # Формируем данные
    data = {
        "analysis_data": [{
            "symbol": "RENDER",
            "up_beta": float(np.nan_to_num(up_beta, nan=0.0)),
            "down_beta": float(np.nan_to_num(down_beta, nan=0.0))
        }]
    }
    
    # 3. Отправка в Gist (структура, которая точно работает)
    payload = {
        "files": {
            "coeffs.json": {
                "content": json.dumps(data)
            }
        }
    }
    
    response = requests.patch(
        f"https://api.github.com/gists/{GIST_ID}", 
        headers={"Authorization": f"token {GIST_TOKEN}", "Content-Type": "application/json"}, 
        json=payload
    )
    
    if response.status_code == 200:
        print("УСПЕХ! Данные RENDER обновлены.")
    else:
        print(f"ОШИБКА {response.status_code}: {response.text}")

if __name__ == "__main__":
    run_render_production()
