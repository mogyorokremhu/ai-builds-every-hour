"""Find the nth weekday of a month (e.g. US Thanksgiving, EU DST switch days)."""
import datetime


def nth_weekday(year: int, month: int, weekday: int, n: int) -> datetime.date:
    """weekday: Mon=0..Sun=6. n>=1 counts from start; n=-1 means the last one."""
    if n > 0:
        first = datetime.date(year, month, 1)
        offset = (weekday - first.weekday()) % 7
        d = first + datetime.timedelta(days=offset + 7 * (n - 1))
        if d.month != month:
            raise ValueError("no such weekday")
        return d
    nxt = datetime.date(year + (month == 12), month % 12 + 1, 1)
    last = nxt - datetime.timedelta(days=1)
    return last - datetime.timedelta(days=(last.weekday() - weekday) % 7)


def us_dst(year: int) -> tuple[datetime.date, datetime.date]:
    return nth_weekday(year, 3, 6, 2), nth_weekday(year, 11, 6, 1)


def eu_dst(year: int) -> tuple[datetime.date, datetime.date]:
    return nth_weekday(year, 3, 6, -1), nth_weekday(year, 10, 6, -1)


if __name__ == "__main__":
    assert nth_weekday(2026, 11, 3, 4) == datetime.date(2026, 11, 26)  # Thanksgiving
    assert us_dst(2026) == (datetime.date(2026, 3, 8), datetime.date(2026, 11, 1))
    assert eu_dst(2026) == (datetime.date(2026, 3, 29), datetime.date(2026, 10, 25))
    for y in range(1990, 2100):
        for m in range(1, 13):
            d = nth_weekday(y, m, 4, -1)
            assert d.weekday() == 4 and (d + datetime.timedelta(days=7)).month != m
    print("Thanksgiving 2026:", nth_weekday(2026, 11, 3, 4))
    print("US DST 2026:", us_dst(2026), "EU DST 2026:", eu_dst(2026))
    print("ok")
