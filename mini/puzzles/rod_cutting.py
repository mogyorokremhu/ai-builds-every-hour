#!/usr/bin/env python3
"""rod_cutting - maximum revenue from cutting a rod: DP vs brute force."""
import sys
from itertools import product


def best_dp(prices: list[int], n: int) -> tuple[int, list[int]]:
    """prices[i] is the price of a piece of length i+1. Returns (revenue, pieces)."""
    best = [0] * (n + 1)
    first = [0] * (n + 1)
    for length in range(1, n + 1):
        for cut in range(1, min(length, len(prices)) + 1):
            v = prices[cut - 1] + best[length - cut]
            if v > best[length]:
                best[length], first[length] = v, cut
    pieces, rem = [], n
    while rem > 0:
        pieces.append(first[rem])
        rem -= first[rem]
    return best[n], pieces


def best_brute(prices: list[int], n: int) -> int:
    def go(rem: int) -> int:
        if rem == 0:
            return 0
        return max(prices[c - 1] + go(rem - c) for c in range(1, min(rem, len(prices)) + 1))
    return go(n)


if __name__ == "__main__":
    classic = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    if "--selftest" in sys.argv:
        assert best_dp(classic, 8)[0] == 22
        assert best_dp(classic, 4)[0] == 10
        for n in range(1, 10):
            assert best_dp(classic, n)[0] == best_brute(classic, n)
        print("ok"); sys.exit()
    for n in range(1, 11):
        rev, pcs = best_dp(classic, n)
        print(f"n={n:>2} revenue={rev:>2} pieces={pcs}")
