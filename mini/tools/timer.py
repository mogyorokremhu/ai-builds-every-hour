#!/usr/bin/env python3
"""timer — countdown, stopwatch and pomodoro timer with big block digits in the terminal.

Usage:
    python timer.py 25m            # countdown (formats: 90, 90s, 5m, 1h30m, 1:30, 1:02:03)
    python timer.py --stopwatch    # count up until Ctrl-C (prints the lap time)
    python timer.py --pomodoro 4   # 4 rounds of 25m work / 5m break (long 15m break after 4)
    python timer.py 10s --small    # one-line display instead of big digits

Rings the terminal bell when a countdown ends. Redraws in place with ANSI escapes; on a
dumb terminal (or when piped) it prints one line per second instead.
"""
from __future__ import annotations

import re
import sys
import time

FONT = {
    "0": ["███", "█ █", "█ █", "█ █", "███"],
    "1": [" ██", "  █", "  █", "  █", "  █"],
    "2": ["███", "  █", "███", "█  ", "███"],
    "3": ["███", "  █", "███", "  █", "███"],
    "4": ["█ █", "█ █", "███", "  █", "  █"],
    "5": ["███", "█  ", "███", "  █", "███"],
    "6": ["███", "█  ", "███", "█ █", "███"],
    "7": ["███", "  █", "  █", "  █", "  █"],
    "8": ["███", "█ █", "███", "█ █", "███"],
    "9": ["███", "█ █", "███", "  █", "███"],
    ":": ["   ", " █ ", "   ", " █ ", "   "],
}


def parse_duration(text: str) -> int:
    """'90' / '90s' / '5m' / '1h30m' / '1:30' / '1:02:03' -> seconds."""
    t = text.strip().lower()
    if ":" in t:
        parts = [int(p) for p in t.split(":")]
        if len(parts) > 3:
            raise ValueError(f"bad duration {text!r}")
        secs = 0
        for p in parts:
            secs = secs * 60 + p
        return secs
    if t.isdigit():
        return int(t)
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", t)
    if not m or not any(m.groups()):
        raise ValueError(f"bad duration {text!r}")
    h, mi, s = (int(g) if g else 0 for g in m.groups())
    return h * 3600 + mi * 60 + s


def clock(secs: int) -> str:
    secs = max(0, int(secs))
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def big(text: str) -> list[str]:
    rows = ["", "", "", "", ""]
    for ch in text:
        glyph = FONT.get(ch, ["   "] * 5)
        for i in range(5):
            rows[i] += glyph[i] + " "
    return rows


def bar(done: float, width: int = 30) -> str:
    done = min(1.0, max(0.0, done))
    full = int(done * width)
    return "[" + "#" * full + "-" * (width - full) + f"] {done * 100:3.0f}%"


class Display:
    def __init__(self, small: bool = False) -> None:
        self.fancy = sys.stdout.isatty() and not small
        self.small = small or not sys.stdout.isatty()
        self.drawn = 0

    def show(self, title: str, text: str, progress: float | None) -> None:
        if self.small:
            line = f"{title}: {text}" + (f"  {bar(progress, 20)}" if progress is not None else "")
            if sys.stdout.isatty():
                sys.stdout.write("\r" + line + "   ")
            else:
                sys.stdout.write(line + "\n")
            sys.stdout.flush()
            return
        lines = [title, ""] + ["  " + r for r in big(text)] + [""]
        if progress is not None:
            lines.append("  " + bar(progress))
        if self.drawn:
            sys.stdout.write(f"\033[{self.drawn}F")
        sys.stdout.write("\n".join(l + "\033[K" for l in lines) + "\n")
        sys.stdout.flush()
        self.drawn = len(lines)


def countdown(total: int, title: str, disp: Display, sleep=time.sleep, now=time.monotonic) -> None:
    start = now()
    while True:
        left = total - (now() - start)
        disp.show(title, clock(int(left + 0.999)), 1 - max(0.0, left) / total if total else 1.0)
        if left <= 0:
            break
        sleep(max(0.05, (left % 1.0) or 1.0))  # wake when the displayed second changes
    sys.stdout.write("\a\n")


def stopwatch(disp: Display) -> None:
    start = time.monotonic()
    try:
        while True:
            disp.show("Stopwatch (Ctrl-C to stop)", clock(int(time.monotonic() - start)), None)
            time.sleep(0.25)
    except KeyboardInterrupt:
        print(f"\nElapsed: {time.monotonic() - start:.2f} s")


def pomodoro_plan(rounds: int, work=25 * 60, short=5 * 60, long=15 * 60) -> list[tuple[str, int]]:
    plan: list[tuple[str, int]] = []
    for r in range(1, rounds + 1):
        plan.append((f"Work {r}/{rounds}", work))
        if r < rounds:
            plan.append(("Long break" if r % 4 == 0 else "Short break", long if r % 4 == 0 else short))
    return plan


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    disp = Display("--small" in argv)
    args = [a for a in argv if a != "--small"]
    try:
        if args[0] == "--stopwatch":
            stopwatch(disp)
        elif args[0] == "--pomodoro":
            for title, secs in pomodoro_plan(int(args[1]) if len(args) > 1 else 4):
                disp.drawn = 0
                countdown(secs, title, disp)
        else:
            countdown(parse_duration(args[0]), f"Countdown {clock(parse_duration(args[0]))}", disp)
    except KeyboardInterrupt:
        print("\nStopped.")
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


def _selftest() -> None:
    assert parse_duration("90") == 90 and parse_duration("1h30m") == 5400
    assert parse_duration("1:02:03") == 3723 and parse_duration("5m") == 300
    assert clock(3723) == "1:02:03" and clock(65) == "01:05"
    assert big("1:0")[0] == " ██     ███ "
    plan = pomodoro_plan(5)
    assert [t for t, _ in plan][7] == "Long break" and len(plan) == 9
    for bad in ("", "5x", "1:2:3:4"):
        try:
            parse_duration(bad)
            raise AssertionError(bad)
        except ValueError:
            pass
    shown: list[str] = []

    class Fake(Display):
        def show(self, title, text, progress):
            shown.append(text)

    t = [0.0]
    countdown(3, "t", Fake(small=True), sleep=lambda d: t.__setitem__(0, t[0] + d), now=lambda: t[0])
    assert shown[0] == "00:03" and shown[-1] == "00:00", shown
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
    else:
        sys.exit(main(sys.argv[1:]))
