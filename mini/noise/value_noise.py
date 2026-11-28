"""1D/2D value noise with smooth interpolation, rendered as ASCII. Usage: python value_noise.py [seed]"""
import random
import sys


def lattice(seed: int, size: int = 64) -> list[list[float]]:
    """Random lattice of values in [0, 1)."""
    rng = random.Random(seed)
    return [[rng.random() for _ in range(size)] for _ in range(size)]


def smooth(t: float) -> float:
    """Smoothstep fade curve."""
    return t * t * (3 - 2 * t)


def value_noise(grid: list[list[float]], x: float, y: float) -> float:
    """Bilinearly interpolate lattice values at (x, y) using the fade curve."""
    n = len(grid)
    x0, y0 = int(x) % n, int(y) % n
    x1, y1 = (x0 + 1) % n, (y0 + 1) % n
    fx, fy = smooth(x - int(x)), smooth(y - int(y))
    top = grid[y0][x0] * (1 - fx) + grid[y0][x1] * fx
    bot = grid[y1][x0] * (1 - fx) + grid[y1][x1] * fx
    return top * (1 - fy) + bot * fy


def render(seed: int = 1, w: int = 60, h: int = 20, scale: float = 0.12) -> str:
    grid = lattice(seed)
    ramp = " .:-=+*#%@"
    rows = []
    for j in range(h):
        row = ""
        for i in range(w):
            v = value_noise(grid, i * scale, j * scale * 2)
            row += ramp[min(int(v * len(ramp)), len(ramp) - 1)]
        rows.append(row)
    return "\n".join(rows)


if __name__ == "__main__":
    print(render(int(sys.argv[1]) if len(sys.argv) > 1 else 1))
