"""Collatz stopping times: longest chain below N and a length histogram."""
import sys


def collatz_lengths(limit: int) -> list[int]:
    """Steps to reach 1 for every n < limit (memoised)."""
    L = [0] * max(limit, 2)
    for n in range(2, limit):
        x, steps = n, 0
        while x >= n:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            steps += 1
        L[n] = steps + L[x]
    return L


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    L = collatz_lengths(limit)
    best = max(range(1, limit), key=lambda n: L[n])
    print(f"longest chain below {limit}: n={best}, steps={L[best]}")
    buckets: dict[int, int] = {}
    for n in range(1, limit):
        buckets[L[n] // 20] = buckets.get(L[n] // 20, 0) + 1
    for b in sorted(buckets):
        print(f"{b * 20:4d}-{b * 20 + 19:<4d} {'#' * (buckets[b] * 50 // limit + 1)} {buckets[b]}")
