'''
#       Sesion 3: Functions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: challenge.py
#
#       Created:                08/29/2025
#       Last Modified:          08/29/2025
'''    
import cmath

# Constant
b = 30

# Input
height_of_table = float(input("Enter the height of the table in cm: "))
h_elbow = float(input("Enter the height of the elbow in cm: "))
c = float(input("Enter the value of delta2 in cm: "))
deltaQ = h_elbow - height_of_table

# Check whether we are under the table
if deltaQ < 0:
    c = deltaQ+c

# Funny part
A = cmath.asin((c/2)/(b))*2 * (180/cmath.pi)
a = cmath.sqrt(b**2 + c**2-2*b*c - cmath.cos(A))
C = abs(cmath.asin((c*cmath.sin(A))/(a)).real * (180/cmath.pi))

if __name__ == "__main__":
    print(f"The angle C is: {C}")