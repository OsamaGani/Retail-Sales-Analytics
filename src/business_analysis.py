
import pandas as pd
import numpy as np

# Load cleaned dataset
df = pd.read_csv("data/cleaned_sales.csv")

print("\n========== RETAIL BUSINESS ANALYSIS ==========")

# 1. Total Revenue
total_revenue = np.sum(df["Sales"])

# 2. Total Profit
total_profit = np.sum(df["Profit"])

# 3. Total Orders
total_orders = df["Order ID"].nunique()

# 4. Total Customers
total_customers = df["Customer ID"].nunique()

# 5. Total Products Sold
total_quantity = np.sum(df["Quantity"])

# 6. Average Sales
average_sales = np.mean(df["Sales"])

# 7. Average Profit
average_profit = np.mean(df["Profit"])

# 8. Overall Profit Margin
profit_margin = (total_profit / total_revenue) * 100

print("\n========== KEY PERFORMANCE INDICATORS ==========")

print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Total Quantity Sold: {total_quantity:,}")
print(f"Average Sales: ${average_sales:,.2f}")
print(f"Average Profit: ${average_profit:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")

# 9. Category-wise Sales
print("\n========== CATEGORY WISE SALES ==========")

category_sales = df.groupby("Category")["Sales"].sum()

print(category_sales.sort_values(ascending=False))

# 10. Region-wise Sales
print("\n========== REGION WISE SALES ==========")

region_sales = df.groupby("Region")["Sales"].sum()

print(region_sales.sort_values(ascending=False))

# 11. Top 10 Products
print("\n========== TOP 10 PRODUCTS ==========")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products)

# 12. Loss-making Products
print("\n========== LOSS MAKING PRODUCTS ==========")

product_profit = df.groupby("Product Name")["Profit"].sum()

loss_products = product_profit[product_profit < 0]

print(loss_products.sort_values().head(10))

print("\n========== ANALYSIS COMPLETED ==========")
