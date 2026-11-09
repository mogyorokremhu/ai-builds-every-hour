"""Count pairs with a given sum using a hash map, checked against brute force.

Usage: python two_sum_pairs.py [target] [count]
"""
import random
import sys
from collections import Counter


def fast(nums, target):
    seen, total = Counter(), 0
    for x in nums:
        total += seen[target - x]
        seen[x] += 1
    return total


def brute(nums, target):
    return sum(1 for i in range(len(nums)) for j in range(i) if nums[i] + nums[j] == target)


if __name__ == "__main__":
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    rng = random.Random(1)
    nums = [rng.randint(0, target) for _ in range(count)]
    print(nums)
    print("pairs summing to", target, ":", fast(nums, target))
    assert fast(nums, target) == brute(nums, target)
