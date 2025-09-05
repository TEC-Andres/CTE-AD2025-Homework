# Stored credentials
usernameStored = "admin"
passwordStored = "password123"

# Count remaining attempts. If failed, lock out after 3 attempts.
def print_feedback(remaining):
    if remaining > 0:
        print(f"Attempts left: {remaining}")
    else:
        print("Locked out.")

# Gives three attempts to login
def login_flow():
    attempts = 3
    # Attempt logic, only has three attempts
    while attempts > 0:
        username = input("Username: ")
        password = input("Password: ")
        if username == usernameStored and password == passwordStored:
            print("Access Granted!")
            break
        # If wrong (implicit else), substract one to attempts, print incorrect and do print_feedback function with the remaining attempts.
        attempts -= 1
        print("Incorrect")
        print_feedback(attempts)

# If name main method to initialize program
if __name__ == "__main__":
    login_flow()