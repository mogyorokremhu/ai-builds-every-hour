"""Ordered (Bayer) and Floyd-Steinberg dithering of a generated gradient."""

BAYER4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def gradient(w: int, h: int) -> list[list[float]]:
    """Diagonal gradient with values in 0..1."""
    return [[(x + y) / (w + h - 2) for x in range(w)] for y in range(h)]


def bayer(img: list[list[float]]) -> list[str]:
    return ["".join("#" if v > (BAYER4[y % 4][x % 4] + 0.5) / 16 else "." for x, v in enumerate(r))
            for y, r in enumerate(img)]


def floyd_steinberg(img: list[list[float]]) -> list[str]:
    g = [r[:] for r in img]
    h, w = len(g), len(g[0])
    out = []
    for y in range(h):
        row = ""
        for x in range(w):
            old = g[y][x]
            new = 1.0 if old >= 0.5 else 0.0
            row += "#" if new else "."
            err = old - new
            for dx, dy, f in ((1, 0, 7), (-1, 1, 3), (0, 1, 5), (1, 1, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    g[ny][nx] += err * f / 16
        out.append(row)
    return out


if __name__ == "__main__":
    img = gradient(40, 12)
    print("Bayer ordered:"); print("\n".join(bayer(img)))
    print("\nFloyd-Steinberg:"); print("\n".join(floyd_steinberg(img)))
