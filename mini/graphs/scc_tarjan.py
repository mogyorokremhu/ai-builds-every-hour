"""Strongly connected components of a directed graph (Kosaraju's algorithm)."""


def kosaraju(graph: dict) -> list:
    """Return a list of SCCs (each a sorted list)."""
    order, seen = [], set()
    for s in graph:
        if s in seen:
            continue
        seen.add(s)
        stack = [(s, iter(graph[s]))]
        while stack:
            u, it = stack[-1]
            for v in it:
                if v not in seen:
                    seen.add(v)
                    stack.append((v, iter(graph.get(v, []))))
                    break
            else:
                order.append(u)
                stack.pop()
    rev = {u: [] for u in graph}
    for u in graph:
        for v in graph[u]:
            rev.setdefault(v, []).append(u)
    comps, assigned = [], set()
    for s in reversed(order):
        if s in assigned:
            continue
        comp, stack = [], [s]
        assigned.add(s)
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in rev.get(u, []):
                if v not in assigned:
                    assigned.add(v)
                    stack.append(v)
        comps.append(sorted(comp))
    return comps


if __name__ == "__main__":
    g = {1: [2], 2: [3], 3: [1, 4], 4: [5], 5: [6], 6: [4], 7: [6, 8], 8: [7]}
    for c in sorted(kosaraju(g)):
        print("SCC:", c)
