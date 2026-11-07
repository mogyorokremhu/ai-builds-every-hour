"""Spiral galaxy drawn with turtle: rotating rainbow dots."""
import colorsys
import math
import turtle

t = turtle.Turtle(visible=False)
turtle.bgcolor("black")
turtle.tracer(0)
t.penup()
for i in range(1800):
    angle = i * 137.508  # golden angle
    r = 4 * math.sqrt(i)
    t.goto(r * math.cos(math.radians(angle)), r * math.sin(math.radians(angle)))
    t.dot(2 + i / 600, colorsys.hsv_to_rgb(i / 1800, 0.8, 1))
turtle.update()
turtle.done()
