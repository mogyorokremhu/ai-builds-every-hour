"""Newton fractal for z^3 - 1 in the terminal: each root gets its own character."""
import cmath

ROOTS = [cmath.exp(2j * cmath.pi * k / 3) for k in range(3)]
CHARS = "#o+"


def basin(z: complex, iters: int = 30) -> str:
    """Return the character of the root Newton's method converges to from z."""
    for _ in range(iters):
        if z == 0:
            return " "
        z = z - (z**3 - 1) / (3 * z**2)
        for root, ch in zip(ROOTS, CHARS):
            if abs(z - root) < 1e-6:
                return ch
    return "."


def render(width: int = 70, height: int = 30, span: float = 1.6) -> str:
    rows = []
    for j in range(height):
        y = span - 2 * span * j / (height - 1)
        rows.append("".join(basin(complex(-span + 2 * span * i / (width - 1), y)) for i in range(width)))
    return "\n".join(rows)


if __name__ == "__main__":
    print(render())
