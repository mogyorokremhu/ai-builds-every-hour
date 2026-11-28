"""Diameter and minimum-width of a point set via rotating calipers on the convex hull. Usage: python rotating_calipers.py"""
import math
import random


def hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts
    def build(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and (h[-1][0]-h[-2][0])*(p[1]-h[-2][1]) - (h[-1][1]-h[-2][1])*(p[0]-h[-2][0]) <= 0:
                h.pop()
            h.append(p)
        return h[:-1]
    return build(pts) + build(pts[::-1])


def diameter(points):
    h = hull(points)
    n = len(h)
    if n < 3:
        return max((math.dist(a, b) for a in h for b in h), default=0.0)
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    best, j = 0.0, 1
    for i in range(n):
        while abs(cross(h[i], h[(i+1) % n], h[(j+1) % n])) > abs(cross(h[i], h[(i+1) % n], h[j])):
            j = (j + 1) % n
        best = max(best, math.dist(h[i], h[j]), math.dist(h[(i+1) % n], h[j]))
    return best


def min_width(points):
    h = hull(points)
    n = len(h)
    best = math.inf
    for i in range(n):
        a, b = h[i], h[(i+1) % n]
        L = math.dist(a, b)
        far = max(abs((b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])) / L for p in h)
        best = min(best, far)
    return best


if __name__ == "__main__":
    random.seed(7)
    pts = [(random.uniform(0, 10), random.uniform(0, 5)) for _ in range(60)]
    d = diameter(pts)
    brute = max(math.dist(a, b) for a in pts for b in pts)
    print("diameter", round(d, 4), "brute", round(brute, 4))
    print("min width", round(min_width(pts), 4))
    assert abs(d - brute) < 1e-9
    assert abs(min_width([(0, 0), (4, 0), (4, 3), (0, 3)]) - 3) < 1e-9
    print("ok")
