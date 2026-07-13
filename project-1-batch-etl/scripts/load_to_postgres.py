import pandas as pd
import psycopg2
import io

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="taxidb",
    user="postgres",
    password="taxi123",
)

print("Reading cleaned data...")
df = pd.read_parquet("data/yellow_tripdata_2024-01_clean.parquet")
print(f"Rows to load: {len(df):,}")

print("Loading into PostgreSQL...")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS taxi_trips;")

# Build CREATE TABLE from dataframe columns
col_types = []
for col, dtype in df.dtypes.items():
    if "int" in str(dtype):
        pg_type = "BIGINT"
    elif "float" in str(dtype):
        pg_type = "DOUBLE PRECISION"
    elif "datetime" in str(dtype):
        pg_type = "TIMESTAMP"
    else:
        pg_type = "TEXT"
    col_types.append(f'"{col}" {pg_type}')
cur.execute(f'CREATE TABLE taxi_trips ({", ".join(col_types)});')
conn.commit()

# Load in CHUNKS to stay within memory
CHUNK = 200000
total = len(df)
for start in range(0, total, CHUNK):
    chunk = df.iloc[start:start + CHUNK]
    buffer = io.StringIO()
    chunk.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    cur.copy_expert('COPY taxi_trips FROM STDIN WITH (FORMAT csv)', buffer)
    conn.commit()
    buffer.close()
    print(f"  loaded {min(start + CHUNK, total):,} / {total:,} rows")

print("Load complete.")

# Verify
print("\n--- Verification queries ---")
cur.execute("SELECT COUNT(*) FROM taxi_trips;")
print(f"Total rows in table: {cur.fetchone()[0]:,}")

cur.execute("SELECT AVG(fare_amount) FROM taxi_trips;")
print(f"Average fare: ${cur.fetchone()[0]:.2f}")

print("\nTrips by day of week:")
cur.execute("""
    SELECT pickup_day_of_week, COUNT(*) AS trips
    FROM taxi_trips
    GROUP BY pickup_day_of_week
    ORDER BY trips DESC;
""")
for row in cur.fetchall():
    print(f"  {row[0]:<10} {row[1]:>10,}")

cur.close()
conn.close()