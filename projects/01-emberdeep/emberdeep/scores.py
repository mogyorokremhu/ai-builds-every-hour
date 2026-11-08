"""High-score table ("hall of fame") stored as JSON next to the save file.

A finished run (death or victory) becomes a :class:`ScoreEntry`. The score rewards
depth most, then experience and kills, with a big bonus for carrying off the Ember Heart
and a small one for finishing quickly.
"""
from __future__ import annotations

import datetime as _dt
import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import TYPE_CHECKING

from . import daily

if TYPE_CHECKING:  # pragma: no cover
    from .game import Game

SCORES_NAME = "scores.json"
MAX_ENTRIES = 50
VICTORY_BONUS = 5000


@dataclass
class ScoreEntry:
    """One hall-of-fame record of a finished run."""
    score: int
    outcome: str        # "victory" or the death cause
    depth: int
    level: int
    xp: int
    kills: int
    turns: int
    seed: int
    mode: str = "normal"
    date: str = ""      # ISO timestamp (UTC) of when the run ended
    ranked: bool = True  # False for repeat daily attempts

    @property
    def won(self) -> bool:
        """True if the run ended in victory."""
        return self.outcome == "victory"


def compute_score(game: "Game") -> int:
    """Score for a finished (or ongoing) run."""
    s = game.max_depth * 150 + game.xp + game.kills * 5 + (game.level - 1) * 40
    if game.victory:
        s += VICTORY_BONUS + max(0, 3000 - game.turn // 2)
    return s


def entry_for(game: "Game", when: _dt.datetime | None = None) -> ScoreEntry:
    """Build the score entry for a finished ``game``, stamped with ``when`` (default now, UTC)."""
    when = when or _dt.datetime.now(_dt.timezone.utc)
    return ScoreEntry(
        score=compute_score(game),
        outcome="victory" if game.victory else (game.death_cause or "died"),
        depth=game.max_depth, level=game.level, xp=game.xp, kills=game.kills, turns=game.turn,
        seed=game.seed, mode=game.mode, date=when.replace(microsecond=0).isoformat(),
    )


def scores_path(directory: Path) -> Path:
    """Path of the hall-of-fame file in ``directory``."""
    return directory / SCORES_NAME


def load_scores(directory: Path) -> list[ScoreEntry]:
    """Read the table (best first). A missing or corrupt file gives an empty table."""
    try:
        raw = json.loads(scores_path(directory).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    known = {f.name for f in fields(ScoreEntry)}
    out = []
    for d in raw if isinstance(raw, list) else []:
        try:
            out.append(ScoreEntry(**{k: v for k, v in d.items() if k in known}))
        except TypeError:
            continue
    return sorted(out, key=lambda e: -e.score)


def save_scores(directory: Path, entries: list[ScoreEntry]) -> None:
    """Write ``entries`` to the hall-of-fame file atomically (via a temp file)."""
    path = scores_path(directory)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps([asdict(e) for e in entries], indent=1), encoding="utf-8")
    tmp.replace(path)


def add_score(directory: Path, entry: ScoreEntry) -> int:
    """Insert ``entry``; returns its 1-based rank, or 0 if it didn't make the table.

    A daily run is unranked if a run with the same daily mode is already recorded.
    """
    entries = load_scores(directory)
    if entry.mode == "explore":
        entry.ranked = False
    if daily.is_daily(entry.mode) and any(e.mode == entry.mode for e in entries):
        entry.ranked = False
    entries.append(entry)
    entries.sort(key=lambda e: -e.score)
    kept = entries[:MAX_ENTRIES]
    save_scores(directory, kept)
    for i, e in enumerate(kept, 1):
        if e is entry:
            return i
    return 0


def format_table(entries: list[ScoreEntry], limit: int = 10, mode: str | None = None) -> list[str]:
    """Pretty rows for the terminal. ``mode`` filters (e.g. one day's daily runs)."""
    rows = [e for e in entries if mode is None or e.mode == mode][:limit]
    if not rows:
        return ["No runs recorded yet. Go and die gloriously!"]
    out = [f"{'#':>2}  {'Score':>6}  {'Depth':>5}  {'Lv':>2}  {'Turns':>6}  Outcome"]
    for i, e in enumerate(rows, 1):
        outcome = "★ carried off the Ember Heart" if e.won else e.outcome
        tag = ""
        if daily.is_daily(e.mode):
            tag = f" [daily {daily.mode_date(e.mode)}{'' if e.ranked else ', practice'}]"
        elif e.mode == "explore":
            tag = " [explore]"
        out.append(f"{i:>2}  {e.score:>6}  {e.depth:>5}  {e.level:>2}  {e.turns:>6}  {outcome}{tag}")
    return out
