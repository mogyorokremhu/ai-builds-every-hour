#!/usr/bin/env python3
"""bases — show a number in every useful base, plus bits, two's complement and Roman numerals.

Usage:
    python bases.py 255          python bases.py 0xff       python bases.py 0b1010
    python bases.py -42 --bits 8   python bases.py MCMXCIV  python bases.py 'z3' --from 36

Input may be decimal, ``0x`` hex, ``0o`` octal, ``0b`` binary, a Roman numeral, or any base
2–36 with ``--from N``. Output: decimal, hex, octal, binary (grouped in nibbles), base 36,
two's-complement for the given width (default: smallest of 8/16/32/64 that fits), Roman
(1–3999), a bit ruler, and the ASCII/Unicode character if printable.
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
    t = text.strip().lower().replace("_", "")
    sign = -1 if t.startswith("-") else 1
    t = t.lstrip("+-")
    if not t:
        raise ValueError("empty number")
    n = 0
    for ch in t:
        d = DIGITS.find(ch)
        if d < 0 or d >= base:
            raise ValueError(f"digit {ch!r} is not valid in base {base}")
        n = n * base + d
    return sign * n


def to_roman(n: int) -> str:
    if not 1 <= n <= 3999:
        raise ValueError("Roman numerals cover 1..3999")
    out = []
    for value, sym in ROMAN:
        q, n = divmod(n, value)
        out.append(sym * q)
    return "".join(out)


def from_roman(text: str) -> int:
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    t = text.upper()
    total = 0
    for i, ch in enumerate(t):
        v = vals[ch]
        total += -v if i + 1 < len(t) and vals[t[i + 1]] > v else v
    if to_roman(total) != t:
        raise ValueError(f"{text!r} is not a canonical Roman numeral (did you mean {to_roman(total)}?)")
    return total


def parse(text: str, base: int | None = None) -> int:
    t = text.strip()
    if base:
        return from_base(t, base)
    low = t.lower().lstrip("-")
    neg = t.startswith("-")
    for prefix, b in (("0x", 16), ("0o", 8), ("0b", 2)):
        if low.startswith(prefix):
            n = from_base(low[2:], b)
            return -n if neg else n
    if t and set(t.upper()) <= set("IVXLCDM"):
        return from_roman(t)
    return from_base(t, 10)


def width_for(n: int) -> int:
    for w in (8, 16, 32, 64, 128):
        if -(1 << (w - 1)) <= n < (1 << w):
            return w
    return n.bit_length() + 1


def twos(n: int, bits: int) -> str:
    if not -(1 << (bits - 1)) <= n < (1 << bits):
        raise ValueError(f"{n} does not fit in {bits} bits")
    return format(n & ((1 << bits) - 1), f"0{bits}b")


def group(bits: str, size: int = 4) -> str:
    pad = (-len(bits)) % size
    bits = "0" * pad + bits
    return " ".join(bits[i:i + size] for i in range(0, len(bits), size))


def report(n: int, bits: int | None = None) -> list[str]:
    bits = bits or width_for(n)
    tc = twos(n, bits)
    lines = [
        f"decimal   {n}",
        f"hex       {'-' if n < 0 else ''}0x{to_base(abs(n), 16)}",
        f"octal     {'-' if n < 0 else ''}0o{to_base(abs(n), 8)}",
        f"binary    {'-' if n < 0 else ''}{group(to_base(abs(n), 2))}",
        f"base 36   {to_base(n, 36)}",
        f"{str(bits) + '-bit':<10}{group(tc)}" + (f"   (unsigned {int(tc, 2)}, signed {int(tc, 2) - (1 << bits) if tc[0] == '1' else int(tc, 2)})"),
    ]
    if bits <= 32:
        ruler = " ".join(f"{i:<4}" for i in range(bits - 1, -1, -4))
        lines.append(f"bit index {ruler.rstrip()}")
    if 1 <= n <= 3999:
        lines.append(f"roman     {to_roman(n)}")
    if 32 <= n < 0x110000 and chr(n).isprintable():
        lines.append(f"char      {chr(n)!r}  U+{n:04X}")
    lines.append(f"bits used {abs(n).bit_length()}, set bits {bin(abs(n)).count('1')}")
    return lines


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    base = bits = None
    rest = []
    it = iter(argv)
    for a in it:
        if a == "--from":
            base = int(next(it))
        elif a == "--bits":
            bits = int(next(it))
        else:
            rest.append(a)
    try:
        for arg in rest:
            print("\n".join(report(parse(arg, base), bits)))
            print()
    except (ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


def _selftest() -> None:
    for n in (0, 1, 7, 255, 4096, -42, 123456789):
        for b in (2, 8, 10, 16, 36):
            assert from_base(to_base(n, b), b) == n
    assert parse("0xff") == 255 and parse("-0b101") == -5 and parse("MCMXCIV") == 1994
    assert parse("z", 36) == 35 and to_roman(3999) == "MMMCMXCIX"
    assert twos(-1, 8) == "11111111" and twos(-128, 8) == "10000000"
    assert width_for(255) == 8 and width_for(-129) == 16
    try:
        from_roman("IIII")
        raise AssertionError
    except ValueError as e:
        assert "IV" in str(e)
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
    else:
        sys.exit(main(sys.argv[1:]))
