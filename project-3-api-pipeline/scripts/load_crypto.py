import requests
import psycopg2
from datetime import datetime, timezone

# --- 1. FETCH ---
def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,cardano,solana,dogecoin",
        "vs_currencies": "usd",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

data = fetch_crypto_prices()
timestamp = datetime.now(timezone.utc)
print(f"Fetched at {timestamp}")

# --- 2. DATA QUALITY CHECKS ---
expected_coins = ["bitcoin", "ethereum", "cardano", "solana", "dogecoin"]
errors = []
for coin in expected_coins:
    price = data.get(coin, {}).get("usd")
    if price is None:
        errors.append(f"Missing price for {coin}")
    elif price <= 0:
        errors.append(f"Non-positive price for {coin}")
if errors:
    print("❌ Data quality checks FAILED:")
    for e in errors:
        print("  -", e)
    raise SystemExit("Aborting.")
print("✅ Data quality checks passed.")

# --- 3. CONNECT ---
conn = psycopg2.connect(
    host="localhost", port=5433, dbname="cryptodb",
    user="postgres", password="crypto123",
)
cur = conn.cursor()

# --- 4. CREATE WIDE TABLE (one column per coin) ---
cur.execute("""
    CREATE TABLE IF NOT EXISTS crypto_prices_wide (
        fetched_at  TIMESTAMP PRIMARY KEY,
        bitcoin     DOUBLE PRECISION,
        ethereum    DOUBLE PRECISION,
        cardano     DOUBLE PRECISION,
        solana      DOUBLE PRECISION,
        dogecoin    DOUBLE PRECISION
    );
""")
conn.commit()

# --- 5. INSERT ONE ROW (timestamp + all coin prices) ---
cur.execute("""
    INSERT INTO crypto_prices_wide (fetched_at, bitcoin, ethereum, cardano, solana, dogecoin)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (fetched_at) DO NOTHING;
""", (
    timestamp,
    data["bitcoin"]["usd"],
    data["ethereum"]["usd"],
    data["cardano"]["usd"],
    data["solana"]["usd"],
    data["dogecoin"]["usd"],
))
conn.commit()
print("Inserted 1 row.")

# --- 6. SHOW LATEST DATA ---
cur.execute("SELECT * FROM crypto_prices_wide ORDER BY fetched_at DESC LIMIT 5;")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()