"""Conway's Doomsday rule: mental-math weekday algorithm, checked against datetime."""
import datetime

ANCHOR = {0: 2, 1: 0, 2: 5, 3: 3}  # century % 4 -> anchor weekday (Sun=0)


def is_leap(y: int) -> bool:
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def doomsday(year: int) -> int:
    """Weekday (Sun=0) shared by 4/4, 6/6, 8/8, 10/10, 12/12, 5/9, 9/5, 7/11, 11/7."""
    c, y = divmod(year, 100)
    return (ANCHOR[c % 4] + y // 12 + y % 12 + (y % 12) // 4) % 7


def weekday(y: int, m: int, d: int) -> int:
    leap = is_leap(y)
    ref = {1: 4 if leap else 3, 2: 29 if leap else 28, 3: 14, 4: 4, 5: 9, 6: 6,
           7: 11, 8: 8, 9: 5, 10: 10, 11: 7, 12: 12}[m]
    return (doomsday(y) + d - ref) % 7


if __name__ == "__main__":
    for y in range(1600, 2400, 3):
        for m in range(1, 13):
            for d in (1, 13, 28):
                assert weekday(y, m, d) == (datetime.date(y, m, d).weekday() + 1) % 7, (y, m, d)
    names = "Sun Mon Tue Wed Thu Fri Sat".split()
    print("Doomsday 2026:", names[doomsday(2026)])
    print("2026-11-27 is a", names[weekday(2026, 11, 27)])
    print("ok")
