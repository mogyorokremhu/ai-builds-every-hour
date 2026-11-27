"""RFC 1071 Internet checksum, plus an IPv4 header builder/verifier."""
import struct


def checksum(data: bytes) -> int:
    """16-bit one's complement sum of the data, complemented."""
    if len(data) % 2:
        data += b"\x00"
    total = sum(struct.unpack(f"!{len(data) // 2}H", data))
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF


def ipv4_header(src: tuple, dst: tuple, payload_len: int, proto: int = 17, ttl: int = 64) -> bytes:
    """Build a 20-byte IPv4 header with a valid checksum."""
    head = struct.pack("!BBHHHBBH4B4B", 0x45, 0, 20 + payload_len, 0x1234, 0,
                       ttl, proto, 0, *src, *dst)
    cs = checksum(head)
    return head[:10] + struct.pack("!H", cs) + head[12:]


if __name__ == "__main__":
    # Classic example header from Wikipedia: checksum should be 0xB861.
    sample = bytes.fromhex("4500 0073 0000 4000 4011 0000 c0a8 0001 c0a8 00c7".replace(" ", ""))
    assert checksum(sample) == 0xB861
    h = ipv4_header((10, 0, 0, 1), (10, 0, 0, 2), 100)
    assert checksum(h) == 0  # a valid header sums to zero
    print("checksum of sample:", hex(checksum(sample)))
    print("header:", h.hex())
    print("verify ok")
