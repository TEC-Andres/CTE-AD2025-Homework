'''
#       Sesion 3: Functions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork6.py
#
#       Created:                08/29/2025
#       Last Modified:          08/29/2025
'''
def getName(name):
    return name.upper(), name.title(), '. '.join([word[0].upper() for word in name.split() if word]) + '.'

name = input("Enter your name: ")
print('\n'.join(getName(name)))