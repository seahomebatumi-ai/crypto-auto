import json, requests, numpy as np, os
from pycoingecko import CoinGeckoAPI

# Инициализация
cg = CoinGeckoAPI()
GIST_ID = '3f50574a29bc37434c18cc8480779ccb'
TOKEN = os.environ.get('GIST_TOKEN') or os.environ.get('GITHUB_TOKEN')

# Полный список 14 монет
coins = {
    'SUI': 'sui', 'ONDO': 'ondo-finance', 'LINK': 'link', 'RENDER': 'render-token', 
    'NEAR': 'near', 'YFI': 'yearn-finance', 'AAVE': 'aave', 'AVAX': 'avalanche-2', 
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TAO': 'bittensor', 'TON': 'the-open-network', 
    'XRP': 'ripple', 'ADA': 'cardano'
}

def update_gist():
    # 1. Данные по Биткоину (60 дней для стабильной статистики)
    btc_data = cg.get_coin_market_chart_by_id('bitcoin', 'usd', 60)
    b_prices = np.array([x[1] for x in btc_data['prices']])
    b_ret = np.diff(b_prices) / b_prices[:-1]
    
    # Структура для Gist
    results = {
        "current_btc_price": round(b_prices[-1], 2),
        "analysis_data": []
    }
    
    # 2. Анализ по каждой монете
    for sym, coin_id in coins.items():
        try:
            data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=60)
            t_prices = np.array([x[1] for x in data['prices']])
            t_ret = np.diff(t_prices) / t_prices[:-1]
            
            # Синхронизация по времени (берем последние N точек)
            min_len = min(len(t_ret), len(b_ret))
            b_slice = b_ret[-min_len:]
            t_slice = t_ret[-min_len:]
            
            # Индекс боли (реакция на падение битка)
            crash_mask = b_slice < 0
            pain = np.mean(t_slice[crash_mask]) / np.mean(b_slice[crash_mask]) if np.sum(crash_mask) > 0 else 1.0
            
            # Доверие к сигналу (R2)
            r2 = np.corrcoef(t_slice, b_slice)[0, 1]**2
            
            results["analysis_data"].append({
                "symbol": sym,
                "price": round(t_prices[-1], 4),
                "pain_index": round(float(pain), 2),
                "trust_factor": round(float(r2), 2)
            })
        except Exception as e:
            print(f"Ошибка по {sym}: {e}")
            continue

    # 3. Отправка в Gist
    payload = {'files': {'coeffs.json': {'content': json.dumps(results, indent=2)}}}
    response = requests.patch(f'https://api.github.com/gists/{GIST_ID}', 
                              headers={'Authorization': f'token {TOKEN}'}, json=payload)
    
    if response.status_code == 200:
        print("Данные успешно обновлены!")
    else:
        print(f"Ошибка при обновлении: {response.status_code}")

if __name__ == '__main__':
    update_gist()
