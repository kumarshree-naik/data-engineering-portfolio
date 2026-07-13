# Data Engineering Portfolio — Complete Guide (Days 1–4)
### Project 1: Batch ETL Pipeline (NYC Taxi Data)

**Author:** Kumarshree Naik
**Stack:** Python · Pandas · PostgreSQL · Docker · Apache Airflow · Git/GitHub
**Environment:** GitHub Codespaces (cloud, browser-based — laptop only runs a browser)
**Cost:** ₹0

---

## How the pieces fit together

Before the steps, here's the big picture of Project 1:

```
GitHub Codespaces (a cloud computer in your browser)
   │
   ├── Docker ──► runs PostgreSQL (the database)
   │
   └── The ETL flow:
        1. NYC taxi data (raw Parquet file)   ← the SOURCE
                    │  Python + Pandas reads & cleans it
                    ▼
        2. Cleaned data (Parquet file)
                    │  Python loads it in batches
                    ▼
        3. PostgreSQL table "taxi_trips"       ← the DESTINATION
                    │
        4. Apache Airflow  ← wraps steps 1–3 to run automatically (Day 5)

   Your CODE is pushed to GitHub. Your DATA stays out of Git (.gitignore).
```

**ETL = Extract, Transform, Load:**
- **Extract** — read the raw taxi data
- **Transform** — clean it and add useful columns
- **Load** — write it into PostgreSQL
- **Orchestrate** — Airflow runs all three on a schedule (Day 5)

---

## DAY 1 — Environment Setup

**Goal:** Set up all free accounts and tools. The foundation everything sits on.

### What you set up
1. **GitHub account + portfolio repository** (`data-engineering-portfolio`, public)
2. **BigQuery Sandbox** — free cloud warehouse (no credit card), for Projects 2 & 4
3. **Google Colab** — free cloud compute for PySpark (Project 2)
4. **Kaggle** — free datasets + backup compute
5. **GitHub Codespaces** — cloud dev environment where all the building happens

### The starter README
Your repo's main README listed the four planned projects and the tech stack.

### Key concepts learned
- **Codespaces** = renting a full computer in the browser; your 8GB laptop only displays it.
- **Sandbox vs paid** = BigQuery Sandbox needs no card; if it ever asks for billing, that's the wrong path.
- **Habit:** always STOP your Codespace when done (github.com/codespaces → ... → Stop) to protect free hours.

**Outcome:** All tools verified and working. One commit pushed (the README).

---

## DAY 2 — Extract (Ingestion & Exploration)

**Goal:** Download real data, load it, and understand what's in it.

### Step 1 — Project structure
```bash
mkdir -p project-1-batch-etl/data project-1-batch-etl/scripts
cd project-1-batch-etl
```
Creates a clean layout: `data/` for files, `scripts/` for code.

### Step 2 — Protect data from Git
```bash
echo "*.parquet" > .gitignore
```
This tells Git to NEVER commit `.parquet` files. **Best practice: code goes in Git, data does not.**

### Step 3 — Download the data
```bash
cd data
curl -O https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet
cd ..
```
Downloads one month of NYC Yellow Taxi trips (~48MB Parquet).

### Step 4 — Install libraries
```bash
pip install pandas pyarrow
```
- `pandas` — data manipulation
- `pyarrow` — reads Parquet files

### Step 5 — The exploration script
**File:** `scripts/explore_data.py`
```python
import pandas as pd

# Load one month of NYC Yellow Taxi data
df = pd.read_parquet("data/yellow_tripdata_2024-01.parquet")

# Basic inspection
print("Shape (rows, columns):", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nMissing values per column:")
print(df.isnull().sum())
```
Run it:
```bash
python3 scripts/explore_data.py
```

### Results
- **2,964,624 rows × 19 columns**
- Datetime columns already correctly typed
- **140,162 nulls** each in `passenger_count`, `RatecodeID`, `store_and_fwd_flag` (~4.7%)
- Hidden invalid rows suspected (zero fares, zero-distance) — to be cleaned Day 3

### What the columns mean
- `tpep_pickup_datetime` / `tpep_dropoff_datetime` — trip start/end times
- `trip_distance` — miles; `passenger_count` — riders
- `PULocationID` / `DOLocationID` — pickup/dropoff zones
- `payment_type` — 1=card, 2=cash, etc.
- `fare_amount`, `tip_amount`, `total_amount` — money columns

### Commit
```bash
cd ..
git add .
git commit -m "Day 2: Project 1 - data ingestion and exploration script"
git push
```

**Concept:** "Know your data before you touch it." Always profile size, types, and nulls first.

---

## DAY 3 — Transform (Cleaning & Feature Engineering)

