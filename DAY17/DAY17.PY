import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("customer_data.csv")

print(df.head())

# Create segments
def spending_category(spending):
    if spending >= 7000:
        return "High"
    elif spending >= 4000:
        return "Medium"
    else:
        return "Low"

df["Segment"] = df["Spending"].apply(spending_category)

# High-value customers
high_value = df[(df["Spending"] >= 7000) & (df["Visits"] >= 10)]

print("\nHigh Value Customers:")
print(high_value)

# Low engagement customers
low_engagement = df[df["Visits"] <= 5]

print("\nLow Engagement Customers:")
print(low_engagement)

# Histogram
plt.hist(df["Spending"], bins=5)
plt.title("Spending Distribution")
plt.xlabel("Spending")
plt.ylabel("Customers")
plt.show()

# Pie Chart
segment_counts = df["Segment"].value_counts()

plt.pie(segment_counts,
        labels=segment_counts.index,
        autopct='%1.1f%%')

plt.title("Customer Segments")
plt.show()