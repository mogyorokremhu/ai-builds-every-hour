"""SWAR byte tricks on 64-bit words: find a zero byte, broadcast, byte-wise add."""
M = (1 << 64) - 1
ONES = 0x0101010101010101
HIGHS = 0x8080808080808080


def broadcast(b: int) -> int:
    return (b & 0xFF) * ONES


def has_zero_byte(w: int) -> bool:
    return bool(((w - ONES) & ~w & HIGHS) & M)


def has_byte(w: int, b: int) -> bool:
    return has_zero_byte(w ^ broadcast(b))


def add_bytes(a: int, b: int) -> int:
    """Per-byte addition mod 256 with no carries between lanes."""
    low = (a & ~HIGHS & M) + (b & ~HIGHS & M)
    return (low ^ ((a ^ b) & HIGHS)) & M


def to_bytes(w: int) -> list[int]:
    return list(w.to_bytes(8, "little"))


if __name__ == "__main__":
    w = int.from_bytes(b"hello, w", "little")
    assert has_byte(w, ord("w")) and not has_byte(w, ord("z"))
    assert not has_zero_byte(w) and has_zero_byte(int.from_bytes(b"ab\0defgh", "little"))
    a = int.from_bytes(bytes([250, 1, 2, 3, 4, 5, 6, 255]), "little")
    b = int.from_bytes(bytes([10, 1, 2, 3, 4, 5, 6, 1]), "little")
    out = to_bytes(add_bytes(a, b))
    print(out)
    assert out == [4, 2, 4, 6, 8, 10, 12, 0]
    print("ok")
