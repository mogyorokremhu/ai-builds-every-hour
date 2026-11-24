"""Hilbert space-filling curve drawn with box-ish characters.
python ascii_hilbert_curve.py [order]"""
import sys


def d2xy(n: int, d: int) -> tuple[int, int]:
    """Convert distance d along the Hilbert curve to (x, y) on an n*n grid."""
    x = y = 0
    s, t = 1, d
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


def main(order: int = 4) -> None:
    n = 2 ** order
    pts = [d2xy(n, d) for d in range(n * n)]
    w = n * 2 - 1
    grid = [[" "] * w for _ in range(n)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        grid[y0][x0 * 2] = "o"
        grid[y1][x1 * 2] = "o"
        grid[(y0 + y1) // 2][x0 + x1] = "-" if y0 == y1 else "|"
    print("\n".join("".join(r).rstrip() for r in grid))
    print(f"order {order}: {n * n} cells visited in one unbroken path")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
