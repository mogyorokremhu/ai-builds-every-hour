"""Koch snowflake: three Koch curves of depth 4, coloured from ice blue to white."""
import turtle

DEPTH = 4
SIZE = 360


def koch(t: turtle.Turtle, length: float, depth: int) -> None:
    """Draw one Koch curve: replace each segment with four of a third the length."""
    if depth == 0:
        t.forward(length)
        return
    for angle in (60, -120, 60, 0):
        koch(t, length / 3, depth - 1)
        t.left(angle)


def main() -> None:
    screen = turtle.Screen()
    screen.bgcolor("#0b1d3a")
    screen.tracer(0)
    t = turtle.Turtle(visible=False)
    t.penup()
    t.goto(-SIZE / 2, SIZE / 3.5)
    t.pendown()
    t.pensize(2)
    for i, color in enumerate(("#7fdbff", "#b8ecff", "#ffffff")):
        t.pencolor(color)
        koch(t, SIZE, DEPTH)
        t.right(120)
    screen.update()
    turtle.done()


if __name__ == "__main__":
    main()
