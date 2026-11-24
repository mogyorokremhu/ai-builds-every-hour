"""Cocktail shaker sort: bubble sort that alternates direction."""
import random


def cocktail_sort(a: list[int]) -> list[int]:
    """Sort a in place; stops early when a pass makes no swaps."""
    lo, hi = 0, len(a) - 1
    swapped = True
    while swapped and lo < hi:
        swapped = False
        for i in range(lo, hi):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        hi -= 1
        for i in range(hi, lo, -1):
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]
                swapped = True
        lo += 1
    return a


if __name__ == "__main__":
    data = random.sample(range(2000), 300)
    assert cocktail_sort(list(data)) == sorted(data)
    print("sorted 300 items ok")
