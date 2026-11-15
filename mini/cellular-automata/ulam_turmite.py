"""A two-state turmite (Langton's ant variant with 3 colours): RLL ant on a wrapping grid."""
import sys

RULE = "RLL"  # turn right / left / left on colours 0 / 1 / 2
GLYPHS = " .#"


def run(steps: int, w: int = 40, h: int = 18):
    grid = [[0] * w for _ in range(h)]
    x, y, d = w // 2, h // 2, 0
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    for _ in range(steps):
        c = grid[y][x]
        d = (d + (1 if RULE[c] == "R" else -1)) % 4
        grid[y][x] = (c + 1) % len(RULE)
        x, y = (x + dirs[d][0]) % w, (y + dirs[d][1]) % h
    return grid


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    print("\n".join("".join(GLYPHS[c] for c in row) for row in run(n)))
