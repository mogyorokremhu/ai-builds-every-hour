"""LSD radix sort (base 10) for non-negative integers."""
import random


def radix_sort(a: list[int], base: int = 10) -> list[int]:
    """Return a sorted copy using least-significant-digit buckets."""
    out = list(a)
    if not out:
        return out
    exp, top = 1, max(out)
    while top // exp > 0:
        buckets: list[list[int]] = [[] for _ in range(base)]
        for x in out:
            buckets[(x // exp) % base].append(x)
        out = [x for b in buckets for x in b]
        exp *= base
    return out


if __name__ == "__main__":
    data = [random.randint(0, 99999) for _ in range(20)]
    out = radix_sort(data)
    print(data, "->", out)
    assert out == sorted(data) and radix_sort(data, 16) == sorted(data)
    print("ok")
