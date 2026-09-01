import pandas as pd
import matplotlib.pyplot as plt


# -------------------------------------------------
# 1. IMPORT DATA
# -------------------------------------------------

df = pd.read_csv("expenses.csv")

df["Date"] = pd.to_datetime(df["Date"])
df["Amount"] = pd.to_numeric(df["Amount"])


# -------------------------------------------------
# 2. AUTOMATIC EXPENSE CATEGORIZATION
# -------------------------------------------------

def categorize_expense(description):

    description = description.lower()

    if any(word in description for word in
           ["swiggy", "restaurant", "food", "zomato"]):
        return "Food"

    elif any(word in description for word in
             ["petrol", "uber", "ola", "transport"]):
        return "Transport"

    elif any(word in description for word in
             ["amazon", "shopping", "clothes"]):
        return "Shopping"

    elif any(word in description for word in
             ["electricity", "internet", "mobile", "recharge"]):
        return "Bills & Utilities"

    elif any(word in description for word in
             ["grocery"]):
        return "Groceries"

    elif any(word in description for word in
             ["medical", "hospital", "medicine"]):
        return "Healthcare"

    elif any(word in description for word in
             ["college", "school", "course", "fees"]):
        return "Education"

    elif any(word in description for word in
             ["movie", "netflix", "entertainment"]):
        return "Entertainment"

    elif "salary" in description:
        return "Income"

    else:
        return "Other"


df["Category"] = df["Description"].apply(categorize_expense)


# -------------------------------------------------
# 3. SEPARATE INCOME AND EXPENSES
# -------------------------------------------------

income = df[df["Category"] == "Income"]

expenses = df[df["Category"] != "Income"]

total_income = income["Amount"].sum()

total_expense = expenses["Amount"].sum()

monthly_savings = total_income - total_expense


# -------------------------------------------------
# 4. BUDGET SUMMARY
# -------------------------------------------------

print("\n========== SMART EXPENSE TRACKER ==========")

print(f"Total Income      : ₹{total_income:,.2f}")
print(f"Total Expenses    : ₹{total_expense:,.2f}")
print(f"Monthly Savings   : ₹{monthly_savings:,.2f}")

if total_income > 0:
    savings_percentage = (monthly_savings / total_income) * 100
else:
    savings_percentage = 0

print(f"Savings Percentage: {savings_percentage:.2f}%")


# -------------------------------------------------
# 5. CATEGORY-WISE EXPENSE
# -------------------------------------------------

category_expense = expenses.groupby(
    "Category"
)["Amount"].sum().sort_values(ascending=False)

print("\n========== CATEGORY-WISE EXPENSE ==========")

print(category_expense)


# -------------------------------------------------
# 6. HIGHEST SPENDING CATEGORY
# -------------------------------------------------

if not category_expense.empty:

    highest_category = category_expense.idxmax()
    highest_amount = category_expense.max()

    print("\nHighest Spending Category:")
    print(f"{highest_category} → ₹{highest_amount:,.2f}")


# -------------------------------------------------
# 7. DAILY SPENDING
# -------------------------------------------------

daily_expense = expenses.groupby(
    expenses["Date"].dt.date
)["Amount"].sum()

print("\n========== DAILY EXPENSE ==========")

print(daily_expense)


# -------------------------------------------------
# 8. VISUALIZATION - CATEGORY EXPENSE
# -------------------------------------------------

plt.figure(figsize=(9, 5))

category_expense.plot(
    kind="bar"
)

plt.title("Category-wise Spending")

plt.xlabel("Category")

plt.ylabel("Amount (₹)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("category_expense.png")

plt.show()


# -------------------------------------------------
# 9. VISUALIZATION - DAILY SPENDING TREND
# -------------------------------------------------

plt.figure(figsize=(10, 5))

daily_expense.plot(
    kind="line",
    marker="o"
)

plt.title("Daily Spending Trend")

plt.xlabel("Date")

plt.ylabel("Amount (₹)")

plt.grid(True)

plt.tight_layout()

plt.savefig("daily_spending.png")

plt.show()


# -------------------------------------------------
# 10. EXPORT FINAL REPORT
# -------------------------------------------------

df.to_csv(
    "expense_report.csv",
    index=False
)

print("\nFinal report exported successfully!")

print("File: expense_report.csv")
# -------------------------------------------------
# 11. EXPENSE PREDICTION
# -------------------------------------------------

import numpy as np

days_passed = expenses["Date"].dt.day.nunique()

if days_passed > 0:

    average_daily_expense = total_expense / days_passed

    last_day = expenses["Date"].dt.day.max()

    remaining_days = 30 - last_day

    predicted_monthly_expense = (
        total_expense +
        (average_daily_expense * remaining_days)
    )

    print("\n========== EXPENSE PREDICTION ==========")

    print(
        f"Average Daily Expense: "
        f"₹{average_daily_expense:,.2f}"
    )

    print(
        f"Predicted Monthly Expense: "
        f"₹{predicted_monthly_expense:,.2f}"
    )

    predicted_savings = (
        total_income - predicted_monthly_expense
    )

    print(
        f"Predicted Savings: "
        f"₹{predicted_savings:,.2f}"
    )