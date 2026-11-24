"""Classic `hexdump -C` style dump of bytes or a file."""
import sys


def hexdump(data: bytes, width: int = 16) -> str:
    lines = []
    for off in range(0, len(data), width):
        row = data[off:off + width]
        hx = " ".join(f"{b:02x}" for b in row).ljust(width * 3 - 1)
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in row)
        lines.append(f"{off:08x}  {hx}  |{asc}|")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "rb") as f:
            print(hexdump(f.read()))
    else:
        print(hexdump(b"Hello, hexdump!\n\x00\x01\x02 binary tail"))
