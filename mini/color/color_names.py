"""Find the nearest named colour to a hex value.

Usage: python color_names.py [#rrggbb]
"""
import sys

NAMES = {
    "black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0), "lime": (0, 255, 0),
    "blue": (0, 0, 255), "yellow": (255, 255, 0), "cyan": (0, 255, 255), "magenta": (255, 0, 255),
    "gray": (128, 128, 128), "maroon": (128, 0, 0), "olive": (128, 128, 0), "green": (0, 128, 0),
    "purple": (128, 0, 128), "teal": (0, 128, 128), "navy": (0, 0, 128), "orange": (255, 165, 0),
    "pink": (255, 192, 203), "brown": (165, 42, 42), "gold": (255, 215, 0), "salmon": (250, 128, 114),
}


def nearest(rgb: tuple[int, int, int]) -> str:
    return min(NAMES, key=lambda n: sum((a - b) ** 2 for a, b in zip(NAMES[n], rgb)))


if __name__ == "__main__":
    assert nearest((250, 5, 5)) == "red"
    h = (sys.argv[1] if len(sys.argv) > 1 else "#ff7f50").lstrip("#")
    print(nearest((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))))
