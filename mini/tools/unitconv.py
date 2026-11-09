#!/usr/bin/env python3
"""Tiny unit converter: unitconv.py 5 km mi   |   unitconv.py 100 c f

Supports length, mass, volume, and temperature. Use --selftest to verify.
"""
from __future__ import annotations
import sys

# factor to a base unit per category
UNITS = {
    "length": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "mi": 1609.344, "yd": 0.9144, "ft": 0.3048, "in": 0.0254},
    "mass": {"kg": 1, "g": 0.001, "mg": 1e-6, "lb": 0.45359237, "oz": 0.028349523125},
    "volume": {"l": 1, "ml": 0.001, "gal": 3.785411784, "qt": 0.946352946, "cup": 0.2365882365, "floz": 0.0295735295625},
}
TEMPS = {"c", "f", "k"}


def convert(value: float, src: str, dst: str) -> float:
    src, dst = src.lower(), dst.lower()
    if src in TEMPS and dst in TEMPS:
        c = value if src == "c" else (value - 32) * 5 / 9 if src == "f" else value - 273.15
        return c if dst == "c" else c * 9 / 5 + 32 if dst == "f" else c + 273.15
    for table in UNITS.values():
        if src in table and dst in table:
            return value * table[src] / table[dst]
    raise ValueError(f"cannot convert {src} to {dst}")


def selftest() -> None:
    assert abs(convert(1, "mi", "km") - 1.609344) < 1e-9
    assert abs(convert(100, "c", "f") - 212) < 1e-9
    assert abs(convert(0, "k", "c") + 273.15) < 1e-9
    try:
        convert(1, "kg", "m")
    except ValueError:
        print("ok")
    else:
        raise AssertionError


if __name__ == "__main__":
    if "--selftest" in sys.argv or len(sys.argv) != 4:
        if "--selftest" in sys.argv:
            selftest()
        else:
            print(__doc__)
    else:
        print(f"{convert(float(sys.argv[1]), sys.argv[2], sys.argv[3]):.6g} {sys.argv[3]}")
