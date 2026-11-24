"""Ugly numbers (only prime factors 2, 3, 5): three-pointer DP, checked by brute force.

Usage: python ugly_numbers.py [N]   (default N = 20)
"""
import sys


def ugly(n: int) -> list[int]:
    """Return the first n ugly numbers in O(n) with three merge pointers."""
    u = [1]
    i2 = i3 = i5 = 0
    while len(u) < n:
        nxt = min(u[i2] * 2, u[i3] * 3, u[i5] * 5)
        u.append(nxt)
        if nxt == u[i2] * 2:
            i2 += 1
        if nxt == u[i3] * 3:
            i3 += 1
        if nxt == u[i5] * 5:
            i5 += 1
    return u


def is_ugly(x: int) -> bool:
    for p in (2, 3, 5):
        while x % p == 0:
            x //= p
    return x == 1


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    res = ugly(n)
    print(res)
    brute = []
    k = 1
    while len(brute) < n:
        if is_ugly(k):
            brute.append(k)
        k += 1
    print("matches brute force:", res == brute)
