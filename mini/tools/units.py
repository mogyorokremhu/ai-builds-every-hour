"""Unit converter with dimensional analysis: `python units.py 3.5 km/h m/s`.

Units compose with * / and ^ (e.g. `kg*m/s^2`, `mi/gal`); conversion checks that both
sides have the same dimensions. Temperatures (C, F, K) are handled specially.

    python units.py 100 km/h mi/h
    python units.py 1 kWh J
    python units.py 9.81 m/s^2 ft/s^2
    python units.py 72 F C
    python units.py --list
"""
from __future__ import annotations

import re
import sys

# dimension vector order: length, mass, time, current, temperature, amount
DIMS = ("m", "kg", "s", "A", "K", "mol")


def _d(**kw: int) -> tuple[int, ...]:
    return tuple(kw.get(k, 0) for k in ("L", "M", "T", "I", "Th", "N"))


L, M, T = _d(L=1), _d(M=1), _d(T=1)

UNITS: dict[str, tuple[float, tuple[int, ...]]] = {
    # length
    "m": (1, L), "km": (1e3, L), "cm": (1e-2, L), "mm": (1e-3, L), "um": (1e-6, L), "nm": (1e-9, L),
    "in": (0.0254, L), "ft": (0.3048, L), "yd": (0.9144, L), "mi": (1609.344, L), "nmi": (1852, L),
    "au": (1.495978707e11, L), "ly": (9.4607e15, L),
    # mass
    "kg": (1, M), "g": (1e-3, M), "mg": (1e-6, M), "t": (1e3, M), "lb": (0.45359237, M), "oz": (0.028349523125, M),
    # time
    "s": (1, T), "ms": (1e-3, T), "min": (60, T), "h": (3600, T), "day": (86400, T), "week": (604800, T),
    "yr": (31557600, T),
    # area / volume
    "ha": (1e4, _d(L=2)), "acre": (4046.8564224, _d(L=2)),
    "l": (1e-3, _d(L=3)), "ml": (1e-6, _d(L=3)), "gal": (3.785411784e-3, _d(L=3)), "cup": (2.365882365e-4, _d(L=3)),
    # derived
    "N": (1, _d(M=1, L=1, T=-2)), "J": (1, _d(M=1, L=2, T=-2)), "kJ": (1e3, _d(M=1, L=2, T=-2)),
    "cal": (4.184, _d(M=1, L=2, T=-2)), "kcal": (4184, _d(M=1, L=2, T=-2)),
    "W": (1, _d(M=1, L=2, T=-3)), "kW": (1e3, _d(M=1, L=2, T=-3)), "hp": (745.69987, _d(M=1, L=2, T=-3)),
    "Wh": (3600, _d(M=1, L=2, T=-2)), "kWh": (3.6e6, _d(M=1, L=2, T=-2)), "eV": (1.602176634e-19, _d(M=1, L=2, T=-2)),
    "Pa": (1, _d(M=1, L=-1, T=-2)), "bar": (1e5, _d(M=1, L=-1, T=-2)), "atm": (101325, _d(M=1, L=-1, T=-2)),
    "psi": (6894.757, _d(M=1, L=-1, T=-2)),
    "Hz": (1, _d(T=-1)), "A": (1, _d(I=1)), "V": (1, _d(M=1, L=2, T=-3, I=-1)), "mol": (1, _d(N=1)),
}

TEMPS = {"C", "F", "K"}


def parse(expr: str) -> tuple[float, tuple[int, ...]]:
    """Parse 'kg*m/s^2' into (scale to SI, dimension vector)."""
    scale, dims = 1.0, [0] * 6
    sign = 1
    for tok in re.findall(r"[*/]|[A-Za-z]+(?:\^-?\d+)?", expr.replace(" ", "")):
        if tok == "*":
            sign = 1
            continue
        if tok == "/":
            sign = -1
            continue
        name, _, power = tok.partition("^")
        p = int(power) if power else 1
        if name not in UNITS:
            raise ValueError(f"unknown unit {name!r} (try --list)")
        f, d = UNITS[name]
        scale *= f ** (p * sign)
        dims = [a + b * p * sign for a, b in zip(dims, d)]
        sign = 1
    return scale, tuple(dims)


def convert_temp(v: float, a: str, b: str) -> float:
    kelvin = {"C": v + 273.15, "F": (v - 32) * 5 / 9 + 273.15, "K": v}[a]
    return {"C": kelvin - 273.15, "F": (kelvin - 273.15) * 9 / 5 + 32, "K": kelvin}[b]


def convert(value: float, src: str, dst: str) -> float:
    if src in TEMPS or dst in TEMPS:
        if not (src in TEMPS and dst in TEMPS):
            raise ValueError("temperatures convert only to other temperatures")
        return convert_temp(value, src, dst)
    fa, da = parse(src)
    fb, db = parse(dst)
    if da != db:
        raise ValueError(f"incompatible: {src} is {dimstr(da)}, {dst} is {dimstr(db)}")
    return value * fa / fb


def dimstr(d: tuple[int, ...]) -> str:
    parts = [f"{n}^{p}" if p != 1 else n for n, p in zip(DIMS, d) if p]
    return "*".join(parts) or "dimensionless"


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] == "--list":
        print("units:", " ".join(sorted(UNITS, key=str.lower)), "+ temperatures C F K")
        print(__doc__)
        return
    if len(args) != 3:
        sys.exit("usage: units.py VALUE FROM TO")
    v, a, b = float(args[0]), args[1], args[2]
    try:
        r = convert(v, a, b)
    except ValueError as exc:
        sys.exit(f"error: {exc}")
    print(f"{v:g} {a} = {r:.6g} {b}")


if __name__ == "__main__":
    main()
