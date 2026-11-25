"""Lorenz attractor (x-z projection) integrated with RK4 and plotted as text.

Usage: python lorenz_attractor_ascii.py [steps]   (default 20000)
"""
import sys


def deriv(s, sigma=10.0, rho=28.0, beta=8 / 3):
    x, y, z = s
    return (sigma * (y - x), x * (rho - z) - y, x * y - beta * z)


def rk4(s, dt):
    def add(a, b, k):
        return tuple(ai + k * bi for ai, bi in zip(a, b))
    k1 = deriv(s)
    k2 = deriv(add(s, k1, dt / 2))
    k3 = deriv(add(s, k2, dt / 2))
    k4 = deriv(add(s, k3, dt))
    return tuple(si + dt / 6 * (a + 2 * b + 2 * c + d)
                 for si, a, b, c, d in zip(s, k1, k2, k3, k4))


def trajectory(steps, dt=0.005):
    s = (1.0, 1.0, 1.0)
    out = []
    for _ in range(steps):
        s = rk4(s, dt)
        out.append(s)
    return out


def render(steps=20000, width=72, height=30):
    pts = trajectory(steps)[500:]
    xs = [p[0] for p in pts]
    zs = [p[2] for p in pts]
    x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
    counts = [[0] * width for _ in range(height)]
    for x, _, z in pts:
        c = int((x - x0) / (x1 - x0) * (width - 1))
        r = int((1 - (z - z0) / (z1 - z0)) * (height - 1))
        counts[r][c] += 1
    ramp = " .:-=+*#%@"
    peak = max(max(r) for r in counts)
    return "\n".join(
        "".join(ramp[min(9, int(v / peak * 9 + (0.99 if v else 0)))] for v in row).rstrip()
        for row in counts)


if __name__ == "__main__":
    print(render(int(sys.argv[1]) if len(sys.argv) > 1 else 20000))
