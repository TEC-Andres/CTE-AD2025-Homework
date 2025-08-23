'''
#       Sesion 2: Programs that make decisions
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
r = float(input("Enter the radius of the circle we are trying to discuss: "))

a = math.pi * r**2
v = (4/3) * math.pi * r**3

print(f"The area of the circle is: {a:.5f}")
print(f"The volume of the sphere is: {v:.5f}")