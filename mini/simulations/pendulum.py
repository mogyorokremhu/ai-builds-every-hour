"""Simple pendulum via RK4; compares to the small-angle period. Usage: python pendulum.py [theta0_degrees]"""
import math
import sys


def period(theta0: float, g: float = 9.81, length: float = 1.0, dt: float = 0.001) -> float:
    """Measure the period by integrating until the angle crosses zero downward twice."""
    def acc(th):
        return -g / length * math.sin(th)

    th, om, t = theta0, 0.0, 0.0
    crossings = []
    prev = th
    while len(crossings) < 2 and t < 20:
        k1t, k1o = om, acc(th)
        k2t, k2o = om + dt / 2 * k1o, acc(th + dt / 2 * k1t)
        k3t, k3o = om + dt / 2 * k2o, acc(th + dt / 2 * k2t)
        k4t, k4o = om + dt * k3o, acc(th + dt * k3t)
        th += dt / 6 * (k1t + 2 * k2t + 2 * k3t + k4t)
        om += dt / 6 * (k1o + 2 * k2o + 2 * k3o + k4o)
        t += dt
        if prev > 0 >= th:
            crossings.append(t)
        prev = th
    return crossings[1] - crossings[0] if len(crossings) == 2 else float("nan")


if __name__ == "__main__":
    deg = float(sys.argv[1]) if len(sys.argv) > 1 else 60.0
    small = 2 * math.pi * math.sqrt(1.0 / 9.81)
    print(f"small-angle period: {small:.4f}s")
    for d in (5, 30, deg, 120):
        print(f"theta0={d:>5.1f} deg  period={period(math.radians(d)):.4f}s")
