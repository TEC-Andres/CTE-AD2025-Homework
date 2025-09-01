from decimal import getcontext, Decimal

getcontext().prec = 1000

def chudnovsky_pi():
    C = 426880 * Decimal(10005).sqrt()
    K = 6
    M = 1
    X = 1
    L = 13591409
    S = L
    for i in range(1, 100000):
        M = (M * (K ** 3 - 16 * K)) // (i ** 3)
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12
    pi = C / S
    return pi

print(chudnovsky_pi())