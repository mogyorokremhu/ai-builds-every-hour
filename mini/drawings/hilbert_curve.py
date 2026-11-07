"""Hilbert space-filling curve of order 6, shading from violet to gold along its path."""
import turtle

ORDER = 6
SIZE = 512


def hilbert_points(order: int) -> list[tuple[int, int]]:
    """Grid points of a Hilbert curve visiting every cell of a 2^order square once."""
    n = 1 << order
    pts = []
    for d in range(n * n):
        x = y = 0
        t = d
        s = 1
        while s < n:
            rx = 1 & (t // 2)
            ry = 1 & (t ^ rx)
            if ry == 0:
                if rx == 1:
                    x, y = s - 1 - x, s - 1 - y
                x, y = y, x
            x += s * rx
            y += s * ry
            t //= 4
            s *= 2
        pts.append((x, y))
    return pts


def lerp(a: tuple[float, ...], b: tuple[float, ...], f: float) -> tuple[float, ...]:
    return tuple(x + (y - x) * f for x, y in zip(a, b))


def main() -> None:
    screen = turtle.Screen()
    screen.bgcolor("#111018")
    screen.tracer(0)
    t = turtle.Turtle(visible=False)
    t.pensize(2)
    pts = hilbert_points(ORDER)
    cell = SIZE / (1 << ORDER)
    off = -SIZE / 2 + cell / 2
    t.penup()
    t.goto(off + pts[0][0] * cell, off + pts[0][1] * cell)
    t.pendown()
    violet, gold = (0.55, 0.25, 0.95), (1.0, 0.8, 0.2)
    for i, (x, y) in enumerate(pts[1:], 1):
        t.pencolor(lerp(violet, gold, i / len(pts)))
        t.goto(off + x * cell, off + y * cell)
    screen.update()
    turtle.done()


if __name__ == "__main__":
    main()
