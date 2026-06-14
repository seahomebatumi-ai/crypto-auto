import os, json, requests, time
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

def get_render_test():
    # Используем проверенный ID 'render-token'
    print("Запрос данных для render-token...")
    c_data = cg.get_coin_market_chart_by_id(id='render-token', vs_currency='usd', days=14)
    b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
    
    if not c_data or 'prices' not in c_data:
        raise Exception("Ошибка: CoinGecko не вернул данные для render-token")

    c_prices = np.array([float(p[1]) for p in c_data['prices']])
    b_prices = np.array([float(p[1]) for p in b_data['prices']])
    
    # Расчет доходности
    min_len = min(len(c_prices), len(b_prices))
    c_ret = np.diff(c_prices[-min_len:]) / c_prices[-min_len-1:-1]
    b_ret = np.diff(b_prices[-min_len:]) / b_prices[-min_len-1:-1]
    
    # Расчет бет с защитой от пустых масок
    up_mask = b_ret > 0
    down_mask = b_ret < 0
    
    up_beta = np.mean(c_ret[up_mask]) / np.mean(b_ret[up_mask]) if np.any(up_mask) else 0.0
    down_beta = np.mean(c_ret[down_mask]) / np.mean(b_ret[down_mask]) if np.any(down_mask) else 0.0
    
    return {
        "symbol": "RENDER", 
        "up_beta": float(np.nan_to_num(up_beta, nan=0.0)), 
        "down_beta": float(np.nan_to_num(down_beta, nan=0.0))
    }

def main():
    try:
        res = get_render_test()
        print(f"Результат расчета: {res}")
        
        # Запись результата
        payload = {
            "files": {
                "coeffs.json": {"content": json.dumps({"analysis_data": [res]})},
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
            print("Тест RENDER прошел успешно и записан в Gist!")
        else:
            print(f"Ошибка GitHub {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        raise e

if __name__ == "__main__":
    main()
