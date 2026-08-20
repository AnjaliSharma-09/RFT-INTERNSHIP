import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. IMPORT DATA
# ==========================================

input_file = "employee_performance.csv"

df = pd.read_csv(input_file)

print("\n===== EMPLOYEE PERFORMANCE DATA =====")
print(df.head())

# ==========================================
# 2. DATA CLEANING
# ==========================================

# Remove duplicate records
df = df.drop_duplicates()

# Convert numeric columns
df["Performance_Score"] = pd.to_numeric(
    df["Performance_Score"], errors="coerce"
)

df["Attendance"] = pd.to_numeric(
    df["Attendance"], errors="coerce"
)

# Remove rows with missing important values
df = df.dropna(
    subset=[
        "Employee_ID",
        "Employee_Name",
        "Department",
        "Performance_Score",
        "Attendance"
    ]
)

# Create output folder
os.makedirs("outputs", exist_ok=True)

# ==========================================
# 3. DEPARTMENT-WISE AVERAGE PERFORMANCE
# ==========================================

department_average = (
    df.groupby("Department")["Performance_Score"]
    .mean()
    .round(2)
    .reset_index()
)

department_average.columns = [
    "Department",
    "Average_Performance"
]

print("\n===== DEPARTMENT-WISE AVERAGE PERFORMANCE =====")
print(department_average)

# ==========================================
# 4. TOP 10 PERFORMERS
# ==========================================

top_10 = (
    df.sort_values(
        by="Performance_Score",
        ascending=False
    )
    .head(10)
)

print("\n===== TOP 10 PERFORMERS =====")
print(
    top_10[
        [
            "Employee_ID",
            "Employee_Name",
            "Department",
            "Performance_Score",
            "Attendance"
        ]
    ]
)

# ==========================================
# 5. EMPLOYEES WITH ATTENDANCE BELOW 75%
# ==========================================

low_attendance = df[df["Attendance"] < 75]

print("\n===== ATTENDANCE BELOW 75% =====")

if len(low_attendance) > 0:
    print(
        low_attendance[
            [
                "Employee_ID",
                "Employee_Name",
                "Department",
                "Performance_Score",
                "Attendance"
            ]
        ]
    )
else:
    print("No employees have attendance below 75%.")

# ==========================================
# 6. PERFORMANCE COMPARISON CHART
# ==========================================

plt.figure(figsize=(10, 6))

plt.bar(
    department_average["Department"],
    department_average["Average_Performance"]
)

plt.title("Department-wise Average Performance")
plt.xlabel("Department")
plt.ylabel("Average Performance Score")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "outputs/performance_comparison.png"
)

plt.show()

# ==========================================
# 7. ATTENDANCE TREND
# ==========================================

# Sort employees by Employee ID
attendance_data = df.sort_values("Employee_ID")

plt.figure(figsize=(12, 6))

plt.plot(
    attendance_data["Employee_ID"],
    attendance_data["Attendance"],
    marker="o"
)

plt.axhline(
    y=75,
    linestyle="--",
    label="75% Attendance Limit"
)

plt.title("Employee Attendance Trend")
plt.xlabel("Employee ID")
plt.ylabel("Attendance (%)")

plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig(
    "outputs/attendance_trend.png"
)

plt.show()

# ==========================================
# 8. DEPARTMENT DISTRIBUTION
# ==========================================

department_count = df["Department"].value_counts()

plt.figure(figsize=(8, 8))

plt.pie(
    department_count.values,
    labels=department_count.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Employee Department Distribution")

plt.tight_layout()

plt.savefig(
    "outputs/department_distribution.png"
)

plt.show()

# ==========================================
# 9. CREATE FINAL REPORT
# ==========================================

# Create ranking
df["Performance_Rank"] = (
    df["Performance_Score"]
    .rank(
        method="min",
        ascending=False
    )
    .astype(int)
)

# Attendance status
df["Attendance_Status"] = df["Attendance"].apply(
    lambda x: "Below 75%" if x < 75 else "Good"
)

# Department average mapped to each employee
df["Department_Average_Performance"] = (
    df["Department"]
    .map(
        department_average.set_index("Department")
        ["Average_Performance"]
    )
)

# Sort by performance
final_report = df.sort_values(
    by="Performance_Score",
    ascending=False
)

# ==========================================
# 10. EXPORT CSV
# ==========================================

output_file = "outputs/employee_final_report.csv"

final_report.to_csv(
    output_file,
    index=False
)

print("\n==========================================")
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("==========================================")

print(f"\nFinal report saved at:")
print(output_file)

print("\nTop 10 performers:")
print(
    top_10[
        ["Employee_Name", "Performance_Score"]
    ]
)
