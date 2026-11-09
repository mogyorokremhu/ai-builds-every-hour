"""Colour converter: python hexcolor.py #ff8800 | rgb 255 136 0 | hsl 32 100 50 (also luminance + contrast)."""
import colorsys, sys


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def rgb_to_hsl(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return round(h * 360), round(s * 100), round(l * 100)


def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return round(r * 255), round(g * 255), round(b * 255)


def luminance(rgb):
    f = lambda c: (c / 255 / 12.92) if c / 255 <= 0.03928 else ((c / 255 + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        assert hex_to_rgb("#f80") == (255, 136, 0)
        assert rgb_to_hex(255, 136, 0) == "#ff8800"
        assert rgb_to_hsl(255, 0, 0) == (0, 100, 50)
        assert hsl_to_rgb(120, 100, 50) == (0, 255, 0)
        assert round(contrast((0, 0, 0), (255, 255, 255))) == 21
        print("ok")
        sys.exit()
    if a and a[0] == "rgb":
        rgb = tuple(map(int, a[1:4]))
    elif a and a[0] == "hsl":
        rgb = hsl_to_rgb(*map(float, a[1:4]))
    else:
        rgb = hex_to_rgb(a[0])
    print(rgb_to_hex(*rgb), rgb, "hsl%s" % (rgb_to_hsl(*rgb),))
    print("contrast vs white %.2f, vs black %.2f" % (contrast(rgb, (255,) * 3), contrast(rgb, (0, 0, 0))))
