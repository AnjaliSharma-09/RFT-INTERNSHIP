import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. LOAD DATA
# ==========================================

file_path = "transactions.csv"

df = pd.read_csv(file_path)

print("First 5 transactions:")
print(df.head())

print("\nDataset Information:")
print(df.info())

# ==========================================
# 2. DATA CLEANING
# ==========================================

df.columns = df.columns.str.strip()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

df = df.dropna(subset=["TransactionID", "AccountID", "Date", "Amount"])

# Remove exact duplicate rows
df = df.drop_duplicates()

# ==========================================
# 3. DUPLICATE TRANSACTIONS
# ==========================================

duplicate_transactions = df[
    df.duplicated(
        subset=["AccountID", "Date", "Amount", "Merchant"],
        keep=False
    )
].copy()

print("\nDuplicate Transactions:")
print(duplicate_transactions)

# ==========================================
# 4. HIGH VALUE TRANSACTIONS
# ==========================================

THRESHOLD = 50000

high_value = df[df["Amount"] > THRESHOLD].copy()

print("\nHigh Value Transactions:")
print(high_value)

# ==========================================
# 5. FREQUENT / SUSPICIOUS ACCOUNTS
# ==========================================

transaction_frequency = (
    df.groupby("AccountID")
    .size()
    .reset_index(name="TransactionCount")
)

FREQUENCY_LIMIT = 10

suspicious_accounts = transaction_frequency[
    transaction_frequency["TransactionCount"] >= FREQUENCY_LIMIT
]

print("\nSuspicious Accounts:")
print(suspicious_accounts)

# ==========================================
# 6. CREATE RISK SCORE
# ==========================================

df["RiskScore"] = 0

# High-value transaction
df.loc[df["Amount"] > THRESHOLD, "RiskScore"] += 40

# Duplicate transaction
duplicate_keys = duplicate_transactions[
    ["AccountID", "Date", "Amount", "Merchant"]
].drop_duplicates()

df = df.merge(
    duplicate_keys.assign(IsDuplicate=True),
    on=["AccountID", "Date", "Amount", "Merchant"],
    how="left"
)

df["IsDuplicate"] = df["IsDuplicate"].fillna(False)

df.loc[df["IsDuplicate"], "RiskScore"] += 30

# Frequent account
frequent_accounts = set(suspicious_accounts["AccountID"])

df["FrequentAccount"] = df["AccountID"].isin(frequent_accounts)

df.loc[df["FrequentAccount"], "RiskScore"] += 20

# Very high-value transaction
df.loc[df["Amount"] > THRESHOLD * 2, "RiskScore"] += 10

# Risk category
def risk_category(score):
    if score >= 70:
        return "High Risk"
    elif score >= 40:
        return "Medium Risk"
    else:
        return "Low Risk"

df["RiskLevel"] = df["RiskScore"].apply(risk_category)

# ==========================================
# 7. SUSPICIOUS TRANSACTIONS
# ==========================================

suspicious_transactions = df[
    df["RiskScore"] >= 40
].copy()

print("\nSuspicious Transactions:")
print(suspicious_transactions)

# ==========================================
# 8. CREATE OUTPUT DIRECTORY
# ==========================================

os.makedirs("outputs", exist_ok=True)

# ==========================================
# 9. EXPORT SUSPICIOUS TRANSACTIONS
# ==========================================

suspicious_transactions.to_csv(
    "outputs/suspicious_transactions.csv",
    index=False
)

print("\nSuspicious transactions exported successfully.")

# ==========================================
# 10. TRANSACTION CATEGORY CHART
# ==========================================

category_count = df["Category"].value_counts()

plt.figure(figsize=(10, 6))

category_count.plot(kind="bar")

plt.title("Transaction Category Distribution")
plt.xlabel("Transaction Category")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/transaction_category_chart.png")

plt.show()

# ==========================================
# 11. DAILY TRANSACTION TREND
# ==========================================

daily_transactions = (
    df.groupby("Date")["Amount"]
    .sum()
)

plt.figure(figsize=(12, 6))

daily_transactions.plot()

plt.title("Daily Transaction Trend")
plt.xlabel("Date")
plt.ylabel("Total Transaction Amount")

plt.tight_layout()

plt.savefig("outputs/daily_transaction_trend.png")

plt.show()

# ==========================================
# 12. TOP 10 HIGHEST TRANSACTIONS
# ==========================================

top_10 = df.nlargest(10, "Amount")

print("\nTop 10 Highest Transactions:")
print(top_10)

plt.figure(figsize=(12, 6))

plt.bar(
    top_10["TransactionID"].astype(str),
    top_10["Amount"]
)

plt.title("Top 10 Highest Transactions")
plt.xlabel("Transaction ID")
plt.ylabel("Transaction Amount")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/top_10_transactions.png")

plt.show()

# ==========================================
# 13. SUMMARY
# ==========================================

print("\n========== FRAUD DETECTION SUMMARY ==========")

print("Total Transactions:", len(df))

print(
    "Duplicate Transactions:",
    len(duplicate_transactions)
)

print(
    "High Value Transactions:",
    len(high_value)
)

print(
    "Suspicious Accounts:",
    len(suspicious_accounts)
)

print(
    "Suspicious Transactions:",
    len(suspicious_transactions)
)

print(
    "Total Transaction Amount:",
    df["Amount"].sum()
)

print("\nRisk Distribution:")
print(df["RiskLevel"].value_counts())

print("\nAnalysis completed successfully!")