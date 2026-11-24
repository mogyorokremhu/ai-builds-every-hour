"""Staircase climbing: ways to climb n steps taking 1..k steps at a time.

Usage: python staircase_ways.py [N] [K]   (default 10 3)
"""
import sys
from itertools import product


def ways(n: int, k: int) -> int:
    dp = [1] + [0] * n
    for i in range(1, n + 1):
        dp[i] = sum(dp[i - s] for s in range(1, min(k, i) + 1))
    return dp[n]


def enumerate_ways(n: int, k: int) -> list[tuple[int, ...]]:
    """Brute force: every composition of n with parts in 1..k."""
    out = []
    for length in range(1, n + 1):
        for combo in product(range(1, k + 1), repeat=length):
            if sum(combo) == n:
                out.append(combo)
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    print(f"{n} steps, up to {k} at a time: {ways(n, k)} ways")
    if n <= 12:
        print("brute force agrees:", len(enumerate_ways(n, k)) == ways(n, k))
