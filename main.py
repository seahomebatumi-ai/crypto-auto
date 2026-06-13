import json, requests, numpy as np, os
from pycoingecko import CoinGeckoAPI

# Конфигурация
cg = CoinGeckoAPI()
GIST_ID = '3f50574a29bc37434c18cc8480779ccb'
TOKEN = os.environ.get('GIST_TOKEN') or os.environ.get('GITHUB_TOKEN')

coins = {
    'SUI': 'sui', 'ONDO': 'ondo-finance', 'LINK': 'chainlink', 'RENDER': 'render-token', 
    'NEAR': 'near', 'YFI': 'yearn-finance', 'AAVE': 'aave', 'AVAX': 'avalanche-2', 
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TAO': 'bittensor', 'TON': 'the-open-network', 
    'XRP': 'ripple', 'ADA': 'cardano'
}

def get_stats(t_ret, b_ret):
    # Разделяем на фазы роста и падения Биткоина
    up_mask = b_ret > 0
    down_mask = b_ret <= 0
    
    # Расчет Беты (насколько агрессивно монета реагирует)
    beta_up = np.cov(t_ret[up_mask], b_ret[up_mask])[0,1] / np.var(b_ret[up_mask]) if np.sum(up_mask) > 1 else 1.0
    beta_down = np.cov(t_ret[down_mask], b_ret[down_mask])[0,1] / np.var(b_ret[down_mask]) if np.sum(down_mask) > 1 else 1.0
    
    # Расчет R-squared (коэффициент доверия)
    correlation_matrix = np.corrcoef(t_ret, b_ret)
    r_squared = correlation_matrix[0, 1]**2
    
    return {
        "beta": {"up": round(float(beta_up), 2), "down": round(float(beta_down), 2)},
        "R2": round(float(r_squared), 2)
    }

def update_gist():
    # Получаем данные Биткоина
    btc_data = cg.get_coin_market_chart_by_id('bitcoin', 'usd', 30)
    b_prices = np.array([x[1] for x in btc_data['prices']])
    b_ret = np.diff(b_prices) / b_prices[:-1]
    
    results = {"analysis_data": []}
    
    # Анализируем альткоины
    for i, (sym, coin_id) in enumerate(coins.items(), 1):
        try:
            data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
            t_prices = np.array([x[1] for x in data['prices']])
            t_ret = np.diff(t_prices) / t_prices[:-1]
            
            min_len = min(len(t_ret), len(b_ret))
            stats = get_stats(t_ret[-min_len:], b_ret[-min_len:])
            
            results["analysis_data"].append({
                "id": i, 
                "symbol": sym, 
                "vs_BTC": stats["beta"], 
                "trust_factor": stats["R2"] 
            })
        except Exception as e:
            print(f"Ошибка по {sym}: {e}")

    # Отправка в Gist
    payload = {'files': {'coeffs.json': {'content': json.dumps(results, indent=2)}}}
    response = requests.patch(f'https://api.github.com/gists/{GIST_ID}', 
                              headers={'Authorization': f'token {TOKEN}'}, json=payload)
    
    if response.status_code == 200:
        print("Успешно: данные обновлены!")
    else:
        print(f"Ошибка API: {response.status_code}")

if __name__ == '__main__':
    update_gist()
