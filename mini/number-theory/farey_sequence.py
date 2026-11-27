"""Farey sequences F_n and the neighbor property (python farey_sequence.py 7)."""
import sys
from fractions import Fraction


def farey(n: int) -> list[Fraction]:
    """All reduced fractions in [0, 1] with denominator <= n, via the next-term recurrence."""
    a, b, c, d = 0, 1, 1, n
    out = [Fraction(a, b)]
    while c <= n:
        k = (n + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        out.append(Fraction(a, b))
    return out


def neighbors_ok(seq: list[Fraction]) -> bool:
    """Adjacent terms p/q, r/s always satisfy r*q - p*s == 1."""
    return all(y.numerator * x.denominator - x.numerator * y.denominator == 1
               for x, y in zip(seq, seq[1:]))


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    f = farey(n)
    print(f"F_{n} has {len(f)} terms:")
    print(" ".join(str(x) for x in f))
    print("neighbor determinant property:", neighbors_ok(f))
