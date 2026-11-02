
import pandas as pd
import numpy as np

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales.csv")

# Convert Order Date into datetime
df["Order Date"] = pd.to_datetime(df["Order Date"])

print("\n========== MONTHLY SALES ANALYSIS ==========")

# Extract year and month
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month

# Create Year-Month column
df["Year-Month"] = df["Order Date"].dt.to_period("M")

# 1. Monthly Revenue
monthly_sales = df.groupby("Year-Month")["Sales"].sum()

print("\n========== MONTHLY REVENUE ==========")
print(monthly_sales.round(2))

# 2. Highest Sales Month
highest_month = monthly_sales.idxmax()
highest_sales = monthly_sales.max()

print("\n========== HIGHEST SALES MONTH ==========")
print("Month:", highest_month)
print("Revenue: $", round(highest_sales, 2))

# 3. Lowest Sales Month
lowest_month = monthly_sales.idxmin()
lowest_sales = monthly_sales.min()

print("\n========== LOWEST SALES MONTH ==========")
print("Month:", lowest_month)
print("Revenue: $", round(lowest_sales, 2))

# 4. Year-wise Revenue
yearly_sales = df.groupby("Year")["Sales"].sum()

print("\n========== YEARLY REVENUE ==========")
print(yearly_sales.round(2))

# 5. Monthly Profit
monthly_profit = df.groupby("Year-Month")["Profit"].sum()

print("\n========== MONTHLY PROFIT ==========")
print(monthly_profit.round(2))

# 6. Month-over-Month Growth
monthly_growth = monthly_sales.pct_change() * 100

print("\n========== MONTHLY SALES GROWTH ==========")
print(monthly_growth.round(2))

# 7. NumPy Statistical Analysis
print("\n========== NUMPY STATISTICS ==========")

print("Mean Monthly Revenue:", round(np.mean(monthly_sales), 2))
print("Median Monthly Revenue:", round(np.median(monthly_sales), 2))
print("Revenue Standard Deviation:", round(np.std(monthly_sales), 2))
print("75th Percentile:", round(np.percentile(monthly_sales, 75), 2))

print("\n========== ANALYSIS COMPLETED ==========")
