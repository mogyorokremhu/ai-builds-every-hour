#!/usr/bin/env python3
"""How long between two dates (or since a date): years/months/days, total days, weeks, weekday, next anniversary.

usage: ageof.py 1990-05-17            ageof.py 2024-02-29 2026-11-08       ageof.py --selftest
"""
import sys
from datetime import date, timedelta

def add_months(a, n):
    """a + n months, clamping the day to the end of the month (Jan 31 + 1 month = Feb 28/29)."""
    y, m = divmod(a.month - 1 + n, 12)
    y += a.year; m += 1
    d = a.day
    while True:
        try:
            return date(y, m, d)
        except ValueError:
            d -= 1

def ymd(a, b):
    """Calendar difference b - a as (years, months, days), a <= b: whole months first, then leftover days."""
    n = (b.year - a.year) * 12 + b.month - a.month
    while n > 0 and add_months(a, n) > b:
        n -= 1
    return n // 12, n % 12, (b - add_months(a, n)).days

def next_anniversary(a, today):
    for yr in (today.year, today.year + 1):
        try:
            c = a.replace(year=yr)
        except ValueError:                      # Feb 29 in a common year
            c = date(yr, 3, 1)
        if c >= today:
            return c

def report(a, b):
    if a > b:
        a, b = b, a
    y, m, d = ymd(a, b)
    days = (b - a).days
    n = next_anniversary(a, b)
    return [f"{a} → {b}: {y} years, {m} months, {d} days",
            f"total: {days} days = {days // 7} weeks + {days % 7} days",
            f"{a} was a {a.strftime('%A')}; next anniversary {n} ({(n - b).days} days away)"]

def selftest():
    assert ymd(date(2000, 1, 31), date(2000, 3, 1)) == (0, 1, 1)  # Jan 31 + 1 month = Feb 29
    assert ymd(date(1990, 5, 17), date(2026, 5, 16)) == (35, 11, 29)
    assert ymd(date(2024, 2, 29), date(2025, 2, 28)) == (1, 0, 0)  # Feb 29 + 1 year clamps to Feb 28
    assert ymd(date(2020, 6, 15), date(2020, 6, 15)) == (0, 0, 0)
    assert next_anniversary(date(2024, 2, 29), date(2026, 1, 1)) == date(2026, 3, 1)
    assert report(date(2026, 1, 1), date(2026, 1, 8))[1].startswith("total: 7 days = 1 weeks")
    print("ageof: ok")

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        selftest()
    elif not a:
        print(__doc__)
    else:
        d1 = date.fromisoformat(a[0])
        d2 = date.fromisoformat(a[1]) if len(a) > 1 else date.today()
        print("\n".join(report(d1, d2)))
