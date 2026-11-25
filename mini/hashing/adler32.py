"""Adler-32 checksum, checked against zlib."""
import zlib


def adler32(data: bytes) -> int:
    a, b = 1, 0
    for byte in data:
        a = (a + byte) % 65521
        b = (b + a) % 65521
    return (b << 16) | a


if __name__ == "__main__":
    for s in (b"", b"Wikipedia", b"hello world" * 100):
        assert adler32(s) == zlib.adler32(s)
    print(hex(adler32(b"Wikipedia")))  # 0x11e60398
