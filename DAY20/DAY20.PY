# =============================
# OPEN DATASET CAPSTONE PROJECT
# SALES DATA ANALYSIS
# =============================

# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
file_path = "sales_data.csv"
df = pd.read_csv(file_path)

# =============================
# 1. DATA CLEANING
# =============================

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATA INFO =====")
print(df.info())

print("\n===== CHECKING NULL VALUES =====")
print(df.isnull().sum())

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Convert Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

print("\n===== CLEANED DATA =====")
print(df.head())

# =============================
# 2. DATA ANALYSIS
# =============================

# Total Sales
total_sales = df['Sales'].sum()
print("\nTotal Sales:", total_sales)

# Total Profit
total_profit = df['Profit'].sum()
print("Total Profit:", total_profit)

# Average Sales
avg_sales = df['Sales'].mean()
print("Average Sales:", avg_sales)

# Region-wise Sales
region_sales = df.groupby('Region')['Sales'].sum()
print("\n===== REGION-WISE SALES =====")
print(region_sales)

# Category-wise Profit
category_profit = df.groupby('Category')['Profit'].sum()
print("\n===== CATEGORY-WISE PROFIT =====")
print(category_profit)

# Top Selling Products
top_products = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(5)
print("\n===== TOP SELLING PRODUCTS =====")
print(top_products)

# =============================
# 3. DATA VISUALIZATION
# =============================

sns.set_style("whitegrid")

# ----- Bar Chart -----
plt.figure(figsize=(8,5))
region_sales.plot(kind='bar', color='skyblue')
plt.title('Region-wise Sales')
plt.xlabel('Region')
plt.ylabel('Sales')
plt.xticks(rotation=0)
plt.show()

# ----- Pie Chart -----
plt.figure(figsize=(7,7))
category_profit.plot(kind='pie', autopct='%1.1f%%')
plt.title('Profit Distribution by Category')
plt.ylabel('')
plt.show()

# ----- Line Chart -----
daily_sales = df.groupby('Date')['Sales'].sum()

plt.figure(figsize=(10,5))
plt.plot(daily_sales.index, daily_sales.values, marker='o')
plt.title('Daily Sales Trend')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.grid(True)
plt.show()

# ----- Heatmap -----
plt.figure(figsize=(6,4))
correlation = df[['Sales', 'Profit', 'Quantity']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# =============================
# 4. DASHBOARD STYLE OUTPUT
# =============================

print("\n==============================")
print("      SALES DASHBOARD")
print("==============================")
print(f"Total Sales   : {total_sales}")
print(f"Total Profit  : {total_profit}")
print(f"Average Sales : {avg_sales:.2f}")
print("==============================")

# =============================
# 5. INSIGHTS
# =============================

print("\n===== BUSINESS INSIGHTS =====")

highest_region = region_sales.idxmax()
print(f"Highest Sales Region: {highest_region}")

highest_category = category_profit.idxmax()
print(f"Most Profitable Category: {highest_category}")

best_product = top_products.idxmax()
print(f"Top Selling Product: {best_product}")

print("\nProject Completed Successfully!")
