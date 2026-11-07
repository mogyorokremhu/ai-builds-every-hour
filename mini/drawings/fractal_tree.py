"""Recursive fractal tree that changes from brown trunk to green leaves."""
import turtle

t = turtle.Turtle(visible=False)
turtle.bgcolor("#101820")
turtle.tracer(0)
turtle.colormode(255)


def branch(length: float, depth: int) -> None:
    if depth == 0:
        return
    g = int(80 + 175 * (1 - depth / 11))
    t.pencolor(120 - depth * 8, g, 40)
    t.pensize(depth)
    t.forward(length)
    t.left(25)
    branch(length * 0.72, depth - 1)
    t.right(50)
    branch(length * 0.72, depth - 1)
    t.left(25)
    t.backward(length)


t.penup(); t.goto(0, -260); t.setheading(90); t.pendown()
branch(140, 11)
turtle.update()
turtle.done()
