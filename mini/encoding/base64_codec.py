"""Hand-written Base64 encoder/decoder (RFC 4648), checked against the stdlib."""
import base64
import os

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def encode(data: bytes) -> str:
    out = []
    for i in range(0, len(data), 3):
        chunk = data[i:i + 3]
        n = int.from_bytes(chunk.ljust(3, b"\0"), "big")
        chars = [ALPHABET[(n >> s) & 63] for s in (18, 12, 6, 0)]
        keep = len(chunk) + 1
        out.append("".join(chars[:keep]) + "=" * (4 - keep))
    return "".join(out)


def decode(text: str) -> bytes:
    text = text.rstrip("=")
    out = bytearray()
    for i in range(0, len(text), 4):
        chunk = text[i:i + 4]
        n = 0
        for c in chunk.ljust(4, "A"):
            n = (n << 6) | ALPHABET.index(c)
        out += n.to_bytes(3, "big")[:len(chunk) - 1]
    return bytes(out)


if __name__ == "__main__":
    for _ in range(200):
        d = os.urandom(os.urandom(1)[0] % 40)
        assert encode(d) == base64.b64encode(d).decode()
        assert decode(encode(d)) == d
    print(encode(b"Hello, world!"))
    print("base64 ok")
