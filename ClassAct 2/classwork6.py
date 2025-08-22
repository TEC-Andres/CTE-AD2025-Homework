'''
#       Sesion 2: Introductory Activity
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork6.py
#
#       Created:                08/22/2025
#       Last Modified:          08/22/2025
'''
# Menu presentation
print("Welcome to Bella Napoli Pizzeria")
print("Types of pizza:\n\t1- Vegetarian\n\t2- Non-Vegetarian")
pizza_type = int(input("Enter the number corresponding to the type of the pizza you want: "))

# Pizza selection
if pizza_type == 1:
    print("Vegetarian pizza ingredients:\n\t1- Pepper\n\t2- Tofu.")
    ingredient = int(input("Choose your ingredients: "))
    print("Vegetarian pizza with mozzarella, tomato, and", end=" ")
    if ingredient == 1:
        print("Pepper.")
    else:
        print("Tofu.")
else:
    print("Non-Vegetarian pizza ingredients:\n\t1- Pepperoni\n\t2- Ham.\n\t3- Salmon")
    ingredient = int(input("Choose your ingredients: "))
    print("Non-Vegetarian pizza with mozzarella, tomato, and", end=" ")
    if ingredient == 1:
        print("Pepperoni.")
    elif ingredient == 2:
        print("Ham.")
    else:
        print("Salmon.")