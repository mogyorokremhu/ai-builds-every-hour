#!/usr/bin/env python3
"""cronx — explain a cron expression in English and list its next run times.

Usage:
    python cronx.py "*/15 9-17 * * 1-5"          # explanation + next 5 runs
    python cronx.py "0 0 1 * *" -n 10            # next 10 runs
    python cronx.py "@daily"

Supports the standard 5 fields (minute hour day-of-month month day-of-week) with
``*``, lists ``1,2``, ranges ``1-5``, steps ``*/10`` and ``10-50/20``, month and weekday
names (``jan``, ``mon``), ``7`` as Sunday, and the ``@hourly/@daily/@weekly/@monthly/
@yearly`` shortcuts. Like Vixie cron, when both day-of-month and day-of-week are
restricted, a day matches if *either* matches.
"""
from __future__ import annotations

import datetime as dt
import sys

FIELDS = [("minute", 0, 59), ("hour", 0, 23), ("day", 1, 31), ("month", 1, 12), ("weekday", 0, 6)]
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
DAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August",
               "September", "October", "November", "December"]
DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
SHORTCUTS = {"@yearly": "0 0 1 1 *", "@annually": "0 0 1 1 *", "@monthly": "0 0 1 * *",
             "@weekly": "0 0 * * 0", "@daily": "0 0 * * *", "@midnight": "0 0 * * *", "@hourly": "0 * * * *"}


class CronError(ValueError):
    pass


def _value(tok: str, idx: int) -> int:
    t = tok.lower()
    if idx == 3 and t in MONTHS:
        return MONTHS.index(t) + 1
    if idx == 4 and t in DAYS:
        return DAYS.index(t)
    try:
        return int(t)
    except ValueError:
        raise CronError(f"bad value {tok!r} in the {FIELDS[idx][0]} field") from None


def parse_field(text: str, idx: int) -> set[int]:
    name, lo, hi = FIELDS[idx]
    out: set[int] = set()
    for part in text.split(","):
        step = 1
        if "/" in part:
            part, s = part.split("/", 1)
            step = int(s)
            if step <= 0:
                raise CronError(f"step must be positive in {name}")
        if part == "*":
            a, b = lo, hi
        elif "-" in part:
            x, y = part.split("-", 1)
            a, b = _value(x, idx), _value(y, idx)
        else:
            a = _value(part, idx)
            b = hi if step > 1 else a
        top = 7 if idx == 4 else hi  # weekday 7 is another name for Sunday
        if not (lo <= a <= top and lo <= b <= top) or a > b:
            raise CronError(f"{part!r} is out of range for {name} ({lo}-{hi})")
        out.update(0 if (idx == 4 and v == 7) else v for v in range(a, b + 1, step))
    return out


