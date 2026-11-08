#!/usr/bin/env python3
"""epoch: convert Unix timestamps <-> ISO dates. Usage: epoch.py [now | 1700000000 | 2026-11-08T12:00:00]"""
import sys
from datetime import datetime, timezone

def to_iso(ts):
    ts = float(ts)
    if ts > 1e11:  # milliseconds
        ts /= 1000
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def to_epoch(iso):
    d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return int(d.timestamp())

def convert(arg):
    if arg == "now":
        return str(int(datetime.now(timezone.utc).timestamp()))
    try:
        return to_iso(arg)
    except ValueError:
        return str(to_epoch(arg))

if __name__ == "__main__":
    assert to_iso(0) == "1970-01-01T00:00:00Z"
    assert to_epoch("1970-01-02") == 86400
    assert to_iso(1700000000000) == to_iso(1700000000)
    for a in sys.argv[1:] or ["now"]:
        print(a, "->", convert(a))
