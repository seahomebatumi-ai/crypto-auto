import os, json, requests
from pycoingecko import CoinGeckoAPI

# Данные для теста
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

def run_render_fix():
    # 1. Формируем данные
    data = {
        "analysis_data": [{
            "symbol": "RENDER",
            "up_beta": 0.5,
            "down_beta": 0.5
        }]
    }
    
    # 2. Формируем payload строго по документации GitHub Gist API
    payload = {
        "files": {
            "coeffs.json": {
                "content": json.dumps(data)
            }
        }
    }
    
    print("Отправка в Gist...")
    
    # 3. Отправка
    response = requests.patch(
        f"https://api.github.com/gists/{GIST_ID}", 
        headers={
            "Authorization": f"token {GIST_TOKEN}",
            "Content-Type": "application/json"
        }, 
        json=payload
    )
    
    # 4. Проверка
    if response.status_code == 200:
        print("УСПЕХ! GitHub принял файл.")
    else:
        print(f"ОШИБКА {response.status_code}: {response.text}")

if __name__ == "__main__":
    run_render_fix()
