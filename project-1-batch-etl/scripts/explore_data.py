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