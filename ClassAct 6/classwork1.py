'''
#       Sesion 6: Lists
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork6.py
#
#       Created:                09/23/2025
#       Last Modified:          09/23/2025
'''
item = [
    "cheese", 
    "tortilla", 
    "tomato", 
    "lettuce", 
    "kg of beef", 
    "kg of chicken"
]

stock = [10, 10, 5, 10, 2, 10]
selectedItems = []
selectedQuantity = []

while(True):
    print("Available items:")
    for i in range(len(item)):
        print(f"{item[i]} - Stock: {stock[i]}")
    print("\n")
    action = input("What action would you like to take?: ").lower().strip()

    if action == "exit":
        break
    elif action == "add":
        a = input("Select an item: ").lower().strip()
        if a not in item:
            print("Item not found.\n")
        else:
            index = item.index(a)
            selectedItems.append(item[index])
            quantity = int(input("Enter quantity: "))
            if quantity > stock[index]:
                print("Insufficient stock.\n")
            else:
                selectedQuantity.append(quantity)
                stock[index] -= quantity
                print("Item added to cart.\n")
    elif action == "remove":
        a = input("Select an item to remove: ").lower().strip()
        if a not in selectedItems:
            print("Item not in cart.\n")
        else:
            while a in selectedItems:
                index = selectedItems.index(a)
                stock[item.index(a)] += selectedQuantity[index]
                selectedItems.pop(index)
                selectedQuantity.pop(index)
            print("Item removed from cart.\n")
    else:
        print("Invalid action. Please choose 'add', 'remove', or 'exit'.")
    
# Checa por duplicados; si existen, suma las cantidades
for i in range(len(selectedItems)):
    for j in range(i + 1, len(selectedItems)):
        if selectedItems[i] == selectedItems[j]:
            selectedQuantity[i] += selectedQuantity[j]
            selectedItems.pop(j)
            selectedQuantity.pop(j)
            break

print("Your cart:")
for i in range(len(selectedItems)):
    print(f"{selectedItems[i]}: {selectedQuantity[i]}")