'''
#       Sesion 3: Functions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork5.py
#
#       Created:                08/26/2025
#       Last Modified:          08/26/2025
'''
def calculate_area(width, height):
    return width * height

def main():
    print("Rectangle area calculator")
    w = float(input("Enter the width of the rectangle: "))
    h = float(input("Enter the height of the rectangle: "))
    area = calculate_area(w, h)
    print(f"The area of the rectangle is: {area}")

main()