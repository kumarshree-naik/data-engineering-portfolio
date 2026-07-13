import pandas as pd
from sqlalchemy import create_engine, text

# --- Connection to the PostgreSQL container ---
# Format: postgresql://user:password@host:port/database
engine = create_engine("postgresql://postgres:taxi123@localhost:5432/taxidb")

# --- Load the cleaned data ---
print("Reading cleaned data...")
df = pd.read_parquet("data/yellow_tripdata_2024-01_clean.parquet")
print(f"Rows to load: {len(df):,}")

# --- Write to PostgreSQL ---
print("Loading into PostgreSQL (this may take a minute)...")
df.to_sql(
    "taxi_trips",
    engine,
    if_exists="replace",
    index=False,
    chunksize=10000,     # smaller batches = lower memory use
)
print("Load complete.")

# --- Verify with SQL queries ---
print("\n--- Verification queries ---")
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM taxi_trips")).scalar()
    print(f"Total rows in table: {count:,}")

    avg_fare = conn.execute(text("SELECT AVG(fare_amount) FROM taxi_trips")).scalar()
    print(f"Average fare: ${avg_fare:.2f}")

    print("\nTrips by day of week:")
    result = conn.execute(text("""
        SELECT pickup_day_of_week, COUNT(*) AS trips
        FROM taxi_trips
        GROUP BY pickup_day_of_week
        ORDER BY trips DESC
    """))
    for row in result:
        print(f"  {row[0]:<10} {row[1]:>10,}")