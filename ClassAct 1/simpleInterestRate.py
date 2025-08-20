'''
#       Sesion 1: Programs that require calculations
#       Andrés Rodríguez Cantú ─ A01287002
#
#       Copyright (C) Tecnológico de Monterrey
#
#       File: simpleInterestRate.py
#
#       Created:                08/19/2025
#       Last Modified:          08/19/2025
'''
def simpleInterestRate(principal, rate, time):
    return (principal * rate * time) / 100

principal = float(input("Enter the principal amount: "))
rate = float(input("Enter the rate of interest: "))
time = float(input("Enter the time (in years): "))
result = simpleInterestRate(principal, rate, time)

print(f"The simple interest is: {result}")
print(f"The total amount after interest is: {result + principal}")
print(f"Total amount of months: {time * 12}")
print(f"Monthly interest: {result / (time * 12)}")