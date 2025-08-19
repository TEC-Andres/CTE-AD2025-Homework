'''
#       Sesion 2: Introductory Activity
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: part1_exc1.py
#
#       Created:                08/19/2025
#       Last Modified:          08/19/2025
'''
import math
c = float(input("Enter the hypotenuse of the triangle in order to get the the opposite side (base of 30°): "))
print(f"The opposite side (base of 30°) is: {math.sin(math.radians(30)) * c:.5f}")