class Cron:
    def __init__(self, expr: str) -> None:
        expr = SHORTCUTS.get(expr.strip().lower(), expr)
        parts = expr.split()
        if len(parts) != 5:
            raise CronError("a cron expression needs 5 fields: minute hour day month weekday")
        self.raw = parts
        self.sets = [parse_field(p, i) for i, p in enumerate(parts)]
        self.dom_any = parts[2] == "*"
        self.dow_any = parts[4] == "*"

    def day_matches(self, d: dt.date) -> bool:
        if d.month not in self.sets[3]:
            return False
        dom = d.day in self.sets[2]
        dow = (d.isoweekday() % 7) in self.sets[4]
        if self.dom_any and self.dow_any:
            return True
        if self.dom_any:
            return dow
        if self.dow_any:
            return dom
        return dom or dow

    def next_runs(self, start: dt.datetime, n: int = 5) -> list[dt.datetime]:
        out: list[dt.datetime] = []
        t = start.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
        limit = start + dt.timedelta(days=366 * 5)
        mins, hours = sorted(self.sets[0]), sorted(self.sets[1])
        while len(out) < n and t < limit:
            if not self.day_matches(t.date()):
                t = dt.datetime.combine(t.date() + dt.timedelta(days=1), dt.time())
                continue
            found = None
            for h in hours:
                if h < t.hour:
                    continue
                for m in mins:
                    if h == t.hour and m < t.minute:
                        continue
                    found = t.replace(hour=h, minute=m)
                    break
                if found:
                    break
            if found is None:
                t = dt.datetime.combine(t.date() + dt.timedelta(days=1), dt.time())
                continue
            out.append(found)
            t = found + dt.timedelta(minutes=1)
        return out

    def explain(self) -> str:
        m, h, dom, mon, dow = self.raw
        def listing(vals: set[int], names: list[str] | None = None, offset: int = 0) -> str:
            v = sorted(vals)
            if names is None and len(v) >= 3 and v == list(range(v[0], v[-1] + 1)):
                return f"{v[0]} through {v[-1]}"
            if names is not None and len(v) >= 3 and v == list(range(v[0], v[-1] + 1)):
                return f"{names[v[0] - offset]} through {names[v[-1] - offset]}"
            words = [names[x - offset] if names else str(x) for x in v]
            return words[0] if len(words) == 1 else ", ".join(words[:-1]) + " and " + words[-1]
        if m == "*" and h == "*":
            when = "every minute"
        elif m.startswith("*/") and h == "*":
            when = f"every {m[2:]} minutes"
        elif h == "*":
            when = f"at minute {listing(self.sets[0])} of every hour"
        elif m.startswith("*/"):
            when = f"every {m[2:]} minutes during hour {listing(self.sets[1])}"
        elif len(self.sets[0]) == 1 and len(self.sets[1]) <= 4:
            mm = next(iter(self.sets[0]))
            times = [f"{hh:02d}:{mm:02d}" for hh in sorted(self.sets[1])]
            when = "at " + (times[0] if len(times) == 1 else ", ".join(times[:-1]) + " and " + times[-1])
        else:
            when = f"at minute {listing(self.sets[0])} past hour {listing(self.sets[1])}"
        parts = [when]
        if dom != "*":
            parts.append(f"on day {listing(self.sets[2])} of the month")
        if dow != "*":
            parts.append(("or " if dom != "*" else "") + "on " + listing(self.sets[4], DAY_NAMES))
        if mon != "*":
            parts.append("in " + listing(self.sets[3], MONTH_NAMES, 1))
        text = " ".join(parts)
        return text[0].upper() + text[1:]


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    n = 5
    if "-n" in argv:
        i = argv.index("-n")
        n = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    try:
        cron = Cron(" ".join(argv))
    except (CronError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(cron.explain() + ".")
    print()
    for t in cron.next_runs(dt.datetime.now(), n):
        print("  " + t.strftime("%a %Y-%m-%d %H:%M"))
    return 0


def _selftest() -> None:
    c = Cron("*/15 9-17 * * 1-5")
    runs = c.next_runs(dt.datetime(2026, 11, 7, 12, 0), 3)  # a Saturday
    assert runs[0] == dt.datetime(2026, 11, 9, 9, 0), runs
    assert runs[1] == dt.datetime(2026, 11, 9, 9, 15)
    assert Cron("@daily").next_runs(dt.datetime(2026, 1, 1, 5), 1)[0] == dt.datetime(2026, 1, 2)
    assert Cron("0 0 29 2 *").next_runs(dt.datetime(2026, 1, 1), 1)[0].year == 2028
    assert parse_field("mon-fri", 4) == {1, 2, 3, 4, 5}
    assert parse_field("7", 4) == {0}
    assert parse_field("5-7", 4) == {5, 6, 0}
    assert "Monday" in Cron("30 8 * * mon").explain()
    assert Cron("*/15 9-17 * * 1-5").explain() == "Every 15 minutes during hour 9 through 17 on Monday through Friday"
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
    else:
        sys.exit(main(sys.argv[1:]))
