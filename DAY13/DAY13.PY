# Project 13 - Distribution Analysis Using Seaborn

# Import Libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sample Dataset - Student Marks
marks = [45, 50, 55, 60, 62, 65, 67, 70, 72, 75,
         78, 80, 82, 85, 87, 90, 92, 95, 98, 100]

# Create DataFrame
df = pd.DataFrame({"Marks": marks})

# Display Dataset
print(df)

# Set Style
sns.set(style="whitegrid")

# Create Histogram with KDE Curve
plt.figure(figsize=(10,6))

sns.histplot(
    data=df,
    x="Marks",
    bins=8,
    kde=True,
    color="skyblue"
)

# Titles and Labels
plt.title("Distribution Analysis of Student Marks", fontsize=16)
plt.xlabel("Marks")
plt.ylabel("Frequency")

# Show Plot
plt.show()

# Identify Skewness
skewness = df["Marks"].skew()

print("\nSkewness Value:", skewness)

# Interpretation
if skewness > 0:
    print("The distribution is Positively Skewed (Right Skewed).")
elif skewness < 0:
    print("The distribution is Negatively Skewed (Left Skewed).")
else:
    print("The distribution is Symmetric.")