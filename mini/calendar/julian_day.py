"""Julian Day Number conversion for Gregorian dates."""
import datetime


def to_jdn(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    yy, mm = y + 4800 - a, m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045


def from_jdn(jdn: int) -> tuple[int, int, int]:
    a = jdn + 32044
    b = (4 * a + 3) // 146097
    c = a - 146097 * b // 4
    d = (4 * c + 3) // 1461
    e = c - 1461 * d // 4
    m = (5 * e + 2) // 153
    return 100 * b + d - 4800 + m // 10, m + 3 - 12 * (m // 10), e - (153 * m + 2) // 5 + 1


if __name__ == "__main__":
    assert to_jdn(2000, 1, 1) == 2451545
    base = datetime.date(1900, 1, 1)
    for i in range(0, 80000, 7):
        dt = base + datetime.timedelta(days=i)
        j = to_jdn(dt.year, dt.month, dt.day)
        assert j == dt.toordinal() + 1721425, dt
        assert from_jdn(j) == (dt.year, dt.month, dt.day), dt
    print("JDN of 2026-11-25:", to_jdn(2026, 11, 25))
    print("ok")
