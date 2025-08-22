age = int(input("How old are you? "))
if age >= 18:
    print("You are an adult.")
elif age < 0:
    print("Age cannot be negative.")
else:
    print("You are a minor.")