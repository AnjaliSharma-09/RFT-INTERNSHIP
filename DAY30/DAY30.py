import pandas as pd
import pdfplumber
import os
import re
from datetime import datetime


# --------------------------------------------------
# 1. Read CSV Invoice Data
# --------------------------------------------------

def read_csv_invoices(file_path):

    df = pd.read_csv(file_path)

    df["Invoice_Date"] = pd.to_datetime(
        df["Invoice_Date"],
        errors="coerce"
    )

    df["Due_Date"] = pd.to_datetime(
        df["Due_Date"],
        errors="coerce"
    )

    return df


# --------------------------------------------------
# 2. Calculate Item Total
# --------------------------------------------------

def calculate_total(df):

    df["Item_Total"] = df["Quantity"] * df["Price"]

    return df


# --------------------------------------------------
# 3. Identify Overdue Invoices
# --------------------------------------------------

def identify_overdue(df):

    today = pd.Timestamp.today().normalize()

    df["Payment_Status"] = df["Due_Date"].apply(
        lambda x: "Overdue"
        if pd.notna(x) and x < today
        else "Pending"
    )

    return df


# --------------------------------------------------
# 4. Extract Text From PDF
# --------------------------------------------------

def extract_pdf_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# --------------------------------------------------
# 5. Extract Invoice Number
# --------------------------------------------------

def extract_invoice_number(text):

    pattern = r"(?:Invoice\s*(?:No|Number|#)?\s*[:\-]?\s*)([A-Za-z0-9\-]+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    return match.group(1) if match else "Unknown"


# --------------------------------------------------
# 6. Extract Invoice Date
# --------------------------------------------------

def extract_invoice_date(text):

    pattern = r"(?:Invoice\s*Date|Date)\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return "Unknown"


# --------------------------------------------------
# 7. Extract Customer Details
# --------------------------------------------------

def extract_customer(text):

    pattern = r"(?:Customer|Bill To|Customer Name)\s*[:\-]?\s*([A-Za-z ]+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    return match.group(1).strip() if match else "Unknown"


# --------------------------------------------------
# 8. Process PDF Invoice
# --------------------------------------------------

def process_pdf_invoice(pdf_path):

    text = extract_pdf_text(pdf_path)

    invoice_number = extract_invoice_number(text)

    invoice_date = extract_invoice_date(text)

    customer = extract_customer(text)

    return {
        "Invoice_Number": invoice_number,
        "Customer_Name": customer,
        "Invoice_Date": invoice_date,
        "Extracted_Text": text
    }


# --------------------------------------------------
# 9. Generate Summary
# --------------------------------------------------

def generate_summary(df):

    total_invoices = df["Invoice_Number"].nunique()

    total_amount = df["Item_Total"].sum()

    overdue = (
        df[df["Payment_Status"] == "Overdue"]
        ["Invoice_Number"]
        .nunique()
    )

    pending = (
        df[df["Payment_Status"] == "Pending"]
        ["Invoice_Number"]
        .nunique()
    )

    summary = {
        "Total Invoices": total_invoices,
        "Total Amount": total_amount,
        "Overdue Invoices": overdue,
        "Pending Invoices": pending
    }

    return summary


# --------------------------------------------------
# 10. Main Program
# --------------------------------------------------

if __name__ == "__main__":

    input_file = "invoices/invoice_data.csv"

    output_file = "output/consolidated_invoice_report.csv"

    # Read data
    df = read_csv_invoices(input_file)

    # Calculate totals
    df = calculate_total(df)

    # Identify overdue invoices
    df = identify_overdue(df)

    # Generate summary
    summary = generate_summary(df)

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Export report
    df.to_csv(
        output_file,
        index=False
    )

    print("\n================================")
    print(" AUTOMATED INVOICE REPORT")
    print("================================")

    for key, value in summary.items():

        print(f"{key}: {value}")

    print("\nReport generated successfully!")

    print(
        f"Location: {output_file}"
    )