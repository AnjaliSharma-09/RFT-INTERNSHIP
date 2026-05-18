# =====================================
# CSV READER PROJECT
# WITHOUT USING PANDAS
# =====================================

# CSV File Name
file_name = "students.csv"

# Empty List
students = []

try:

    # Open CSV File
    with open(file_name, "r") as file:

        # Read all lines
        lines = file.readlines()

        # Skip Header Line
        for line in lines[1:]:

            # Remove newline/spaces
            line = line.strip()

            # Skip empty lines
            if line == "":
                continue

            # Split line using comma
            data = line.split(",")

            # Store values
            name = data[0]
            age = int(data[1])
            marks = int(data[2])

            # Create Dictionary
            student = {
                "NAME": name,
                "AGE": age,
                "MARKS": marks
            }

            # Add Dictionary into List
            students.append(student)

    # =====================================
    # DISPLAY STUDENT RECORDS
    # =====================================

    print("\nSTUDENT RECORDS\n")

    for student in students:
        print(student)

    # =====================================
    # TOTAL & AVERAGE
    # =====================================

    total_marks = 0

    for student in students:
        total_marks += student["MARKS"]

    average = total_marks / len(students)

    print("\nTotal Marks :", total_marks)
    print("Average Marks :", average)

    # =====================================
    # FIND TOPPER
    # =====================================

    topper = students[0]

    for student in students:

        if student["MARKS"] > topper["MARKS"]:
            topper = student

    print("\nTOPPER DETAILS")
    print("Name :", topper["NAME"])
    print("Marks :", topper["MARKS"])

except FileNotFoundError:
    print("CSV File Not Found!")

except Exception as e:
    print("Error:", e)