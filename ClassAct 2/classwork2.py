'''
#       Sesion 2: Programs that make decisions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork2.py
#
#       Created:                08/22/2025
#       Last Modified:          08/23/2025
'''
# Get the password of the user and compare it with the key
key = "password"
password = input("Enter the password: ")
if password == key:
    print("Access granted.")
else:
    print("Access denied.")
