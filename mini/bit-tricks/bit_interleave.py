"""Morton codes: interleave the bits of x and y (Z-order curve)."""


def spread(v: int) -> int:
    """Insert a zero bit between each bit of a 16-bit value."""
    v &= 0xFFFF
    v = (v | (v << 8)) & 0x00FF00FF
    v = (v | (v << 4)) & 0x0F0F0F0F
    v = (v | (v << 2)) & 0x33333333
    v = (v | (v << 1)) & 0x55555555
    return v


def compact(v: int) -> int:
    v &= 0x55555555
    v = (v | (v >> 1)) & 0x33333333
    v = (v | (v >> 2)) & 0x0F0F0F0F
    v = (v | (v >> 4)) & 0x00FF00FF
    v = (v | (v >> 8)) & 0x0000FFFF
    return v


def encode(x: int, y: int) -> int:
    return spread(x) | (spread(y) << 1)


def decode(z: int) -> tuple[int, int]:
    return compact(z), compact(z >> 1)


if __name__ == "__main__":
    for y in range(4):
        print(" ".join(f"{encode(x, y):2d}" for x in range(4)))
    for x, y in [(0, 0), (123, 456), (65535, 65535), (1, 0), (0, 1)]:
        assert decode(encode(x, y)) == (x, y)
    print("round-trips ok")
