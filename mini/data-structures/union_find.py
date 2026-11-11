"""Union-Find (disjoint set) with path compression and union by rank. Usage: python union_find.py"""


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True


if __name__ == "__main__":
    uf = UnionFind(10)
    for a, b in [(0, 1), (2, 3), (1, 3), (5, 6), (7, 7)]:
        uf.union(a, b)
    assert uf.find(0) == uf.find(2) and uf.find(0) != uf.find(5)
    print("components:", uf.count)
