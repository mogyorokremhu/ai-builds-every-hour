"""Bellman-Ford shortest paths with negative edges and negative-cycle detection."""

EDGES = [("S", "A", 4), ("S", "B", 5), ("A", "C", 3), ("B", "A", -2), ("C", "D", 2), ("B", "D", 7)]


def bellman_ford(nodes, edges, src):
    """Return (dist, prev); raises ValueError on a reachable negative cycle."""
    dist = {n: float("inf") for n in nodes}
    prev = {n: None for n in nodes}
    dist[src] = 0
    for _ in range(len(nodes) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v], prev[v] = dist[u] + w, u
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            raise ValueError("negative cycle detected")
    return dist, prev


def path(prev, t):
    out = []
    while t is not None:
        out.append(t)
        t = prev[t]
    return out[::-1]


if __name__ == "__main__":
    nodes = sorted({n for e in EDGES for n in e[:2]})
    dist, prev = bellman_ford(nodes, EDGES, "S")
    for n in nodes:
        print(n, dist[n], " -> ".join(path(prev, n)))
    try:
        bellman_ford(nodes, EDGES + [("D", "B", -10)], "S")
    except ValueError as e:
        print("with extra edge D->B(-10):", e)
