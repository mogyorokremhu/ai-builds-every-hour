"""A layered star flower made of rotated polygons."""
import turtle

t = turtle.Turtle(visible=False)
turtle.bgcolor("black")
turtle.tracer(0)
colors = ["#ff595e", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93"]
for i in range(72):
    t.pencolor(colors[i % len(colors)])
    for _ in range(5):
        t.forward(200)
        t.right(144)
    t.right(5)
turtle.update()
turtle.done()
