"""Floyd-Warshall all-pairs shortest paths with path reconstruction."""
INF = float("inf")


def floyd_warshall(n, edges):
    """edges: (u, v, w) directed. Return (dist matrix, next-hop matrix)."""
    dist = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    nxt = [[None] * n for _ in range(n)]
    for u, v, w in edges:
        dist[u][v] = w
        nxt[u][v] = v
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def path(nxt, u, v):
    """Vertex list from u to v, or [] if unreachable."""
    if nxt[u][v] is None:
        return [u] if u == v else []
    out = [u]
    while u != v:
        u = nxt[u][v]
        out.append(u)
    return out


if __name__ == "__main__":
    edges = [(0, 1, 3), (1, 2, -2), (2, 3, 2), (3, 1, 1), (0, 3, 10)]
    dist, nxt = floyd_warshall(4, edges)
    for row in dist:
        print(" ".join("inf" if x == INF else f"{x:3}" for x in row))
    print("0 -> 3:", path(nxt, 0, 3))
    assert dist[0][3] == 3 and path(nxt, 0, 3) == [0, 1, 2, 3]
    assert path(nxt, 3, 0) == []
