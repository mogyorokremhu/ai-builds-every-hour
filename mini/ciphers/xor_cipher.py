"""Repeating-key XOR, output as hex. Symmetric: decrypt takes the hex back.

Usage: python xor_cipher.py KEY "text" [-d]
"""
import sys


def xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def encrypt(text: str, key: str) -> str:
    return xor(text.encode(), key.encode()).hex()


def decrypt(hexstr: str, key: str) -> str:
    return xor(bytes.fromhex(hexstr), key.encode()).decode()


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "-d"]
    key, text = args[0], args[1]
    print(decrypt(text, key) if "-d" in sys.argv else encrypt(text, key))
