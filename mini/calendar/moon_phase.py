"""Approximate moon phase from a date using the mean synodic month."""
import datetime

SYNODIC = 29.530588853
NEW_MOON_REF = datetime.date(2000, 1, 6)  # a known new moon
NAMES = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
         "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]


def age(d: datetime.date) -> float:
    """Days since the last new moon (0 <= age < 29.53)."""
    return (d - NEW_MOON_REF).days % SYNODIC


def phase_name(d: datetime.date) -> str:
    return NAMES[int(age(d) / SYNODIC * 8 + 0.5) % 8]


if __name__ == "__main__":
    assert phase_name(datetime.date(2000, 1, 6)) == "New Moon"
    assert phase_name(datetime.date(2000, 1, 21)) == "Full Moon"
    for d in (datetime.date(2026, 11, 26), datetime.date(2026, 12, 4)):
        print(d, f"age {age(d):.1f}d", phase_name(d))
