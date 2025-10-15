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

replacements = {
    'á': 'a', 'ä': 'a', 'à': 'a', 'â': 'a', 'ã': 'a',
    'é': 'e', 'ë': 'e', 'è': 'e', 'ê': 'e',
    'í': 'i', 'ï': 'i', 'ì': 'i', 'î': 'i',
    'ó': 'o', 'ö': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o',
    'ú': 'u', 'ü': 'u', 'ù': 'u', 'û': 'u',
    'ñ': 'n', 'ç': 'c'
}

for k, v in replacements.items():
    a = a.replace(k, v)

b = a.replace('e', '3').replace('o', 'h').replace("a", "4")
    
print(b)