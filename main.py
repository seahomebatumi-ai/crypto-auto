import os, json, time, requests
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
# Ваш GIST_ID остается прежним
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

TOKENS = {
    'SUI': 'sui', 'ONDO': 'ondo', 'LINK': 'chainlink', 'RENDER': 'render', 
    'NEAR': 'near', 'YFI': 'yearn-finance', 'AAVE': 'aave', 'AVAX': 'avalanche-2', 
    'FET': 'fetch-ai', 'ENA': 'ethena', 'TAO': 'bittensor', 'TON': 'the-open-network', 
    'XRP': 'ripple', 'ADA': 'cardano'
}

def get_downside_beta(coin_id):
    time.sleep(1.5) # Задержка для API, чтобы не ловить ошибки
    try:
        # Получаем исторические данные в USD (надежный источник)
        c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
        b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)
        
        c_prices = np.array([p[1] for p in c_data['prices']])
        b_prices = np.array([p[1] for p in b_data['prices']])
        
        # Считаем процентные изменения (доходность)
        c_ret = np.diff(c_prices) / c_prices[:-1]
        b_ret = np.diff(b_prices) / b_prices[:-1]
        
        # Выделяем только моменты падения Биткоина (фильтр "просадки")
        mask = b_ret < 0
        if sum(mask) < 5: return 1.5 # Если данных мало, берем среднее значение
        
        # Коэффициент Бета: отношение средней просадки альта к просадке BTC
        beta = np.mean(c_ret[mask]) / np.mean(b_ret[mask])
        return float(beta)
    except:
        return 1.5

def main():
    analysis_data = []
    for s, i in TOKENS.items():
        beta_val = get_downside_beta(i)
        analysis_data.append({"symbol": s, "beta": beta_val, "status": "OK"})
    
    # Отправляем обновленные коэффициенты в ваш Gist
    payload = {"files": {"coeffs.json": {"content": json.dumps({"analysis_data": analysis_data})}}}
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=payload)

if __name__ == "__main__":
    main()
