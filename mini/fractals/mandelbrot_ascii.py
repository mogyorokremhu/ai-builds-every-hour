"""Render the Mandelbrot set as ASCII art."""

CHARS = " .:-=+*#%@"


def escape(c: complex, limit: int = 60) -> int:
    z = 0j
    for i in range(limit):
        z = z * z + c
        if abs(z) > 2:
            return i
    return limit


def render(w: int = 70, h: int = 24, limit: int = 60) -> str:
    rows = []
    for y in range(h):
        row = ""
        for x in range(w):
            c = complex(-2.2 + 3.2 * x / w, -1.2 + 2.4 * y / h)
            n = escape(c, limit)
            row += "@" if n == limit else CHARS[n * (len(CHARS) - 2) // limit]
        rows.append(row)
    return "\n".join(rows)


if __name__ == "__main__":
    print(render())
