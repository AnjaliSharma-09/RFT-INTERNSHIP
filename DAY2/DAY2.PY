# ----------- Functions -----------

def calculate_average(data):
    return sum(data) / len(data)

def find_min_max(data):
    return min(data), max(data)

def count_above_average(data, avg):
    count = 0
    for x in data:
        if x > avg:
            count += 1
    return count

def calculate_median(data):
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2

def grade_distribution(data):
    grades = {"A": 0, "B": 0, "C": 0, "FAIL": 0}
    
    for mark in data:
        if mark >= 90:
            grades["A"] += 1
        elif mark >= 75:
            grades["B"] += 1
        elif mark >= 50:
            grades["C"] += 1
        else:
            grades["FAIL"] += 1
    
    return grades

def performance_summary(avg):
    if avg >= 90:
        return "Excellent Performance"
    elif avg >= 75:
        return "Good Performance"
    elif avg >= 50:
        return "Average Performance"
    else:
        return "Needs Improvement"

# ----------- Main Program -----------

marks = [78, 85, 90, 67, 85, 92, 78]   # ✅ Keep this as list

avg = calculate_average(marks)         # ✅ Store average separately
low, high = find_min_max(marks)
above_avg = count_above_average(marks, avg)
median = calculate_median(marks)
grades = grade_distribution(marks)
summary = performance_summary(avg)

# ----------- Output -----------

print("📊 STUDENT SCORE ANALYZER")
print("-" * 35)

print("Marks:", marks)
print("Average Score:", round(avg, 2))
print("Median Score:", median)
print("Highest Score:", high)
print("Lowest Score:", low)
print("Students Above Average:", above_avg)

print("\n📈 Grade Distribution:")
for grade, count in grades.items():
    print(grade, ":", count)

print("\n📌 Performance Summary:")
print(summary)