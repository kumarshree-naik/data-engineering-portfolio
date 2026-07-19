import requests

# CoinGecko free endpoint — current prices for a few coins
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin,ethereum,cardano,solana,dogecoin",
    "vs_currencies": "usd",
    "include_market_cap": "true",
    "include_24hr_change": "true",
}

response = requests.get(url, params=params)
print("Status code:", response.status_code)
print("\nResponse:")
import json
print(json.dumps(response.json(), indent=2))