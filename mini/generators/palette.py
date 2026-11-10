"""Random harmonious colour palettes printed as hex codes with ANSI swatches.

Usage: python palette.py [scheme] [seed]   scheme: analogous | complement | triad | mono
"""
import colorsys
import random
import sys


def hsl_hex(h: float, s: float, l: float) -> str:
    """Convert HSL (0-1 floats) to a #rrggbb string."""
    r, g, b = colorsys.hls_to_rgb(h % 1.0, l, s)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def palette(scheme: str, rng: random.Random) -> list[str]:
    """Return five hex colours following the given colour-theory scheme."""
    base = rng.random()
    offsets = {
        "analogous": [-0.17, -0.08, 0, 0.08, 0.17],
        "complement": [0, 0.04, 0.5, 0.54, 0.5],
        "triad": [0, 1 / 3, 2 / 3, 0.03, 1 / 3 + 0.03],
        "mono": [0, 0, 0, 0, 0],
    }[scheme]
    out = []
    for i, off in enumerate(offsets):
        light = 0.25 + 0.12 * i if scheme == "mono" else rng.uniform(0.35, 0.7)
        out.append(hsl_hex(base + off, rng.uniform(0.5, 0.85), light))
    return out


if __name__ == "__main__":
    scheme = sys.argv[1] if len(sys.argv) > 1 else "analogous"
    rng = random.Random(int(sys.argv[2])) if len(sys.argv) > 2 else random.Random()
    for hexcode in palette(scheme, rng):
        r, g, b = (int(hexcode[i:i + 2], 16) for i in (1, 3, 5))
        print(f"\x1b[48;2;{r};{g};{b}m      \x1b[0m {hexcode}")
