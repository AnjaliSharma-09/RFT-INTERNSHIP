import streamlit as st
import pandas as pd
import os

from DAY30 import (
    read_csv_invoices,
    calculate_total,
    identify_overdue,
    generate_summary,
    process_pdf_invoice
)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Invoice Processing System",
    page_icon="🧾",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🧾 Automated Invoice Processing System")

st.write(
    "Upload CSV or PDF invoices and automatically "
    "extract, analyze and generate invoice reports."
)


# --------------------------------------------------
# File Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Invoice File",
    type=["csv", "pdf"]
)


if uploaded_file:

    # ==============================================
    # CSV PROCESSING
    # ==============================================

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

        # Convert dates
        df["Invoice_Date"] = pd.to_datetime(
            df["Invoice_Date"],
            errors="coerce"
        )

        df["Due_Date"] = pd.to_datetime(
            df["Due_Date"],
            errors="coerce"
        )

        # Calculate total
        df = calculate_total(df)

        # Identify overdue invoices
        df = identify_overdue(df)

        # Summary
        summary = generate_summary(df)

        st.success(
            "CSV invoice processed successfully!"
        )

        # ==========================================
        # SUMMARY CARDS
        # ==========================================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Invoices",
            summary["Total Invoices"]
        )

        col2.metric(
            "Total Amount",
            f"₹{summary['Total Amount']:,.2f}"
        )

        col3.metric(
            "Overdue",
            summary["Overdue Invoices"]
        )

        col4.metric(
            "Pending",
            summary["Pending Invoices"]
        )

        # ==========================================
        # DATA TABLE
        # ==========================================

        st.subheader("📋 Consolidated Invoice Report")

        st.dataframe(
            df,
            use_container_width=True
        )

        # ==========================================
        # OVERDUE INVOICES
        # ==========================================

        st.subheader("⚠️ Overdue Invoices")

        overdue_df = df[
            df["Payment_Status"] == "Overdue"
        ]

        st.dataframe(
            overdue_df,
            use_container_width=True
        )

        # ==========================================
        # CUSTOMER SPENDING
        # ==========================================

        st.subheader("💰 Customer-wise Invoice Amount")

        customer_amount = (
            df.groupby("Customer_Name")
            ["Item_Total"]
            .sum()
        )

        st.bar_chart(customer_amount)

        # ==========================================
        # EXPORT
        # ==========================================

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Consolidated Report",
            data=csv_data,
            file_name="consolidated_invoice_report.csv",
            mime="text/csv"
        )


    # ==============================================
    # PDF PROCESSING
    # ==============================================

    elif uploaded_file.name.endswith(".pdf"):

        temp_path = os.path.join(
            "invoices",
            uploaded_file.name
        )

        os.makedirs(
            "invoices",
            exist_ok=True
        )

        with open(temp_path, "wb") as f:

            f.write(
                uploaded_file.getbuffer()
            )

        result = process_pdf_invoice(
            temp_path
        )

        st.success(
            "PDF invoice processed successfully!"
        )

        # ==========================================
        # EXTRACTED INFORMATION
        # ==========================================

        st.subheader("🔍 Extracted Invoice Information")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Invoice Number",
            result["Invoice_Number"]
        )

        col2.metric(
            "Customer",
            result["Customer_Name"]
        )

        col3.metric(
            "Invoice Date",
            result["Invoice_Date"]
        )

        # ==========================================
        # RAW TEXT
        # ==========================================

        with st.expander(
            "📄 View Extracted PDF Text"
        ):

            st.text(
                result["Extracted_Text"]
            )