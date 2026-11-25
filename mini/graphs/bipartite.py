"""Bipartite check via BFS 2-colouring, with an odd cycle witness on failure."""
from collections import deque


def two_colour(graph: dict):
    """Return (True, colours) or (False, (u, v)) for an edge joining same-coloured nodes."""
    colour = {}
    for s in graph:
        if s in colour:
            continue
        colour[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]
                    q.append(v)
                elif colour[v] == colour[u]:
                    return False, (u, v)
    return True, colour


if __name__ == "__main__":
    square = {1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [3, 1]}
    triangle = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    for name, g in (("square", square), ("triangle", triangle)):
        ok, info = two_colour(g)
        print(name, "bipartite" if ok else "NOT bipartite", info)
