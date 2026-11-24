"""Pollard's rho factorisation with a Miller-Rabin primality check."""
import math
import random
import sys


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    while True:
        c = random.randrange(1, n)
        x = y = random.randrange(0, n)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d


def factor(n: int) -> list:
    if n == 1:
        return []
    if is_prime(n):
        return [n]
    d = rho(n)
    return sorted(factor(d) + factor(n // d))


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 600851475143 * 1000003
    print(n, "=", " x ".join(map(str, factor(n))))
