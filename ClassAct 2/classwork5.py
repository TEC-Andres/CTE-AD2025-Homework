'''
#       Sesion 2: Programs that make decisions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork5.py
#
#       Created:                08/22/2025
#       Last Modified:          08/23/2025
'''
age = int(input("How old are you? "))
if age >= 18:
    print("You are an adult.")
elif age < 0:
    print("Age cannot be negative.")
else:
    print("You are a minor.")