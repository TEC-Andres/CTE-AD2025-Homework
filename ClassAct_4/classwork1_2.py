odd,even = 0,0
while True:
    a = int(input("Enter a number (0 to stop): ")) 
    if a == 0:
        break
    if a % 2 == 0:
        even += 1
    else:
        odd += 1
print(f"Total odd: {odd}")
print(f"Total even: {even}")