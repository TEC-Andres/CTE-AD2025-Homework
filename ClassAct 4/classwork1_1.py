count = 0
while True:
    a = int(input("Enter a number (-1 to stop): "))
    count += a
    if a == -1:
        break
print(f"Sum: {count}")