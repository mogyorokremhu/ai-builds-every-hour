"""Interval set: add/merge overlapping ranges, query coverage. Usage: python interval_merge.py"""
from bisect import bisect_left


class IntervalSet:
    def __init__(self) -> None:
        self.iv: list[tuple[int, int]] = []  # sorted, disjoint, half-open [a, b)

    def add(self, a: int, b: int) -> None:
        i = bisect_left(self.iv, (a, a))
        if i > 0 and self.iv[i - 1][1] >= a:
            i -= 1
        j = i
        while j < len(self.iv) and self.iv[j][0] <= b:
            a, b = min(a, self.iv[j][0]), max(b, self.iv[j][1])
            j += 1
        self.iv[i:j] = [(a, b)]

    def covers(self, x: int) -> bool:
        i = bisect_left(self.iv, (x + 1, x + 1)) - 1
        return i >= 0 and self.iv[i][0] <= x < self.iv[i][1]

    def total(self) -> int:
        return sum(b - a for a, b in self.iv)


if __name__ == "__main__":
    s = IntervalSet()
    for a, b in [(1, 3), (8, 10), (2, 5), (5, 6), (20, 25), (9, 21)]:
        s.add(a, b)
    print(s.iv, "total", s.total(), s.covers(7), s.covers(12))
    assert s.iv == [(1, 6), (8, 25)] and s.total() == 22
