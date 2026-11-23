"""Heap sort with an explicit sift-down max-heap."""
import random


def _sift_down(a: list[int], start: int, end: int) -> None:
    root = start
    while 2 * root + 1 <= end:
        child = 2 * root + 1
        if child + 1 <= end and a[child] < a[child + 1]:
            child += 1
        if a[root] >= a[child]:
            return
        a[root], a[child] = a[child], a[root]
        root = child


def heap_sort(a: list[int]) -> list[int]:
    """Sort list a in place and return it."""
    n = len(a)
    for s in range(n // 2 - 1, -1, -1):
        _sift_down(a, s, n - 1)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        _sift_down(a, 0, end - 1)
    return a


if __name__ == "__main__":
    data = random.sample(range(1000), 15)
    out = heap_sort(list(data))
    assert out == sorted(data)
    print(data, "->", out)
