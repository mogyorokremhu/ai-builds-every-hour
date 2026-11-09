#!/usr/bin/env python3
"""sum_of_squares - write n as a sum of two squares (Fermat) or four (Lagrange).

  python3 sum_of_squares.py 65
"""
import sys
from math import isqrt


def two(n):
    return [(a, isqrt(n - a * a)) for a in range(isqrt(n // 2) + 1)
            if isqrt(n - a * a) ** 2 == n - a * a]


def four(n):
    for a in range(isqrt(n) + 1):
        for b in range(a, isqrt(n - a * a) + 1):
            for c in range(b, isqrt(n - a * a - b * b) + 1):
                d2 = n - a * a - b * b - c * c
                d = isqrt(d2)
                if d >= c and d * d == d2:
                    return (a, b, c, d)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 65
    print("two squares:", two(n) or "none")
    print("four squares:", four(n))
