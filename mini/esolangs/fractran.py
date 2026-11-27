"""FRACTRAN interpreter (Conway). Usage: python fractran.py  -> runs Conway's prime generator and an adder."""
from fractions import Fraction
from typing import Iterator

PRIMES = [Fraction(n, d) for n, d in (
    (17, 91), (78, 85), (19, 51), (23, 38), (29, 33), (77, 29), (95, 23),
    (77, 19), (1, 17), (11, 13), (13, 11), (15, 14), (15, 2), (55, 1))]


def run(program: list[Fraction], n: int, limit: int = 10**6) -> Iterator[int]:
    """Yield successive values of n until no fraction applies."""
    for _ in range(limit):
        yield n
        for f in program:
            m = n * f
            if m.denominator == 1:
                n = int(m)
                break
        else:
            return


def primes(count: int) -> list[int]:
    found = []
    for n in run(PRIMES, 2, 10**7):
        if n & (n - 1) == 0 and n > 2:  # power of two 2^k with k prime
            found.append(n.bit_length() - 1)
            if len(found) == count:
                break
    return found


def add(a: int, b: int) -> int:
    """2^a * 3^b -> 2^(a+b) using the single fraction 2/3."""
    *_, last = run([Fraction(2, 3)], 2**a * 3**b)
    return last.bit_length() - 1


if __name__ == "__main__":
    print("primes:", primes(8))
    print("3 + 4 =", add(3, 4))
