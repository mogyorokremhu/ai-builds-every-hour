"""Lorenz attractor integrated with RK4 and projected onto the x-z plane in ASCII."""


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


def render(w: int = 70, h: int = 30, steps: int = 20000, dt: float = 0.01) -> str:
    s = (1.0, 1.0, 1.0)
    counts = [[0] * w for _ in range(h)]
    for i in range(steps):
        s = rk4(s, dt)
        if i < 200:
            continue
        col = int((s[0] + 25) / 50 * (w - 1))
        row = h - 1 - int(s[2] / 55 * (h - 1))
        if 0 <= col < w and 0 <= row < h:
            counts[row][col] += 1
    shades = " .:-=+*#%@"
    top = max(max(r) for r in counts) or 1
    return "\n".join(
        "".join(shades[min(9, int(9 * (c / top) ** 0.5))] for c in r).rstrip()
        for r in counts)


if __name__ == "__main__":
    print(render())
