"""Scale2x (EPX) pixel-art upscaler on text bitmaps."""

SPRITE = """\
..##..
.#..#.
#....#
#.##.#
.#..#.
..##..
""".splitlines()


def scale2x(g: list[str]) -> list[str]:
    h, w = len(g), len(g[0])

    def px(x: int, y: int) -> str:
        return g[min(max(y, 0), h - 1)][min(max(x, 0), w - 1)]

    out = []
    for y in range(h):
        top, bot = [], []
        for x in range(w):
            p, a, b, c, d = px(x, y), px(x, y - 1), px(x + 1, y), px(x - 1, y), px(x, y + 1)
            e = [p] * 4
            if c == a and c != d and a != b:
                e[0] = a
            if a == b and a != c and b != d:
                e[1] = b
            if d == c and d != b and c != a:
                e[2] = c
            if b == d and b != a and d != c:
                e[3] = d
            top += [e[0], e[1]]
            bot += [e[2], e[3]]
        out += ["".join(top), "".join(bot)]
    return out


if __name__ == "__main__":
    big = scale2x(SPRITE)
    assert len(big) == 12 and all(len(r) == 12 for r in big)
    print("\n".join(big))
