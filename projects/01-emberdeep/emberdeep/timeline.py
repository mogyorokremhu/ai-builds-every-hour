"""Run timeline: the story of a run as a list of dated events plus a depth-over-time chart.

The game records an event whenever something notable happens — reaching a new depth,
gaining a level, the first kill of each kind of monster, identifying an item, praying,
the boss changing phase, dying or winning. The post-run "ascend" screen, the text-mode
epilogue and the morgue file all show :meth:`Timeline.chart` (depth reached per turn as an
ASCII step plot) and :meth:`Timeline.story` (the event list).

The timeline is plain data and round-trips through :meth:`to_dict` / :meth:`from_dict`
so it survives save/load.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

#: Event kinds, with the marker used in the story list.
KINDS: dict[str, str] = {
    "depth": ">",     # arrived on a new depth
    "level": "+",     # experience level gained
    "kill": "x",      # first kill of a monster kind
    "boss": "&",      # boss events (phase changes, slain)
    "item": "!",      # identified an item kind, picked up an artifact
    "altar": "_",     # prayed at an altar
    "revive": "~",    # explore mode: rescued from death
    "end": "*",       # victory or death
}


@dataclass
class Event:
    turn: int
    depth: int
    kind: str
    text: str

    @property
    def marker(self) -> str:
        return KINDS.get(self.kind, "-")


@dataclass
class Timeline:
    events: list[Event] = field(default_factory=list)
    #: (turn, depth) each time the player arrived somewhere new
    depths: list[tuple[int, int]] = field(default_factory=list)
    end_turn: int | None = None

    # ---- recording ------------------------------------------------------
    def add(self, turn: int, depth: int, kind: str, text: str) -> Event:
        ev = Event(turn, depth, kind, text)
        self.events.append(ev)
        return ev

    def reach_depth(self, turn: int, depth: int, theme: str = "") -> None:
        """Record arriving on ``depth`` (only new depths make a story event)."""
        new = all(d < depth for _, d in self.depths)
        self.depths.append((turn, depth))
        if new:
            where = f" ({theme})" if theme else ""
            self.add(turn, depth, "depth", f"Reached depth {depth}{where}")

    def finish(self, turn: int, depth: int, text: str) -> None:
        """Mark the end of the run (idempotent: only the first call counts)."""
        if self.end_turn is not None:
            return
        self.end_turn = turn
        self.add(turn, depth, "end", text)

    # ---- queries ------------------------------------------------------------
    def depth_at(self, turn: int) -> int:
        """Depth the player was on at ``turn`` (0 before the run started)."""
        depth = 0
        for t, d in self.depths:
            if t > turn:
                break
            depth = d
        return depth

    def turns_per_depth(self, last_turn: int | None = None) -> dict[int, int]:
        """How many turns were spent on each depth."""
        end = self.end_turn if self.end_turn is not None else (last_turn or 0)
        out: dict[int, int] = {}
        for i, (t, d) in enumerate(self.depths):
            nxt = self.depths[i + 1][0] if i + 1 < len(self.depths) else max(end, t)
            out[d] = out.get(d, 0) + max(0, nxt - t)
        return out

    def of_kind(self, kind: str) -> list[Event]:
        return [e for e in self.events if e.kind == kind]

    # ---- rendering ----------------------------------------------------------
    def chart(self, last_turn: int, width: int = 50, max_depth: int = 10) -> list[str]:
        """Depth-over-time as an ASCII step plot (deeper is lower), ``max_depth`` rows tall.

        Each column covers ``last_turn / width`` turns and shows the deepest depth reached
        in that span; ``█`` marks the current depth, ``│`` connects descents.
        """
        width = max(10, width)
        last_turn = max(1, last_turn)
        top = max([max_depth] + [d for _, d in self.depths])
        cols: list[int] = []
        for c in range(width):
            lo = c * last_turn // width
            hi = max(lo, (c + 1) * last_turn // width - 1)
            deepest = self.depth_at(hi)
            # a depth reached and left within one span still counts
            for t, d in self.depths:
                if lo <= t <= hi:
                    deepest = max(deepest, d)
            cols.append(deepest)
        rows = []
        for depth in range(1, top + 1):
            line = []
            prev = 0
            for d in cols:
                if d == depth:
                    line.append("█")
                elif prev < depth < d:
                    line.append("│")
                else:
                    line.append(" ")
                prev = d
            rows.append(f"{depth:>3} ┤" + "".join(line).rstrip())
        axis = "    └" + "─" * width
        left, right = "0", f"{last_turn} turns"
        labels = "     " + left + " " * max(1, width - len(left) - len(right)) + right
        return rows + [axis, labels]

    def story(self, limit: int | None = None) -> list[str]:
        """The events as ``[turn] marker text`` lines (newest last)."""
        evs = self.events if limit is None else self.events[-limit:]
        return [f"[{e.turn:>5}] {e.marker} {e.text}" for e in evs]

    def report(self, last_turn: int, width: int = 50, limit: int | None = None) -> list[str]:
        """Chart + per-depth turn counts + the story, ready to print."""
        out = ["Depth over time", ""] + self.chart(last_turn, width)
        spent = self.turns_per_depth(last_turn)
        if spent:
            out += ["", "Turns per depth: " + "  ".join(f"D{d}:{n}" for d, n in sorted(spent.items()))]
        out += ["", "Timeline", ""] + self.story(limit)
        return out

    # ---- persistence -----------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "events": [[e.turn, e.depth, e.kind, e.text] for e in self.events],
            "depths": [list(p) for p in self.depths],
            "end": self.end_turn,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "Timeline":
        if not data:
            return cls()
        tl = cls([Event(t, d, k, s) for t, d, k, s in data.get("events", [])],
                 [(t, d) for t, d in data.get("depths", [])], data.get("end"))
        return tl
