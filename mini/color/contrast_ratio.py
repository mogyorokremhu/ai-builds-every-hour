"""WCAG contrast ratio between two colours.

Usage: python contrast_ratio.py [#fg] [#bg]
"""
import sys


def parse(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rel_lum(c: tuple[int, int, int]) -> float:
    def f(v: int) -> float:
        s = v / 255
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4
    r, g, b = (f(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la, lb = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main() -> None:
    fg = sys.argv[1] if len(sys.argv) > 1 else "#777777"
    bg = sys.argv[2] if len(sys.argv) > 2 else "#ffffff"
    r = contrast(parse(fg), parse(bg))
    print(f"{fg} on {bg}: {r:.2f}:1  AA-normal={'pass' if r >= 4.5 else 'fail'}  AAA-normal={'pass' if r >= 7 else 'fail'}")


if __name__ == "__main__":
    assert abs(contrast((0, 0, 0), (255, 255, 255)) - 21) < 1e-6
    main()
