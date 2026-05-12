# student_dashboard.py

import pandas as pd

# Create Dataset
data = {
    "Name": ["AMIT", "RIYA", "JOHN"],
    "Math": [80, 90, 60],
    "Science": [70, 88, 65],
    "English": [85, 92, 70]
}

# Create DataFrame
df = pd.DataFrame(data)

print("===== STUDENT PERFORMANCE DASHBOARD =====")
print("\nOriginal Data:")
print(df)

# Calculate Average Marks Per Student
df["Average"] = (
    df["Math"] +
    df["Science"] +
    df["English"]
) / 3

# Add Grade Column
def calculate_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    else:
        return "Fail"

df["Grade"] = df["Average"].apply(calculate_grade)

print("\n===== STUDENT AVERAGES =====")
print(df[["Name", "Average", "Grade"]])

# Find Topper
topper = df.loc[df["Average"].idxmax()]

print("\n===== TOPPER =====")
print("Name:", topper["Name"])
print("Average Marks:", round(topper["Average"], 2))

# Overall Average
overall_average = df["Average"].mean()

print("\nOverall Class Average:", round(overall_average, 2))

# Count Students Above Average
above_average_students = df[df["Average"] > overall_average]

print("\n===== STUDENTS ABOVE CLASS AVERAGE =====")
print(above_average_students[["Name", "Average"]])

print("\nNumber of Students Above Average:",
      len(above_average_students))

# Subject-wise Average
subject_average = {
    "Math": df["Math"].mean(),
    "Science": df["Science"].mean(),
    "English": df["English"].mean()
}

print("\n===== SUBJECT-WISE AVERAGE =====")

for subject, avg in subject_average.items():
    print(subject, ":", round(avg, 2))

# Final Dashboard
print("\n===== FINAL DASHBOARD =====")
print(df)
