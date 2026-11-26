"""1-D collisions between two masses with a coefficient of restitution."""


def collide(m1: float, v1: float, m2: float, v2: float, e: float = 1.0):
    """Return post-collision velocities (conserves momentum; e=1 elastic, e=0 sticky)."""
    total = m1 + m2
    p = m1 * v1 + m2 * v2
    return (p + m2 * e * (v2 - v1)) / total, (p + m1 * e * (v1 - v2)) / total


def kinetic(m1: float, v1: float, m2: float, v2: float) -> float:
    return 0.5 * m1 * v1 * v1 + 0.5 * m2 * v2 * v2


def main() -> None:
    for e in (1.0, 0.5, 0.0):
        a, b = collide(2.0, 3.0, 1.0, -1.0, e)
        lost = kinetic(2, 3, 1, -1) - kinetic(2, a, 1, b)
        print(f"e={e:.1f}: v1'={a:.3f} v2'={b:.3f} momentum={2*a+b:.3f} energy lost={lost:.3f}")


if __name__ == "__main__":
    main()
