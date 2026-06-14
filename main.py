import os, json, requests, time
import numpy as np
from pycoingecko import CoinGeckoAPI

# Инициализация
cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

def run_render_only_test():
    print("--- ЗАПУСК ТЕСТА RENDER ---")
    
    # 1. Запрос данных именно по render-token
    c_data = cg.get_coin_market_chart_by_id(id='render-token', vs_currency='usd', days=14)
    b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
    
    if not c_data or 'prices' not in c_data:
        raise Exception("Критическая ошибка: данные не получены от CoinGecko (проверьте ID)")

    # 2. Математика
    c_prices = np.array([float(p[1]) for p in c_data['prices']])
    b_prices = np.array([float(p[1]) for p in b_data['prices']])
    
    min_len = min(len(c_prices), len(b_prices))
    c_ret = np.diff(c_prices[-min_len:]) / c_prices[-min_len-1:-1]
    b_ret = np.diff(b_prices[-min_len:]) / b_prices[-min_len-1:-1]
    
    # Защита от деления на ноль и пустых массивов
    up_beta = np.mean(c_ret[b_ret > 0]) if np.any(b_ret > 0) else 0.0
    down_beta = np.mean(c_ret[b_ret < 0]) if np.any(b_ret < 0) else 0.0
    
    res = {
        "symbol": "RENDER",
        "up_beta": float(np.nan_to_num(up_beta, nan=0.0)),
        "down_beta": float(np.nan_to_num(down_beta, nan=0.0)),
        "check": "TEST_SUCCESS"
    }
    
    # 3. Отправка в Gist
    payload = {
        "files": {
            "coeffs.json": {"content": json.dumps({"analysis_data": [res]}, indent=2)},
            "debug.json": {"content": json.dumps({"status": "render_test_ok", "time": time.time()})},
            "test_results.json": None
        }
    }
    
    print(f"Отправка данных: {res}")
    response = requests.patch(
        f"https://api.github.com/gists/{GIST_ID}", 
        headers={"Authorization": f"token {GIST_TOKEN}"}, 
        json=payload
    )
    
    if response.status_code == 200:
        print("ГОТОВО: Рендер успешно записан!")
    else:
        print(f"ОШИБКА GITHUB {response.status_code}: {response.text}")
        raise Exception("Запись не удалась")

if __name__ == "__main__":
    run_render_only_test()
