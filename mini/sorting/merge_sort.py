"""Top-down merge sort that also counts comparisons."""
import random


def merge_sort(xs: list[int], stats: dict | None = None) -> list[int]:
    """Return a sorted copy of xs; stats['comparisons'] is incremented."""
    stats = stats if stats is not None else {"comparisons": 0}
    if len(xs) <= 1:
        return list(xs)
    mid = len(xs) // 2
    left, right = merge_sort(xs[:mid], stats), merge_sort(xs[mid:], stats)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        stats["comparisons"] += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


if __name__ == "__main__":
    data = random.sample(range(100), 20)
    st = {"comparisons": 0}
    res = merge_sort(data, st)
    assert res == sorted(data)
    print(data, "->", res, st)
