"""Variable-length integers: LEB128 (unsigned/signed) and protobuf ZigZag."""


def uleb_encode(n: int) -> bytes:
    if n < 0:
        raise ValueError("unsigned only")
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def uleb_decode(data: bytes) -> tuple[int, int]:
    """Return (value, bytes_consumed)."""
    n = shift = 0
    for i, b in enumerate(data):
        n |= (b & 0x7F) << shift
        if not b & 0x80:
            return n, i + 1
        shift += 7
    raise ValueError("truncated varint")


def sleb_encode(n: int) -> bytes:
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if (n == 0 and not b & 0x40) or (n == -1 and b & 0x40):
            out.append(b)
            return bytes(out)
        out.append(b | 0x80)


def sleb_decode(data: bytes) -> tuple[int, int]:
    n = shift = 0
    for i, b in enumerate(data):
        n |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            if b & 0x40:
                n -= 1 << shift
            return n, i + 1
    raise ValueError("truncated varint")


def zigzag(n: int) -> int:
    return (n << 1) if n >= 0 else ((-n) << 1) - 1


def unzigzag(z: int) -> int:
    return (z >> 1) if not z & 1 else -((z + 1) >> 1)


if __name__ == "__main__":
    assert uleb_encode(624485) == bytes([0xE5, 0x8E, 0x26])
    assert sleb_encode(-123456) == bytes([0xC0, 0xBB, 0x78])
    for v in (0, 1, 127, 128, 300, 2**32, 2**63):
        assert uleb_decode(uleb_encode(v)) == (v, len(uleb_encode(v)))
    for v in (0, 1, -1, 63, -64, 64, -65, -123456, 2**40, -(2**40)):
        assert sleb_decode(sleb_encode(v))[0] == v
        assert unzigzag(zigzag(v)) == v
    print("uleb(300) =", uleb_encode(300).hex(), "| zigzag(-3) =", zigzag(-3))
    print("ok")
