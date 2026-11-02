
import pandas as pd
import numpy as np

# 1. Load Dataset
df = pd.read_csv("data/sales.csv", encoding="latin1")

# 2. Display first 5 records
print("\n========== FIRST 5 RECORDS ==========")
print(df.head())

# 3. Dataset dimensions
print("\n========== DATASET SHAPE ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 4. Column names
print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# 5. Dataset information
print("\n========== DATASET INFORMATION ==========")
df.info()

# 6. Statistical summary
print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe())

# 7. Missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# 8. Duplicate records
print("\n========== DUPLICATE RECORDS ==========")
print(df.duplicated().sum())
