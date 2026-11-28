"""Classic 2D Perlin gradient noise with fractal (octave) layering, rendered as ASCII. Usage: python perlin.py [seed] [octaves]"""
import math
import random
import sys


class Perlin:
    def __init__(self, seed: int = 0) -> None:
        p = list(range(256))
        random.Random(seed).shuffle(p)
        self.p = p + p

    @staticmethod
    def fade(t: float) -> float:
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def grad(h: int, x: float, y: float) -> float:
        a = h & 3
        return (x if a & 1 else -x) + (y if a & 2 else -y)

    def noise(self, x: float, y: float) -> float:
        """Perlin noise in roughly [-1, 1]; zero at integer lattice points."""
        xi, yi = math.floor(x) & 255, math.floor(y) & 255
        xf, yf = x - math.floor(x), y - math.floor(y)
        u, v = self.fade(xf), self.fade(yf)
        p = self.p
        aa, ab = p[p[xi] + yi], p[p[xi] + yi + 1]
        ba, bb = p[p[xi + 1] + yi], p[p[xi + 1] + yi + 1]
        x1 = self.grad(aa, xf, yf) * (1 - u) + self.grad(ba, xf - 1, yf) * u
        x2 = self.grad(ab, xf, yf - 1) * (1 - u) + self.grad(bb, xf - 1, yf - 1) * u
        return x1 * (1 - v) + x2 * v

    def fractal(self, x: float, y: float, octaves: int = 4) -> float:
        total, amp, freq, norm = 0.0, 1.0, 1.0, 0.0
        for _ in range(octaves):
            total += self.noise(x * freq, y * freq) * amp
            norm += amp
            amp *= 0.5
            freq *= 2
        return total / norm


def render(seed: int = 3, octaves: int = 4, w: int = 64, h: int = 22) -> str:
    pn = Perlin(seed)
    ramp = " .:-=+*#%@"
    out = []
    for j in range(h):
        line = ""
        for i in range(w):
            v = (pn.fractal(i * 0.07, j * 0.14, octaves) + 0.7) / 1.4
            line += ramp[max(0, min(int(v * len(ramp)), len(ramp) - 1))]
        out.append(line)
    return "\n".join(out)


if __name__ == "__main__":
    a = sys.argv[1:]
    print(render(int(a[0]) if a else 3, int(a[1]) if len(a) > 1 else 4))
