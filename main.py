import json, requests, numpy as np, os
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = '3f50574a29bc37434c18cc8480779ccb'
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN') # Убедись, что переменная GIST_TOKEN или GITHUB_TOKEN совпадает в твоем секрете

coins = {
    'SUI': 'sui', 'ONDO': 'ondo-finance', 'LINK': 'chainlink', 'RENDER': 'render-token',
    'NEAR': 'near', 'YFI': 'yearn-finance', 'AAVE': 'aave', 'AVAX': 'avalanche-2',
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TAO': 'bittensor', 'TON': 'the-open-network',
    'XRP': 'ripple', 'ADA': 'cardano'
}

def calculate_beta(t_ret, b_ret):
    """Считает бету по всему массиву данных за 30 дней"""
    up_mask = b_ret > 0
    down_mask = b_ret <= 0
    
    beta_up = np.cov(t_ret[up_mask], b_ret[up_mask])[0,1] / np.var(b_ret[up_mask]) if np.sum(up_mask) > 1 else 1.0
    beta_down = np.cov(t_ret[down_mask], b_ret[down_mask])[0,1] / np.var(b_ret[down_mask]) if np.sum(down_mask) > 1 else 1.0
    
    return {"up": round(float(beta_up), 2), "down": round(float(beta_down), 2)}

def update_gist():
    # 1. Получаем Биткоин
    btc_data = cg.get_coin_market_chart_by_id('bitcoin', 'usd', 30)
    btc_prices = np.array([x[1] for x in btc_data['prices']])
    b_ret = np.diff(btc_prices) / btc_prices[:-1]
    
    results = {}
    debug_stats = {"total_days_requested": 30, "coins_data": {}}
    
    # 2. Проходим по всем монетам
    for sym, coin_id in coins.items():
        try:
            data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
            token_prices = np.array([x[1] for x in data['prices']])
            t_ret = np.diff(token_prices) / token_prices[:-1]
            
            # Записываем количество точек для проверки качества данных
            debug_stats["coins_data"][sym] = len(data['prices'])
            
            # 3. Математика: используем все имеющиеся точки
            min_len = min(len(t_ret), len(b_ret))
            results[sym] = calculate_beta(t_ret[-min_len:], b_ret[-min_len:])
        except:
            results[sym] = {"up": 1.0, "down": 1.0}

    # 4. Отправка в Gist
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    payload = {'files': {
        'coeffs.json': {'content': json.dumps(results)},
        'debug.json': {'content': json.dumps(debug_stats)}
    }}
    requests.patch(f'https://api.github.com/gists/{GIST_ID}', headers=headers, json=payload)

if __name__ == '__main__':
    update_gist()
