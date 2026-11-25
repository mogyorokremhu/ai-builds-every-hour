"""Table-driven CRC-32 (IEEE), checked against zlib."""
import zlib

TABLE = []
for n in range(256):
    c = n
    for _ in range(8):
        c = 0xEDB88320 ^ (c >> 1) if c & 1 else c >> 1
    TABLE.append(c)


def crc32(data: bytes) -> int:
    c = 0xFFFFFFFF
    for byte in data:
        c = TABLE[(c ^ byte) & 0xFF] ^ (c >> 8)
    return c ^ 0xFFFFFFFF


if __name__ == "__main__":
    for s in (b"", b"123456789", b"The quick brown fox"):
        assert crc32(s) == zlib.crc32(s)
    print(hex(crc32(b"123456789")))  # 0xcbf43926
