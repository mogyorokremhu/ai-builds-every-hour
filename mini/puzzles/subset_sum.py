"""Subset sum: find a subset hitting a target (DP with back-pointers) and count all of them.

Usage: python subset_sum.py [target] [n1 n2 ...]
"""
import sys


def find_subset(nums: list[int], target: int) -> list[int] | None:
    """Return one subset of positive ints summing to target, or None."""
    reach: dict[int, int] = {0: -1}  # sum -> index of last number used
    for i, n in enumerate(nums):
        for s in sorted(reach, reverse=True):
            t = s + n
            if t <= target and t not in reach:
                reach[t] = i
    if target not in reach:
        return None
    out, s = [], target
    while s:
        i = reach[s]
        out.append(nums[i])
        s -= nums[i]
    return sorted(out)


def count_subsets(nums: list[int], target: int) -> int:
    ways = [1] + [0] * target
    for n in nums:
        for s in range(target, n - 1, -1):
            ways[s] += ways[s - n]
    return ways[target]


if __name__ == "__main__":
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    nums = [int(a) for a in sys.argv[2:]] or [3, 34, 4, 12, 5, 2, 27, 8, 15, 21]
    print("numbers:", nums, "target:", target)
    print("one subset:", find_subset(nums, target))
    print("count:", count_subsets(nums, target))
