import matplotlib.pyplot as plt
import numpy as np

# Dataset
students = ["AMIT", "RIYA", "JOHN"]

maths = [85, 92, 78]
science = [88, 90, 80]
english = [82, 95, 76]

x = np.arange(len(students))
width = 0.25

# Create Grouped Bar Chart
plt.figure(figsize=(9,5))

plt.bar(x - width, maths, width, label='Maths')
plt.bar(x, science, width, label='Science')
plt.bar(x + width, english, width, label='English')

# Labels and Title
plt.xlabel("Students")
plt.ylabel("Marks")
plt.title("Student Performance Comparison")
plt.xticks(x, students)

# Legend
plt.legend()
# Show Plot
plt.show()

