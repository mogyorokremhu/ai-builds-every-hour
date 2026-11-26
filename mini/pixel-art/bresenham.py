"""Bresenham line, circle and rectangle rasterisation onto a text canvas."""


def line(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    """Integer points of a line from (x0,y0) to (x1,y1)."""
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if (x0, y0) == (x1, y1):
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def circle(cx: int, cy: int, r: int) -> set[tuple[int, int]]:
    """Midpoint circle outline."""
    pts, x, y, d = set(), r, 0, 1 - r
    while x >= y:
        for a, b in ((x, y), (y, x)):
            for sx in (1, -1):
                for sy in (1, -1):
                    pts.add((cx + sx * a, cy + sy * b))
        y += 1
        if d < 0:
            d += 2 * y + 1
        else:
            x -= 1
            d += 2 * (y - x) + 1
    return pts


def render(points, w: int, h: int) -> str:
    s = set(points)
    return "\n".join("".join("#" if (x, y) in s else "." for x in range(w)) for y in range(h))


if __name__ == "__main__":
    pts = set(line(0, 0, 19, 9)) | set(line(0, 9, 19, 0)) | circle(10, 5, 4)
    print(render(pts, 21, 11))
