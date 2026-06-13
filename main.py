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

def get_full_analysis(t_ret, b_ret):
    # Бета
    up_mask = b_ret > 0
    down_mask = b_ret <= 0
    beta_up = np.cov(t_ret[up_mask], b_ret[up_mask])[0,1] / np.var(b_ret[up_mask]) if np.sum(up_mask) > 1 else 1.0
    beta_down = np.cov(t_ret[down_mask], b_ret[down_mask])[0,1] / np.var(b_ret[down_mask]) if np.sum(down_mask) > 1 else 1.0
    
    # R2
    r2 = np.corrcoef(t_ret, b_ret)[0, 1]**2
    
    # Волатильность к USDT (стандартное отклонение доходности)
    vol_usdt = np.std(t_ret)
    
    return {
        "vs_BTC": {"up": round(float(beta_up), 2), "down": round(float(beta_down), 2)},
        "vs_USDT_vol": round(float(vol_usdt), 4),
        "trust_factor": round(float(r2), 2)
    }

def update_gist():
    btc_data = cg.get_coin_market_chart_by_id('bitcoin', 'usd', 30)
    b_ret = np.diff(np.array([x[1] for x in btc_data['prices']])) / np.array([x[1] for x in btc_data['prices']])[:-1]
    
    results = {"analysis_data": []}
    
    for i, (sym, coin_id) in enumerate(coins.items(), 1):
        data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
        t_ret = np.diff(np.array([x[1] for x in data['prices']])) / np.array([x[1] for x in data['prices']])[:-1]
        
        min_len = min(len(t_ret), len(b_ret))
        analysis = get_full_analysis(t_ret[-min_len:], b_ret[-min_len:])
        
        results["analysis_data"].append({"id": i, "symbol": sym, **analysis})

    payload = {'files': {'coeffs.json': {'content': json.dumps(results, indent=2)}}}
    requests.patch(f'https://api.github.com/gists/{GIST_ID}', headers={'Authorization': f'token {TOKEN}'}, json=payload)

if __name__ == '__main__':
    update_gist()
