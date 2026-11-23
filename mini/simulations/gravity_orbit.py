"""Leapfrog orbit of a planet around a star, ASCII plot + energy drift. Usage: python gravity_orbit.py [steps]"""
import math
import sys


def orbit(steps: int = 2000, dt: float = 0.005, ecc_v: float = 0.8):
    x, y, vx, vy = 1.0, 0.0, 0.0, ecc_v  # GM = 1; v=1 is circular
    energy = lambda: 0.5 * (vx * vx + vy * vy) - 1 / math.hypot(x, y)
    e0 = energy()
    path = []
    ax, ay = -x / math.hypot(x, y) ** 3, -y / math.hypot(x, y) ** 3
    for _ in range(steps):
        vx += 0.5 * dt * ax
        vy += 0.5 * dt * ay
        x += dt * vx
        y += dt * vy
        r3 = math.hypot(x, y) ** 3
        ax, ay = -x / r3, -y / r3
        vx += 0.5 * dt * ax
        vy += 0.5 * dt * ay
        path.append((x, y))
    return e0, energy(), path


def plot(path, w: int = 61, h: int = 25) -> str:
    grid = [[" "] * w for _ in range(h)]
    span = max(max(abs(x), abs(y)) for x, y in path) * 1.05
    for x, y in path:
        c = int((x / span + 1) / 2 * (w - 1))
        r = int((1 - (y / span + 1) / 2) * (h - 1))
        grid[r][c] = "."
    grid[h // 2][w // 2] = "*"
    return "\n".join("".join(r) for r in grid)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    e0, e1, path = orbit(n)
    print(plot(path))
    print(f"energy {e0:.6f} -> {e1:.6f} (drift {abs(e1 - e0):.2e})")
