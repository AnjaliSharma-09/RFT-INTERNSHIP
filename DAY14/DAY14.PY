# Category Breakdown (Pie Chart)

import matplotlib.pyplot as plt

# Dataset
categories = ["FOOD", "TRAVEL", "SHOPPING"]
expenses = [500, 300, 200]

# Explode the highest category (FOOD)
explode = [0.1, 0, 0]

# Create Pie Chart
plt.figure(figsize=(7,7))

plt.pie(
    expenses,
    labels=categories,
    autopct='%1.1f%%',   # Percentage labels
    explode=explode,     # Highlight highest category
    shadow=True,
    startangle=90
)

# Title
plt.title("Category Breakdown of Expenses")

# Display Chart
plt.show()