"""Colour-harmony palettes from a base hue, printed as ANSI swatches.

Usage: python palette_harmony.py [hue 0-359]
"""
import colorsys
import sys

SCHEMES = {
    "complementary": [0, 180],
    "analogous": [-30, 0, 30],
    "triadic": [0, 120, 240],
    "tetradic": [0, 90, 180, 270],
    "split-complementary": [0, 150, 210],
}


def swatch(hue: float, s: float = 0.7, l: float = 0.5) -> tuple[str, str]:
    r, g, b = (round(c * 255) for c in colorsys.hls_to_rgb((hue % 360) / 360, l, s))
    block = f"\x1b[48;2;{r};{g};{b}m      \x1b[0m"
    return block, f"#{r:02x}{g:02x}{b:02x}"


def main() -> None:
    base = float(sys.argv[1]) if len(sys.argv) > 1 else 200
    for name, offsets in SCHEMES.items():
        print(f"{name:20}", end="")
        hexes = []
        for off in offsets:
            block, hx = swatch(base + off)
            print(block, end=" ")
            hexes.append(hx)
        print(" ".join(hexes))


if __name__ == "__main__":
    main()
