"""Convert colours between hex, RGB and HSL (`python hex_rgb_hsl.py "#ff8800"`)."""
import colorsys
import sys


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def rgb_to_hsl(r: int, g: int, b: int) -> tuple[int, int, int]:
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return round(h * 360) % 360, round(s * 100), round(l * 100)


def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return round(r * 255), round(g * 255), round(b * 255)


def main() -> None:
    src = sys.argv[1] if len(sys.argv) > 1 else "#ff8800"
    r, g, b = hex_to_rgb(src)
    h, s, l = rgb_to_hsl(r, g, b)
    print(f"hex  {rgb_to_hex(r, g, b)}")
    print(f"rgb  ({r}, {g}, {b})")
    print(f"hsl  ({h}deg, {s}%, {l}%)")
    print(f"back {rgb_to_hex(*hsl_to_rgb(h, s, l))}")


if __name__ == "__main__":
    main()
