import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# STEP 1: CREATE SAMPLE DATASET

np.random.seed(42)

customer_data = {
    "Customer_ID": range(1, 101),
    "Age": np.random.randint(18, 65, 100),
    "Spending": np.random.randint(100, 5000, 100),
    "Visits": np.random.randint(1, 30, 100)
}

df = pd.DataFrame(customer_data)

# Save dataset to CSV
df.to_csv("customer_segmentation.csv", index=False)

print("Dataset Created Successfully!\n")
print(df.head())

# STEP 2: CUSTOMER SEGMENTATION

# Create Spending Categories
def spending_category(amount):
    if amount >= 3500:
        return "High"
    elif amount >= 1500:
        return "Medium"
    else:
        return "Low"

df["Segment"] = df["Spending"].apply(spending_category)

print("\nCustomer Segments:")
print(df["Segment"].value_counts())

# STEP 3: IDENTIFY CUSTOMER TYPES

# High-Value Customers
high_value = df[df["Spending"] >= 3500]

# Low-Engagement Users
low_engagement = df[df["Visits"] <= 5]

print("\nHigh-Value Customers:")
print(high_value.head())

print("\nLow-Engagement Users:")
print(low_engagement.head())

# STEP 4: VISUALIZATION

plt.figure(figsize=(15, 5))

# Spending Distribution
plt.subplot(1, 2, 1)
sns.histplot(df["Spending"], bins=10, kde=True)
plt.title("Spending Distribution")
plt.xlabel("Spending")
plt.ylabel("Count")

# Customer Categories
plt.subplot(1, 2, 2)
sns.countplot(x="Segment", data=df)
plt.title("Customer Categories")

plt.tight_layout()
plt.show()

# STEP 5: BUSINESS STRATEGIES

print("\n========== BUSINESS STRATEGIES ==========")

print("""
1. HIGH-VALUE CUSTOMERS
   - Provide premium membership offers
   - Give exclusive discounts and rewards
   - Personalized marketing campaigns

2. MEDIUM-SPENDING CUSTOMERS
   - Encourage more purchases with combo offers
   - Introduce loyalty programs

3. LOW-SPENDING CUSTOMERS
   - Offer first-time coupons
   - Run engagement campaigns

4. LOW-ENGAGEMENT USERS
   - Send reminder emails/SMS
   - Give visit-based incentives
""")

# STEP 6: SUMMARY REPORT

print("\n========== SUMMARY REPORT ==========")

print(f"Total Customers: {len(df)}")
print(f"High-Value Customers: {len(high_value)}")
print(f"Low-Engagement Users: {len(low_engagement)}")

print("\nSegment Distribution:")
print(df["Segment"].value_counts())
