import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Fraud Detection & Transaction Analysis System")

st.markdown(
    "Analyze transactions, identify suspicious activity "
    "and calculate transaction risk scores."
)

# ==========================================
# LOAD DATA
# ==========================================

uploaded_file = st.file_uploader(
    "Upload Transaction CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df.columns = df.columns.str.strip()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "TransactionID",
            "AccountID",
            "Date",
            "Amount"
        ]
    )

    # ==========================================
    # SIDEBAR FILTERS
    # ==========================================

    st.sidebar.header("🔎 Filters")

    threshold = st.sidebar.number_input(
        "High Value Threshold",
        min_value=0,
        value=50000,
        step=5000
    )

    categories = st.sidebar.multiselect(
        "Transaction Category",
        options=sorted(df["Category"].unique()),
        default=sorted(df["Category"].unique())
    )

    search_account = st.sidebar.text_input(
        "Search Account ID"
    )

    # ==========================================
    # APPLY FILTERS
    # ==========================================

    filtered_df = df[
        df["Category"].isin(categories)
    ]

    if search_account:
        filtered_df = filtered_df[
            filtered_df["AccountID"]
            .astype(str)
            .str.contains(
                search_account,
                case=False,
                na=False
            )
        ]

    # ==========================================
    # RISK SCORE
    # ==========================================

    filtered_df = filtered_df.copy()

    filtered_df["RiskScore"] = 0

    filtered_df.loc[
        filtered_df["Amount"] > threshold,
        "RiskScore"
    ] += 40

    # Duplicate detection
    duplicate_mask = filtered_df.duplicated(
        subset=[
            "AccountID",
            "Date",
            "Amount",
            "Merchant"
        ],
        keep=False
    )

    filtered_df.loc[
        duplicate_mask,
        "RiskScore"
    ] += 30

    # Frequent accounts
    account_counts = (
        filtered_df.groupby("AccountID")
        .size()
    )

    frequent_accounts = account_counts[
        account_counts >= 10
    ].index

    filtered_df.loc[
        filtered_df["AccountID"].isin(
            frequent_accounts
        ),
        "RiskScore"
    ] += 20

    # Very high transaction
    filtered_df.loc[
        filtered_df["Amount"] > threshold * 2,
        "RiskScore"
    ] += 10

    # Risk level
    filtered_df["RiskLevel"] = pd.cut(
        filtered_df["RiskScore"],
        bins=[-1, 39, 69, 100],
        labels=[
            "Low Risk",
            "Medium Risk",
            "High Risk"
        ]
    )

    # ==========================================
    # KPI CARDS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Transactions",
        len(filtered_df)
    )

    col2.metric(
        "Total Amount",
        f"₹{filtered_df['Amount'].sum():,.0f}"
    )

    col3.metric(
        "High Value Transactions",
        len(
            filtered_df[
                filtered_df["Amount"] > threshold
            ]
        )
    )

    col4.metric(
        "Suspicious Transactions",
        len(
            filtered_df[
                filtered_df["RiskScore"] >= 40
            ]
        )
    )

    st.divider()

    # ==========================================
    # TRANSACTION CATEGORY CHART
    # ==========================================

    st.subheader("📊 Transaction Category Distribution")

    category_data = (
        filtered_df["Category"]
        .value_counts()
        .reset_index()
    )

    category_data.columns = [
        "Category",
        "Count"
    ]

    fig1 = px.bar(
        category_data,
        x="Category",
        y="Count",
        title="Transaction Category Chart"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # ==========================================
    # DAILY TRANSACTION TREND
    # ==========================================

    st.subheader("📈 Daily Transaction Trend")

    daily = (
        filtered_df
        .groupby("Date")["Amount"]
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        daily,
        x="Date",
        y="Amount",
        markers=True,
        title="Daily Transaction Trend"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ==========================================
    # TOP 10 TRANSACTIONS
    # ==========================================

    st.subheader("💰 Top 10 Highest Transactions")

    top10 = filtered_df.nlargest(
        10,
        "Amount"
    )

    fig3 = px.bar(
        top10,
        x="TransactionID",
        y="Amount",
        title="Top 10 Highest Transactions"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # ==========================================
    # RISK DISTRIBUTION
    # ==========================================

    st.subheader("⚠️ Risk Distribution")

    risk_data = (
        filtered_df["RiskLevel"]
        .value_counts()
        .reset_index()
    )

    risk_data.columns = [
        "RiskLevel",
        "Count"
    ]

    fig4 = px.pie(
        risk_data,
        names="RiskLevel",
        values="Count",
        title="Transaction Risk Distribution"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    # ==========================================
    # SUSPICIOUS TRANSACTIONS
    # ==========================================

    st.subheader("🚨 Suspicious Transactions")

    suspicious = filtered_df[
        filtered_df["RiskScore"] >= 40
    ].sort_values(
        "RiskScore",
        ascending=False
    )

    st.dataframe(
        suspicious,
        use_container_width=True
    )

    # ==========================================
    # DOWNLOAD CSV
    # ==========================================

    csv = suspicious.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Suspicious Transactions",
        data=csv,
        file_name="suspicious_transactions.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Please upload a transactions CSV file "
        "to start the analysis."
    )
    