"""Simulate a pendulum with RK4 and compare with the small-angle period."""
import math
import sys

G = 9.81


def simulate(theta0: float, length: float = 1.0, dt: float = 0.001, t_max: float = 5.0):
    """Yield (t, theta) samples for a pendulum released from rest."""
    def acc(th: float) -> float:
        return -G / length * math.sin(th)

    th, om, t = theta0, 0.0, 0.0
    while t <= t_max:
        yield t, th
        k1t, k1o = om, acc(th)
        k2t, k2o = om + dt / 2 * k1o, acc(th + dt / 2 * k1t)
        k3t, k3o = om + dt / 2 * k2o, acc(th + dt / 2 * k2t)
        k4t, k4o = om + dt * k3o, acc(th + dt * k3t)
        th += dt / 6 * (k1t + 2 * k2t + 2 * k3t + k4t)
        om += dt / 6 * (k1o + 2 * k2o + 2 * k3o + k4o)
        t += dt


def measured_period(theta0: float, length: float = 1.0) -> float:
    """Period measured from the second downward zero crossing of the angle."""
    crossings, prev = [], None
    for t, th in simulate(theta0, length, t_max=10.0):
        if prev is not None and prev > 0 >= th:
            crossings.append(t)
        prev = th
    return crossings[1] - crossings[0] if len(crossings) > 1 else float("nan")


if __name__ == "__main__":
    for deg in (5, 30, 60, 90):
        small = 2 * math.pi * math.sqrt(1.0 / G)
        p = measured_period(math.radians(deg))
        print(f"{deg:>3} deg: period {p:.4f}s (small-angle {small:.4f}s, +{(p / small - 1) * 100:.1f}%)")
