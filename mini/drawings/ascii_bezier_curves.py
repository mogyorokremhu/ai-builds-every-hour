"""Quadratic Bezier curves with their control polygon (de Casteljau).
python ascii_bezier_curves.py"""


def lerp(a: tuple[float, float], b: tuple[float, float], t: float) -> tuple[float, float]:
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def bezier(p0, p1, p2, steps: int = 200):
    for i in range(steps + 1):
        t = i / steps
        yield lerp(lerp(p0, p1, t), lerp(p1, p2, t), t)


def main(w: int = 72, h: int = 24) -> None:
    grid = [[" "] * w for _ in range(h)]

    def plot(p, ch):
        x, y = int(round(p[0])), int(round(p[1]))
        if 0 <= x < w and 0 <= y < h:
            grid[y][x] = ch

    curves = [((2, 20), (36, -14), (69, 20), "#"),
              ((2, 3), (36, 38), (69, 3), "+"),
              ((10, 12), (36, 12), (62, 12), ".")]
    for p0, p1, p2, ch in curves[:2]:
        for s in range(41):
            plot(lerp(p0, p1, s / 40), ":")
            plot(lerp(p1, p2, s / 40), ":")
    for p0, p1, p2, ch in curves[:2]:
        for p in bezier(p0, p1, p2, 400):
            plot(p, ch)
        for c in (p0, p1, p2):
            plot(c, "O")
    print("\n".join("".join(r).rstrip() for r in grid))


if __name__ == "__main__":
    main()
