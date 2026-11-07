"""ASCII mountain range: three ridgelines from midpoint displacement, a moon and stars.

Run with an optional seed:  python ascii_mountains.py 42
"""
import random
import sys

W, H = 78, 24
#: far to near: (fill glyph, roughness, highest peak as a fraction of H, height variation)
LAYERS = ((":", 0.9, 0.22, 0.30), ("%", 0.7, 0.42, 0.25), ("#", 0.5, 0.62, 0.22))


def ridge(width: int, roughness: float, rng: random.Random) -> list[float]:
    """1-D midpoint displacement: heights in [0, 1] for each column."""
    size = 1
    while size < width:
        size *= 2
    pts = [0.0] * (size + 1)
    pts[0], pts[size] = rng.random(), rng.random()
    step, scale = size, 1.0
    while step > 1:
        half = step // 2
        for i in range(half, size, step):
            pts[i] = (pts[i - half] + pts[i + half]) / 2 + rng.uniform(-scale, scale) * roughness
        step, scale = half, scale * 0.55
    lo, hi = min(pts), max(pts)
    return [(p - lo) / (hi - lo or 1) for p in pts[:width]]


def draw(seed: int) -> list[str]:
    rng = random.Random(seed)
    sky = [[" "] * W for _ in range(H)]
    for _ in range(45):
        sky[rng.randrange(H // 2)][rng.randrange(W)] = rng.choice(".·*+")
    mx, my = rng.randrange(8, W - 8), rng.randrange(2, 5)
    for dy in range(-2, 3):
        for dx in range(-4, 5):
            if (dx / 2) ** 2 + dy ** 2 <= 4.2:
                sky[my + dy][mx + dx] = "O" if (dx / 2) ** 2 + dy ** 2 < 2 else "o"
    for glyph, rough, peak, amp in LAYERS:
        heights = ridge(W, rough, rng)
        tops = [int(H * peak + (1 - h) * H * amp) for h in heights]
        for x, top in enumerate(tops):
            prev = tops[x - 1] if x else top
            edge = "/" if prev > top else "\\" if prev < top else "_"
            for y in range(max(0, top), H):
                sky[y][x] = edge if y == top else glyph
    return ["".join(row) for row in sky]


if __name__ == "__main__":
    print("\n".join(draw(int(sys.argv[1]) if len(sys.argv) > 1 else random.randrange(10**6))))
