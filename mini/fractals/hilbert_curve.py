"""Hilbert space-filling curve: index <-> (x, y) conversion and ASCII drawing."""


def d2xy(n: int, d: int) -> tuple[int, int]:
    """Convert distance d along the curve to (x, y) on an n x n grid (n a power of 2)."""
    x = y = 0
    t = d
    s = 1
    while s < n:
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
    return x, y


def xy2d(n: int, x: int, y: int) -> int:
    d = 0
    s = n // 2
    while s > 0:
        rx = 1 if x & s else 0
        ry = 1 if y & s else 0
        d += s * s * ((3 * rx) ^ ry)
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            x, y = y, x
        s //= 2
    return d


def render(order: int = 3) -> str:
    n = 2 ** order
    pts = [d2xy(n, d) for d in range(n * n)]
    grid = [[" "] * (2 * n - 1) for _ in range(2 * n - 1)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        grid[2 * ay][2 * ax] = grid[2 * by][2 * bx] = "o"
        grid[ay + by][ax + bx] = "-" if ay == by else "|"
    return "\n".join("".join(r) for r in grid)


if __name__ == "__main__":
    print(render(3))
