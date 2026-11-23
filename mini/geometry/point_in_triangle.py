"""Triangle utilities: area, point containment (barycentric), circumcircle. Usage: python point_in_triangle.py"""
import math


def area(a, b, c):
    return abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2


def contains(a, b, c, p):
    total = area(a, b, c)
    return math.isclose(total, area(p, b, c) + area(a, p, c) + area(a, b, p), abs_tol=1e-9)


def circumcircle(a, b, c):
    d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    ux = ((a[0]**2 + a[1]**2) * (b[1] - c[1]) + (b[0]**2 + b[1]**2) * (c[1] - a[1]) + (c[0]**2 + c[1]**2) * (a[1] - b[1])) / d
    uy = ((a[0]**2 + a[1]**2) * (c[0] - b[0]) + (b[0]**2 + b[1]**2) * (a[0] - c[0]) + (c[0]**2 + c[1]**2) * (b[0] - a[0])) / d
    return (ux, uy), math.dist((ux, uy), a)


if __name__ == "__main__":
    A, B, C = (0, 0), (4, 0), (0, 3)
    print("area:", area(A, B, C))
    print("(1,1) inside:", contains(A, B, C, (1, 1)))
    print("(4,3) inside:", contains(A, B, C, (4, 3)))
    centre, r = circumcircle(A, B, C)
    print("circumcircle centre", centre, "radius", r)
    assert centre == (2.0, 1.5) and math.isclose(r, 2.5)
