"""Visual effects for spells and projectiles.

The game logic doesn't animate anything; it just *records* what flew where by calling
:func:`emit`. A front-end that can animate (the curses UI) turns each :class:`Effect` into
frames with :func:`frames` and plays them, then clears the queue. Front-ends that can't
(text mode, the balance bot) simply ignore it — the queue is bounded, so it never grows.

Effect kinds:

* ``bolt``  — a single glyph travelling along ``cells`` (ember bolts, thrown daggers);
* ``beam``  — the whole line lights up at once and flickers (lightning);
* ``blast`` — an explosion spreading out from ``cells[0]`` in rings (fireball, nova).
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .geometry import chebyshev

if TYPE_CHECKING:  # pragma: no cover
    from .game import Game

Cell = tuple[int, int]
Frame = list[tuple[int, int, str, str]]  # (x, y, glyph, colour)

MAX_QUEUED = 24
TRAIL = 1          # bolt trail length (cells behind the head)


@dataclass
class Effect:
    kind: str                 # bolt | beam | blast
    cells: list[Cell]         # the path (bolt/beam) or [centre, *area] (blast)
    glyph: str = "*"
    color: str = "bright_yellow"


def new_queue() -> deque[Effect]:
    return deque(maxlen=MAX_QUEUED)


def emit(game: "Game", kind: str, cells: list[Cell], glyph: str = "*", color: str = "bright_yellow") -> None:
    """Record an effect for the UI to animate (no-op for empty paths)."""
    if not cells:
        return
    q = getattr(game, "fx", None)
    if q is None:
        q = game.fx = new_queue()
    q.append(Effect(kind, list(cells), glyph, color))


def drain(game: "Game") -> list[Effect]:
    """Take every pending effect (oldest first) and empty the queue."""
    q = getattr(game, "fx", None)
    if not q:
        return []
    out = list(q)
    q.clear()
    return out


def bolt_glyph(prev: Cell, cur: Cell) -> str:
    """A line glyph matching the direction of travel."""
    dx, dy = cur[0] - prev[0], cur[1] - prev[1]
    if dy == 0:
        return "-"
    if dx == 0:
        return "|"
    return "\\" if (dx > 0) == (dy > 0) else "/"


def frames(effect: Effect, origin: Cell | None = None) -> list[Frame]:
    """Turn an effect into animation frames. ``origin`` is where a bolt/beam started."""
    cells = effect.cells
    if effect.kind == "bolt":
        out: list[Frame] = []
        for i, cell in enumerate(cells):
            frame: Frame = []
            for j in range(max(0, i - TRAIL), i):
                frame.append((*cells[j], "·", effect.color))
            frame.append((*cell, effect.glyph, effect.color))
            out.append(frame)
        return out
    if effect.kind == "beam":
        prev = origin if origin is not None else cells[0]
        line: Frame = []
        for cell in cells:
            line.append((*cell, bolt_glyph(prev, cell) if prev != cell else "*", effect.color))
            prev = cell
        dim = [(x, y, g, "white") for x, y, g, _ in line]
        return [line, dim, line]
    if effect.kind == "blast":
        centre = cells[0]
        rings: dict[int, list[Cell]] = {}
        for c in cells:
            rings.setdefault(chebyshev(c, centre), []).append(c)
        out = []
        shown: list[Cell] = []
        for r in sorted(rings):
            shown += rings[r]
            out.append([(x, y, "*" if chebyshev((x, y), centre) == r else "░", effect.color)
                        for x, y in shown])
        return out
    raise ValueError(f"unknown effect kind {effect.kind!r}")
