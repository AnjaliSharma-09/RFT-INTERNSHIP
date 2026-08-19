import pandas as pd
import matplotlib.pyplot as plt
# 1. Load CSV dataset
df = pd.read_csv("sales_data.csv")

print("Original Dataset:")
print(df.head())

print("\nDataset Shape:", df.shape)
# 2. DATA CLEANING
# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove rows having missing values
df = df.dropna()

# Remove duplicate rows
print("\nDuplicate rows before cleaning:", df.duplicated().sum())

df = df.drop_duplicates()

print("Duplicate rows after cleaning:", df.duplicated().sum())

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])
# Make sure Revenue is numeric
df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")

# Remove rows where Revenue could not be converted
df = df.dropna(subset=["Revenue"])

print("\nCleaned Dataset:")
print(df.head())
# 3. TOTAL SALES
total_sales = df["Revenue"].sum()

print("\n================================")
print("TOTAL SALES")
print("================================")
print(f"₹{total_sales:,.2f}")
# 4. AVERAGE REVENUE
average_revenue = df["Revenue"].mean()

print("\n================================")
print("AVERAGE REVENUE")
print("================================")
print(f"₹{average_revenue:,.2f}")
# 5. TOP 5 CUSTOMERS
top_customers = (
    df.groupby("Customer")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\n================================")
print("TOP 5 CUSTOMERS")
print("================================")
print(top_customers)
# 6. SALES TREND - LINE CHART
daily_sales = (
    df.groupby("Date")["Revenue"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(10, 5))

plt.plot(
    daily_sales.index,
    daily_sales.values,
    marker="o"
)

plt.title("Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales Revenue")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()
# 7. TOP PRODUCTS - BAR CHART
top_products = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

plt.figure(figsize=(9, 5))

plt.bar(
    top_products.index,
    top_products.values
)

plt.title("Top 5 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()
# 8. CATEGORY DISTRIBUTION - PIE CHART
category_sales = (
    df.groupby("Category")["Revenue"]
    .sum()
)

plt.figure(figsize=(7, 7))

plt.pie(
    category_sales.values,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Sales Distribution by Category")

plt.tight_layout()
plt.show()
# 9. ADDITIONAL DASHBOARD INFORMATION
total_orders = len(df)

total_quantity = df["Quantity"].sum()

average_order_value = df["Revenue"].mean()

best_product = top_products.index[0]

best_category = category_sales.idxmax()

print("\n================================")
print("BUSINESS SUMMARY")
print("================================")

print("Total Sales       :", f"₹{total_sales:,.2f}")
print("Average Revenue   :", f"₹{average_revenue:,.2f}")
print("Total Orders      :", total_orders)
print("Total Quantity    :", total_quantity)
print("Average Order Value:", f"₹{average_order_value:,.2f}")
print("Best Product      :", best_product)
print("Best Category     :", best_category)

# 10. TOP CUSTOMER DETAILS
print("\n================================")
print("TOP 5 CUSTOMERS WITH REVENUE")
print("================================")

for customer, revenue in top_customers.items():
    print(f"{customer}: ₹{revenue:,.2f}")

print("\nDashboard analysis completed successfully!")

