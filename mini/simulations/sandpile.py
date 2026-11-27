"""Abelian sandpile: drop grains on the centre, topple cells with >=4 grains. Usage: python sandpile.py [grains] [size]"""
import sys


def run(grains: int = 2000, size: int = 31) -> list[list[int]]:
    """Drop all grains at the centre, toppling after each; grains falling off the edge are lost."""
    g = [[0] * size for _ in range(size)]
    c = size // 2
    for _ in range(grains):
        g[c][c] += 1
        stack = [(c, c)]
        while stack:
            x, y = stack.pop()
            if g[x][y] < 4:
                continue
            k = g[x][y] // 4
            g[x][y] -= 4 * k
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < size and 0 <= ny < size:
                    g[nx][ny] += k
                    if g[nx][ny] >= 4:
                        stack.append((nx, ny))
    return g


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    sz = int(sys.argv[2]) if len(sys.argv) > 2 else 31
    grid = run(n, sz)
    for row in grid:
        print("".join(" .:*#"[v] for v in row))
    print(f"grains left on table: {sum(map(sum, grid))} of {n}")
