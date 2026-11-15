"""Sierpinski triangle via the chaos game, drawn in ASCII."""
import random


def chaos(w: int = 64, h: int = 32, points: int = 20000, seed: int = 1) -> str:
    rnd = random.Random(seed)
    verts = [(w // 2, 0), (0, h - 1), (w - 1, h - 1)]
    grid = [[" "] * w for _ in range(h)]
    x, y = 10.0, 10.0
    for i in range(points):
        vx, vy = rnd.choice(verts)
        x, y = (x + vx) / 2, (y + vy) / 2
        if i > 20:
            grid[int(y)][int(x)] = "*"
    return "\n".join("".join(r) for r in grid)


if __name__ == "__main__":
    print(chaos())
