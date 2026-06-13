import json, requests, numpy as np, os
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = '3f50574a29bc37434c18cc8480779ccb'
# Пытаемся взять токен из любого из стандартных имен
TOKEN = os.environ.get('GIST_TOKEN') or os.environ.get('GITHUB_TOKEN')

coins = {
    'SUI': 'sui', 'ONDO': 'ondo-finance', 'LINK': 'chainlink', 'RENDER': 'render-token',
    'NEAR': 'near', 'YFI': 'yearn-finance', 'AAVE': 'aave', 'AVAX': 'avalanche-2',
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TAO': 'bittensor', 'TON': 'the-open-network',
    'XRP': 'ripple', 'ADA': 'cardano'
}

def calculate_beta(t_ret, b_ret):
    up_mask = b_ret > 0
    down_mask = b_ret <= 0
    beta_up = np.cov(t_ret[up_mask], b_ret[up_mask])[0,1] / np.var(b_ret[up_mask]) if np.sum(up_mask) > 1 else 1.0
    beta_down = np.cov(t_ret[down_mask], b_ret[down_mask])[0,1] / np.var(b_ret[down_mask]) if np.sum(down_mask) > 1 else 1.0
    return {"up": round(float(beta_up), 2), "down": round(float(beta_down), 2)}

def update_gist():
    if not TOKEN:
        print("ОШИБКА: Токен не найден! Проверь настройки Secrets.")
        return

    btc_data = cg.get_coin_market_chart_by_id('bitcoin', 'usd', 30)
    btc_prices = np.array([x[1] for x in btc_data['prices']])
    b_ret = np.diff(btc_prices) / btc_prices[:-1]
    
    results = {}
    debug_stats = {"total_days": 30, "coins_count": {}}
    
    for sym, coin_id in coins.items():
        try:
            data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
            token_prices = np.array([x[1] for x in data['prices']])
            t_ret = np.diff(token_prices) / token_prices[:-1]
            debug_stats["coins_count"][sym] = len(data['prices'])
            
            min_len = min(len(t_ret), len(b_ret))
            results[sym] = calculate_beta(t_ret[-min_len:], b_ret[-min_len:])
        except Exception as e:
            print(f"Ошибка по {sym}: {e}")
            results[sym] = {"up": 1.0, "down": 1.0}

    headers = {'Authorization': f'token {TOKEN}'}
    payload = {'files': {
        'coeffs.json': {'content': json.dumps(results)},
        'debug.json': {'content': json.dumps(debug_stats)}
    }}
    
    response = requests.patch(f'https://api.github.com/gists/{GIST_ID}', headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Успешно: Gist обновлен!")
    else:
        print(f"Ошибка GitHub API ({response.status_code}): {response.text}")

if __name__ == '__main__':
    update_gist()
