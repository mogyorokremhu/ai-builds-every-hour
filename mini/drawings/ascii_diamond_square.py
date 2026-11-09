"""Diamond-square terrain heightmap shaded with characters (python ascii_diamond_square.py 7)."""
import random
import sys


def terrain(n: int = 5, seed: int = 1, rough: float = 0.55) -> list[list[float]]:
    rnd, size = random.Random(seed), 2 ** n + 1
    m = [[0.0] * size for _ in range(size)]
    for y, x in ((0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)):
        m[y][x] = rnd.random()
    step, amp = size - 1, 1.0
    while step > 1:
        half = step // 2
        for y in range(half, size, step):
            for x in range(half, size, step):
                a = (m[y - half][x - half] + m[y - half][x + half] + m[y + half][x - half] + m[y + half][x + half]) / 4
                m[y][x] = a + rnd.uniform(-amp, amp)
        for y in range(0, size, half):
            for x in range((y + half) % step, size, step):
                v = [m[y + dy][x + dx] for dy, dx in ((-half, 0), (half, 0), (0, -half), (0, half))
                     if 0 <= y + dy < size and 0 <= x + dx < size]
                m[y][x] = sum(v) / len(v) + rnd.uniform(-amp, amp)
        step, amp = half, amp * rough
    return m


if __name__ == "__main__":
    m = terrain(5, int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    flat = [v for r in m for v in r]
    lo, hi = min(flat), max(flat)
    shades = "~.:-=+*#%@"
    for r in m:
        print("".join(shades[min(9, int((v - lo) / (hi - lo + 1e-9) * 10))] * 2 for v in r))
