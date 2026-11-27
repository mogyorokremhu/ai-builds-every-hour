"""Friday-the-13th finder and statistics over the 400-year Gregorian cycle."""
import datetime
from collections import Counter


def friday13s(year: int) -> list[datetime.date]:
    return [datetime.date(year, m, 13) for m in range(1, 13)
            if datetime.date(year, m, 13).weekday() == 4]


def next_friday13(after: datetime.date) -> datetime.date:
    y, m = after.year, after.month
    while True:
        d = datetime.date(y, m, 13)
        if d > after and d.weekday() == 4:
            return d
        y, m = y + (m == 12), m % 12 + 1


if __name__ == "__main__":
    assert friday13s(2026) == [datetime.date(2026, 2, 13), datetime.date(2026, 3, 13), datetime.date(2026, 11, 13)]
    assert next_friday13(datetime.date(2026, 11, 27)) == datetime.date(2027, 8, 13)
    counts = Counter(d.weekday() for y in range(2000, 2400) for m in range(1, 13)
                     for d in [datetime.date(y, m, 13)])
    assert counts[4] == 688 and counts[4] > counts[0]  # Friday is the most common 13th
    assert all(1 <= len(friday13s(y)) <= 3 for y in range(1900, 2200))
    print("Friday 13ths per 400 years:", counts[4])
    print("next after today:", next_friday13(datetime.date(2026, 11, 27)))
    print("ok")
