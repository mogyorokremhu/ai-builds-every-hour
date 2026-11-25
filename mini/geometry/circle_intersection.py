"""Intersection points of two circles. Usage: python circle_intersection.py"""
import math


def intersect(c1, r1, c2, r2):
    d = math.dist(c1, c2)
    if d == 0 or d > r1 + r2 or d < abs(r1 - r2):
        return []
    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h = math.sqrt(max(r1**2 - a**2, 0))
    mx = c1[0] + a * (c2[0] - c1[0]) / d
    my = c1[1] + a * (c2[1] - c1[1]) / d
    dx, dy = h * (c2[1] - c1[1]) / d, h * (c2[0] - c1[0]) / d
    pts = [(mx + dx, my - dy), (mx - dx, my + dy)]
    return pts if h > 1e-12 else pts[:1]


if __name__ == "__main__":
    for args in [((0, 0), 5, (6, 0), 5), ((0, 0), 1, (2, 0), 1), ((0, 0), 1, (5, 0), 1)]:
        pts = intersect(*args)
        print(args, "->", [(round(x, 3), round(y, 3)) for x, y in pts])
        for p in pts:
            assert abs(math.dist(p, args[0]) - args[1]) < 1e-9 and abs(math.dist(p, args[2]) - args[3]) < 1e-9
    print("ok")
