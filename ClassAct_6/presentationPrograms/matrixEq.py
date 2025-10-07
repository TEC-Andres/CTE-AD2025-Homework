import random
import time
from src.matrixmult import save_matrix
import os 

def matrix_multiply(A, B):
    """
    Multiplies two matrices A and B using the standard O(n^3) algorithm.
    A: m x n matrix (list of lists)
    B: n x p matrix (list of lists)
    Returns: m x p matrix (list of lists)
    """
    m = len(A)
    n = len(A[0])
    p = len(B[0])
    # Initialize result matrix with zeros
    result = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

# Example usage:
if __name__ == "__main__":
    n = 400
    mat1 = [[random.randint(0, 20) for _ in range(n)] for _ in range(n)]
    mat2 = [[random.randint(0, 20) for _ in range(n)] for _ in range(n)]

    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_results')
    os.makedirs(results_dir, exist_ok=True)
    save_matrix(mat1, os.path.join(results_dir, 'A.txt'))
    save_matrix(mat2, os.path.join(results_dir, 'B.txt'))

    start_time = time.time()
    C = matrix_multiply(mat1, mat2)
    end_time = time.time()
    print(f"Time taken for matrix multiplication: {end_time - start_time} seconds")
    save_matrix(C, os.path.join(results_dir, '_AxB.txt'))
