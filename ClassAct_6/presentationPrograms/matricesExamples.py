import random
import time
import os
from src.matrixmult import strassen_multiply, save_matrix

if __name__ == "__main__":
    n = 1000
    mat1 = [[random.randint(0, 20) for _ in range(n)] for _ in range(n)]
    mat2 = [[random.randint(0, 20) for _ in range(n)] for _ in range(n)]
    
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_results')
    os.makedirs(results_dir, exist_ok=True)
    save_matrix(mat1, os.path.join(results_dir, 'A.txt'))
    save_matrix(mat2, os.path.join(results_dir, 'B.txt'))
    
    start_time = time.time()
    result = strassen_multiply(mat1, mat2)
    elapsed_time = time.time() - start_time
    print(f"\nTime taken for multiplication: {elapsed_time:.4f} seconds")
    
    save_matrix(result, os.path.join(results_dir, '_AxB.txt'))