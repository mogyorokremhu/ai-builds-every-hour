"""Fenwick tree (binary indexed tree): prefix sums with point updates. Usage: python fenwick_tree.py"""


class Fenwick:
    def __init__(self, n: int) -> None:
        self.n = n
        self.t = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        """Add delta at 0-based index i."""
        i += 1
        while i <= self.n:
            self.t[i] += delta
            i += i & -i

    def prefix(self, i: int) -> int:
        """Sum of elements [0, i)."""
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

    def range_sum(self, lo: int, hi: int) -> int:
        """Sum of elements [lo, hi)."""
        return self.prefix(hi) - self.prefix(lo)


if __name__ == "__main__":
    data = [5, 3, 7, 9, 6, 4, 1, 2]
    f = Fenwick(len(data))
    for i, v in enumerate(data):
        f.add(i, v)
    assert f.range_sum(2, 6) == sum(data[2:6])
    f.add(3, 10)
    data[3] += 10
    assert f.range_sum(0, 8) == sum(data)
    print("fenwick ok:", f.range_sum(2, 6))
