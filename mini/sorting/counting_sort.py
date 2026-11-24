"""Counting sort for small non-negative/negative integer ranges (stable)."""
import random


def counting_sort(a: list[int]) -> list[int]:
    """Return a new stably sorted list; O(n + k) for value range k."""
    if not a:
        return []
    lo, hi = min(a), max(a)
    counts = [0] * (hi - lo + 1)
    for x in a:
        counts[x - lo] += 1
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    out = [0] * len(a)
    for x in reversed(a):
        counts[x - lo] -= 1
        out[counts[x - lo]] = x
    return out


if __name__ == "__main__":
    data = [random.randint(-20, 20) for _ in range(25)]
    out = counting_sort(data)
    print(data, "->", out)
    assert out == sorted(data) and counting_sort([]) == []
    print("ok")
