"""Mix several hex colours (average in linear light) and print the result.

Usage: python mix_colors.py #ff0000 #0000ff ...
"""
import sys


def to_lin(v: int) -> float:
    s = v / 255
    return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4


def to_srgb(x: float) -> int:
    s = 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
    return max(0, min(255, round(s * 255)))


def mix(hexes: list[str]) -> str:
    chans = [[to_lin(int(h.lstrip("#")[i:i + 2], 16)) for i in (0, 2, 4)] for h in hexes]
    out = [to_srgb(sum(c[i] for c in chans) / len(chans)) for i in range(3)]
    return "#%02x%02x%02x" % tuple(out)


if __name__ == "__main__":
    assert mix(["#000000", "#ffffff"]) == "#bcbcbc"
    args = sys.argv[1:] or ["#ff0000", "#0000ff"]
    print(f"mix of {' '.join(args)} = {mix(args)}")
