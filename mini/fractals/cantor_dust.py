"""Print the Cantor set (and a 2D Cantor dust) as ASCII art."""


def cantor_row(width: int, depth: int) -> str:
    """Return one row of the Cantor set after `depth` removals."""
    cells = [True] * width

    def cut(lo: int, hi: int, d: int) -> None:
        if d == 0 or hi - lo < 3:
            return
        third = (hi - lo) // 3
        for i in range(lo + third, lo + 2 * third):
            cells[i] = False
        cut(lo, lo + third, d - 1)
        cut(lo + 2 * third, hi, d - 1)

    cut(0, width, depth)
    return "".join("#" if c else " " for c in cells)


def cantor_set(width: int = 81, depth: int = 4) -> str:
    return "\n".join(cantor_row(width, d) for d in range(depth + 1))


def cantor_dust(size: int = 27, depth: int = 3) -> str:
    """2D dust: a cell is filled iff both its row and column are in the set."""
    row = cantor_row(size, depth)
    return "\n".join("".join("#" if a == b == "#" else " " for b in row) if a == "#" else " " * size for a in row)


if __name__ == "__main__":
    print(cantor_set())
    print()
    print(cantor_dust())
