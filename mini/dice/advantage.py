"""D&D advantage/disadvantage: exact distribution of d20 roll-twice-keep-best/worst."""
import sys


def distribution(sides: int, mode: str) -> list[float]:
    """P(result = v) for v = 1..sides. mode: 'adv', 'dis', or 'normal'."""
    out = []
    for v in range(1, sides + 1):
        if mode == "adv":
            out.append((2 * v - 1) / sides**2)
        elif mode == "dis":
            out.append((2 * (sides - v) + 1) / sides**2)
        else:
            out.append(1 / sides)
    return out


def main() -> None:
    sides = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    for mode in ("normal", "adv", "dis"):
        d = distribution(sides, mode)
        mean = sum((i + 1) * p for i, p in enumerate(d))
        hit = sum(d[10:])  # P(>= 11)
        print(f"{mode:6s} mean={mean:.3f} P(>=11)={hit:.3f}")


if __name__ == "__main__":
    main()
