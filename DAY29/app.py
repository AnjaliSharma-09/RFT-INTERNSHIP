import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("💰 Smart Expense Tracker & Budget Analyzer")

st.write(
    "Analyze your income, expenses, savings and "
    "spending patterns."
)


# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your expense CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df["Date"] = pd.to_datetime(df["Date"])

    df["Amount"] = pd.to_numeric(df["Amount"])


    # -------------------------------------------------
    # CATEGORY FUNCTION
    # -------------------------------------------------

    def categorize_expense(description):

        description = description.lower()

        if any(x in description for x in
               ["swiggy", "zomato", "restaurant", "food"]):
            return "Food"

        elif any(x in description for x in
                 ["petrol", "uber", "ola", "transport"]):
            return "Transport"

        elif any(x in description for x in
                 ["amazon", "shopping", "clothes"]):
            return "Shopping"

        elif any(x in description for x in
                 ["electricity", "internet", "mobile", "recharge"]):
            return "Bills & Utilities"

        elif "grocery" in description:
            return "Groceries"

        elif any(x in description for x in
                 ["medical", "hospital", "medicine"]):
            return "Healthcare"

        elif any(x in description for x in
                 ["college", "school", "course", "fees"]):
            return "Education"

        elif any(x in description for x in
                 ["movie", "netflix", "entertainment"]):
            return "Entertainment"

        elif "salary" in description:
            return "Income"

        else:
            return "Other"


    df["Category"] = df["Description"].apply(
        categorize_expense
    )


    # -------------------------------------------------
    # INCOME / EXPENSE
    # -------------------------------------------------

    income = df[
        df["Category"] == "Income"
    ]

    expenses = df[
        df["Category"] != "Income"
    ]

    total_income = income["Amount"].sum()

    total_expense = expenses["Amount"].sum()

    savings = total_income - total_expense


    # -------------------------------------------------
    # DASHBOARD METRICS
    # -------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💵 Total Income",
        f"₹{total_income:,.0f}"
    )

    col2.metric(
        "💸 Total Expenses",
        f"₹{total_expense:,.0f}"
    )

    col3.metric(
        "💰 Monthly Savings",
        f"₹{savings:,.0f}"
    )


    st.divider()


    # -------------------------------------------------
    # CATEGORY ANALYSIS
    # -------------------------------------------------

    category_expense = expenses.groupby(
        "Category"
    )["Amount"].sum().sort_values(
        ascending=False
    )


    col1, col2 = st.columns(2)


    with col1:

        st.subheader("📊 Category-wise Spending")

        st.bar_chart(category_expense)


    with col2:

        st.subheader("🥧 Spending Distribution")

        fig, ax = plt.subplots()

        category_expense.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax
        )

        ax.set_ylabel("")

        st.pyplot(fig)


    # -------------------------------------------------
    # DAILY TREND
    # -------------------------------------------------

    st.subheader("📈 Daily Spending Trend")

    daily_expense = expenses.groupby(
        expenses["Date"].dt.date
    )["Amount"].sum()

    st.line_chart(daily_expense)


    # -------------------------------------------------
    # PREDICTION
    # -------------------------------------------------

    st.subheader("🔮 Expense Prediction")

    days = expenses["Date"].dt.day.nunique()

    if days > 0:

        average_daily = total_expense / days

        last_day = expenses["Date"].dt.day.max()

        remaining_days = max(0, 30 - last_day)

        predicted_expense = (
            total_expense +
            average_daily * remaining_days
        )

        predicted_savings = (
            total_income - predicted_expense
        )

        p1, p2 = st.columns(2)

        p1.metric(
            "Predicted Monthly Expense",
            f"₹{predicted_expense:,.0f}"
        )

        p2.metric(
            "Predicted Savings",
            f"₹{predicted_savings:,.0f}"
        )


    # -------------------------------------------------
    # DATA TABLE
    # -------------------------------------------------

    st.subheader("📋 Expense Records")

    st.dataframe(
        df,
        use_container_width=True
    )


    # -------------------------------------------------
    # DOWNLOAD REPORT
    # -------------------------------------------------

    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Download Final Report",
        data=csv,
        file_name="expense_report.csv",
        mime="text/csv"
    )

else:

    st.info(
        "👆 Upload expenses.csv to start analyzing your expenses."
    )