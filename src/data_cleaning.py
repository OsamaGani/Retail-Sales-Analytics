
import pandas as pd
import numpy as np

# Load raw dataset
df = pd.read_csv("data/sales.csv", encoding="latin1")

print("========== DATA CLEANING STARTED ==========")

# 1. Clean column names
df.columns = df.columns.str.strip()

# 2. Remove unnecessary spaces from text columns
text_columns = df.select_dtypes(include=["object", "str"]).columns

for column in text_columns:
    df[column] = df[column].str.strip()

# 3. Convert date columns into datetime format
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%m/%d/%Y",
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%m/%d/%Y",
    errors="coerce"
)

# 4. Convert numeric columns
numeric_columns = ["Sales", "Quantity", "Discount", "Profit"]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# 5. Check missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# 6. Check duplicate records
print("\n========== DUPLICATE RECORDS ==========")
print("Duplicates:", df.duplicated().sum())

# 7. Check invalid dates
print("\n========== INVALID DATES ==========")
print("Invalid Order Dates:", df["Order Date"].isnull().sum())
print("Invalid Ship Dates:", df["Ship Date"].isnull().sum())

# 8. Check invalid business values
print("\n========== BUSINESS VALIDATION ==========")

print("Negative Sales:", (df["Sales"] < 0).sum())
print("Invalid Quantity:", (df["Quantity"] <= 0).sum())
print(
    "Invalid Discount:",
    ((df["Discount"] < 0) | (df["Discount"] > 1)).sum()
)

# 9. Remove exact duplicate records
df = df.drop_duplicates()

# 10. Save cleaned dataset
df.to_csv("data/cleaned_sales.csv", index=False)

print("\n========== CLEANING COMPLETED ==========")
print("Final Rows:", len(df))
print("Final Columns:", len(df.columns))
print("Cleaned dataset saved successfully!")
