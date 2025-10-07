#!/usr/bin/env python3
"""
Large prime generator.

Generates a prime with the requested number of decimal digits.
Uses Miller-Rabin probabilistic primality test with k rounds (default 25).

Example: generate a 500-digit prime:
    prime = generate_large_prime(500)
    print(prime)
"""

import secrets

def is_probable_prime(n: int, k: int = 25) -> bool:
    """Miller-Rabin primality test (probabilistic).
    n: integer to test (n >= 2)
    k: number of rounds (higher -> lower error probability)
    Returns True if n is very likely prime, False if composite.
    """
    if n < 2:
        return False
    # small primes quick check
    small_primes = (2,3,5,7,11,13,17,19,23,29)
    for p in small_primes:
        if n % p == 0:
            return n == p

    # write n-1 as d * 2^s with d odd
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # witness loop
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # random in [2, n-2]
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(digits: int = 500, k: int = 25) -> int:
    """Generate a prime number with the specified number of decimal digits.
    digits: number of decimal digits (>=1)
    k: Miller-Rabin rounds passed to is_probable_prime
    """
    if digits < 1:
        raise ValueError("digits must be >= 1")

    low = 10**(digits - 1)
    high = 10**digits - 1

    # Precompute a modulus to avoid trivial divisibility by 2 or 5
    # We'll loop until we find a candidate that passes MR test.
    while True:
        # create a random number in [low, high]
        # choose uniformly: secrets.randbelow(high - low + 1) + low
        candidate = secrets.randbelow(high - low + 1) + low

        # ensure it's odd and not divisible by 5
        if candidate % 2 == 0:
            candidate += 1
        # if %5==0, add 2 (this preserves oddness)
        if candidate % 5 == 0:
            candidate += 2

        # It's possible the increment pushed candidate > high, so wrap:
        if candidate > high:
            candidate = low + (candidate - high - 1)

        # Quick small-prime sieve: skip candidates divisible by small primes
        # (reduces Miller-Rabin calls)
        small_primes = (3,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)
        for p in small_primes:
            if candidate % p == 0 and candidate != p:
                break
        else:
            # run Miller-Rabin
            if is_probable_prime(candidate, k=k):
                return candidate
        # otherwise try next odd candidate
        candidate += 2
        if candidate > high:
            candidate = low + (candidate - high - 1)

if __name__ == "__main__":
    # Example usage: generate and print a 500-digit prime
    digits = 500
    print(f"Generating a {digits}-digit prime (this may take a while)...")
    prime = generate_large_prime(digits=digits, k=25)
    print("Done.\n")
    print(prime)
