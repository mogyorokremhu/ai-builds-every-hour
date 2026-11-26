#!/usr/bin/env python3
"""partition_equal - split numbers into two groups with equal sums (subset-sum bitset DP)."""
import sys


def partition(nums: list[int]):
    """Return (groupA, groupB) with equal sums, or None."""
    total = sum(nums)
    if total % 2:
        return None
    target = total // 2
    reach = {0: ()}  # sum -> tuple of indices used
    for i, x in enumerate(nums):
        for s, used in list(reach.items()):
            t = s + x
            if t <= target and t not in reach:
                reach[t] = used + (i,)
    if target not in reach:
        return None
    idx = set(reach[target])
    a = [x for i, x in enumerate(nums) if i in idx]
    b = [x for i, x in enumerate(nums) if i not in idx]
    return a, b


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        a, b = partition([1, 5, 11, 5])
        assert sum(a) == sum(b) == 11
        assert partition([1, 2, 3, 5]) is None
        assert partition([]) == ([], [])
        assert partition([3]) is None
        print("ok"); sys.exit()
    for case in ([1, 5, 11, 5], [1, 2, 3, 5], [4, 4, 4, 4, 8], [7, 3, 2, 5, 8, 1]):
        print(case, "->", partition(case))
