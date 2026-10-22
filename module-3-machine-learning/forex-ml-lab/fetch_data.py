import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

TOKEN = os.getenv('OANDA_ACCESS_TOKEN')
ACCOUNT_ID = os.getenv('OANDA_ACCOUNT_ID')
ENV = os.getenv('OANDA_ENV', 'practice')


if not TOKEN or not ACCOUNT_ID:
    raise SystemExit("Missing OANDA_ACCESS_TOKEN or OANDA_ACCOUNT_ID.")

if ENV != "practice":
    raise SystemExit("This learning project only supports OANDA practice mode.")

BASE_URL = "https://api-fxpractice.oanda.com/v3" if ENV == "practice" else "https://api-fxtrade.oanda.com/v3"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

def get(path, params=None):
    url = f"{BASE_URL}{path}"
    print(f"\nGET {url}")
    if params:
        print("Params:", params)

    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    print("Status Code:", r.status_code)

    return r.json()

def fetch_candles():
    data = get(
            "/instruments/EUR_USD/candles",
            params={
                "granularity": "H1",
                  "count": 1000,
                    "price": "M"
                    }
        )
    if data is None:
            return
    
    candles_df = pd.json_normalize(data['candles'])
    candles_df = candles_df[candles_df['complete'] ==True]
    candles_df = candles_df.drop(columns='complete')
    candles_df = candles_df.rename(columns= {
        'time': 'timestamp',
        'mid.o': 'open',
        'mid.h': 'high',
        'mid.l': 'low',
        'mid.c': 'close'
    })
    candles_df['timestamp'] = pd.to_datetime(candles_df['timestamp'])
    candles_df[["open", "high", "low", "close"]] = (candles_df[["open", "high", "low", "close"]]).astype(float)
    candles_df = candles_df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    candles_df = candles_df.sort_values('timestamp').reset_index(drop=True)
    
    return candles_df


def main():

    candles_df = fetch_candles()

    output_path = Path(__file__).parent/'data'/'eur_usd_h1.csv'

    output_path.parent.mkdir(parents=True, exist_ok=True)
    candles_df.to_csv(output_path, index= False)
    
    print(f'Saved {len(candles_df)} candles to {output_path}')

if __name__ == "__main__":
    main()