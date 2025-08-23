'''
#       Sesion 2: Programs that make decisions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: exercise3.py
#       Title: Triangle Classifier (validity, side type, angle type)
#
#       Created:                08/22/2025
#       Last Modified:          08/23/2025
'''
# Inputs
a = float(input("Enter side a: "))
b = float(input("Enter side b: "))
c = float(input("Enter side c: "))

# Output strings
triangleType = ""
angleType = ""

if {a,b,c} == {abs(a),abs(b),abs(c)}:
    pass
else:
    raise Exception("Invalid triangle sides; please try with positive values.")

# Check for the type of triangle
if a != b and b != c and a != c:
    triangleType = "Scalene"
elif a == b or b == c or a == c:
    triangleType = "Isosceles"
else:
    triangleType = "Equilateral"

# Check angle type
if a**2 + b**2 > c**2:
    angleType = "Acute"
elif a**2 + b**2 < c**2:
    angleType = "Obtuse"
else:
    angleType = "Right"

# Print results to the console
print(f"{triangleType} and {angleType} triangle.")