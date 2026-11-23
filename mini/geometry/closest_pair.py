"""Closest pair of points: divide and conquer vs brute force. Usage: python closest_pair.py"""
import math
import random


def brute(pts):
    best = (math.inf, None, None)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = math.dist(pts[i], pts[j])
            if d < best[0]:
                best = (d, pts[i], pts[j])
    return best


def closest(pts):
    px = sorted(pts)

    def rec(p):
        if len(p) <= 3:
            return brute(p)
        mid = len(p) // 2
        midx = p[mid][0]
        best = min(rec(p[:mid]), rec(p[mid:]), key=lambda t: t[0])
        strip = sorted((q for q in p if abs(q[0] - midx) < best[0]), key=lambda q: q[1])
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= best[0]:
                    break
                d = math.dist(strip[i], strip[j])
                if d < best[0]:
                    best = (d, strip[i], strip[j])
        return best

    return rec(px)


if __name__ == "__main__":
    random.seed(7)
    for _ in range(50):
        pts = list({(random.randint(0, 100), random.randint(0, 100)) for _ in range(60)})
        assert abs(closest(pts)[0] - brute(pts)[0]) < 1e-9
    d, a, b = closest(pts)
    print(f"closest pair {a} {b} distance {d:.3f} (50 random checks passed)")
