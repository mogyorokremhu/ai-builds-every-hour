"""A run timeline: when you reached each depth, levelled up, met new foes, and how it ended.

The game appends :class:`Event` records as things happen. At the end of a run the
timeline powers the "ascend" stats screen and a section of the morgue file, including an
ASCII chart of depth over time::

    depth
     10 |                              ▄▄█
      5 |           ▄▄▄▄█████████████████
      1 |▄▄▄████████████████████████████
        +--------------------------------
         0                       turn 2412
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: event kinds and the marker shown in the event list
MARKERS = {"depth": ">", "level": "+", "first": "!", "boss": "&", "victory": "*", "death": "x",
           "item": "?"}


@dataclass
class Event:
    turn: int
    depth: int
    kind: str      # see MARKERS
    text: str

    def line(self) -> str:
        return f"[{self.turn:>5}] D{self.depth:<2} {MARKERS.get(self.kind, '-')} {self.text}"


@dataclass
class Timeline:
    events: list[Event] = field(default_factory=list)
    seen_kinds: set[str] = field(default_factory=set)   # monster kinds already met (for "first")

    def add(self, turn: int, depth: int, kind: str, text: str) -> Event:
        ev = Event(turn, depth, kind, text)
        self.events.append(ev)
        return ev

    def first_kill(self, turn: int, depth: int, name: str) -> bool:
        """Record the first kill of a monster kind. Returns True if it was the first."""
        if name in self.seen_kinds:
            return False
        self.seen_kinds.add(name)
        self.add(turn, depth, "first", f"first {name} slain")
        return True

    def of_kind(self, kind: str) -> list[Event]:
        return [e for e in self.events if e.kind == kind]

    def depth_points(self, final_turn: int) -> list[tuple[int, int]]:
        """(turn, depth) at each descent plus the end of the run."""
        pts = [(e.turn, e.depth) for e in self.of_kind("depth")]
        if not pts:
            pts = [(0, 1)]
        last_depth = pts[-1][1]
        if final_turn > pts[-1][0]:
            pts.append((final_turn, last_depth))
        return pts

    def depth_at(self, turn: int) -> int:
        d = 1
        for e in self.of_kind("depth"):
            if e.turn <= turn:
                d = e.depth
        return d

    def turns_per_depth(self, final_turn: int) -> dict[int, int]:
        """How many turns were spent on each depth."""
        out: dict[int, int] = {}
        pts = self.depth_points(final_turn)
        for (t0, d), (t1, _) in zip(pts, pts[1:]):
            out[d] = out.get(d, 0) + (t1 - t0)
        if len(pts) == 1:
            out[pts[0][1]] = final_turn - pts[0][0]
        return out

    # ---- persistence ----------------------------------------------------------
    def to_list(self) -> dict:
        return {"events": [[e.turn, e.depth, e.kind, e.text] for e in self.events],
                "seen": sorted(self.seen_kinds)}

    @classmethod
    def from_list(cls, data: dict | None) -> "Timeline":
        tl = cls()
        if not data:
            return tl
        tl.events = [Event(int(t), int(d), str(k), str(x)) for t, d, k, x in data.get("events", [])]
        tl.seen_kinds = set(data.get("seen", []))
        return tl


def depth_chart(tl: Timeline, final_turn: int, width: int = 40, height: int = 8,
                max_depth: int | None = None) -> list[str]:
    """ASCII chart of depth over time (deeper = taller columns)."""
    width, height = max(8, width), max(3, height)
    top = max_depth or max((e.depth for e in tl.of_kind("depth")), default=1)
    top = max(1, top)
    height = max(1, min(height, top))  # never more rows than depths
    span = max(1, final_turn)
    cols = []
    for c in range(width):
        turn = (c * span) // max(1, width - 1) if width > 1 else span
        cols.append(tl.depth_at(turn))
    rows: list[str] = []
    for r in range(height, 0, -1):
        # this row represents depths in ((r-1)/height*top, r/height*top]
        hi = r * top / height
        lo = (r - 1) * top / height
        label = f"{max(1, round(hi)):>3}" if r in (height, 1) else "   "
        line = []
        for d in cols:
            if d >= hi:
                line.append("█")
            elif d > lo:
                line.append("▄")
            else:
                line.append(" ")
        rows.append(f"{label} |" + "".join(line).rstrip())
    rows.append("    +" + "-" * width)
    end = f"turn {final_turn}"
    rows.append("     0" + " " * max(1, width - len(end) - 1) + end)
    return rows


def summary_lines(tl: Timeline, final_turn: int, limit: int = 12) -> list[str]:
    """Turns per depth plus the most recent notable events (descents are summarised)."""
    per = tl.turns_per_depth(final_turn)
    out = ["Turns per depth: " + "  ".join(f"D{d}:{n}" for d, n in sorted(per.items()))]
    notable = [e for e in tl.events if e.kind != "depth"]
    if len(notable) > limit:
        out.append(f"  ... {len(notable) - limit} earlier events")
        notable = notable[-limit:]
    out += [e.line() for e in notable]
    return out
