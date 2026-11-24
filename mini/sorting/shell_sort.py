"""Shell sort with Ciura's gap sequence."""
import random

GAPS = [701, 301, 132, 57, 23, 10, 4, 1]


def shell_sort(a: list[int]) -> list[int]:
    """Sort a in place using gapped insertion sort; return it."""
    n = len(a)
    for gap in GAPS:
        for i in range(gap, n):
            tmp, j = a[i], i
            while j >= gap and a[j - gap] > tmp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = tmp
    return a


if __name__ == "__main__":
    data = random.sample(range(5000), 800)
    assert shell_sort(list(data)) == sorted(data)
    print("sorted 800 items ok")
