"""Explain a cron expression in English and list its next run times.

    python cronnext.py "*/15 9-17 * * 1-5"          # every 15 min, 9–17h, Mon–Fri
    python cronnext.py "0 0 1 * *" -n 5             # next 5 runs
    python cronnext.py "30 6 * * sun" --from 2026-11-08T00:00
    python cronnext.py @daily

Supports the standard 5 fields (minute hour day-of-month month day-of-week) with
``*``, lists ``a,b``, ranges ``a-b``, steps ``*/n`` and ``a-b/n``, month/day names and the
``@hourly @daily @weekly @monthly @yearly`` shortcuts. Like Vixie cron, when both
day-of-month and day-of-week are restricted a time matches if *either* does.
"""
from __future__ import annotations

import datetime as dt
import sys

FIELDS = [("minute", 0, 59), ("hour", 0, 23), ("day of month", 1, 31), ("month", 1, 12),
          ("day of week", 0, 6)]
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
DAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August",
               "September", "October", "November", "December"]
DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
MACROS = {"@hourly": "0 * * * *", "@daily": "0 0 * * *", "@midnight": "0 0 * * *",
          "@weekly": "0 0 * * 0", "@monthly": "0 0 1 * *", "@yearly": "0 0 1 1 *", "@annually": "0 0 1 1 *"}


class CronError(ValueError):
    pass


def _value(tok: str, idx: int) -> int:
    t = tok.lower()
    if idx == 3 and t[:3] in MONTHS and not t.isdigit():
        return MONTHS.index(t[:3]) + 1
    if idx == 4 and t[:3] in DAYS and not t.isdigit():
        return DAYS.index(t[:3])
    if not t.isdigit():
        raise CronError(f"bad value {tok!r} in {FIELDS[idx][0]}")
    v = int(t)
    if idx == 4 and v == 7:
        v = 0  # 7 is also Sunday
    return v


def parse_field(text: str, idx: int) -> set[int]:
    name, lo, hi = FIELDS[idx]
    out: set[int] = set()
    for part in text.split(","):
        rng, _, step_s = part.partition("/")
        step = int(step_s) if step_s else 1
        if step <= 0:
            raise CronError(f"bad step in {name}")
        if rng == "*":
            a, b = lo, hi
        elif "-" in rng:
            a_s, b_s = rng.split("-", 1)
            a, b = _value(a_s, idx), _value(b_s, idx)
            if idx == 4 and b == 0 and b_s != "0":
                b = 6 if a > 0 else 0  # "1-7" style ranges
        else:
            a = _value(rng, idx)
            b = hi if step_s else a
        if not (lo <= a <= hi and lo <= b <= hi) or a > b:
            raise CronError(f"{part!r} out of range for {name} ({lo}-{hi})")
        out.update(range(a, b + 1, step))
    return out


class Cron:
    def __init__(self, expr: str) -> None:
        expr = MACROS.get(expr.strip().lower(), expr)
        parts = expr.split()
        if len(parts) != 5:
            raise CronError("expected 5 fields: minute hour day-of-month month day-of-week")
        self.raw = parts
        self.sets = [parse_field(p, i) for i, p in enumerate(parts)]

    def matches(self, t: dt.datetime) -> bool:
        mins, hours, doms, months, dows = self.sets
        if t.minute not in mins or t.hour not in hours or t.month not in months:
            return False
        dow = (t.weekday() + 1) % 7
        dom_any, dow_any = self.raw[2] == "*", self.raw[4] == "*"
        if dom_any and dow_any:
            return True
        if dom_any:
            return dow in dows
        if dow_any:
            return t.day in doms
        return t.day in doms or dow in dows

    def next_runs(self, start: dt.datetime, n: int = 5) -> list[dt.datetime]:
        out: list[dt.datetime] = []
        t = start.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
        limit = t + dt.timedelta(days=366 * 5)
        while len(out) < n and t < limit:
            if t.month not in self.sets[3]:
                # jump to the 1st of the next month
                t = (t.replace(day=1, hour=0, minute=0) + dt.timedelta(days=32)).replace(day=1)
                continue
            if t.hour not in self.sets[1]:
                t = t.replace(minute=0) + dt.timedelta(hours=1)
                continue
            if self.matches(t):
                out.append(t)
            t += dt.timedelta(minutes=1)
        return out

    def describe(self) -> str:
        m, h, dom, mon, dow = self.raw

        def lst(vals: set[int], names: list[str] | None = None, offset: int = 0) -> str:
            items = sorted(vals)
            name = (lambda v: names[v - offset]) if names else str
            if len(items) > 2 and items == list(range(items[0], items[-1] + 1)):
                return f"{name(items[0])} through {name(items[-1])}"
            words = [name(v) for v in items]
            return words[0] if len(words) == 1 else ", ".join(words[:-1]) + " and " + words[-1]

        if m.startswith("*/") and h == "*":
            when = f"every {m[2:]} minutes"
        elif m == "*" and h == "*":
            when = "every minute"
        elif m == "*":
            when = f"every minute during hour {lst(self.sets[1])}"
        elif h == "*":
            when = f"at minute {lst(self.sets[0])} of every hour"
        elif m.startswith("*/"):
            when = f"every {m[2:]} minutes during hours {lst(self.sets[1])}"
        elif len(self.sets[0]) * len(self.sets[1]) <= 6:
            times = [f"{hh:02d}:{mm:02d}" for hh in sorted(self.sets[1]) for mm in sorted(self.sets[0])]
            when = "at " + (times[0] if len(times) == 1 else ", ".join(times[:-1]) + " and " + times[-1])
        else:
            when = f"at minutes {lst(self.sets[0])} past hours {lst(self.sets[1])}"
        bits = [when]
        if dom != "*":
            bits.append(f"on day {lst(self.sets[2])} of the month")
        if dow != "*":
            bits.append(("or " if dom != "*" else "") + f"on {lst(self.sets[4], DAY_NAMES)}")
        if mon != "*":
            bits.append(f"in {lst(self.sets[3], MONTH_NAMES, 1)}")
        text = " ".join(bits)
        return text[0].upper() + text[1:]


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    n = 5
    start = dt.datetime.now()
    args = list(argv)
    if "-n" in args:
        i = args.index("-n")
        n = int(args[i + 1])
        del args[i: i + 2]
    if "--from" in args:
        i = args.index("--from")
        start = dt.datetime.fromisoformat(args[i + 1])
        del args[i: i + 2]
    try:
        cron = Cron(" ".join(args))
    except CronError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(cron.describe() + ".")
    for t in cron.next_runs(start, n):
        print("  " + t.strftime("%a %Y-%m-%d %H:%M"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
