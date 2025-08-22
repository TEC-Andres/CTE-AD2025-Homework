'''
#       Sesion 2: Introductory Activity
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork4.py
#
#       Created:                08/22/2025
#       Last Modified:          08/22/2025
'''
age = int(input("How old are you? "))
if age >= 18:
    print("You are an adult.")
elif age < 0:
    print("Age cannot be negative.")
else:
    print("You are a minor.")