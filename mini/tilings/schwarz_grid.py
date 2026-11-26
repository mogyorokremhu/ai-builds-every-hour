"""Regular polygon tiling check: which regular n-gons tile the plane, via angle sums."""
from fractions import Fraction


def interior(n: int) -> Fraction:
    return Fraction((n - 2) * 180, n)


def regular_tilings() -> list[int]:
    """n such that 360 / interior angle is an integer."""
    return [n for n in range(3, 50) if (Fraction(360) / interior(n)).denominator == 1]


def vertex_configs(max_n: int = 12) -> list[tuple[int, ...]]:
    """Vertex configurations of regular polygons summing to 360 degrees (sorted)."""
    out: set[tuple[int, ...]] = set()

    def rec(cur: list[int], total: Fraction, lo: int) -> None:
        if total == 360 and len(cur) >= 3:
            out.add(tuple(cur))
        if total >= 360:
            return
        for n in range(lo, max_n + 1):
            rec(cur + [n], total + interior(n), n)

    rec([], Fraction(0), 3)
    return sorted(out)


if __name__ == "__main__":
    assert regular_tilings() == [3, 4, 6]
    cfgs = vertex_configs()
    assert (3, 3, 3, 3, 3, 3) in cfgs and (4, 4, 4, 4) in cfgs and (3, 12, 12) in cfgs
    print(len(cfgs), "vertex configurations;", regular_tilings(), "tile alone")
