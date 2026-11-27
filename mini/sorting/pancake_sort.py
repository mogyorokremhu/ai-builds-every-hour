"""Pancake sort: sort using only prefix reversals (flips)."""
import random


def pancake_sort(a: list) -> tuple[list, list[int]]:
    """Return (sorted copy, list of flip sizes used)."""
    a, flips = list(a), []
    for size in range(len(a), 1, -1):
        m = a.index(max(a[:size]))
        if m == size - 1:
            continue
        if m:
            a[: m + 1] = a[: m + 1][::-1]
            flips.append(m + 1)
        a[:size] = a[:size][::-1]
        flips.append(size)
    return a, flips


if __name__ == "__main__":
    data = random.sample(range(100), 20)
    out, flips = pancake_sort(data)
    assert out == sorted(data)
    print(f"pancake sort ok in {len(flips)} flips")
