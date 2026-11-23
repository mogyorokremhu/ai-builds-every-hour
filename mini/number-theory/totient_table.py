"""Euler's totient via a sieve, with a check against brute-force gcd counting."""
import sys
from math import gcd


def totients(limit: int) -> list[int]:
    """phi(n) for 0 <= n <= limit."""
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:  # p is prime
            for m in range(p, limit + 1, p):
                phi[m] -= phi[m] // p
    return phi


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    phi = totients(n)
    for k in range(1, n + 1):
        assert phi[k] == sum(1 for j in range(1, k + 1) if gcd(j, k) == 1)
    print(" ".join(f"phi({k})={phi[k]}" for k in range(1, n + 1)))
    print("sum phi(1..n) =", sum(phi[1:]))
