# Sales Trend Visualization using Matplotlib

import matplotlib.pyplot as plt

# Dataset
dates = ["MON", "TUE", "WED", "THU", "FRI"]
sales = [200, 250, 300, 280, 350]

# Find highest and lowest sales
highest_sale = max(sales)
lowest_sale = min(sales)

highest_day = dates[sales.index(highest_sale)]
lowest_day = dates[sales.index(lowest_sale)]

# Create line plot
plt.figure(figsize=(8,5))

plt.plot(dates, sales, marker='o', linewidth=2)

# Highlight highest and lowest sales points
plt.scatter(highest_day, highest_sale, s=120, label="Highest Sale")
plt.scatter(lowest_day, lowest_sale, s=120, label="Lowest Sale")

# Add labels and title
plt.title("Weekly Sales Trend")
plt.xlabel("Days")
plt.ylabel("Sales")

# Add value labels
for i in range(len(dates)):
    plt.text(dates[i], sales[i] + 5, str(sales[i]), ha='center')

# Grid and legend
plt.grid(True)
plt.legend()

# Show plot
plt.show()

# Trend Analysis
print("Highest Sales:", highest_sale, "on", highest_day)
print("Lowest Sales:", lowest_sale, "on", lowest_day)