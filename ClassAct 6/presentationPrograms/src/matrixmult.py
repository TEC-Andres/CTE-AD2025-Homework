import ctypes
import os
import random
import time

# Load the shared library
# First compile the C++ file:
# On Windows: g++ -shared -o matrixEq.dll -fPIC -static-libgcc -static-libstdc++ matrixEq.cpp
# On Linux: g++ -shared -o matrixEq.so -fPIC matrixEq.cpp

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(script_dir, "..", "bin")

# Try to load the appropriate library
try:
    if os.name == 'nt':  # Windows
        lib_path = os.path.join(script_dir, 'matrixEq.dll')
        lib = ctypes.CDLL(lib_path)
    else:
        lib_path = os.path.join(script_dir, 'matrixEq.so')
        print(f"[DEBUG] Attempting to load SO at: {lib_path}")
        lib = ctypes.CDLL(lib_path)
except OSError as e:
    print(f"[ERROR] Could not load shared library at: {lib_path}")
    print(f"OSError: {e}")
    print("On Windows: g++ -shared -o matrixEq.dll -fPIC -static-libgcc -static-libstdc++ matrixEq.cpp")
    print("On Linux/Mac: g++ -shared -o matrixEq.so -fPIC matrixEq.cpp")
    exit(1)

lib.strassen.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_int
]
lib.strassen.restype = None

def strassen_multiply(A, B):
    """
    Multiply two square matrices using Strassen's algorithm via C++.

    Args:
        A: First matrix (2D list)
        B: Second matrix (2D list)

    Returns:
        Result matrix as 2D list
    """
    n = len(A)
    if n == 0 or n != len(A[0]) or n != len(B) or n != len(B[0]):
        raise ValueError("Both matrices must be non-empty, square, and of the same dimensions.")

    # Flatten matrices using list comprehension for efficiency
    A_flat = [float(x) for row in A for x in row]
    B_flat = [float(x) for row in B for x in row]

    # Create ctypes arrays
    A_array = (ctypes.c_double * (n * n))(*A_flat)
    B_array = (ctypes.c_double * (n * n))(*B_flat)
    C_array = (ctypes.c_double * (n * n))()

    # Call the C++ function
    lib.strassen(A_array, B_array, C_array, n)

    # Convert result back to 2D list using list comprehension
    return [list(C_array[i * n:(i + 1) * n]) for i in range(n)]


def save_matrix(matrix, filename):
    with open(filename, 'w') as f:
        for row in matrix:
            f.write('	'.join(f"{num}" for num in row) + '\n')