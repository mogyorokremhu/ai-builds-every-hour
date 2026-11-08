"""Visual effects queue: projectiles and blasts for the front-ends to animate.

The game logic never sleeps or draws. Instead, actions that send something flying (thrown
items, fireballs, lightning, monster spells) push an :class:`Effect` onto
``game.effects``. The curses UI drains the queue after each action and plays the frames
(:func:`frames`) with a short delay; the text front-end and tests simply discard it.
"""
from __future__ import annotations

from dataclasses import dataclass, field

Cell = tuple[int, int]

#: glyph for a bolt travelling in direction (dx, dy)
BOLT_GLYPHS: dict[Cell, str] = {
    (0, -1): "|", (0, 1): "|", (-1, 0): "-", (1, 0): "-",
    (-1, -1): "\\", (1, 1): "\\", (1, -1): "/", (-1, 1): "/",
}
MAX_QUEUE = 32   # effects beyond this are dropped (a huge fight shouldn't freeze the UI)


@dataclass
class Effect:
    kind: str              # "bolt" (moving glyph along a path) or "blast" (cells flash at once)
    cells: list[Cell]
    color: str = "bright_yellow"
    glyph: str | None = None   # None: pick from the direction of travel (bolts) or "*"


@dataclass
class Frame:
    cells: dict[Cell, tuple[str, str]] = field(default_factory=dict)  # cell -> (glyph, color)


def bolt_glyph(prev: Cell, cur: Cell) -> str:
    dx = (cur[0] > prev[0]) - (cur[0] < prev[0])
    dy = (cur[1] > prev[1]) - (cur[1] < prev[1])
    return BOLT_GLYPHS.get((dx, dy), "*")


def frames(effect: Effect, origin: Cell | None = None) -> list[Frame]:
    """The animation frames for ``effect``. Bolts show one moving cell per frame (with a
    one-cell trail); blasts expand in two frames (centre then the whole area)."""
    out: list[Frame] = []
    if not effect.cells:
        return out
    if effect.kind == "bolt":
        prev = origin if origin is not None else effect.cells[0]
        trail: Cell | None = None
        for cell in effect.cells:
            glyph = effect.glyph or bolt_glyph(prev, cell)
            f = Frame({cell: (glyph, effect.color)})
            if trail is not None:
                f.cells[trail] = ("·", effect.color)
            out.append(f)
            trail, prev = cell, cell
        return out
    glyph = effect.glyph or "*"
    centre = effect.cells[0]
    out.append(Frame({centre: (glyph, effect.color)}))
    out.append(Frame({c: (glyph, effect.color) for c in effect.cells}))
    return out


def push(game, effect: Effect) -> None:
    """Queue ``effect`` on ``game`` (silently capped at :data:`MAX_QUEUE`)."""
    queue = getattr(game, "effects", None)
    if queue is None:
        return
    if len(queue) < MAX_QUEUE:
        queue.append(effect)


def drain(game) -> list[Effect]:
    """Take every queued effect off ``game``."""
    queue = getattr(game, "effects", None) or []
    out = list(queue)
    queue.clear()
    return out
