"""Render tiny pixel sprites defined as text, scaled up with block characters."""

SPRITES = {
    "heart": [
        ".##.##.",
        "#######",
        "#######",
        ".#####.",
        "..###..",
        "...#...",
    ],
    "invader": [
        "..#.....#..",
        "...#...#...",
        "..#######..",
        ".##.###.##.",
        "###########",
        "#.#######.#",
        "#.#.....#.#",
        "...##.##...",
    ],
}


def render(rows: list[str], scale: int = 2) -> str:
    """Scale each pixel to scale x scale block characters."""
    out = []
    for row in rows:
        line = "".join(("██" if c == "#" else "  ") * scale for c in row)
        out.extend([line.rstrip()] * scale)
    return "\n".join(out)


if __name__ == "__main__":
    for name, rows in SPRITES.items():
        print(name)
        print(render(rows, 1))
        print()
