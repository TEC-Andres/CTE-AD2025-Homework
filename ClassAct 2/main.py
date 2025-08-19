'''
#       Sesion 2: Introductory Activity
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: main.py
#
#       Created:                08/19/2025
#       Last Modified:          08/19/2025
'''
# Inport math module
import math

# Get the legs lengths
a = float(input("Enter the first coefficient: "))
b = float(input("Enter the second coefficient: "))
c = float(input("Enter the third coefficient: "))

# Define s to prevent messy implementation
s = (a+b+c)/2

# Return to user the area of the triangle
print(math.sqrt(s*(s-a)*(s-b)*(s-c)))
