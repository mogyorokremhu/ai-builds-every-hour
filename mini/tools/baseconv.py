"""Convert numbers between bases and show them every way at once.

    python baseconv.py 255            # decimal, hex, octal, binary, base36, roman, bytes...
    python baseconv.py 0xff           # prefixes 0x 0o 0b are understood
    python baseconv.py zz --from 36   # any base 2..36
    python baseconv.py 42 --to 7      # just the number in base 7
    python baseconv.py -- -17         # negatives work too (two's complement shown for 8/16/32/64 bits)
    python baseconv.py MCMXCIV        # roman numerals are recognised

Everything is done by hand (no int(x, base) for output), including roman numerals.
"""
from __future__ import annotations

import sys

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"
ROMAN = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
         (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def to_base(n: int, base: int) -> str:
    if not 2 <= base <= 36:
        raise ValueError("base must be 2..36")
    if n == 0:
        return "0"
    sign, n = ("-", -n) if n < 0 else ("", n)
    out = []
    while n:
        n, r = divmod(n, base)
        out.append(DIGITS[r])
    return sign + "".join(reversed(out))


def from_base(text: str, base: int) -> int:
    text = text.strip().lower().replace("_", "")
    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("+-")
    if not text:
        raise ValueError("empty number")
    n = 0
    for ch in text:
        d = DIGITS.find(ch)
        if d < 0 or d >= base:
            raise ValueError(f"digit {ch!r} not valid in base {base}")
        n = n * base + d
    return sign * n


def to_roman(n: int) -> str | None:
    if not 0 < n < 4000:
        return None
    out = []
    for value, sym in ROMAN:
        while n >= value:
            out.append(sym)
            n -= value
    return "".join(out)


def from_roman(text: str) -> int | None:
    text = text.upper()
    if not text or any(ch not in "MDCLXVI" for ch in text):
        return None
    vals = {"M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1}
    total = 0
    for i, ch in enumerate(text):
        v = vals[ch]
        total += -v if i + 1 < len(text) and vals[text[i + 1]] > v else v
    return total if to_roman(total) == text else None  # reject non-canonical forms


def parse(text: str, base: int | None = None) -> int:
    if base is not None:
        return from_base(text, base)
    t = text.strip().lower()
    neg = t.startswith("-")
    body = t.lstrip("+-")
    for prefix, b in (("0x", 16), ("0o", 8), ("0b", 2)):
        if body.startswith(prefix):
            n = from_base(body[2:], b)
            return -n if neg else n
    roman = from_roman(text.strip())
    if roman is not None:
        return roman
    return from_base(t, 10)


def group(s: str, size: int, sep: str = "_") -> str:
    head = s.lstrip("-")
    sign = s[: len(s) - len(head)]
    parts = []
    while head:
        parts.append(head[-size:])
        head = head[:-size]
    return sign + sep.join(reversed(parts))


def twos(n: int, bits: int) -> str | None:
    if not -(1 << (bits - 1)) <= n < (1 << (bits - 1)):
        return None
    return to_base(n & ((1 << bits) - 1), 16).rjust(bits // 4, "0")


def report(n: int) -> list[str]:
    lines = [
        f"decimal   {group(str(n), 3, ',')}",
        f"hex       0x{to_base(n, 16)}" if n >= 0 else f"hex       -0x{to_base(-n, 16)}",
        f"octal     0o{to_base(n, 8)}" if n >= 0 else f"octal     -0o{to_base(-n, 8)}",
        f"binary    0b{group(to_base(n, 2), 4)}" if n >= 0 else f"binary    -0b{group(to_base(-n, 2), 4)}",
        f"base36    {to_base(n, 36)}",
    ]
    r = to_roman(n)
    if r:
        lines.append(f"roman     {r}")
    if n >= 0:
        nbytes = max(1, (n.bit_length() + 7) // 8)
        lines.append(f"bytes BE  {n.to_bytes(nbytes, 'big').hex(' ')}")
        lines.append(f"bits      {n.bit_length()} (popcount {bin(n).count('1')})")
        if 32 <= n < 0x110000 and not 0xD800 <= n <= 0xDFFF:
            lines.append(f"char      {chr(n)!r}  U+{n:04X}")
    else:
        for bits in (8, 16, 32, 64):
            t = twos(n, bits)
            if t:
                lines.append(f"int{bits:<5} 0x{t}  (two's complement)")
    return lines


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--"]
    base_in = base_out = None
    if "--from" in args:
        i = args.index("--from")
        base_in = int(args[i + 1])
        del args[i: i + 2]
    if "--to" in args:
        i = args.index("--to")
        base_out = int(args[i + 1])
        del args[i: i + 2]
    if not args:
        print(__doc__)
        return 2
    try:
        n = parse(args[0], base_in)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if base_out:
        print(to_base(n, base_out))
    else:
        print("\n".join(report(n)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
