"""Insertion sort with binary search for the insertion point."""
import bisect
import random


def insertion_sort(a: list[int]) -> list[int]:
    """Sort a in place using binary insertion; return it."""
    for i in range(1, len(a)):
        x = a[i]
        pos = bisect.bisect_right(a, x, 0, i)
        a[pos + 1:i + 1] = a[pos:i]
        a[pos] = x
    return a


if __name__ == "__main__":
    data = random.sample(range(3000), 500)
    assert insertion_sort(list(data)) == sorted(data)
    assert insertion_sort([]) == [] and insertion_sort([1]) == [1]
    print("sorted 500 items ok")
