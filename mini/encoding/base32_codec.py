"""Hand-written Base32 (RFC 4648) encoder/decoder, checked against the stdlib."""
import base64
import os

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"


def encode(data: bytes) -> str:
    bits = "".join(f"{b:08b}" for b in data)
    bits += "0" * (-len(bits) % 5)
    out = "".join(ALPHABET[int(bits[i:i + 5], 2)] for i in range(0, len(bits), 5))
    return out + "=" * (-len(out) % 8)


def decode(text: str) -> bytes:
    bits = "".join(f"{ALPHABET.index(c):05b}" for c in text.rstrip("="))
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) - len(bits) % 8, 8))


if __name__ == "__main__":
    for n in range(0, 20):
        data = os.urandom(n)
        assert encode(data) == base64.b32encode(data).decode()
        assert decode(encode(data)) == data
    print(encode(b"hello"))
