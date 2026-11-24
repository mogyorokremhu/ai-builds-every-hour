"""Print a month calendar from scratch (Monday-first)."""
import datetime

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def is_leap(y: int) -> bool:
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def days_in(y: int, m: int) -> int:
    return [31, 29 if is_leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]


def render(y: int, m: int) -> str:
    title = f"{MONTHS[m - 1]} {y}".center(20)
    lines = [title.rstrip(), "Mo Tu We Th Fr Sa Su"]
    row = ["  "] * datetime.date(y, m, 1).weekday()
    for d in range(1, days_in(y, m) + 1):
        row.append(f"{d:2d}")
        if len(row) == 7:
            lines.append(" ".join(row))
            row = []
    if row:
        lines.append(" ".join(row))
    return "\n".join(lines)


if __name__ == "__main__":
    import calendar
    for y, m in [(2026, 11), (2024, 2), (2023, 10)]:
        ref = calendar.TextCalendar(0).formatmonth(y, m).split("\n")
        mine = render(y, m).split("\n")
        assert [s.strip() for s in mine[1:]] == [s.strip() for s in ref[1:] if s], (y, m)
    print(render(2026, 11))
    print("ok")
