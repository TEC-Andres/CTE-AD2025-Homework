'''
#       Sesion 2: Introductory Activity
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: part2_exc1.py
#
#       Created:                08/19/2025
#       Last Modified:          08/19/2025
'''
# Import necesarry libraries
import cmath

# Get coefficients
a = float(input("Enter the first coefficient: "))
b = float(input("Enter the second coefficient: "))
c = float(input("Enter the third coefficient: "))

# Get results
posResult = (-b+cmath.sqrt(b**2-4*a*c))/(2*a)   
negResult = (-b-cmath.sqrt(b**2-4*a*c))/(2*a)

# All of the things the problem is asking us
print(f"Root 1: {posResult}")
print(f"Root 2: {negResult}")
print(f"Sum of roots: {posResult + negResult}")
print(f"Product of roots: {posResult * negResult}")
print(f"Magnitude of Root 1: {abs(posResult):.4f}")
print(f"Magnitude of Root 2: {abs(negResult):.4f}")