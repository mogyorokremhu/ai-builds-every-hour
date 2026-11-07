"""A colourful hexdump (like `xxd`) with optional reverse mode.

    python hexdump.py FILE              dump a file (or stdin when FILE is '-')
    python hexdump.py FILE -w 8         8 bytes per row
    python hexdump.py FILE --no-color
    python hexdump.py -r DUMP > out.bin turn a dump back into bytes
    python hexdump.py --demo            dump this script's first 128 bytes
"""
from __future__ import annotations

import argparse
import sys

RESET = "\033[0m"


def byte_color(b: int) -> str:
    if b == 0:
        return "\033[90m"         # grey: NUL
    if 32 <= b < 127:
        return "\033[32m"         # green: printable
    if b in (9, 10, 13):
        return "\033[33m"         # yellow: whitespace
    if b == 255:
        return "\033[31m"         # red
    return "\033[35m"             # magenta: other


def dump_lines(data: bytes, width: int = 16, color: bool = True, offset: int = 0) -> list[str]:
    lines = []
    for start in range(0, len(data), width):
        chunk = data[start:start + width]
        hexes, chars = [], []
        for i, b in enumerate(chunk):
            h = f"{b:02x}"
            c = chr(b) if 32 <= b < 127 else "."
            if color:
                h, c = byte_color(b) + h + RESET, byte_color(b) + c + RESET
            hexes.append(h + (" " if i % 8 == 7 else ""))
            chars.append(c)
        pad = "   " * (width - len(chunk)) + " " * ((width - len(chunk) + 7) // 8)
        lines.append(f"{offset + start:08x}: {' '.join(hexes)}{pad} |{''.join(chars)}|")
    return lines


def undump(text: str) -> bytes:
    """Parse lines produced by :func:`dump_lines` (without colour) back into bytes."""
    out = bytearray()
    for line in text.splitlines():
        if ":" not in line:
            continue
        body = line.split(":", 1)[1].split("|", 1)[0]
        out.extend(bytes.fromhex(body.replace(" ", "")))
    return bytes(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", default=None)
    ap.add_argument("-w", "--width", type=int, default=16)
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("-r", "--reverse", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo or a.file is None:
        with open(__file__, "rb") as f:
            data = f.read(128)
        print("\n".join(dump_lines(data, a.width, not a.no_color)))
        return
    if a.reverse:
        text = sys.stdin.read() if a.file == "-" else open(a.file).read()
        sys.stdout.buffer.write(undump(text))
        return
    data = sys.stdin.buffer.read() if a.file == "-" else open(a.file, "rb").read()
    color = not a.no_color and sys.stdout.isatty()
    print("\n".join(dump_lines(data, a.width, color)))


if __name__ == "__main__":
    main()
