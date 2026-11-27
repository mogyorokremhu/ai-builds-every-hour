"""Banker's algorithm: safe-state check for deadlock avoidance. Usage: python banker.py"""
from __future__ import annotations


def safe_sequence(available: list[int], alloc: list[list[int]], maximum: list[list[int]]) -> list[int] | None:
    """Return a safe process order, or None if the state is unsafe."""
    n = len(alloc)
    need = [[m - a for m, a in zip(maximum[i], alloc[i])] for i in range(n)]
    work = available[:]
    done = [False] * n
    order: list[int] = []
    while len(order) < n:
        for i in range(n):
            if not done[i] and all(x <= w for x, w in zip(need[i], work)):
                work = [w + a for w, a in zip(work, alloc[i])]
                done[i] = True
                order.append(i)
                break
        else:
            return None
    return order


def request(pid: int, req: list[int], available: list[int], alloc: list[list[int]], maximum: list[list[int]]) -> bool:
    """Would granting `req` to process `pid` leave the system safe?"""
    if any(r > m - a for r, m, a in zip(req, maximum[pid], alloc[pid])) or any(r > v for r, v in zip(req, available)):
        return False
    new_av = [v - r for v, r in zip(available, req)]
    new_alloc = [row[:] for row in alloc]
    new_alloc[pid] = [a + r for a, r in zip(new_alloc[pid], req)]
    return safe_sequence(new_av, new_alloc, maximum) is not None


if __name__ == "__main__":
    av = [3, 3, 2]
    al = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    mx = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    print("safe sequence:", ["P%d" % p for p in safe_sequence(av, al, mx) or []])
    print("P1 requests [1,0,2]:", "grant" if request(1, [1, 0, 2], av, al, mx) else "deny")
    print("P0 requests [0,2,0]:", "grant" if request(0, [0, 2, 0], av, al, mx) else "deny")
