"""Gnome sort: walk forward, step back on inversion."""
import random


def gnome_sort(a: list) -> list:
    """Return a sorted copy using gnome sort."""
    a = list(a)
    i = 0
    while i < len(a):
        if i == 0 or a[i - 1] <= a[i]:
            i += 1
        else:
            a[i - 1], a[i] = a[i], a[i - 1]
            i -= 1
    return a


if __name__ == "__main__":
    data = [random.randint(-50, 50) for _ in range(200)]
    assert gnome_sort(data) == sorted(data)
    assert gnome_sort([]) == []
    print("gnome sort ok")
