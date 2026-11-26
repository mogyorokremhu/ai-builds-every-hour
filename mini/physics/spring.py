"""Damped spring-mass oscillator (semi-implicit Euler) with an ASCII displacement plot."""
import math


def simulate(k: float = 20.0, m: float = 1.0, c: float = 0.8, x0: float = 1.0,
             dt: float = 0.01, steps: int = 400):
    """Return the list of displacements for x'' = -(k/m)x - (c/m)x'."""
    x, v, out = x0, 0.0, []
    for _ in range(steps):
        v += (-(k / m) * x - (c / m) * v) * dt
        x += v * dt
        out.append(x)
    return out


def main() -> None:
    xs = simulate()
    zeta = 0.8 / (2 * math.sqrt(20.0 * 1.0))
    print(f"damping ratio = {zeta:.3f}, final |x| = {abs(xs[-1]):.4f}")
    for x in xs[::10]:
        col = int(30 + x * 28)
        row = [" "] * 61
        row[30] = "|"
        row[max(0, min(60, col))] = "*"
        print("".join(row))


if __name__ == "__main__":
    main()
