"""Lotka-Volterra predator/prey with a text sparkline. Usage: python predator_prey.py [steps]"""
import sys

BARS = " ▁▂▃▄▅▆▇█"


def run(steps: int = 400, prey: float = 10.0, pred: float = 5.0, dt: float = 0.02):
    a, b, c, d = 1.1, 0.4, 0.4, 0.1
    hist = []
    for _ in range(steps):
        prey, pred = prey + (a * prey - b * prey * pred) * dt, pred + (d * prey * pred - c * pred) * dt
        hist.append((prey, pred))
    return hist


def spark(vals, width=60):
    step = max(1, len(vals) // width)
    vals = vals[::step]
    lo, hi = min(vals), max(vals)
    return "".join(BARS[int((v - lo) / (hi - lo or 1) * 8)] for v in vals)


if __name__ == "__main__":
    h = run(int(sys.argv[1]) if len(sys.argv) > 1 else 400)
    print("prey:", spark([p for p, _ in h]))
    print("pred:", spark([q for _, q in h]))
