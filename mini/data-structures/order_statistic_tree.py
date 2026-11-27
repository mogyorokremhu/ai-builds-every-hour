"""Order-statistic structure: k-th smallest and rank in O(log n) via a Fenwick tree over a
fixed key universe. Usage: python order_statistic_tree.py"""


class OrderStatistics:
    def __init__(self, universe: int):
        self.n = universe
        self.tree = [0] * (universe + 1)
        self.log = universe.bit_length()

    def add(self, key: int, delta: int = 1):
        i = key + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def rank(self, key: int) -> int:
        """Number of stored items strictly smaller than key."""
        i, s = key, 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def kth(self, k: int) -> int:
        """0-based k-th smallest stored key (binary descent over the Fenwick tree)."""
        pos = 0
        for b in range(self.log, -1, -1):
            nxt = pos + (1 << b)
            if nxt <= self.n and self.tree[nxt] <= k:
                pos = nxt
                k -= self.tree[nxt]
        return pos


if __name__ == "__main__":
    os_ = OrderStatistics(100)
    data = [42, 7, 99, 7, 15, 63, 0, 50]
    for x in data:
        os_.add(x)
    s = sorted(data)
    print("sorted:", s)
    print("kth(0..7):", [os_.kth(i) for i in range(len(s))])
    print("rank(50):", os_.rank(50))
    assert [os_.kth(i) for i in range(len(s))] == s
    assert os_.rank(50) == sum(1 for x in data if x < 50)
