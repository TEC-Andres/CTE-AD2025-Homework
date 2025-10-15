'''
#       Sesion 7: Strings and lists
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: p1.py
#
#       Created:                10/14/2025
#       Last Modified:          10/14/2025
'''

a = input("Place a word here: ")
b = input("Place another word here: ")

atemp = len(a); btemp = len(b)

if atemp > btemp:
    print(a)
elif btemp > atemp:
    print(b)
elif atemp == btemp:
    print(a); print(b)
else:
    raise Exception("Unexpected condition encountered.")