'''
#       Sesion 3: Functions
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classwork4.py
#
#       Created:                08/26/2025
#       Last Modified:          08/26/2025
'''
def get_favorite_color():
    return input("What is your favorite color? ")

def show_message():
    color = get_favorite_color()
    print(f"Nice choice! {color} is a beautiful color.")

def main():
    print("Welcome to the color app!")
    show_message()

main()