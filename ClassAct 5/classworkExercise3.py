def inspect_and_print(pw):
    hasDigit = "NO"
    hasLower = "NO"
    hasUpper = "NO"
    hasSpecial = "NO"
    for i in range(len(pw)):
        if pw[i].isdigit():
            hasDigit = "YES"
        elif pw[i].islower():
            hasLower = "YES"
        elif pw[i].isupper():
            hasUpper = "YES"
        elif not pw[i].isalnum():
            hasSpecial = "YES"
    print(f"Contains digit: {hasDigit}")
    print(f"Contains lowercase: {hasLower}")
    print(f"Contains uppercase: {hasUpper}")
    print(f"Contains special character: {hasSpecial}")

def run_pw_check():
    password = input("Enter password: ")
    inspect_and_print(password)

if __name__ == "__main__":
    run_pw_check()