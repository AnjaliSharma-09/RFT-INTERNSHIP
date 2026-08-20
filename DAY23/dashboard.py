import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Employee Performance Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Employee Performance Analytics Dashboard")

st.write(
    "Interactive analysis of employee performance, "
    "attendance and department distribution."
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("employee_performance.csv")

# Remove duplicates
df = df.drop_duplicates()

# Convert numeric values
df["Performance_Score"] = pd.to_numeric(
    df["Performance_Score"],
    errors="coerce"
)

df["Attendance"] = pd.to_numeric(
    df["Attendance"],
    errors="coerce"
)

df = df.dropna()

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🔎 Filters")

departments = sorted(
    df["Department"].unique()
)

selected_departments = st.sidebar.multiselect(
    "Select Department",
    departments,
    default=departments
)

min_performance = st.sidebar.slider(
    "Minimum Performance Score",
    min_value=0,
    max_value=100,
    value=0
)

min_attendance = st.sidebar.slider(
    "Minimum Attendance (%)",
    min_value=0,
    max_value=100,
    value=0
)

# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df[
    (df["Department"].isin(selected_departments))
    &
    (df["Performance_Score"] >= min_performance)
    &
    (df["Attendance"] >= min_attendance)
]

# ==========================================
# KEY METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Employees",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average Performance",
        round(
            filtered_df["Performance_Score"].mean(),
            2
        )
    )

with col3:
    st.metric(
        "Average Attendance",
        f"{filtered_df['Attendance'].mean():.2f}%"
    )

with col4:
    low_attendance_count = len(
        filtered_df[
            filtered_df["Attendance"] < 75
        ]
    )

    st.metric(
        "Attendance < 75%",
        low_attendance_count
    )

# ==========================================
# DATA TABLE
# ==========================================

st.subheader("👥 Employee Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ==========================================
# DEPARTMENT PERFORMANCE
# ==========================================

st.subheader("📊 Department-wise Performance")

department_avg = (
    filtered_df
    .groupby("Department")["Performance_Score"]
    .mean()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots()

department_avg.plot(
    kind="bar",
    ax=ax1
)

ax1.set_xlabel("Department")
ax1.set_ylabel("Average Performance")
ax1.set_title(
    "Department-wise Average Performance"
)

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig1)

# ==========================================
# ATTENDANCE TREND
# ==========================================

st.subheader("📈 Attendance Trend")

attendance_data = filtered_df.sort_values(
    "Employee_ID"
)

fig2, ax2 = plt.subplots()

ax2.plot(
    attendance_data["Employee_ID"],
    attendance_data["Attendance"],
    marker="o"
)

ax2.axhline(
    75,
    linestyle="--",
    label="75% Limit"
)

ax2.set_xlabel("Employee ID")
ax2.set_ylabel("Attendance (%)")
ax2.set_title("Employee Attendance Trend")

plt.xticks(rotation=45)
ax2.legend()

plt.tight_layout()

st.pyplot(fig2)

# ==========================================
# DEPARTMENT DISTRIBUTION
# ==========================================

st.subheader("🥧 Department Distribution")

department_count = (
    filtered_df["Department"]
    .value_counts()
)

fig3, ax3 = plt.subplots()

ax3.pie(
    department_count.values,
    labels=department_count.index,
    autopct="%1.1f%%",
    startangle=90
)

ax3.set_title(
    "Employee Department Distribution"
)

st.pyplot(fig3)

# ==========================================
# TOP 10 PERFORMERS
# ==========================================

st.subheader("🏆 Top 10 Performers")

top_10 = (
    filtered_df
    .sort_values(
        "Performance_Score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_10[
        [
            "Employee_ID",
            "Employee_Name",
            "Department",
            "Performance_Score",
            "Attendance"
        ]
    ],
    use_container_width=True
)

# ==========================================
# LOW ATTENDANCE EMPLOYEES
# ==========================================

st.subheader("⚠️ Employees with Attendance Below 75%")

low_attendance = filtered_df[
    filtered_df["Attendance"] < 75
]

if len(low_attendance) > 0:

    st.dataframe(
        low_attendance[
            [
                "Employee_ID",
                "Employee_Name",
                "Department",
                "Performance_Score",
                "Attendance"
            ]
        ],
        use_container_width=True
    )

else:

    st.success(
        "No employees have attendance below 75%."
    )

# ==========================================
# DOWNLOAD REPORT
# ==========================================

st.subheader("📥 Download Report")

csv_data = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="Download Employee Report",
    data=csv_data,
    file_name="employee_final_report.csv",
    mime="text/csv"
)
