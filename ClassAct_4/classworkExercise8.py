'''
#       Sesion 4: For and while loops
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: classworkExercise8.py
#
#       Created:                09/05/2025
#       Last Modified:          09/05/2025
'''
# O(n^2) solution
def is_prime(num):
    # Base case for 2
    if num == 2:
        return 1
    # Loops through all numbers that are divisible by any number other than 1 and itself
    for i in range(2, num):
        if num % i == 0:
            return 0
    return 1

def count_up_to_n_prime(num):
    count = 0
    # Loops through all numbers up to num
    for i in range(2, num+1):
        # If it's prime, add to count
        if (is_prime(i) == 1):
            count += 1
    return count

# If name main method to initialize program
if __name__ == "__main__":
    a = int(input("Enter N: "))
    print(f"Primes up to {a}: {count_up_to_n_prime(a)}")