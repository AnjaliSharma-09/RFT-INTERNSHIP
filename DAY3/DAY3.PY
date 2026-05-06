def phonebook_app():
    # Initialize the phonebook with the provided data
    phonebook = {
        "AMIT": "9876543210",
        "RIYA": "9123456780"
    }

    while True:
        print("\n--- Dictionary-Based Phonebook ---")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Delete Contact")
        print("4. Display All")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ")

        if choice == '1':
            # Feature: Add Contact & Bonus: Prevent Duplicate Entries
            name = input("Enter Name: ").upper()
            if name in phonebook:
                print(f"Error: {name} already exists.")
            else:
                number = input("Enter Phone Number: ")
                phonebook[name] = number
                print("Contact added successfully!")

        elif choice == '2':
            # Feature: Search Contact & Bonus: Partial Name Search
            query = input("Enter name to search: ").upper()
            results = {k: v for k, v in phonebook.items() if query in k}
            
            if results:
                print("\nResults found:")
                for name, num in results.items():
                    print(f"{name}: {num}")
            else:
                print("No matching contacts found.")

        elif choice == '3':
            # Feature: Delete Contact
            name = input("Enter name to delete: ").upper()
            if name in phonebook:
                del phonebook[name]
                print(f"Contact {name} deleted.")
            else:
                print("Contact not found.")

        elif choice == '4':
            print("\n--- Current Phonebook ---")
            for name, num in phonebook.items():
                print(f"{name}: {num}")

        elif choice == '5':
            print("Exiting Phonebook. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

# Run the task
phonebook_app()