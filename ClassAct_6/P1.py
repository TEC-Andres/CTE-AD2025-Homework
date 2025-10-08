while True:
    n = int(input("How many elements do you want in the list? "))
    if n > 0:
        break
    else:
        print("Please enter a number greater than 0.")

list_a = []
for i in range(n):
    element = input(f"Enter element #{i+1}: ")
    list_a.append(element)

for i, element in enumerate(list_a):
    print(f"list_a[{i}] = {element}")