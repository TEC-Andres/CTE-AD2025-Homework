#include <vector>
#include <cstring>

extern "C" {
    // Helper function to add two matrices
    void addMatrix(double* A, double* B, double* C, int size) {
        for (int i = 0; i < size * size; i++) {
            C[i] = A[i] + B[i];
        }
    }

    // Helper function to subtract two matrices
    void subtractMatrix(double* A, double* B, double* C, int size) {
        for (int i = 0; i < size * size; i++) {
            C[i] = A[i] - B[i];
        }
    }

    // Standard matrix multiplication for base case
    void standardMultiply(double* A, double* B, double* C, int size) {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                C[i * size + j] = 0;
                for (int k = 0; k < size; k++) {
                    C[i * size + j] += A[i * size + k] * B[k * size + j];
                }
            }
        }
    }

    // Strassen's algorithm implementation
    void strassenMultiply(double* A, double* B, double* C, int n) {
        // Base case: use standard multiplication for small matrices
        if (n <= 64) {
            standardMultiply(A, B, C, n);
            return;
        }

        // Ensure n is even (Strassen requires power of 2, but we'll handle even numbers)
        if (n % 2 != 0) {
            standardMultiply(A, B, C, n);
            return;
        }

        int newSize = n / 2;
        int quadrantSize = newSize * newSize;

        // Allocate memory for submatrices and intermediate results
        double* A11 = new double[quadrantSize];
        double* A12 = new double[quadrantSize];
        double* A21 = new double[quadrantSize];
        double* A22 = new double[quadrantSize];
        
        double* B11 = new double[quadrantSize];
        double* B12 = new double[quadrantSize];
        double* B21 = new double[quadrantSize];
        double* B22 = new double[quadrantSize];
        
        double* M1 = new double[quadrantSize];
        double* M2 = new double[quadrantSize];
        double* M3 = new double[quadrantSize];
        double* M4 = new double[quadrantSize];
        double* M5 = new double[quadrantSize];
        double* M6 = new double[quadrantSize];
        double* M7 = new double[quadrantSize];
        
        double* temp1 = new double[quadrantSize];
        double* temp2 = new double[quadrantSize];

        // Divide matrices into quadrants
        for (int i = 0; i < newSize; i++) {
            for (int j = 0; j < newSize; j++) {
                int idx = i * newSize + j;
                
                A11[idx] = A[i * n + j];
                A12[idx] = A[i * n + j + newSize];
                A21[idx] = A[(i + newSize) * n + j];
                A22[idx] = A[(i + newSize) * n + j + newSize];
                
                B11[idx] = B[i * n + j];
                B12[idx] = B[i * n + j + newSize];
                B21[idx] = B[(i + newSize) * n + j];
                B22[idx] = B[(i + newSize) * n + j + newSize];
            }
        }

        // Calculate M1 = (A11 + A22) * (B11 + B22)
        addMatrix(A11, A22, temp1, newSize);
        addMatrix(B11, B22, temp2, newSize);
        strassenMultiply(temp1, temp2, M1, newSize);

        // Calculate M2 = (A21 + A22) * B11
        addMatrix(A21, A22, temp1, newSize);
        strassenMultiply(temp1, B11, M2, newSize);

        // Calculate M3 = A11 * (B12 - B22)
        subtractMatrix(B12, B22, temp2, newSize);
        strassenMultiply(A11, temp2, M3, newSize);

        // Calculate M4 = A22 * (B21 - B11)
        subtractMatrix(B21, B11, temp2, newSize);
        strassenMultiply(A22, temp2, M4, newSize);

        // Calculate M5 = (A11 + A12) * B22
        addMatrix(A11, A12, temp1, newSize);
        strassenMultiply(temp1, B22, M5, newSize);

        // Calculate M6 = (A21 - A11) * (B11 + B12)
        subtractMatrix(A21, A11, temp1, newSize);
        addMatrix(B11, B12, temp2, newSize);
        strassenMultiply(temp1, temp2, M6, newSize);

        // Calculate M7 = (A12 - A22) * (B21 + B22)
        subtractMatrix(A12, A22, temp1, newSize);
        addMatrix(B21, B22, temp2, newSize);
        strassenMultiply(temp1, temp2, M7, newSize);

        // Calculate result quadrants
        // C11 = M1 + M4 - M5 + M7
        // C12 = M3 + M5
        // C21 = M2 + M4
        // C22 = M1 - M2 + M3 + M6

        for (int i = 0; i < newSize; i++) {
            for (int j = 0; j < newSize; j++) {
                int idx = i * newSize + j;
                
                C[i * n + j] = M1[idx] + M4[idx] - M5[idx] + M7[idx];
                C[i * n + j + newSize] = M3[idx] + M5[idx];
                C[(i + newSize) * n + j] = M2[idx] + M4[idx];
                C[(i + newSize) * n + j + newSize] = M1[idx] - M2[idx] + M3[idx] + M6[idx];
            }
        }

        // Free allocated memory
        delete[] A11; delete[] A12; delete[] A21; delete[] A22;
        delete[] B11; delete[] B12; delete[] B21; delete[] B22;
        delete[] M1; delete[] M2; delete[] M3; delete[] M4;
        delete[] M5; delete[] M6; delete[] M7;
        delete[] temp1; delete[] temp2;
    }

    // Main function to be called from Python
    void strassen(double* A, double* B, double* C, int n) {
        strassenMultiply(A, B, C, n);
    }
}   