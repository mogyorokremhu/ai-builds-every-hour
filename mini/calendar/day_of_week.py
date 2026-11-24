"""Day of week via Zeller's congruence, checked against datetime."""
import datetime

NAMES = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def zeller(y: int, m: int, d: int) -> str:
    """Gregorian day name for a date."""
    if m < 3:
        m += 12
        y -= 1
    k, j = y % 100, y // 100
    h = (d + 13 * (m + 1) // 5 + k + k // 4 + j // 4 + 5 * j) % 7
    return NAMES[h]


if __name__ == "__main__":
    for y, m, d in [(2000, 1, 1), (2026, 11, 24), (1969, 7, 20), (2024, 2, 29)]:
        expect = datetime.date(y, m, d).strftime("%A")
        assert zeller(y, m, d) == expect, (y, m, d)
        print(f"{y}-{m:02d}-{d:02d} is a {zeller(y, m, d)}")
    print("ok")
