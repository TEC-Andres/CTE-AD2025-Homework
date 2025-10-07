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

        // Use stack memory via std::vector
        std::vector<double> A11(quadrantSize);
        std::vector<double> A12(quadrantSize);
        std::vector<double> A21(quadrantSize);
        std::vector<double> A22(quadrantSize);
        std::vector<double> B11(quadrantSize);
        std::vector<double> B12(quadrantSize);
        std::vector<double> B21(quadrantSize);
        std::vector<double> B22(quadrantSize);
        std::vector<double> M1(quadrantSize);
        std::vector<double> M2(quadrantSize);
        std::vector<double> M3(quadrantSize);
        std::vector<double> M4(quadrantSize);
        std::vector<double> M5(quadrantSize);
        std::vector<double> M6(quadrantSize);
        std::vector<double> M7(quadrantSize);
        std::vector<double> temp1(quadrantSize);
        std::vector<double> temp2(quadrantSize);

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
        addMatrix(A11.data(), A22.data(), temp1.data(), newSize);
        addMatrix(B11.data(), B22.data(), temp2.data(), newSize);
        strassenMultiply(temp1.data(), temp2.data(), M1.data(), newSize);

        // Calculate M2 = (A21 + A22) * B11
        addMatrix(A21.data(), A22.data(), temp1.data(), newSize);
        strassenMultiply(temp1.data(), B11.data(), M2.data(), newSize);

        // Calculate M3 = A11 * (B12 - B22)
        subtractMatrix(B12.data(), B22.data(), temp2.data(), newSize);
        strassenMultiply(A11.data(), temp2.data(), M3.data(), newSize);

        // Calculate M4 = A22 * (B21 - B11)
        subtractMatrix(B21.data(), B11.data(), temp2.data(), newSize);
        strassenMultiply(A22.data(), temp2.data(), M4.data(), newSize);

        // Calculate M5 = (A11 + A12) * B22
        addMatrix(A11.data(), A12.data(), temp1.data(), newSize);
        strassenMultiply(temp1.data(), B22.data(), M5.data(), newSize);

        // Calculate M6 = (A21 - A11) * (B11 + B12)
        subtractMatrix(A21.data(), A11.data(), temp1.data(), newSize);
        addMatrix(B11.data(), B12.data(), temp2.data(), newSize);
        strassenMultiply(temp1.data(), temp2.data(), M6.data(), newSize);

        // Calculate M7 = (A12 - A22) * (B21 + B22)
        subtractMatrix(A12.data(), A22.data(), temp1.data(), newSize);
        addMatrix(B21.data(), B22.data(), temp2.data(), newSize);
        strassenMultiply(temp1.data(), temp2.data(), M7.data(), newSize);

        // Calculate result quadrants
        for (int i = 0; i < newSize; i++) {
            for (int j = 0; j < newSize; j++) {
                int idx = i * newSize + j;

                C[i * n + j] = M1[idx] + M4[idx] - M5[idx] + M7[idx];
                C[i * n + j + newSize] = M3[idx] + M5[idx];
                C[(i + newSize) * n + j] = M2[idx] + M4[idx];
                C[(i + newSize) * n + j + newSize] = M1[idx] - M2[idx] + M3[idx] + M6[idx];
            }
        }
    }

    // Main function to be called from Python
    void strassen(double* A, double* B, double* C, int n) {
        strassenMultiply(A, B, C, n);
    }
}
