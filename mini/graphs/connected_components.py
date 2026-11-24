"""Connected components of an undirected graph (iterative DFS) plus bridges check."""


def components(n, edges):
    """Return a list of components, each a sorted list of vertices."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen, out = [False] * n, []
    for s in range(n):
        if seen[s]:
            continue
        stack, comp = [s], []
        seen[s] = True
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj[x]:
                if not seen[y]:
                    seen[y] = True
                    stack.append(y)
        out.append(sorted(comp))
    return out


def bridges(n, edges):
    """Edges whose removal increases the component count (brute force)."""
    base = len(components(n, edges))
    return [e for i, e in enumerate(edges)
            if len(components(n, edges[:i] + edges[i + 1:])) > base]


if __name__ == "__main__":
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (4, 5), (6, 6)]
    comps = components(7, edges)
    print("components:", comps)
    print("bridges:", bridges(7, edges))
    assert comps == [[0, 1, 2, 3], [4, 5], [6]]
    assert bridges(7, edges) == [(2, 3), (4, 5)]
