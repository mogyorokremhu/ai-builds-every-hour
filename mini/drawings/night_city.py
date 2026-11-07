"""Random night city skyline with lit windows and a moon."""
import random
import turtle

random.seed()
t = turtle.Turtle(visible=False)
turtle.setup(800, 500)
turtle.bgcolor("#0b0d2a")
turtle.tracer(0)


def rect(x, y, w, h, color):
    t.penup(); t.goto(x, y); t.pendown()
    t.fillcolor(color); t.pencolor(color); t.begin_fill()
    for side in (w, h, w, h):
        t.forward(side); t.left(90)
    t.end_fill()


t.penup(); t.goto(260, 140); t.dot(80, "#f5f3ce")
for _ in range(120):
    t.goto(random.randint(-400, 400), random.randint(0, 250)); t.dot(2, "white")
x = -400
while x < 400:
    w, h = random.randint(40, 90), random.randint(80, 320)
    rect(x, -250, w, h, "#1c1f3f")
    for wx in range(x + 8, x + w - 10, 14):
        for wy in range(-240, -250 + h - 14, 18):
            if random.random() < 0.35:
                rect(wx, wy, 7, 9, "#ffd166")
    x += w + random.randint(0, 6)
turtle.update()
turtle.done()
