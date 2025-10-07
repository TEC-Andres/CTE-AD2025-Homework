'''
#       Sesion 3: Functions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork3.py
#
#       Created:                08/26/2025
#       Last Modified:          08/26/2025
'''
# Function that recieves height and base to calculate the triangle area
def areaTri(base, height):
    area = (base * height) / 2
    print(f"The area of the triangle with height {height} and base {base} is: {area}")

# Ask the user for the values
a = int(input("Enter the base of the triangle: "))
b = int(input("Enter the height of the triangle: "))

# Calling the function
areaTri(a, b)