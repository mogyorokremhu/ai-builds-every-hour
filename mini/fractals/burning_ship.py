"""Render the Burning Ship fractal as ASCII art."""

CHARS = " .:-=+*#%@"


def escape(c: complex, limit: int = 60) -> int:
    z = 0j
    for i in range(limit):
        z = complex(abs(z.real), abs(z.imag)) ** 2 + c
        if abs(z) > 2:
            return i
    return limit


def render(w: int = 70, h: int = 28, limit: int = 60) -> str:
    rows = []
    for y in range(h):
        row = ""
        for x in range(w):
            c = complex(-2.2 + 2.8 * x / w, -2.0 + 2.4 * y / h)
            n = escape(c, limit)
            row += CHARS[min(n * (len(CHARS) - 1) // limit, len(CHARS) - 1)]
        rows.append(row)
    return "\n".join(rows)


if __name__ == "__main__":
    print(render())
