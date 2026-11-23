"""Koch curve points and an ASCII plot of the snowflake outline."""
import math


def koch(p1: complex, p2: complex, depth: int) -> list[complex]:
    """Return points of the Koch curve from p1 to p2 (excluding p2)."""
    if depth == 0:
        return [p1]
    d = (p2 - p1) / 3
    a, b = p1 + d, p1 + 2 * d
    peak = a + d * complex(math.cos(math.pi / 3), -math.sin(math.pi / 3))
    pts: list[complex] = []
    for s, e in ((p1, a), (a, peak), (peak, b), (b, p2)):
        pts += koch(s, e, depth - 1)
    return pts


def snowflake(depth: int = 3) -> list[complex]:
    tri = [complex(0, 0), complex(1, 0), complex(0.5, -math.sqrt(3) / 2)]
    pts: list[complex] = []
    for i in range(3):
        pts += koch(tri[i], tri[(i + 1) % 3], depth)
    return pts


def plot(pts: list[complex], w: int = 72, h: int = 32) -> str:
    grid = [[" "] * w for _ in range(h)]
    xs, ys = [p.real for p in pts], [p.imag for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for p in pts:
        gx = int((p.real - x0) / (x1 - x0) * (w - 1))
        gy = int((p.imag - y0) / (y1 - y0) * (h - 1))
        grid[gy][gx] = "*"
    return "\n".join("".join(r) for r in grid)


if __name__ == "__main__":
    print(plot(snowflake(4)))
