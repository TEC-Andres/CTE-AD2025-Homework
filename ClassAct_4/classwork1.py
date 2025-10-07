'''
#       Sesion 4: For and while loops
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork1.py
#
#       Created:                09/05/2025
#       Last Modified:          09/05/2025
'''
a = 0
evenCount = 0
total = 0
while(a != -1):
    a = int(input("Enter a number (-1 to stop): "))
    if(a != -1):
        print(f"You entered: {a}")
    total += a

    if (a % 2 == 0):
        evenCount += 1

print(f"Total even numbers: {evenCount}")
print(f"Total sum: {total}")