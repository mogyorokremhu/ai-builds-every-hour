"""Sierpinski triangle via the chaos game — 30,000 random points."""
import random
import turtle

t = turtle.Turtle(visible=False)
turtle.bgcolor("black")
turtle.tracer(0)
t.penup()
corners = [(-300, -260), (300, -260), (0, 260)]
colors = ["#ef476f", "#06d6a0", "#118ab2"]
x, y = 0.0, 0.0
for _ in range(30000):
    i = random.randrange(3)
    cx, cy = corners[i]
    x, y = (x + cx) / 2, (y + cy) / 2
    t.goto(x, y)
    t.dot(2, colors[i])
turtle.update()
turtle.done()
