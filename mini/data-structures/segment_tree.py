"""Segment tree: range sum queries with point updates. Usage: python segment_tree.py"""
import random


class SegmentTree:
    def __init__(self, data: list[int]) -> None:
        self.n = len(data)
        self.t = [0] * (2 * self.n) if self.n else []
        self.t[self.n:] = data
        for i in range(self.n - 1, 0, -1):
            self.t[i] = self.t[2 * i] + self.t[2 * i + 1]

    def update(self, i: int, value: int) -> None:
        i += self.n
        self.t[i] = value
        while i > 1:
            i //= 2
            self.t[i] = self.t[2 * i] + self.t[2 * i + 1]

    def query(self, lo: int, hi: int) -> int:
        """Sum of data[lo:hi]."""
        total = 0
        lo += self.n
        hi += self.n
        while lo < hi:
            if lo & 1:
                total += self.t[lo]
                lo += 1
            if hi & 1:
                hi -= 1
                total += self.t[hi]
            lo //= 2
            hi //= 2
        return total


if __name__ == "__main__":
    rng = random.Random(3)
    data = [rng.randint(0, 99) for _ in range(50)]
    st = SegmentTree(data)
    for _ in range(200):
        if rng.random() < 0.3:
            i, v = rng.randrange(50), rng.randint(0, 99)
            data[i] = v
            st.update(i, v)
        else:
            a = rng.randrange(50)
            b = rng.randint(a, 50)
            assert st.query(a, b) == sum(data[a:b])
    print("segment tree ok, total =", st.query(0, 50))
