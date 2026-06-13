import json, requests, numpy as np, os
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = '3f50574a29bc37434c18cc8480779ccb'
TOKEN = os.environ.get('GIST_TOKEN') or os.environ.get('GITHUB_TOKEN')

coins = {
    'SUI': 'sui', 'ONDO': 'ondo-finance', 'LINK': 'chainlink', 'RENDER': 'render-token', 
    'NEAR': 'near', 'YFI': 'yearn-finance', 'AAVE': 'aave', 'AVAX': 'avalanche-2', 
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TAO': 'bittensor', 'TON': 'the-open-network', 
    'XRP': 'ripple', 'ADA': 'cardano'
}

def update_gist():
    # Получаем данные
    btc_data = cg.get_coin_market_chart_by_id('bitcoin', 'usd', 30)
    b_prices = np.array([x[1] for x in btc_data['prices']])
    b_ret = np.diff(b_prices) / b_prices[:-1]
    
    results = {"analysis_data": []}
    
    for sym, coin_id in coins.items():
        try:
            data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
            t_prices = np.array([x[1] for x in data['prices']])
            t_ret = np.diff(t_prices) / t_prices[:-1]
            
            # Синхронизация
            min_len = min(len(t_ret), len(b_ret))
            b_s, t_s = b_ret[-min_len:], t_ret[-min_len:]
            
            # Разделение на фазы: рост BTC и падение BTC
            up_m, down_m = b_s > 0, b_s <= 0
            
            # Четкий расчет беты: ковариация / дисперсия BTC
            # Это дает коэффициент, показывающий, на сколько % меняется альт при изменении BTC на 1%
            beta_up = np.cov(t_s[up_m], b_s[up_m])[0,1] / np.var(b_s[up_m]) if np.sum(up_m) > 1 else 1.0
            beta_down = np.cov(t_s[down_m], b_s[down_m])[0,1] / np.var(b_s[down_m]) if np.sum(down_m) > 1 else 1.0
            
            results["analysis_data"].append({
                "symbol": sym, 
                "up": round(float(beta_up), 2), 
                "down": round(float(beta_down), 2)
            })
        except: continue

    # Отправка в Gist
    payload = {'files': {'coeffs.json': {'content': json.dumps(results, indent=2)}}}
    requests.patch(f'https://api.github.com/gists/{GIST_ID}', headers={'Authorization': f'token {TOKEN}'}, json=payload)
    print("Данные успешно рассчитаны и отправлены в Gist")

if __name__ == '__main__':
    update_gist()
