"""Draws tonight's Moon (or any date's) in ASCII: the phase is computed from the mean
synodic month, and the lit part of the disc is shaded with a little limb darkening.

    python ascii_moon.py               # today
    python ascii_moon.py 2026-12-24    # any date
    python ascii_moon.py --month       # one small moon per day for the next 30 days
"""
import datetime as dt
import math
import sys

SYNODIC = 29.530588853                     # days between new moons
NEW_MOON = dt.datetime(2000, 1, 6, 18, 14)  # a known new moon (UTC)
SHADES = " .:-=+*#%@"
NAMES = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
         "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]


def phase(when: dt.datetime) -> float:
    """Moon age as a fraction of the cycle: 0 = new, 0.5 = full."""
    days = (when - NEW_MOON).total_seconds() / 86400
    return (days / SYNODIC) % 1.0


def phase_name(p: float) -> str:
    """Traditional name of the phase."""
    return NAMES[int((p * 8) + 0.5) % 8]


def illumination(p: float) -> float:
    """Lit fraction of the disc."""
    return (1 - math.cos(2 * math.pi * p)) / 2


def draw(p: float, radius: int = 12) -> list[str]:
    """The disc as text rows (2 characters per unit of width keep it round)."""
    # the terminator is an ellipse: x = cos(2πp) * sqrt(1 - y²); lit side depends on waxing/waning
    k = math.cos(2 * math.pi * p)
    waxing = p < 0.5
    rows = []
    for j in range(-radius, radius + 1):
        y = j / radius
        line = ""
        for i in range(-2 * radius, 2 * radius + 1):
            x = i / (2 * radius)
            if x * x + y * y > 1:
                line += " "
                continue
            half = math.sqrt(1 - y * y)
            edge = k * half
            lit = x > edge if waxing else x < -edge
            if lit:
                depth = math.sqrt(max(0.0, 1 - x * x - y * y))
                line += SHADES[min(len(SHADES) - 1, 4 + int(depth * 5.99))]
            else:
                line += "." if x * x + y * y > 0.78 else " "  # faint rim of the dark side
        rows.append(line.rstrip())
    return rows


def main(argv: list[str]) -> None:
    """Print one moon or a month strip."""
    if "--month" in argv:
        start = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
        for week in range(0, 30, 6):
            discs = [draw(phase(start + dt.timedelta(days=d)), 4) for d in range(week, min(30, week + 6))]
            for row in zip(*discs):
                print("   ".join(r.ljust(17) for r in row))
            print("   ".join(f"+{d:<2} {int(illumination(phase(start + dt.timedelta(days=d))) * 100):>3}%".ljust(17)
                             for d in range(week, min(30, week + 6))))
            print()
        return
    when = dt.datetime.fromisoformat(argv[0]) if argv else dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    p = phase(when)
    print("\n".join(draw(p)))
    print(f"{when:%Y-%m-%d}: {phase_name(p)}, {illumination(p) * 100:.0f}% lit, age {p * SYNODIC:.1f} days")


if __name__ == "__main__":
    main(sys.argv[1:])
