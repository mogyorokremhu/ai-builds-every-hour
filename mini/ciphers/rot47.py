"""ROT47: rotate all printable ASCII (33..126) by 47. Self-inverse. Usage: python rot47.py "text" """
import sys


def rot47(s: str) -> str:
    return "".join(chr(33 + (ord(c) - 33 + 47) % 94) if 33 <= ord(c) <= 126 else c for c in s)


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "Hello, World!"
    print(rot47(text))
    assert rot47(rot47(text)) == text
