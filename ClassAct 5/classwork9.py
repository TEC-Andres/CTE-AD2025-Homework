fruits = ["apple", "banana", "cherry", "orange", "grape"]

def color_of_fruit(fruit):
    if fruit == "apple" or fruit == "cherry":
        return "red"
    elif fruit == "banana" or fruit == "orange":
        return "yellow"
    elif fruit == "grape":
        return "purple"
    else:
        return "unknown"


print("Checking if the fruits are red or not:")
for fruit in fruits:
    color = color_of_fruit(fruit)
    
    if color == "red":
        print(f"{fruit} is red")
    else:
        print(f"{fruit} is not red")