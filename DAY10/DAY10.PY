# Sample Logs
logs = [
    "ERROR Disk Full",
    "INFO System Started",
    "ERROR File Missing",
    "WARNING Memory Low",
    "INFO User Logged In",
    "WARNING CPU Temperature High",
    "ERROR Network Failure",
    "info Backup Completed"
]

# Dictionary to store log counts
log_count = {}

# List to store detected log types
detected_logs = []

# Process each log
for log in logs:

    # Ignore case sensitivity
    log_upper = log.upper()

    # Extract first word as log type
    log_type = log_upper.split()[0]

    # Store detected log type
    detected_logs.append(log_type)

    # Count frequency
    if log_type in log_count:
        log_count[log_type] += 1
    else:
        log_count[log_type] = 1

print("=" * 40)
print("         LOG ANALYSIS REPORT")
print("=" * 40)

print("\nTotal Logs:", len(logs))

print("\nLog Type Counts:")
for key, value in log_count.items():
    print(f"{key:<10} : {value}")

# Most Frequent Log Type
most_frequent = max(log_count, key=log_count.get)

print("\nMost Frequent Log Type :", most_frequent)

# Percentage Analysis
print("\nLog Percentage Analysis:")
for key, value in log_count.items():
    percentage = (value / len(logs)) * 100
    print(f"{key:<10} : {percentage:.2f}%")

# Error Detection
print("\nCritical Error Logs:")
for log in logs:
    if "ERROR" in log.upper():
        print("->", log)

print("\nAnalysis Completed Successfully!")
print("=" * 40)