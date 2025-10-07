'''
#       Sesion 6: For and while loops
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classworkExercise1.py
#
#       Created:                10/03/2025
#       Last Modified:          10/03/2025
'''
def create_matrix_numbers(n):
    return [[i for j in range(n)] for i in range(n)]

def display_matrix(matrix):
    for row in matrix:
        print("  ".join(f"{val}" for val in row))


if __name__ == "__main__":
    n = int(input("Enter the size of the square matrix: "))
    matrix = create_matrix_numbers(n)
    display_matrix(matrix)