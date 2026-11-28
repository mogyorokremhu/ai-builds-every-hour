"""Articulation points (cut vertices) via Tarjan's low-link DFS."""
import sys


def articulation_points(graph: dict) -> set:
    """Return the set of vertices whose removal disconnects their component."""
    sys.setrecursionlimit(10000)
    disc, low, result = {}, {}, set()
    timer = [0]

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0
        for v in graph[u]:
            if v == parent:
                continue
            if v in disc:
                low[u] = min(low[u], disc[v])
            else:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if parent is not None and low[v] >= disc[u]:
                    result.add(u)
        if parent is None and children > 1:
            result.add(u)

    for s in graph:
        if s not in disc:
            dfs(s, None)
    return result


if __name__ == "__main__":
    g = {1: [2, 3], 2: [1, 3], 3: [1, 2, 4], 4: [3, 5], 5: [4, 6, 7], 6: [5, 7], 7: [5, 6]}
    print("Articulation points:", sorted(articulation_points(g)))  # [3, 4, 5]
