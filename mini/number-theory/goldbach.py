"""Goldbach's conjecture: verify for even numbers up to N and show the widest-gap decompositions."""
import sys


def primes_upto(n: int) -> list[bool]:
    """Boolean primality table for 0..n."""
    is_p = [n >= 2] * (n + 1)
    is_p[0:2] = [False, False][: n + 1]
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return is_p


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    is_p = primes_upto(n)
    best = (0, 0)
    for e in range(4, n + 1, 2):
        ways = [p for p in range(2, e // 2 + 1) if is_p[p] and is_p[e - p]]
        assert ways, f"counterexample {e}!"
        if len(ways) > best[1]:
            best = (e, len(ways))
    print(f"Goldbach holds for all even numbers 4..{n}")
    print(f"most decompositions: {best[0]} has {best[1]}")
    print("e.g. 100 =", " , ".join(f"{p}+{100 - p}" for p in range(2, 51) if is_p[p] and is_p[100 - p]) if n >= 100 else "")
