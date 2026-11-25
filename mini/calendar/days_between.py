"""Days between two dates, and business days, without datetime arithmetic."""
import datetime


def days_from_civil(y: int, m: int, d: int) -> int:
    """Days since 1970-01-01 (Howard Hinnant's algorithm)."""
    y -= m <= 2
    era = y // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def business_days(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    """Count Mon-Fri days in [a, b)."""
    da, db = days_from_civil(*a), days_from_civil(*b)
    return sum(1 for n in range(da, db) if (n + 3) % 7 < 5)  # 1970-01-01 was Thursday


if __name__ == "__main__":
    a, b = (2026, 1, 1), (2026, 11, 25)
    delta = days_from_civil(*b) - days_from_civil(*a)
    assert delta == (datetime.date(*b) - datetime.date(*a)).days
    expect = sum(1 for i in range(delta) if (datetime.date(*a) + datetime.timedelta(i)).weekday() < 5)
    assert business_days(a, b) == expect
    print(delta, "days,", business_days(a, b), "business days")
    print("ok")
