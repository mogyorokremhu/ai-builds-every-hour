"""Compound interest growth table with regular contributions. Usage: python compound.py [start] [monthly] [rate_pct] [years]"""
import sys


def grow(start: float, monthly: float, annual_pct: float, years: int) -> list[float]:
    """Balance at the end of each year, compounding monthly."""
    r = annual_pct / 100 / 12
    bal = start
    out = []
    for _ in range(years):
        for _ in range(12):
            bal = bal * (1 + r) + monthly
        out.append(bal)
    return out


def doubling_time(annual_pct: float) -> float:
    """Exact years to double with annual compounding."""
    import math
    return math.log(2) / math.log(1 + annual_pct / 100)


def main(argv: list[str]) -> None:
    start = float(argv[1]) if len(argv) > 1 else 1000
    monthly = float(argv[2]) if len(argv) > 2 else 100
    rate = float(argv[3]) if len(argv) > 3 else 7.0
    years = int(argv[4]) if len(argv) > 4 else 20
    balances = grow(start, monthly, rate, years)
    top = max(balances)
    for y, b in enumerate(balances, 1):
        contributed = start + monthly * 12 * y
        print(f"Year {y:>2}: {b:>12,.2f} (paid in {contributed:>10,.0f}) " + "#" * int(40 * b / top))
    print(f"Doubling time at {rate}%: {doubling_time(rate):.2f} years (rule of 72: {72 / rate:.2f})")


if __name__ == "__main__":
    main(sys.argv)
