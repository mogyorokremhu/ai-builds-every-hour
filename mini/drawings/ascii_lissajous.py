"""Lissajous figures in ASCII: x = sin(a t + d), y = sin(b t), several frequency pairs."""
import math

W, H = 38, 17
PAIRS = ((1, 2), (3, 2), (3, 4), (5, 4))
DENSITY = " .:*#"


def figure(a: int, b: int, delta: float = math.pi / 2) -> list[str]:
    """Plot one curve; cells the curve crosses more often get denser characters."""
    hits = [[0] * W for _ in range(H)]
    steps = 4000
    for i in range(steps):
        t = 2 * math.pi * i / steps
        x = int((math.sin(a * t + delta) + 1) / 2 * (W - 1))
        y = int((math.sin(b * t) + 1) / 2 * (H - 1))
        hits[y][x] += 1
    peak = max(max(r) for r in hits)
    return ["".join(DENSITY[min(len(DENSITY) - 1, math.ceil(v / peak * (len(DENSITY) - 1) * 3))] if v else " "
                    for v in row) for row in hits]


def main() -> None:
    figs = [(f"a={a} b={b}", figure(a, b)) for a, b in PAIRS]
    for left, right in zip(figs[::2], figs[1::2]):
        print(f"{left[0]:<{W}}    {right[0]}")
        for l_row, r_row in zip(left[1], right[1]):
            print(f"{l_row}    {r_row}")
        print()


if __name__ == "__main__":
    main()
