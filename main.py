import time
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

# Тестируем только эти две монеты
TEST_TOKENS = {
    'ONDO': 'ondo-finance', 
    'RENDER': 'render'
}

def test_coins():
    for symbol, coin_id in TEST_TOKENS.items():
        try:
            print(f"--- Тестирую {symbol} (ID: {coin_id}) ---")
            # Запрос данных за 1 день, чтобы снизить нагрузку на API
            data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=1)
            if data and 'prices' in data:
                print(f"УСПЕХ: {symbol} отвечает. Записей: {len(data['prices'])}")
            else:
                print(f"ОШИБКА: {symbol} не вернул цены.")
            time.sleep(5) # Увеличенная пауза для стабильности
        except Exception as e:
            print(f"КРИТИЧЕСКАЯ ОШИБКА для {symbol}: {e}")

if __name__ == "__main__":
    test_coins()
