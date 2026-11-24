"""Easter Sunday date (anonymous Gregorian algorithm)."""
import datetime


def easter(year: int) -> datetime.date:
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return datetime.date(year, month, day)


if __name__ == "__main__":
    known = {2000: (4, 23), 2019: (4, 21), 2024: (3, 31), 2026: (4, 5)}
    for y, (m, d) in known.items():
        assert easter(y) == datetime.date(y, m, d), y
        assert easter(y).weekday() == 6
    for y in range(2025, 2031):
        print(y, easter(y))
    print("ok")
