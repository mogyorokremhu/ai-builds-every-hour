"""Ear-clipping triangulation of a simple polygon. Usage: python polygon_triangulation.py"""


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def area(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
               for i in range(len(poly))) / 2


def inside(p, a, b, c):
    return cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0


def triangulate(poly):
    pts = list(poly) if area(poly) > 0 else list(reversed(poly))
    tris = []
    while len(pts) > 3:
        for i in range(len(pts)):
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % len(pts)]
            if cross(a, b, c) <= 0:
                continue
            if any(inside(p, a, b, c) for p in pts if p not in (a, b, c)):
                continue
            tris.append((a, b, c))
            del pts[i]
            break
        else:
            raise ValueError("polygon is not simple")
    tris.append(tuple(pts))
    return tris


if __name__ == "__main__":
    poly = [(0, 0), (4, 0), (4, 4), (2, 2), (0, 4)]
    tris = triangulate(poly)
    for t in tris:
        print(t)
    assert len(tris) == len(poly) - 2
    assert abs(sum(abs(area(t)) for t in tris) - abs(area(poly))) < 1e-9
    print("area preserved, triangles:", len(tris))
