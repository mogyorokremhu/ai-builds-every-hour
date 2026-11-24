"""Barnsley fern via the iterated function system, plotted in ASCII."""
import random

# (a, b, c, d, e, f, probability)
RULES = [
    (0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01),
    (0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 0.85),
    (0.2, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07),
    (-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07),
]


def points(n: int = 20000, seed: int = 1):
    rng = random.Random(seed)
    x = y = 0.0
    for _ in range(n):
        r = rng.random()
        acc = 0.0
        for a, b, c, d, e, f, p in RULES:
            acc += p
            if r <= acc:
                break
        x, y = a * x + b * y + e, c * x + d * y + f
        yield x, y


def render(w: int = 60, h: int = 30, n: int = 20000) -> str:
    grid = [[0] * w for _ in range(h)]
    for x, y in points(n):
        col = int((x + 2.5) / 5.0 * (w - 1))
        row = h - 1 - int(y / 10.0 * (h - 1))
        if 0 <= col < w and 0 <= row < h:
            grid[row][col] += 1
    chars = " .:*#"
    return "\n".join("".join(chars[min(c, 4)] for c in row) for row in grid)


if __name__ == "__main__":
    print(render())
