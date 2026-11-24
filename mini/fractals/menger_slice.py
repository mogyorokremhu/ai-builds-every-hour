"""Sierpinski carpet / Menger sponge cross-section drawn in ASCII."""


def in_carpet(x: int, y: int) -> bool:
    """True if (x, y) survives in the Sierpinski carpet."""
    while x or y:
        if x % 3 == 1 and y % 3 == 1:
            return False
        x //= 3
        y //= 3
    return True


def carpet(level: int = 3) -> str:
    n = 3 ** level
    return "\n".join("".join("#" if in_carpet(x, y) else " " for x in range(n)) for y in range(n))


def menger_cell(x: int, y: int, z: int) -> bool:
    """True if the unit cube (x, y, z) is part of the Menger sponge."""
    while x or y or z:
        ones = (x % 3 == 1) + (y % 3 == 1) + (z % 3 == 1)
        if ones >= 2:
            return False
        x //= 3
        y //= 3
        z //= 3
    return True


def menger_slice(level: int = 2, z: int = 0) -> str:
    n = 3 ** level
    return "\n".join("".join("#" if menger_cell(x, y, z) else " " for x in range(n)) for y in range(n))


if __name__ == "__main__":
    print(carpet(3))
    print()
    print(menger_slice(2, 1))
