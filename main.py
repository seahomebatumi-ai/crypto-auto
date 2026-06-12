import json, requests, numpy as np, os
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = '9d8c8acf467c76de582faebd77a91820'
GITHUB_TOKEN = os.environ.get('GIST_TOKEN')

coins = {
    'SUI': 'sui', 'ONDO': 'ondo-finance', 'LINK': 'chainlink', 'RENDER': 'render-token',
    'NEAR': 'near', 'YFI': 'yearn-finance', 'AAVE': 'aave', 'AVAX': 'avalanche-2',
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TAO': 'bittensor', 'TON': 'the-open-network',
    'XRP': 'ripple', 'ADA': 'cardano'
}

def calculate_beta(t_ret, b_ret):
    """Рассчитывает асимметричную бету для роста и падения"""
    up_mask = b_ret > 0
    down_mask = b_ret <= 0
    
    # Расчет бета для роста (Upside Beta)
    # Используем проверку на размер выборки, чтобы избежать деления на ноль
    beta_up = np.cov(t_ret[up_mask], b_ret[up_mask])[0,1] / np.var(b_ret[up_mask]) if np.sum(up_mask) > 1 else 1.0
    
    # Расчет бета для падения (Downside Beta)
    beta_down = np.cov(t_ret[down_mask], b_ret[down_mask])[0,1] / np.var(b_ret[down_mask]) if np.sum(down_mask) > 1 else 1.0
    
    return {"up": round(float(beta_up), 2), "down": round(float(beta_down), 2)}

def update_gist():
    # Данные BTC
    btc_data = cg.get_coin_market_chart_by_id('bitcoin', 'usd', 30)
    btc = np.array([x[1] for x in btc_data['prices']])
    b_ret = np.diff(btc) / btc[:-1]
    
    results = {}
    
    for sym, coin_id in coins.items():
        try:
            data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
            token_prices = np.array([x[1] for x in data['prices']])
            t_ret = np.diff(token_prices) / token_prices[:-1]
            
            # Выравниваем по длине
            min_len = min(len(t_ret), len(b_ret))
            results[sym] = calculate_beta(t_ret[-min_len:], b_ret[-min_len:])
        except:
            results[sym] = {"up": 1.0, "down": 1.0}

    # Отправка в Gist
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    payload = {'files': {'coeffs.json': {'content': json.dumps(results)}}}
    requests.patch(f'https://api.github.com/gists/{GIST_ID}', headers=headers, json=payload)

if __name__ == '__main__':
    update_gist()