**Goal:** Turn messy raw data into clean, analysis-ready data. The heart of ETL.

### The transformation script
**File:** `scripts/transform_data.py`
```python
import pandas as pd

# --- EXTRACT ---
print("Loading raw data...")
df = pd.read_parquet("data/yellow_tripdata_2024-01.parquet")
rows_start = len(df)
print(f"Raw rows: {rows_start:,}")

# --- TRANSFORM ---

# 1. Handle missing values
df["passenger_count"] = df["passenger_count"].fillna(1).astype(int)
df["RatecodeID"] = df["RatecodeID"].fillna(1).astype(int)
df["store_and_fwd_flag"] = df["store_and_fwd_flag"].fillna("N")

# 2. Remove invalid rows
df = df[df["fare_amount"] > 0]
df = df[df["trip_distance"] > 0]
df = df[df["passenger_count"] > 0]
df = df[df["total_amount"] > 0]

# 3. Keep only trips actually in January 2024
df = df[
    (df["tpep_pickup_datetime"] >= "2024-01-01") &
    (df["tpep_pickup_datetime"] < "2024-02-01")
]

# 4. Add derived columns (feature engineering)
df["trip_duration_min"] = (
    (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"])
    .dt.total_seconds() / 60
)
df = df[df["trip_duration_min"] > 0]
df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
df["pickup_day_of_week"] = df["tpep_pickup_datetime"].dt.day_name()

# --- REPORT ---
rows_end = len(df)
print(f"Clean rows: {rows_end:,}")
print(f"Removed: {rows_start - rows_end:,} rows ({(rows_start-rows_end)/rows_start*100:.1f}%)")
print("\nSample of cleaned data:")
print(df[["tpep_pickup_datetime", "trip_distance", "fare_amount",
          "trip_duration_min", "pickup_hour", "pickup_day_of_week"]].head())

# --- SAVE ---
df.to_parquet("data/yellow_tripdata_2024-01_clean.parquet", index=False)
print("\nSaved cleaned data to data/yellow_tripdata_2024-01_clean.parquet")
```
Run it:
```bash
python3 scripts/transform_data.py
```

### What each part does
1. **Fill nulls** — the 140k missing values get sensible defaults instead of being deleted (filling often beats dropping)
2. **Remove invalid rows** — drops the bad data hiding in the file (zero/negative fares, zero-distance trips)
3. **Date filter** — keeps only actual January trips (files sometimes contain stray dates)
4. **Derived columns (feature engineering)** — creates new useful columns:
   - `trip_duration_min` — calculated from the two timestamps
   - `pickup_hour` — hour of day
   - `pickup_day_of_week` — Monday, Tuesday, etc.
5. **Save separately** — writes a NEW clean file; never overwrite the source

### Results
- **2,964,624 → 2,838,928 rows (125,696 removed, 4.2%)**
- Verified: Jan 1, 2024 = Monday; durations calculated correctly
- Clean Parquet saved

### Commit
```bash
cd ..
git add .
git commit -m "Day 3: Project 1 - transformation logic (clean nulls, remove invalid rows, add derived columns)"
git push
```

**Concept:** Cleaning meaningfully (4.2%) without over-deleting. Feature engineering adds value beyond the raw source.

---

## DAY 4 — Load (into PostgreSQL)

**Goal:** Load the clean data into a real database. The "L" in ETL. Docker enters here.

### Step 1 — Start PostgreSQL in Docker
```bash
docker run --name taxi-postgres -e POSTGRES_PASSWORD=taxi123 \
  -e POSTGRES_DB=taxidb -p 5432:5432 -d postgres:16
```
Each part:
- `--name taxi-postgres` — names the container
- `POSTGRES_PASSWORD=taxi123` — sets DB password
- `POSTGRES_DB=taxidb` — creates a database named `taxidb`
- `-p 5432:5432` — opens the database port
- `-d postgres:16` — runs PostgreSQL 16 in the background

Confirm it's running:
```bash
docker ps
```
Look for `taxi-postgres` with status "Up".

### Step 2 — Install DB libraries
```bash
pip install sqlalchemy psycopg2-binary
```
- `sqlalchemy` — lets Python talk to databases
- `psycopg2-binary` — the PostgreSQL driver

### Step 3 — The load script
**File:** `scripts/load_to_postgres.py`
```python
import pandas as pd
from sqlalchemy import create_engine, text

# Connection: postgresql://user:password@host:port/database
engine = create_engine("postgresql://postgres:taxi123@localhost:5432/taxidb")

print("Reading cleaned data...")
df = pd.read_parquet("data/yellow_tripdata_2024-01_clean.parquet")
print(f"Rows to load: {len(df):,}")

print("Loading into PostgreSQL...")
df.to_sql(
    "taxi_trips",
    engine,
    if_exists="replace",
    index=False,
    chunksize=10000,     # batch loading — memory-safe
)
print("Load complete.")

# Verify with SQL
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
```
Run it:
```bash
python3 scripts/load_to_postgres.py
```

