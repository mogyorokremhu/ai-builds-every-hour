"""Clifford strange attractor density plot.  python ascii_clifford_attractor.py"""
import math

def main(a=-1.4, b=1.6, c=1.0, d=0.7, w=78, h=36, n=200_000) -> None:
    counts = [[0] * w for _ in range(h)]
    x = y = 0.1
    for i in range(n):
        x, y = math.sin(a * y) + c * math.cos(a * x), math.sin(b * x) + d * math.cos(b * y)
        if i > 100:
            px = int((x + 2.4) / 4.8 * (w - 1))
            py = int((y + 2.4) / 4.8 * (h - 1))
            if 0 <= px < w and 0 <= py < h:
                counts[py][px] += 1
    top = max(max(r) for r in counts) or 1
    ramp = " .:-=+*#%@"
    for r in counts:
        print("".join(ramp[min(9, int(9 * math.sqrt(v / top)))] for v in r))

if __name__ == "__main__":
    main()
