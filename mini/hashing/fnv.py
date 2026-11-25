"""FNV-1a hash (32 and 64 bit) from scratch, checked against known vectors."""

def fnv1a(data: bytes, bits: int = 32) -> int:
    """Return the FNV-1a hash of data for 32 or 64 bits."""
    if bits == 32:
        h, prime, mask = 0x811C9DC5, 0x01000193, 0xFFFFFFFF
    elif bits == 64:
        h, prime, mask = 0xCBF29CE484222325, 0x100000001B3, 0xFFFFFFFFFFFFFFFF
    else:
        raise ValueError("bits must be 32 or 64")
    for b in data:
        h = ((h ^ b) * prime) & mask
    return h

if __name__ == "__main__":
    assert fnv1a(b"") == 0x811C9DC5
    assert fnv1a(b"a") == 0xE40C292C
    assert fnv1a(b"foobar") == 0xBF9CF968
    assert fnv1a(b"a", 64) == 0xAF63DC4C8601EC8C
    for w in ("hello", "world", "fnv"):
        print(f"{w:6} {fnv1a(w.encode()):08x} {fnv1a(w.encode(), 64):016x}")
