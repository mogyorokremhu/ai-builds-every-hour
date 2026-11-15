"""Sparse table: O(1) range-minimum queries after O(n log n) build. Usage: python sparse_table.py"""


class SparseTable:
    def __init__(self, xs: list[int]):
        self.t = [list(xs)]
        j = 1
        while (1 << j) <= len(xs):
            prev, half = self.t[-1], 1 << (j - 1)
            self.t.append([min(prev[i], prev[i + half]) for i in range(len(xs) - (1 << j) + 1)])
            j += 1

    def query(self, lo: int, hi: int) -> int:
        """Minimum of xs[lo..hi] inclusive."""
        j = (hi - lo + 1).bit_length() - 1
        return min(self.t[j][lo], self.t[j][hi - (1 << j) + 1])


if __name__ == "__main__":
    xs = [7, 2, 9, 4, 1, 8, 3, 6]
    st = SparseTable(xs)
    for lo, hi in [(0, 3), (2, 5), (4, 7), (0, 7)]:
        print(f"min{xs[lo:hi+1]} = {st.query(lo, hi)}")
        assert st.query(lo, hi) == min(xs[lo:hi + 1])
