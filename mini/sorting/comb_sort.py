"""Comb sort: bubble sort with a shrinking gap (factor 1.3)."""
import random


def comb_sort(a: list) -> list:
    """Return a sorted copy using comb sort."""
    a = list(a)
    gap, swapped = len(a), True
    while gap > 1 or swapped:
        gap = max(1, int(gap / 1.3))
        swapped = False
        for i in range(len(a) - gap):
            if a[i] > a[i + gap]:
                a[i], a[i + gap] = a[i + gap], a[i]
                swapped = True
    return a


if __name__ == "__main__":
    data = [random.randint(-1000, 1000) for _ in range(500)]
    assert comb_sort(data) == sorted(data)
    assert comb_sort([3]) == [3]
    print("comb sort ok")
