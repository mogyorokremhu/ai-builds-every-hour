"""Break a span between two dates into years, months and days."""
import calendar
import datetime


def diff_ymd(a: datetime.date, b: datetime.date) -> tuple[int, int, int]:
    """Whole years/months/days from a to b (borrowing the month before b)."""
    if a > b:
        a, b = b, a
    y, m, d = b.year - a.year, b.month - a.month, b.day - a.day
    if d < 0:
        m -= 1
        py, pm = (b.year, b.month - 1) if b.month > 1 else (b.year - 1, 12)
        d += calendar.monthrange(py, pm)[1]
    if m < 0:
        y -= 1
        m += 12
    return y, m, d


if __name__ == "__main__":
    assert diff_ymd(datetime.date(2020, 1, 15), datetime.date(2020, 3, 10)) == (0, 1, 24)
    assert diff_ymd(datetime.date(2000, 2, 29), datetime.date(2026, 11, 26)) == (26, 8, 28)
    print(diff_ymd(datetime.date(2026, 11, 26), datetime.date(2027, 1, 1)))
