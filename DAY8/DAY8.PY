# Employee Salary Insights Project
# Concepts Used:
# - Grouping
# - Aggregation (groupby)

import pandas as pd

# -----------------------------
# STEP 1: Create Dataset
# -----------------------------
data = {
    "NAME": ["A", "B", "C", "D"],
    "DEPT": ["IT", "HR", "IT", "HR"],
    "SALARY": [50000, 40000, 60000, 45000]
}

df = pd.DataFrame(data)

print("===== EMPLOYEE DATA =====")
print(df)

# -----------------------------
# STEP 2: Average Salary Per Department
# -----------------------------
avg_salary = df.groupby("DEPT")["SALARY"].mean()

print("\n===== AVERAGE SALARY PER DEPARTMENT =====")
print(avg_salary)

# -----------------------------
# STEP 3: Highest Paid Employee Per Department
# -----------------------------
highest_paid = df.loc[df.groupby("DEPT")["SALARY"].idxmax()]

print("\n===== HIGHEST PAID EMPLOYEE PER DEPARTMENT =====")
print(highest_paid)

# -----------------------------
# BONUS 1: Count Employees Per Department
# -----------------------------
employee_count = df.groupby("DEPT")["NAME"].count()

print("\n===== EMPLOYEE COUNT PER DEPARTMENT =====")
print(employee_count)

# -----------------------------
# BONUS 2: Sort Departments By Average Salary
# -----------------------------
sorted_avg_salary = avg_salary.sort_values(ascending=False)

print("\n===== DEPARTMENTS SORTED BY AVG SALARY =====")
print(sorted_avg_salary)
