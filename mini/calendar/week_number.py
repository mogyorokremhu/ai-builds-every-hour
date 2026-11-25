"""ISO 8601 week number and week-year, computed by hand."""
import datetime


def iso_week(d: datetime.date) -> tuple[int, int]:
    """Return (iso_year, iso_week) using the Thursday rule."""
    thursday = d + datetime.timedelta(days=3 - d.weekday())
    jan1 = datetime.date(thursday.year, 1, 1)
    return thursday.year, (thursday - jan1).days // 7 + 1


if __name__ == "__main__":
    d = datetime.date(2020, 1, 1)
    end = datetime.date(2030, 12, 31)
    while d <= end:
        assert iso_week(d) == tuple(d.isocalendar())[:2], d
        d += datetime.timedelta(days=1)
    for s in ("2026-01-01", "2026-11-25", "2027-01-01", "2024-12-30"):
        print(s, iso_week(datetime.date.fromisoformat(s)))
    print("ok")
