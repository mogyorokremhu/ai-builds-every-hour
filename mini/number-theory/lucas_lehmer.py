"""Lucas-Lehmer test: finds Mersenne primes 2^p - 1 (python lucas_lehmer.py 1300)."""
import sys


def is_prime_small(n: int) -> bool:
    """Trial-division primality for small exponents."""
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def lucas_lehmer(p: int) -> bool:
    """True if 2^p - 1 is prime (p must be an odd prime, or p == 2)."""
    if p == 2:
        return True
    m = (1 << p) - 1
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % m
    return s == 0


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1300
    found = [p for p in range(2, limit) if is_prime_small(p) and lucas_lehmer(p)]
    print("Mersenne exponents below", limit, ":", found)
    assert found[:8] == [2, 3, 5, 7, 13, 17, 19, 31]
    print("perfect numbers from them:", [(1 << (p - 1)) * ((1 << p) - 1) for p in found[:6]])
