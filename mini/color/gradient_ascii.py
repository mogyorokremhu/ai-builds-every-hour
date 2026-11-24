"""Linear colour gradient as truecolor bars plus an ASCII luminance ramp.

Usage: python gradient_ascii.py [#from] [#to] [width]
"""
import sys

RAMP = " .:-=+*#%@"


def lerp(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))  # type: ignore[return-value]


def parse(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def luminance(c: tuple[int, int, int]) -> float:
    return (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255


def main() -> None:
    a = parse(sys.argv[1] if len(sys.argv) > 1 else "#ff0066")
    b = parse(sys.argv[2] if len(sys.argv) > 2 else "#00ccff")
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    colors = [lerp(a, b, i / (width - 1)) for i in range(width)]
    print("".join(f"\x1b[48;2;{r};{g};{bl}m \x1b[0m" for r, g, bl in colors))
    print("".join(RAMP[min(9, int(luminance(c) * 10))] for c in colors))


if __name__ == "__main__":
    main()
