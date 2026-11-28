"""Sutherland-Hodgman clipping of a polygon against a convex clip polygon. Usage: python polygon_clip.py"""


def _inside(p, a, b):
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0


def _cross_point(p, q, a, b):
    x1, y1, x2, y2 = p[0], p[1], q[0], q[1]
    x3, y3, x4, y4 = a[0], a[1], b[0], b[1]
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def clip(subject, clipper):
    """Clip `subject` by convex counter-clockwise `clipper`."""
    out = list(subject)
    for i in range(len(clipper)):
        a, b = clipper[i], clipper[(i + 1) % len(clipper)]
        inp, out = out, []
        for j in range(len(inp)):
            p, q = inp[j], inp[(j + 1) % len(inp)]
            if _inside(q, a, b):
                if not _inside(p, a, b):
                    out.append(_cross_point(p, q, a, b))
                out.append(q)
            elif _inside(p, a, b):
                out.append(_cross_point(p, q, a, b))
        if not out:
            break
    return out


def area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))) / 2


if __name__ == "__main__":
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    tri = [(2, -2), (6, 2), (2, 6)]
    res = clip(tri, square)
    print([(round(x, 3), round(y, 3)) for x, y in res])
    print("area", round(area(res), 4))
    assert abs(area(clip(square, square)) - 16) < 1e-9
    assert clip([(10, 10), (12, 10), (11, 12)], square) == []
    assert 0 < area(res) < area(tri)
    print("ok")
