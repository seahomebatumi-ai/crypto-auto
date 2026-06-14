import os, json, time, requests
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
GIST_ID = "3f50574a29bc37434c18cc8480779ccb"
GIST_TOKEN = os.environ.get('GIST_TOKEN')

# Ваш список монет
TOKENS = {'SUI': 'sui', 'ONDO': 'ondo', 'LINK': 'chainlink', 'RENDER': 'render', 'NEAR': 'near', 'YFI': 'yearn-finance', 'AAVE': 'aave', 'AVAX': 'avalanche-2', 'FET': 'fetch-ai', 'ENA': 'ethena', 'TAO': 'bittensor', 'TON': 'the-open-network', 'XRP': 'ripple', 'ADA': 'ada'}

def get_asymmetric_beta(coin_id):
    # Увеличенная пауза для избежания бана от CoinGecko (2.5 сек)
    time.sleep(2.5) 
    
    # Запрос данных строго за 14 дней
    c_data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=14)
    b_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=14)
    
    # Проверка целостности данных
    if not c_data.get('prices') or not b_data.get('prices'):
        raise Exception(f"Пустые данные для {coin_id}")

    # Расчет доходности
    c_ret = np.diff([p[1] for p in c_data['prices']]) / [p[1] for p in c_data['prices']][:-1]
    b_ret = np.diff([p[1] for p in b_data['prices']]) / [p[1] for p in b_data['prices']][:-1]
    
    # Расчет Бета роста (b_ret > 0)
    up_mask = b_ret > 0
    if sum(up_mask) < 5: raise Exception(f"Недостаточно данных роста для {coin_id}")
    up_beta = np.mean(c_ret[up_mask]) / np.mean(b_ret[up_mask])
    
    # Расчет Бета падения (b_ret < 0)
    down_mask = b_ret < 0
    if sum(down_mask) < 5: raise Exception(f"Недостаточно данных падения для {coin_id}")
    down_beta = np.mean(c_ret[down_mask]) / np.mean(b_ret[down_mask])
    
    return {"up_beta": float(up_beta), "down_beta": float(down_beta)}

def main():
    results = []
    for s, i in TOKENS.items():
        try:
            # Пытаемся получить реальные данные
            results.append({"symbol": s, **get_asymmetric_beta(i)})
        except Exception as e:
            # Если возникла ошибка - прерываем процесс, чтобы не "портить" Gist
            print(f"ОШИБКА: Расчет для {s} невозможен: {e}")
            return
    
    # Обновляем Gist только если все 14 монет прошли проверку
    requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers={"Authorization": f"token {GIST_TOKEN}"}, 
                   json={"files": {"coeffs.json": {"content": json.dumps({"analysis_data": results})}}})
    print("Успешно: Данные обновлены и подтверждены.")

if __name__ == "__main__":
    main()
