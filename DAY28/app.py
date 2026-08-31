import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Stock Portfolio Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Market Portfolio Analyzer")

st.write(
    "Analyze portfolio performance, returns, sectors "
    "and moving-average trends."
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Stock CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

else:

    df = pd.read_csv("stock_data.csv")


# -------------------------------------------------
# DATA PREPROCESSING
# -------------------------------------------------

df["Date"] = pd.to_datetime(df["Date"])

df["Investment"] = (
    df["Buy_Price"] * df["Quantity"]
)

df["Current_Value"] = (
    df["Current_Price"] * df["Quantity"]
)

df["Profit_Loss"] = (
    df["Current_Value"] - df["Investment"]
)

df["Return_%"] = (
    df["Profit_Loss"]
    / df["Investment"]
) * 100


# -------------------------------------------------
# STOCK SUMMARY
# -------------------------------------------------

summary = df.groupby(
    ["Stock", "Sector"]
).agg(
    Investment=("Investment", "first"),
    Current_Value=("Current_Value", "last"),
    Profit_Loss=("Profit_Loss", "last"),
    Return_Percent=("Return_%", "last")
).reset_index()


# -------------------------------------------------
# PORTFOLIO METRICS
# -------------------------------------------------

total_investment = summary[
    "Investment"
].sum()

total_value = summary[
    "Current_Value"
].sum()

profit_loss = (
    total_value - total_investment
)

portfolio_return = (
    profit_loss / total_investment
) * 100


# -------------------------------------------------
# METRIC CARDS
# -------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Investment",
    f"₹{total_investment:,.0f}"
)

col2.metric(
    "Current Value",
    f"₹{total_value:,.0f}"
)

col3.metric(
    "Profit / Loss",
    f"₹{profit_loss:,.0f}"
)

col4.metric(
    "Portfolio Return",
    f"{portfolio_return:.2f}%"
)


# -------------------------------------------------
# STOCK PERFORMANCE
# -------------------------------------------------

st.header("📊 Stock Performance")

st.dataframe(
    summary.round(2),
    use_container_width=True
)


# -------------------------------------------------
# BEST AND WORST STOCK
# -------------------------------------------------

best = summary.loc[
    summary["Return_Percent"].idxmax()
]

worst = summary.loc[
    summary["Return_Percent"].idxmin()
]

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"🏆 Best Stock: {best['Stock']} "
        f"({best['Return_Percent']:.2f}%)"
    )

with col2:

    st.error(
        f"⚠️ Worst Stock: {worst['Stock']} "
        f"({worst['Return_Percent']:.2f}%)"
    )


# -------------------------------------------------
# DAILY PORTFOLIO
# -------------------------------------------------

daily = df.groupby("Date").agg(
    Current_Value=("Current_Value", "sum")
).reset_index()

daily["Daily_Return_%"] = (
    daily["Current_Value"]
    .pct_change() * 100
)

daily["Moving_Average"] = (
    daily["Current_Value"]
    .rolling(3)
    .mean()
)


# -------------------------------------------------
# PORTFOLIO GROWTH CHART
# -------------------------------------------------

st.header("📈 Portfolio Growth")

fig, ax = plt.subplots()

ax.plot(
    daily["Date"],
    daily["Current_Value"],
    marker="o"
)

ax.set_xlabel("Date")
ax.set_ylabel("Portfolio Value (₹)")
ax.set_title("Portfolio Growth")

ax.grid(True)

st.pyplot(fig)


# -------------------------------------------------
# SECTOR INVESTMENT
# -------------------------------------------------

st.header("📊 Sector-wise Investment")

sector = df.groupby("Sector")[
    "Investment"
].first()

fig, ax = plt.subplots()

sector.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Sector")
ax.set_ylabel("Investment (₹)")
ax.set_title("Sector-wise Investment")

plt.xticks(rotation=45)

st.pyplot(fig)


# -------------------------------------------------
# DAILY RETURN
# -------------------------------------------------

st.header("📉 Daily Return Analysis")

fig, ax = plt.subplots()

ax.plot(
    daily["Date"],
    daily["Daily_Return_%"],
    marker="o"
)

ax.axhline(
    0,
    linestyle="--"
)

ax.set_xlabel("Date")
ax.set_ylabel("Return (%)")
ax.set_title("Daily Portfolio Return")

ax.grid(True)

st.pyplot(fig)


# -------------------------------------------------
# MOVING AVERAGE
# -------------------------------------------------

st.header("⭐ Moving Average Trend Prediction")

fig, ax = plt.subplots()

ax.plot(
    daily["Date"],
    daily["Current_Value"],
    marker="o",
    label="Portfolio Value"
)

ax.plot(
    daily["Date"],
    daily["Moving_Average"],
    marker="o",
    label="3-Day Moving Average"
)

ax.set_xlabel("Date")
ax.set_ylabel("Value (₹)")

ax.legend()
ax.grid(True)

st.pyplot(fig)


# -------------------------------------------------
# PREDICTION
# -------------------------------------------------

latest_value = daily[
    "Current_Value"
].iloc[-1]

latest_ma = daily[
    "Moving_Average"
].iloc[-1]

st.subheader("🔮 Next Day Trend")

if latest_value > latest_ma:

    st.success(
        "📈 Predicted Trend: UPWARD"
    )

elif latest_value < latest_ma:

    st.warning(
        "📉 Predicted Trend: DOWNWARD"
    )

else:

    st.info(
        "➡️ Predicted Trend: SIDEWAYS"
    )