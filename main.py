import os, json, requests
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

# Только 4 монеты, без Ondo и Render. 
# Используем проверенные ID для CoinGecko API.
TEST_TOKENS = {
    'FET': 'fetch-ai',
    'ENA': 'ethena',
    'TON': 'the-open-network',
    'AVAX': 'avalanche-2'
}

def main():
    results = {}
    for s, i in TEST_TOKENS.items():
        print(f"Запрос для {s} ({i})...")
        data = cg.get_coin_market_chart_by_id(id=i, vs_currency='usd', days=1)
        if data and 'prices' in data:
            results[s] = "OK"
        else:
            results[s] = "ERROR: No data"
    
    # Записываем результат в файл test_results.json в Gist
    requests.patch(
        f"https://api.github.com/gists/{GIST_ID}", 
        headers={"Authorization": f"token {GIST_TOKEN}"}, 
        json={"files": {"test_results.json": {"content": json.dumps(results)}}}
    )
    print("Тест завершен. Проверьте test_results.json в вашем Gist.")

if __name__ == "__main__":
    main()
