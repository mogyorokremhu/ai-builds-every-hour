"""Topological sort (Kahn's algorithm) with cycle detection."""
from collections import deque

TASKS = {
    "wake up": [],
    "shower": ["wake up"],
    "dress": ["shower"],
    "coffee": ["wake up"],
    "breakfast": ["coffee", "dress"],
    "leave": ["breakfast"],
}


def topo_sort(deps):
    """deps maps node -> list of prerequisites. Raises ValueError on a cycle."""
    indeg = {n: len(p) for n, p in deps.items()}
    users = {n: [] for n in deps}
    for n, ps in deps.items():
        for p in ps:
            users[p].append(n)
    q = deque(sorted(n for n, d in indeg.items() if d == 0))
    order = []
    while q:
        n = q.popleft()
        order.append(n)
        for m in sorted(users[n]):
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    if len(order) != len(deps):
        raise ValueError("cycle detected")
    return order


if __name__ == "__main__":
    print(" -> ".join(topo_sort(TASKS)))
    try:
        topo_sort({"a": ["b"], "b": ["a"]})
    except ValueError as e:
        print("error:", e)
