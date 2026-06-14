import os, json, time, requests
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

# Проверяем только эти две монеты
TOKENS = {
    'ONDO': 'ondo-finance', 
    'RENDER': 'render'
}

def check_coin(coin_id):
    # Прямой запрос к API для проверки доступности
    data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=1)
    return True if data and 'prices' in data else False

def main():
    for s, i in TOKENS.items():
        try:
            print(f"Тестирую ID для {s}: {i}...")
            if check_coin(i):
                print(f"УСПЕХ: {s} ({i}) доступен в API.")
            else:
                print(f"ОШИБКА: {s} ({i}) не возвращает данные.")
        except Exception as e:
            print(f"КРИТИЧЕСКАЯ ОШИБКА для {s} ({i}): {e}")
    
    print("Тест завершен. Проверьте логи GitHub Actions.")

if __name__ == "__main__":
    main()
