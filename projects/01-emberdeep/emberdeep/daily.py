"""Daily seed mode: everyone playing on the same (UTC) day gets the same dungeon.

The seed is derived from the date with SHA-256, so it is stable across machines and
Python versions. Daily runs are tagged ``daily:YYYY-MM-DD`` in the high-score table; only
your first daily attempt each day counts as *ranked* (later ones are marked practice).
"""
from __future__ import annotations

import datetime as _dt
import hashlib

SEED_BITS = 30
PREFIX = "daily:"


def today() -> _dt.date:
    return _dt.datetime.now(_dt.timezone.utc).date()


def daily_seed(day: _dt.date | None = None) -> int:
    """Deterministic seed for ``day`` (default: today, UTC)."""
    day = day or today()
    digest = hashlib.sha256(f"emberdeep-daily-{day.isoformat()}".encode()).digest()
    return int.from_bytes(digest[:8], "big") & ((1 << SEED_BITS) - 1)


def daily_mode(day: _dt.date | None = None) -> str:
    return PREFIX + (day or today()).isoformat()


def is_daily(mode: str) -> bool:
    return mode.startswith(PREFIX)


def mode_date(mode: str) -> str | None:
    """'daily:2026-11-07' -> '2026-11-07'; None for normal runs."""
    return mode[len(PREFIX):] if is_daily(mode) else None


def parse_date(text: str) -> _dt.date:
    """Parse YYYY-MM-DD (used by ``--daily=2026-11-07`` to replay a past day)."""
    return _dt.date.fromisoformat(text)
