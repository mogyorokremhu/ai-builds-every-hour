"""Shoelace area, centroid and point-in-polygon. Usage: python polygon_area.py"""


def area(poly):
    s = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]))
    return s / 2


def centroid(poly):
    a = area(poly)
    cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        c = x1 * y2 - x2 * y1
        cx += (x1 + x2) * c
        cy += (y1 + y2) * c
    return cx / (6 * a), cy / (6 * a)


def contains(poly, pt):
    x, y = pt
    inside = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


if __name__ == "__main__":
    sq = [(0, 0), (4, 0), (4, 3), (0, 3)]
    assert area(sq) == 12 and centroid(sq) == (2, 1.5)
    assert contains(sq, (1, 1)) and not contains(sq, (5, 1))
    print("area", area(sq), "centroid", centroid(sq), "ok")
