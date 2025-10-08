'''
#       Sesion 6: For and while loops
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classworkExercise7.py
#
#       Created:                10/03/2025
#       Last Modified:          10/03/2025
'''
matrix_val = []
below_max = []
max_val = int(input("Maximum value: "))
num_rows = int(input("Number of rows: "))
num_cols = int(input("Number of columns: "))

for i in range(num_rows):
    matrix_val.append([0] * num_cols)

for i in range(num_rows):
    for j in range(num_cols):
        matrix_val[i][j] = int(input(f"Enter the value for row {i+1}, column {j+1}: "))

def to_list(matrix, max_value):
    result = []
    for row in matrix:
        for val in row:
            if val <= max_value:
                result.append(val)
    return result

below_max = to_list(matrix_val, max_val)
print(f"A list of numbers that are less than the given maximum value: {below_max}")