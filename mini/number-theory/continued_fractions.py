"""Continued fractions: expansion, convergents, and sqrt(n) periods."""
import math
import sys
from fractions import Fraction


def expand(fr: Fraction) -> list:
    out = []
    a, b = fr.numerator, fr.denominator
    while b:
        out.append(a // b)
        a, b = b, a % b
    return out


def convergents(terms: list) -> list:
    h0, h1, k0, k1 = 0, 1, 1, 0
    res = []
    for a in terms:
        h0, h1 = h1, a * h1 + h0
        k0, k1 = k1, a * k1 + k0
        res.append(Fraction(h1, k1))
    return res


def sqrt_cf(n: int):
    """Return (a0, period) for sqrt(n); period empty if n is square."""
    a0 = math.isqrt(n)
    if a0 * a0 == n:
        return a0, []
    m, d, a, period = 0, 1, a0, []
    while True:
        m = d * a - m
        d = (n - m * m) // d
        a = (a0 + m) // d
        period.append(a)
        if a == 2 * a0:
            return a0, period


if __name__ == "__main__":
    print("355/113 ->", expand(Fraction(355, 113)))
    print("convergents of 3.14159265:", [str(c) for c in convergents(expand(Fraction("3.14159265")))[:6]])
    for n in (2, 7, 13, 61):
        a0, per = sqrt_cf(n)
        print(f"sqrt({n}) = [{a0}; {per}]")
