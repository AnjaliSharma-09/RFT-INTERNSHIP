# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV File
df = pd.read_csv("sales_data.csv")

# Display Dataset
print(df.head())

# Set Style
sns.set(style="whitegrid")

# Create Subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# =====================================
# 1. LINE CHART
# =====================================

monthly_sales = df.groupby("Month")["Sales"].sum()

axes[0, 0].plot(
    monthly_sales.index,
    monthly_sales.values,
    marker='o'
)

axes[0, 0].set_title("Monthly Sales Trend")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Sales")

# =====================================
# 2. BAR CHART
# =====================================

category_sales = df.groupby("Category")["Sales"].sum()

axes[0, 1].bar(
    category_sales.index,
    category_sales.values
)

axes[0, 1].set_title("Sales by Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Total Sales")

# =====================================
# 3. HISTOGRAM
# =====================================

axes[1, 0].hist(
    df["Sales"],
    bins=6
)

axes[1, 0].set_title("Sales Distribution")
axes[1, 0].set_xlabel("Sales")
axes[1, 0].set_ylabel("Frequency")

# =====================================
# 4. BOXPLOT
# =====================================

axes[1, 1].boxplot(df["Sales"])

axes[1, 1].set_title("Outlier Detection")

# Adjust Layout
plt.tight_layout()

# Show Dashboard
plt.show()