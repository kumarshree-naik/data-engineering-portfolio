import pandas as pd

# --- EXTRACT ---
print("Loading raw data...")
df = pd.read_parquet("data/yellow_tripdata_2024-01.parquet")
rows_start = len(df)
print(f"Raw rows: {rows_start:,}")

# --- TRANSFORM ---

# 1. Handle missing values
# passenger_count nulls -> fill with 1 (most common), convert to int
df["passenger_count"] = df["passenger_count"].fillna(1).astype(int)
# RatecodeID nulls -> fill with 1 (standard rate)
df["RatecodeID"] = df["RatecodeID"].fillna(1).astype(int)
# store_and_fwd_flag nulls -> fill with 'N'
df["store_and_fwd_flag"] = df["store_and_fwd_flag"].fillna("N")

# 2. Remove invalid rows
df = df[df["fare_amount"] > 0]            # no zero/negative fares
df = df[df["trip_distance"] > 0]          # no zero-distance trips
df = df[df["passenger_count"] > 0]        # at least 1 passenger
df = df[df["total_amount"] > 0]           # no zero/negative totals

# 3. Keep only trips actually in January 2024 (remove stray dates)
df = df[
    (df["tpep_pickup_datetime"] >= "2024-01-01") &
    (df["tpep_pickup_datetime"] < "2024-02-01")
]

# 4. Add derived columns (feature engineering)
df["trip_duration_min"] = (
    (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"])
    .dt.total_seconds() / 60
)
df = df[df["trip_duration_min"] > 0]      # drop trips with bad durations
df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
df["pickup_day_of_week"] = df["tpep_pickup_datetime"].dt.day_name()

# --- REPORT ---
rows_end = len(df)
print(f"Clean rows: {rows_end:,}")
print(f"Removed: {rows_start - rows_end:,} rows ({(rows_start-rows_end)/rows_start*100:.1f}%)")
print("\nNew derived columns added: trip_duration_min, pickup_hour, pickup_day_of_week")
print("\nSample of cleaned data:")
print(df[["tpep_pickup_datetime", "trip_distance", "fare_amount",
          "trip_duration_min", "pickup_hour", "pickup_day_of_week"]].head())

# --- SAVE cleaned output ---
df.to_parquet("data/yellow_tripdata_2024-01_clean.parquet", index=False)
print("\nSaved cleaned data to data/yellow_tripdata_2024-01_clean.parquet")