"""Convert between bytes and human sizes.  Usage: humansize.py 1536000 | 1.5MiB | --selftest"""
import re
import sys

UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]


def human(n: int, base: int = 1024) -> str:
    """Format a byte count, e.g. 1536 -> '1.50 KiB'."""
    names = UNITS if base == 1024 else ["B", "kB", "MB", "GB", "TB", "PB"]
    x = float(n)
    i = 0
    while abs(x) >= base and i < len(names) - 1:
        x /= base
        i += 1
    return f"{int(x)} B" if i == 0 else f"{x:.2f} {names[i]}"


def parse(s: str) -> int:
    """Parse '1.5MiB' / '2 kB' / '300' into bytes."""
    m = re.fullmatch(r"\s*([\d.]+)\s*([a-zA-Z]*)\s*", s)
    if not m:
        raise ValueError(f"bad size: {s!r}")
    num, unit = float(m.group(1)), m.group(2).lower()
    if unit in ("", "b"):
        return int(num)
    pw = "kmgtp".index(unit[0]) + 1
    base = 1024 if unit.endswith("ib") or unit in ("k", "m", "g", "t", "p") else 1000
    return int(num * base ** pw)


def selftest() -> None:
    assert human(1536) == "1.50 KiB" and human(999) == "999 B"
    assert human(1_500_000, 1000) == "1.50 MB"
    assert parse("1.5MiB") == 1572864 and parse("2kB") == 2000 and parse("300") == 300
    print("humansize ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--selftest"]:
        selftest()
    elif a:
        for s in a:
            print(human(int(s)) if s.isdigit() else f"{parse(s)} bytes")
    else:
        print(__doc__)
