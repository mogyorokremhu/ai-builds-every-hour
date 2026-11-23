"""A bitset-backed prime sieve using one Python int as the bit array."""
import sys


def sieve(limit: int) -> list[int]:
    """Return primes <= limit. Bit i of `composite` set means i is composite."""
    composite = 0
    primes = []
    for i in range(2, limit + 1):
        if not (composite >> i) & 1:
            primes.append(i)
            for m in range(i * i, limit + 1, i):
                composite |= 1 << m
    return primes


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    p = sieve(n)
    assert sieve(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    print(len(p), "primes <=", n, ":", p[:20], "..." if len(p) > 20 else "")
