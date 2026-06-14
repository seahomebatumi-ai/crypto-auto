import os, json, requests
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

def test_render():
    # Пробуем ID 'render-token'
    c_data = cg.get_coin_market_chart_by_id(id='render-token', vs_currency='usd', days=14)
    if not c_data or 'prices' not in c_data:
        raise Exception("Ошибка: ID 'render-token' не найден")
    return {"symbol": "RENDER", "status": "OK", "data_points": len(c_data['prices'])}

def main():
    result = test_render()
    
    # Обновляем Gist: сохраняем только результат теста и удаляем debug/test_results
    payload = {
        "files": {
            "coeffs.json": {"content": json.dumps({"test_result": result})},
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
        print("Тест Render успешен!")
    else:
        raise Exception(f"Ошибка GitHub {response.status_code}")

if __name__ == "__main__":
    main()
