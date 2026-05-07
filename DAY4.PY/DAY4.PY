def analyze_logs(logs):

    log_count = {
        "ERROR": 0,
        "INFO": 0,
        "WARNING": 0
    }

    for log in logs:
        log = log.upper()

        for log_type in log_count:
            if log_type in log:
                log_count[log_type] += 1

    print("===== LOG ANALYZER REPORT =====")

    for key, value in log_count.items():
        print(f"{key} COUNT : {value}")

    most_frequent = max(log_count, key=log_count.get)

    print("\nMost Frequent Log Type :", most_frequent)


# Sample Logs
logs = [
    "ERROR DISK FULL",
    "info started",
    "Error File Missing",
    "WARNING MEMORY LOW"
]

analyze_logs(logs)