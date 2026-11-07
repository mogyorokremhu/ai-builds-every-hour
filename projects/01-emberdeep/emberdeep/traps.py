"""Traps: hidden until found, then shown as ``^``.

Hidden traps can be noticed passively when you stand next to them, or found on purpose
with the search command (which takes a turn but has a much better chance). Walking onto a
*known* trap needs a second, deliberate step. Monsters know their own lairs and never
trigger traps.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .geometry import chebyshev

if TYPE_CHECKING:  # pragma: no cover
    from .game import Game

Pos = tuple[int, int]

#: kind -> (display name, colour, minimum depth, weight)
TRAP_KINDS: dict[str, tuple[str, str, int, int]] = {
    "dart": ("poison dart trap", "bright_green", 1, 30),
    "fire": ("fire trap", "bright_red", 2, 22),
    "alarm": ("alarm trap", "bright_yellow", 1, 18),
    "teleport": ("teleport trap", "bright_magenta", 3, 12),
    "net": ("snare trap", "cyan", 1, 18),
}

PASSIVE_CHANCE = 0.15   # per adjacent hidden trap per turn
SEARCH_CHANCE = 0.7     # per hidden trap within SEARCH_RADIUS when searching
SEARCH_RADIUS = 2


@dataclass
class Trap:
    kind: str
    x: int
    y: int
    hidden: bool = True
    triggered: int = 0

    @property
    def pos(self) -> Pos:
        return (self.x, self.y)

    @property
    def name(self) -> str:
        return TRAP_KINDS[self.kind][0]

    @property
    def color(self) -> str:
        return TRAP_KINDS[self.kind][1]


def roll_kind(depth: int, rng: random.Random) -> str:
    pool = [(k, w) for k, (_, _, lo, w) in TRAP_KINDS.items() if depth >= lo]
    kinds, weights = zip(*pool)
    return rng.choices(kinds, weights=weights)[0]


def traps_for_depth(depth: int, rng: random.Random) -> int:
    """How many loose traps a level gets outside trap rooms."""
    return rng.randint(0, 1 + depth // 2)


def place(game: "Game", cells: list[Pos], count: int, kind: str | None = None) -> list[Trap]:
    """Place up to ``count`` hidden traps on free cells from ``cells``."""
    placed: list[Trap] = []
    gmap = game.gmap
    free = [c for c in cells if c not in game.traps and c != game.player.pos and c != gmap.stairs
            and gmap.walkable(*c) and gmap.get(*c).name != "door"
            and chebyshev(c, game.player.pos) > 2]
    game.rng.shuffle(free)
    for x, y in free[:count]:
        trap = Trap(kind or roll_kind(game.depth, game.rng), x, y)
        game.traps[(x, y)] = trap
        placed.append(trap)
    return placed


def passive_detect(game: "Game") -> list[Trap]:
    """Chance to notice hidden traps next to the player. Returns the newly found traps."""
    return _detect(game, 1, PASSIVE_CHANCE)


def search(game: "Game") -> list[Trap]:
    return _detect(game, SEARCH_RADIUS, SEARCH_CHANCE)


def _detect(game: "Game", radius: int, chance: float) -> list[Trap]:
    found = []
    for trap in game.traps.values():
        if trap.hidden and chebyshev(trap.pos, game.player.pos) <= radius and game.rng.random() < chance:
            trap.hidden = False
            found.append(trap)
    return found


def trigger(game: "Game", trap: Trap) -> None:
    """Spring ``trap`` on the player."""
    from .game import C_BAD, C_MAGIC  # local import: game imports this module

    was_hidden = trap.hidden
    trap.hidden = False
    trap.triggered += 1
    p = game.player
    game.say(("You step on a hidden " if was_hidden else "You set off the ") + f"{trap.name}!", C_BAD)
    if trap.kind == "dart":
        dealt = p.fighter.take_damage(game.rng.randint(1, 3))
        game.say(f"A dart pricks you for {dealt}.", C_BAD)
        if p.fighter.alive:
            game.apply_status(p, "poisoned", 4 + game.depth // 2, 1)
        else:
            game.death_cause = "killed by a poison dart"
    elif trap.kind == "fire":
        dealt = p.fighter.take_damage(2 + game.depth // 2)
        game.say(f"Flames burst from the floor for {dealt}!", C_BAD)
        if p.fighter.alive:
            game.apply_status(p, "burning", 3, 1)
        else:
            game.death_cause = "burned by a fire trap"
    elif trap.kind == "net":
        game.apply_status(p, "slowed", 6)
    elif trap.kind == "alarm":
        game.say("A shrill alarm echoes through the halls!", C_MAGIC)
        for m in game.monsters:
            m.asleep = False
            m.memory = p.pos
    elif trap.kind == "teleport":
        game._effect_teleport(None, None)
