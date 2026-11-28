"""Bresenham line and circle rasterisation drawn as ASCII. Usage: python bresenham_line.py"""


def line(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
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


def circle(cx, cy, r):
    pts, x, y, d = set(), 0, r, 3 - 2 * r
    while x <= y:
        for px, py in ((x, y), (y, x), (-x, y), (-y, x), (x, -y), (y, -x), (-x, -y), (-y, -x)):
            pts.add((cx + px, cy + py))
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
    return pts


def render(points, w=30, h=15):
    grid = [[" "] * w for _ in range(h)]
    for x, y in points:
        if 0 <= x < w and 0 <= y < h:
            grid[y][x] = "#"
    return "\n".join("".join(r) for r in grid)


if __name__ == "__main__":
    ln = line(0, 0, 12, 5)
    assert ln[0] == (0, 0) and ln[-1] == (12, 5) and len(ln) == 13
    assert line(3, 3, 3, 3) == [(3, 3)]
    c = circle(20, 7, 5)
    assert all(abs(((x-20)**2 + (y-7)**2) ** 0.5 - 5) < 0.8 for x, y in c)
    print(render(set(ln) | c))
    print("ok")
