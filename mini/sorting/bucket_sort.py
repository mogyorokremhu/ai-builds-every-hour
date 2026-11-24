"""Bucket sort for floats in [0, 1)."""
import random


def bucket_sort(a: list[float], buckets: int = 10) -> list[float]:
    """Return a sorted copy; values must lie in [0, 1)."""
    bins: list[list[float]] = [[] for _ in range(buckets)]
    for x in a:
        bins[int(x * buckets)].append(x)
    return [x for b in bins for x in sorted(b)]


if __name__ == "__main__":
    data = [random.random() for _ in range(1000)]
    assert bucket_sort(data) == sorted(data)
    assert bucket_sort([]) == []
    print("sorted 1000 floats ok")
