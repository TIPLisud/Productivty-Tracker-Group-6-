users = {}


def create_account():
    print("\n--- Create Account ---")
    username = input("Enter username: ")

    if username in users:
        print("Username already exists!")
        return

    password = input("Enter password: ")
    users[username] = password
    print("Account created successfully!")


def login():
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username] == password:
        print("Login successful!")
        main_menu(username)
    else:
        print("Invalid username or password.")


def main_menu(current_user):
    while True:
        print(f"\n--- Main Menu (User: {current_user}) ---")
        print("1. View Projects")
        print("2. Create Project")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            print("No projects yet (placeholder).")

        elif choice == "2":
            print("Create project feature (placeholder).")

        elif choice == "3":
            print("Logging out...")
            break

        else:
            print("Invalid choice.")


while True:
    print("\nProductivity Tracker ")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        login()

    elif choice == "3":
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Try again.")
