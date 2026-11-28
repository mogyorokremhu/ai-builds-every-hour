"""Eulerian path / circuit in an undirected multigraph (Hierholzer's algorithm)."""
from collections import defaultdict


def euler_path(edges: list):
    """Return a vertex list using every edge once, or None if impossible."""
    adj = defaultdict(list)
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, i))
        adj[b].append((a, i))
    odd = [v for v in adj if len(adj[v]) % 2]
    if len(odd) not in (0, 2):
        return None
    start = odd[0] if odd else edges[0][0]
    used, stack, path = [False] * len(edges), [start], []
    while stack:
        u = stack[-1]
        while adj[u] and used[adj[u][-1][1]]:
            adj[u].pop()
        if adj[u]:
            v, i = adj[u].pop()
            used[i] = True
            stack.append(v)
        else:
            path.append(stack.pop())
    return path[::-1] if len(path) == len(edges) + 1 else None


if __name__ == "__main__":
    print(euler_path([(1, 2), (2, 3), (3, 1), (3, 4)]))   # path
    print(euler_path([(1, 2), (2, 3), (3, 1)]))           # circuit
    print(euler_path([(1, 2), (3, 4)]))                   # None
