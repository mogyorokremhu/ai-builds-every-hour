"""Small sets as bitmasks: union, intersection, subsets, and a subset-sum DP."""
from itertools import combinations


def to_mask(items) -> int:
    m = 0
    for i in items:
        m |= 1 << i
    return m


def to_items(m: int) -> list[int]:
    return [i for i in range(m.bit_length()) if m >> i & 1]


def subsets(m: int):
    """Yield every submask of m (including 0 and m)."""
    s = m
    while True:
        yield s
        if s == 0:
            return
        s = (s - 1) & m


def subset_sum_reachable(values: list[int]) -> int:
    """Bitmask of reachable sums, using one int as the DP table."""
    reach = 1
    for v in values:
        reach |= reach << v
    return reach


if __name__ == "__main__":
    a, b = to_mask([1, 3, 5]), to_mask([3, 4, 5])
    print("union", to_items(a | b), "inter", to_items(a & b), "diff", to_items(a & ~b))
    assert len(list(subsets(a))) == 2 ** 3
    assert sorted(map(to_items, subsets(a))) == sorted(
        [list(c) for r in range(4) for c in combinations([1, 3, 5], r)])
    r = subset_sum_reachable([3, 5, 9])
    print("reachable sums:", to_items(r))
    assert to_items(r) == [0, 3, 5, 8, 9, 12, 14, 17]
    print("ok")
