import requests
import pandas as pd
from datetime import datetime, timezone

def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,cardano,solana,dogecoin",
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_change": "true",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()   # raises an error if the request failed
    return response.json()

def transform(data):
    # Flatten the nested JSON into rows
    timestamp = datetime.utcnow()
    rows = []
    for coin, values in data.items():
        rows.append({
            "coin": coin,
            "price_usd": values.get("usd"),
            "market_cap_usd": values.get("usd_market_cap"),
            "change_24h_pct": values.get("usd_24h_change"),
            "fetched_at": timestamp,
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    raw = fetch_crypto_prices()
    df = transform(raw)
    print(f"Fetched {len(df)} coins at {datetime.utcnow()}")
    print(df)