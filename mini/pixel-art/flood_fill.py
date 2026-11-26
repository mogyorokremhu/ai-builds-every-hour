"""Flood fill (paint bucket) on a text bitmap, 4- or 8-connected."""
from collections import deque

SHAPE = """\
..........
.######...
.#....#...
.#....####
.######..#
.....#####
""".splitlines()


def fill(grid: list[str], x: int, y: int, ch: str, diagonal: bool = False) -> list[str]:
    g = [list(r) for r in grid]
    target = g[y][x]
    if target == ch:
        return grid[:]
    steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diagonal:
        steps += [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    q = deque([(x, y)])
    g[y][x] = ch
    while q:
        cx, cy = q.popleft()
        for dx, dy in steps:
            nx, ny = cx + dx, cy + dy
            if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and g[ny][nx] == target:
                g[ny][nx] = ch
                q.append((nx, ny))
    return ["".join(r) for r in g]


if __name__ == "__main__":
    out = fill(SHAPE, 3, 2, "o")
    assert out[2][2] == "o" and out[0][0] == "."
    print("\n".join(out))
