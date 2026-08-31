import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# 1. READ CSV FILE
# -------------------------------------------------

df = pd.read_csv("stock_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------------------------
# 2. CALCULATE INVESTMENT
# -------------------------------------------------

df["Investment"] = df["Buy_Price"] * df["Quantity"]

# -------------------------------------------------
# 3. CALCULATE CURRENT VALUE
# -------------------------------------------------

df["Current_Value"] = df["Current_Price"] * df["Quantity"]

# -------------------------------------------------
# 4. CALCULATE PROFIT / LOSS
# -------------------------------------------------

df["Profit_Loss"] = df["Current_Value"] - df["Investment"]

# -------------------------------------------------
# 5. CALCULATE RETURN %
# -------------------------------------------------

df["Return_%"] = (
    df["Profit_Loss"] / df["Investment"]
) * 100

# -------------------------------------------------
# 6. DISPLAY STOCK PERFORMANCE
# -------------------------------------------------

stock_summary = df.groupby(
    ["Stock", "Sector"]
).agg(
    Investment=("Investment", "first"),
    Current_Value=("Current_Value", "last"),
    Profit_Loss=("Profit_Loss", "last"),
    Return_Percent=("Return_%", "last")
).reset_index()

print("\n========== STOCK PERFORMANCE ==========\n")

print(stock_summary.round(2))

# -------------------------------------------------
# 7. BEST PERFORMING STOCK
# -------------------------------------------------

best_stock = stock_summary.loc[
    stock_summary["Return_Percent"].idxmax()
]

print("\n========== BEST PERFORMING STOCK ==========")

print("Stock:", best_stock["Stock"])
print("Return:", round(best_stock["Return_Percent"], 2), "%")

# -------------------------------------------------
# 8. WORST PERFORMING STOCK
# -------------------------------------------------

worst_stock = stock_summary.loc[
    stock_summary["Return_Percent"].idxmin()
]

print("\n========== WORST PERFORMING STOCK ==========")

print("Stock:", worst_stock["Stock"])
print("Return:", round(worst_stock["Return_Percent"], 2), "%")

# -------------------------------------------------
# 9. OVERALL PORTFOLIO RETURN
# -------------------------------------------------

total_investment = stock_summary["Investment"].sum()

total_current_value = stock_summary["Current_Value"].sum()

total_profit_loss = (
    total_current_value - total_investment
)

portfolio_return = (
    total_profit_loss / total_investment
) * 100

print("\n========== PORTFOLIO SUMMARY ==========")

print("Total Investment: ₹", round(total_investment, 2))
print("Current Value: ₹", round(total_current_value, 2))
print("Profit/Loss: ₹", round(total_profit_loss, 2))
print("Portfolio Return:", round(portfolio_return, 2), "%")

# -------------------------------------------------
# 10. PORTFOLIO GROWTH
# -------------------------------------------------

daily_portfolio = df.groupby("Date").agg(
    Investment=("Investment", "sum"),
    Current_Value=("Current_Value", "sum")
).reset_index()

plt.figure(figsize=(10, 5))

plt.plot(
    daily_portfolio["Date"],
    daily_portfolio["Current_Value"],
    marker="o",
    label="Portfolio Value"
)

plt.plot(
    daily_portfolio["Date"],
    daily_portfolio["Investment"],
    marker="o",
    label="Investment"
)

plt.title("Portfolio Growth")
plt.xlabel("Date")
plt.ylabel("Value (₹)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# -------------------------------------------------
# 11. SECTOR-WISE INVESTMENT
# -------------------------------------------------

sector_data = df.groupby("Sector")[
    "Investment"
].first()

plt.figure(figsize=(8, 5))

sector_data.plot(
    kind="bar"
)

plt.title("Sector-wise Investment")
plt.xlabel("Sector")
plt.ylabel("Investment (₹)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# -------------------------------------------------
# 12. DAILY RETURN ANALYSIS
# -------------------------------------------------

daily_returns = (
    daily_portfolio["Current_Value"]
    .pct_change() * 100
)

daily_portfolio["Daily_Return_%"] = daily_returns

plt.figure(figsize=(10, 5))

plt.plot(
    daily_portfolio["Date"],
    daily_portfolio["Daily_Return_%"],
    marker="o"
)

plt.axhline(
    0,
    linestyle="--"
)

plt.title("Daily Portfolio Return")
plt.xlabel("Date")
plt.ylabel("Daily Return (%)")

plt.grid(True)

plt.tight_layout()
plt.show()

# -------------------------------------------------
# 13. MOVING AVERAGE
# -------------------------------------------------

daily_portfolio["Moving_Average"] = (
    daily_portfolio["Current_Value"]
    .rolling(window=3)
    .mean()
)

print("\n========== MOVING AVERAGE ==========\n")

print(
    daily_portfolio[
        ["Date", "Current_Value", "Moving_Average"]
    ].round(2)
)

# -------------------------------------------------
# 14. NEXT DAY TREND PREDICTION
# -------------------------------------------------

latest_value = daily_portfolio[
    "Current_Value"
].iloc[-1]

latest_ma = daily_portfolio[
    "Moving_Average"
].iloc[-1]

print("\n========== NEXT DAY TREND ==========")

if latest_value > latest_ma:
    print("Prediction: 📈 UPWARD TREND")
elif latest_value < latest_ma:
    print("Prediction: 📉 DOWNWARD TREND")
else:
    print("Prediction: ➡️ SIDEWAYS TREND")