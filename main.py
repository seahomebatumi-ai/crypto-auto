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
    btc_data = cg.get_coin_market_chart_by_id('bitcoin', 'usd', 30)
    b_prices = np.array([x[1] for x in btc_data['prices']])
    b_ret = np.diff(b_prices) / b_prices[:-1]
    
    results = {"current_btc_price": round(b_prices[-1], 2), "analysis_data": []}
    
    for sym, coin_id in coins.items():
        try:
            data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
            t_prices = np.array([x[1] for x in data['prices']])
            t_ret = np.diff(t_prices) / t_prices[:-1]
            
            min_len = min(len(t_ret), len(b_ret))
            b_s, t_s = b_ret[-min_len:], t_ret[-min_len:]
            
            up_m, down_m = b_s > 0, b_s <= 0
            beta_up = np.cov(t_s[up_m], b_s[up_m])[0,1] / np.var(b_s[up_m]) if np.sum(up_m) > 1 else 1.0
            beta_down = np.cov(t_s[down_m], b_s[down_m])[0,1] / np.var(b_s[down_m]) if np.sum(down_m) > 1 else 1.0
            r2 = np.corrcoef(t_s, b_s)[0, 1]**2
            
            results["analysis_data"].append({
                "symbol": sym, "price": round(t_prices[-1], 4), 
                "up": round(float(beta_up), 2), "down": round(float(beta_down), 2), 
                "r2": round(float(r2), 2), "status": "OK"
            })
        except Exception as e:
            # Если ошибка, добавляем запись с пометкой ERROR
            results["analysis_data"].append({"symbol": sym, "status": f"ERROR: {str(e)}"})

    payload = {'files': {'coeffs.json': {'content': json.dumps(results, indent=2)}}}
    requests.patch(f'https://api.github.com/gists/{GIST_ID}', headers={'Authorization': f'token {TOKEN}'}, json=payload)
    print(f"Обработка завершена. Всего элементов: {len(results['analysis_data'])}")

if __name__ == '__main__':
    update_gist()
