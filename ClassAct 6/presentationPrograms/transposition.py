import random
def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]

if __name__ == "__main__":
    n = 200
    matrix = [[random.randint(0, 20) for _ in range(n)] for _ in range(n)]

    transposed = transpose_matrix(matrix)
    print("Original matrix:")
    for row in matrix:
        print(row)
    print("\nTransposed matrix:")
    for row in transposed:
        print(row)