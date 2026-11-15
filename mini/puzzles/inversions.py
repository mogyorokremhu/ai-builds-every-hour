"""Count inversions in O(n log n) with merge sort, checked against O(n^2).

Usage: python inversions.py [n1 n2 ...]   (random list if none)
"""
import random
import sys


def count(seq: list[int]) -> tuple[list[int], int]:
    if len(seq) < 2:
        return seq[:], 0
    mid = len(seq) // 2
    left, a = count(seq[:mid])
    right, b = count(seq[mid:])
    merged, inv, i, j = [], a + b, 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
            inv += len(left) - i
    merged += left[i:] + right[j:]
    return merged, inv


def brute(seq: list[int]) -> int:
    return sum(seq[i] > seq[j] for i in range(len(seq)) for j in range(i + 1, len(seq)))


if __name__ == "__main__":
    data = [int(x) for x in sys.argv[1:]] or random.Random(3).sample(range(100), 30)
    inv = count(data)[1]
    print(data)
    print("inversions:", inv)
    assert inv == brute(data)
    print("verified against brute force")
