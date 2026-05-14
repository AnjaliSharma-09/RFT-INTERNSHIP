# data_filtering_tool.py

import pandas as pd

# -----------------------------
# STEP 1: Create Sample Dataset
# -----------------------------
data = {
    "Name": ["Anjali", "Rahul", "Priya", "Aman", "Neha"],
    "Age": [24, 35, 27, 29, 32],
    "Salary": [60000, 45000, 75000, 52000, 48000]
}

df = pd.DataFrame(data)

print("Original Dataset:\n")
print(df)

# ----------------------------------------
# STEP 2: Apply Multiple Filter Conditions
# ----------------------------------------

filtered_data = df[
    (df["Salary"] > 50000) &
    (df["Age"] < 30)
]

# -----------------------------
# STEP 3: Display Filtered Data
# -----------------------------

print("\nFiltered Results:\n")
print(filtered_data)

# -----------------------------------
# STEP 4: Save Filtered Data to File
# -----------------------------------

filtered_data.to_csv("filtered_data.csv", index=False)

print("\nFiltered data saved to 'filtered_data.csv'")