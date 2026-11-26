"""Two-body orbit with velocity Verlet; prints energy drift and an ASCII orbit."""
import math


def orbit(r0: float = 1.0, v0: float = 0.8, steps: int = 6000, dt: float = 0.002):
    """Simulate a unit-mass body around a fixed centre with GM=1. Returns (points, energy drift)."""
    x, y, vx, vy = r0, 0.0, 0.0, v0

    def acc(px: float, py: float):
        r3 = (px * px + py * py) ** 1.5
        return -px / r3, -py / r3

    def energy():
        return 0.5 * (vx * vx + vy * vy) - 1 / math.hypot(x, y)

    e0, pts = energy(), []
    ax, ay = acc(x, y)
    for _ in range(steps):
        x += vx * dt + 0.5 * ax * dt * dt
        y += vy * dt + 0.5 * ay * dt * dt
        nax, nay = acc(x, y)
        vx += 0.5 * (ax + nax) * dt
        vy += 0.5 * (ay + nay) * dt
        ax, ay = nax, nay
        pts.append((x, y))
    return pts, energy() - e0


def render(pts, w: int = 61, h: int = 25) -> str:
    """ASCII plot of the orbit with the centre marked 'O'."""
    m = max(max(abs(p[0]), abs(p[1])) for p in pts) * 1.05
    g = [[" "] * w for _ in range(h)]
    for px, py in pts:
        c, r = int((px / m + 1) / 2 * (w - 1)), int((1 - (py / m + 1) / 2) * (h - 1))
        g[r][c] = "."
    g[h // 2][w // 2] = "O"
    return "\n".join("".join(r) for r in g)


if __name__ == "__main__":
    pts, drift = orbit()
    print(render(pts))
    print(f"energy drift: {drift:.2e}")
