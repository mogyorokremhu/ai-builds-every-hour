"""Kruskal's minimum spanning tree with a union-find structure."""


class DSU:
    """Disjoint-set union with path compression and union by size."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


def kruskal(n, edges):
    """edges: (weight, u, v). Return (total weight, chosen edges)."""
    dsu = DSU(n)
    chosen, total = [], 0
    for w, u, v in sorted(edges):
        if dsu.union(u, v):
            chosen.append((u, v, w))
            total += w
    return total, chosen


if __name__ == "__main__":
    edges = [(7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3), (7, 1, 4),
             (5, 2, 4), (15, 3, 4), (6, 3, 5), (8, 4, 5), (9, 4, 6), (11, 5, 6)]
    total, tree = kruskal(7, edges)
    for u, v, w in tree:
        print(f"{u} - {v}  ({w})")
    print("total:", total)
    assert total == 39 and len(tree) == 6