### The memory problem (and the fix)
The first attempt used `chunksize=50000` and `method="multi"` and printed **"Terminated"** — the process ran out of memory on the free tier.

**Fix:** lower `chunksize` to 10000 and remove `method="multi"`. This loads in smaller batches, keeping memory low.

**Why batching works:** instead of pushing all 2.84M rows at once (memory spike → crash), send 10,000 at a time. Only 10k rows are held in memory at any moment. Same result, no crash. This is a REAL data engineering technique — production pipelines always batch because datasets are too big to fit in memory.

### Results
- **Total rows in table: 2,838,928** (matches clean data exactly)
- **Average fare: $18.52**
- **Busiest day: Wednesday (475,839); quietest: Sunday (323,085)**

### Step 4 — Query the database directly
```bash
docker exec -it taxi-postgres psql -U postgres -d taxidb
```
This opens a live SQL prompt (`taxidb=#`). Example queries:
```sql
-- Busiest pickup hours
SELECT pickup_hour, COUNT(*) AS trips
FROM taxi_trips
GROUP BY pickup_hour
ORDER BY trips DESC
LIMIT 5;

-- Average fare by passenger count
SELECT passenger_count, ROUND(AVG(fare_amount),2) AS avg_fare
FROM taxi_trips
GROUP BY passenger_count
ORDER BY passenger_count;
```
Exit with:
```
\q
```
Useful psql commands: `\dt` (list tables), `\d taxi_trips` (table structure), `\q` (quit).

### Key finding
**Peak demand is 3–7 PM** (evening rush): hour 18 had 204,162 trips, the busiest.

### Commit
```bash
cd ..
git add .
git commit -m "Day 4: Project 1 - load clean data into PostgreSQL with verification queries"
git push
```

### Important concept — where data lives
- **Raw + clean Parquet files** → on the Codespace disk (not in Git)
- **`taxi_trips` table** → inside the PostgreSQL container (local, private, NOT online)
- The table is **temporary** — if the container is removed, the table is gone, BUT it can always be rebuilt by re-running the load script. The pipeline is what's valuable, not the copy of data.
- Contrast: **BigQuery** (Projects 2 & 4) IS an online cloud database that persists.

---

## Where you stand after Day 4

| Stage | Status | Script |
|-------|--------|--------|
| Extract | Done | `explore_data.py` |
| Transform | Done | `transform_data.py` |
| Load | Done | `load_to_postgres.py` |
| Orchestrate | Day 5 | Airflow DAG |

The full **E-T-L core is complete and working** — genuinely the hardest part of Project 1.

---

## Key concepts you now understand

- **ETL** — Extract, Transform, Load; the fundamental data pipeline pattern
- **Parquet** — compressed columnar file format used across the industry
- **Data profiling** — checking size, types, nulls before processing
- **Feature engineering** — deriving new useful columns from existing data
- **Docker containers** — running software (PostgreSQL) in isolated, disposable boxes
- **Batch/chunked loading** — processing large data in small pieces to bound memory
- **SQL verification** — using queries to confirm and explore loaded data
- **Git discipline** — code in Git, data excluded via `.gitignore`; daily commits

---

## Interview talking points from Project 1

1. "I built an end-to-end batch ETL pipeline processing ~3M NYC taxi trips."
2. "I cleaned 4.2% invalid/null data and engineered features like trip duration and pickup hour."
3. "I hit a memory constraint loading 2.84M rows and solved it with chunked batch inserts — a technique that scales to any dataset size."
4. "I verified the load with SQL and found demand peaks during evening rush hour (3–7 PM)."
5. "Code is version-controlled on GitHub with data excluded via .gitignore."

---

## Commands quick-reference

```bash
# Reopen work
cd project-1-batch-etl

# Start database
docker run --name taxi-postgres -e POSTGRES_PASSWORD=taxi123 \
  -e POSTGRES_DB=taxidb -p 5432:5432 -d postgres:16
docker ps                          # check it's running

# Run the pipeline
python3 scripts/explore_data.py
python3 scripts/transform_data.py
python3 scripts/load_to_postgres.py

# Query the database
docker exec -it taxi-postgres psql -U postgres -d taxidb
#   ...SQL queries..., then \q to exit

# Save to GitHub
git add .
git commit -m "message"
git push

# When done: stop the Codespace at github.com/codespaces
```

---

*Next: Day 5 — Apache Airflow to orchestrate the pipeline into an automated, scheduled workflow.*