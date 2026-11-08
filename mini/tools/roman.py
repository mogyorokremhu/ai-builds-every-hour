#!/usr/bin/env python3
"""roman - convert between Roman numerals and integers (1..3999)."""
import sys
PAIRS = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),(50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]

def to_roman(n: int) -> str:
    if not 0 < n < 4000: raise ValueError("1..3999 only")
    out = ""
    for v, s in PAIRS:
        while n >= v: out += s; n -= v
    return out

def from_roman(s: str) -> int:
    s = s.upper(); n = 0; i = 0
    for v, r in PAIRS:
        while s.startswith(r, i): n += v; i += len(r)
    if i != len(s) or to_roman(n) != s: raise ValueError(f"bad numeral {s}")
    return n

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert all(from_roman(to_roman(n)) == n for n in range(1, 4000)); assert to_roman(1994) == "MCMXCIV"
        print("ok"); sys.exit()
    for a in sys.argv[1:]:
        print(a, "=", to_roman(int(a)) if a.isdigit() else from_roman(a))
