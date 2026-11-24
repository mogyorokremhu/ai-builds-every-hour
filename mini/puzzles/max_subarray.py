"""Maximum subarray (Kadane) with indices, compared to the O(n^2) brute force.

Usage: python max_subarray.py [numbers...]
"""
import random
import sys


def kadane(a: list[int]) -> tuple[int, int, int]:
    """Return (best_sum, start, end_inclusive)."""
    best = cur = a[0]
    bs = cs = be = 0
    for i in range(1, len(a)):
        if cur < 0:
            cur, cs = a[i], i
        else:
            cur += a[i]
        if cur > best:
            best, bs, be = cur, cs, i
    return best, bs, be


def brute(a: list[int]) -> int:
    return max(sum(a[i:j + 1]) for i in range(len(a)) for j in range(i, len(a)))


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]] or [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    s, i, j = kadane(a)
    print(f"{a}\nbest sum {s} at [{i}..{j}] = {a[i:j + 1]}")
    for _ in range(200):
        r = [random.randint(-9, 9) for _ in range(random.randint(1, 12))]
        assert kadane(r)[0] == brute(r)
    print("200 random cases agree with brute force")
