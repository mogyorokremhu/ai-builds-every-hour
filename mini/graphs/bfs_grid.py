"""Shortest path through an ASCII maze with breadth-first search."""
from collections import deque

MAZE = [
    "S.#.......",
    ".##.####.#",
    "....#..#..",
    ".####.##.#",
    "......#..E",
]


def solve(grid):
    """Return the grid with the shortest S->E path marked by '*'."""
    h, w = len(grid), len(grid[0])
    find = lambda ch: next((r, c) for r in range(h) for c in range(w) if grid[r][c] == ch)
    start, end = find("S"), find("E")
    prev = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == end:
            break
        r, c = cur
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (r + dr, c + dc)
            if 0 <= n[0] < h and 0 <= n[1] < w and grid[n[0]][n[1]] != "#" and n not in prev:
                prev[n] = cur
                q.append(n)
    if end not in prev:
        return None
    out = [list(row) for row in grid]
    node = prev[end]
    while node and node != start:
        out[node[0]][node[1]] = "*"
        node = prev[node]
    return ["".join(r) for r in out]


if __name__ == "__main__":
    res = solve(MAZE)
    print("\n".join(res) if res else "no path")
