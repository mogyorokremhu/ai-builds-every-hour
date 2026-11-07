"""Heighway dragon curve built from an L-system, drawn as a rainbow."""
import colorsys
import turtle

ITERATIONS = 12
STEP = 4


def dragon(iterations: int) -> str:
    """L-system: X -> X+YF+, Y -> -FX-Y (F draws, +/- turn 90 degrees)."""
    s = "FX"
    rules = {"X": "X+YF+", "Y": "-FX-Y"}
    for _ in range(iterations):
        s = "".join(rules.get(ch, ch) for ch in s)
    return s


def main() -> None:
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.tracer(0)
    t = turtle.Turtle(visible=False)
    t.penup()
    t.goto(120, 80)
    t.pendown()
    program = dragon(ITERATIONS)
    total = program.count("F")
    drawn = 0
    for ch in program:
        if ch == "F":
            r, g, b = colorsys.hsv_to_rgb(drawn / total, 0.85, 1.0)
            t.pencolor(r, g, b)
            t.forward(STEP)
            drawn += 1
        elif ch == "+":
            t.right(90)
        elif ch == "-":
            t.left(90)
    screen.update()
    turtle.done()


if __name__ == "__main__":
    main()
