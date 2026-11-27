"""Deadlock detection via cycle search in a wait-for graph. Usage: python deadlock_detect.py"""
from __future__ import annotations


def find_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    """Return one cycle (list of nodes) in the wait-for graph, or None."""
    color: dict[str, int] = {}
    stack: list[str] = []

    def dfs(u: str) -> list[str] | None:
        color[u] = 1
        stack.append(u)
        for v in graph.get(u, []):
            if color.get(v, 0) == 1:
                return stack[stack.index(v):] + [v]
            if color.get(v, 0) == 0:
                c = dfs(v)
                if c:
                    return c
        stack.pop()
        color[u] = 2
        return None

    for n in list(graph):
        if color.get(n, 0) == 0:
            c = dfs(n)
            if c:
                return c
    return None


if __name__ == "__main__":
    ok = {"P1": ["P2"], "P2": ["P3"], "P3": []}
    bad = {"P1": ["P2"], "P2": ["P3"], "P3": ["P1"], "P4": ["P1"]}
    for name, g in (("ok", ok), ("bad", bad)):
        c = find_cycle(g)
        print(name, "->", " -> ".join(c) if c else "no deadlock")
