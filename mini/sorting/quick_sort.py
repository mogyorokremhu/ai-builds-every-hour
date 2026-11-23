"""In-place quicksort (Lomuto partition, median-of-three pivot) with a swap counter."""
import random


def quick_sort(a: list[int], lo: int = 0, hi: int | None = None, stats: dict | None = None) -> list[int]:
    """Sort list a in place and return it."""
    stats = stats if stats is not None else {"swaps": 0}
    hi = len(a) - 1 if hi is None else hi
    if lo < hi:
        mid = (lo + hi) // 2
        # median-of-three: move the median value to hi as pivot
        trio = sorted([(a[lo], lo), (a[mid], mid), (a[hi], hi)])
        p = trio[1][1]
        a[p], a[hi] = a[hi], a[p]
        pivot, i = a[hi], lo
        for j in range(lo, hi):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]; stats["swaps"] += 1
                i += 1
        a[i], a[hi] = a[hi], a[i]; stats["swaps"] += 1
        quick_sort(a, lo, i - 1, stats)
        quick_sort(a, i + 1, hi, stats)
    return a


if __name__ == "__main__":
    data = [random.randint(0, 50) for _ in range(25)]
    st = {"swaps": 0}
    out = quick_sort(list(data), stats=st)
    assert out == sorted(data)
    print(data, "->", out, st)
