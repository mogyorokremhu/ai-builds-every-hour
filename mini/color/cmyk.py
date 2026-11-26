"""Convert between RGB and CMYK (naive, device-independent formula).

Usage: python cmyk.py [#rrggbb]
"""
import sys


def rgb_to_cmyk(r: int, g: int, b: int) -> tuple[float, float, float, float]:
    if (r, g, b) == (0, 0, 0):
        return 0.0, 0.0, 0.0, 1.0
    rr, gg, bb = r / 255, g / 255, b / 255
    k = 1 - max(rr, gg, bb)
    return tuple((1 - c - k) / (1 - k) for c in (rr, gg, bb)) + (k,)  # type: ignore[return-value]


def cmyk_to_rgb(c: float, m: float, y: float, k: float) -> tuple[int, int, int]:
    return tuple(round(255 * (1 - v) * (1 - k)) for v in (c, m, y))  # type: ignore[return-value]


if __name__ == "__main__":
    assert rgb_to_cmyk(255, 0, 0) == (0.0, 1.0, 1.0, 0.0)
    assert cmyk_to_rgb(*rgb_to_cmyk(200, 100, 50)) == (200, 100, 50)
    h = (sys.argv[1] if len(sys.argv) > 1 else "#ff7f50").lstrip("#")
    rgb = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    print("CMYK %: C={:.0f} M={:.0f} Y={:.0f} K={:.0f}".format(*(100 * v for v in rgb_to_cmyk(*rgb))))
