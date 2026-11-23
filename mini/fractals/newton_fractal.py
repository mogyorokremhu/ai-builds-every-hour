"""Newton fractal for z^3 - 1: each root gets its own character."""

ROOTS = [complex(1, 0), complex(-0.5, 3 ** 0.5 / 2), complex(-0.5, -(3 ** 0.5) / 2)]
CHARS = "#o+"


def basin(z: complex, limit: int = 30) -> int:
    for _ in range(limit):
        if z == 0:
            return -1
        z = z - (z ** 3 - 1) / (3 * z ** 2)
        for i, r in enumerate(ROOTS):
            if abs(z - r) < 1e-6:
                return i
    return -1


def render(w: int = 70, h: int = 28) -> str:
    rows = []
    for y in range(h):
        row = ""
        for x in range(w):
            i = basin(complex(-2 + 4 * x / w, -1.5 + 3 * y / h))
            row += "." if i < 0 else CHARS[i]
        rows.append(row)
    return "\n".join(rows)


if __name__ == "__main__":
    print(render())
