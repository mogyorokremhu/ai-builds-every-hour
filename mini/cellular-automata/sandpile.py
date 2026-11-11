"""Abelian sandpile: drop grains in the centre; cells with 4+ grains topple."""
import sys


def topple(grid: list) -> int:
    """Stabilise in place; return number of topplings. Grains fall off the edge."""
    n = len(grid)
    count = 0
    stack = [(y, x) for y in range(n) for x in range(n) if grid[y][x] >= 4]
    while stack:
        y, x = stack.pop()
        if grid[y][x] < 4:
            continue
        k = grid[y][x] // 4
        grid[y][x] -= 4 * k
        count += k
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < n and 0 <= nx < n:
                grid[ny][nx] += k
                if grid[ny][nx] >= 4:
                    stack.append((ny, nx))
    return count


def render(grid: list) -> str:
    return "\n".join("".join(" .:#"[min(c, 3)] for c in row) for row in grid)


if __name__ == "__main__":
    grains = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    n = 21
    g = [[0] * n for _ in range(n)]
    g[n // 2][n // 2] = grains
    print("topplings:", topple(g))
    print(render(g))
