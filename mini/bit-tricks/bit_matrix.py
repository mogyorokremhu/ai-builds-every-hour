"""8x8 bit matrices packed in a 64-bit int: transpose, rotate, and print."""


def get(m: int, r: int, c: int) -> int:
    return (m >> (r * 8 + c)) & 1


def from_rows(rows: list[str]) -> int:
    m = 0
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "#":
                m |= 1 << (r * 8 + c)
    return m


def transpose(m: int) -> int:
    out = 0
    for r in range(8):
        for c in range(8):
            if get(m, r, c):
                out |= 1 << (c * 8 + r)
    return out


def flip_vertical(m: int) -> int:
    return int.from_bytes(m.to_bytes(8, "little")[::-1], "little")


def rotate90(m: int) -> int:
    return flip_vertical(transpose(m))


def show(m: int) -> str:
    return "\n".join("".join("#" if get(m, r, c) else "." for c in range(8)) for r in range(8))


if __name__ == "__main__":
    arrow = from_rows(["...#....", "..###...", ".#.#.#..", "...#....", "...#....", "...#....", "...#....", "........"])
    print(show(arrow)); print()
    print(show(rotate90(arrow)))
    assert transpose(transpose(arrow)) == arrow
    m = arrow
    for _ in range(4):
        m = rotate90(m)
    assert m == arrow
    print("ok")
