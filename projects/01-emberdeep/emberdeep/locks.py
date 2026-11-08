"""Locked doors and the iron keys that open them.

Now and then a room is sealed with locked doors (shown as a red ``+``). Monsters can't
open them, and they block sight. Somewhere *outside* the room — always reachable without
passing a locked door — lies an iron key. Bumping a locked door with a key in your pack
unlocks it (the key is used up). Without a key you can try to force the door: each attempt
takes a turn, is very loud, and succeeds more often the mightier you are.

Locked rooms are usually treasuries (if the level has one) or "storerooms" with extra loot.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from . import loot
from .gen_caves import bfs_distances
from .geometry import Rect
from .items import make_item
from .tiles import LOCKED_DOOR, OPEN_DOOR

if TYPE_CHECKING:  # pragma: no cover
    from .game import Game

LOCK_CHANCE = 0.35          # chance a room level (depth >= 2) gets a locked room
MAX_OPENINGS = 3
FORCE_BASE = 0.08           # chance to force a door open ...
FORCE_PER_POWER = 0.025     # ... plus this per point of power

Pos = tuple[int, int]


def border(rect: Rect) -> list[Pos]:
    """The ring of cells forming the room's wall (the rectangle's edge)."""
    cells: list[Pos] = []
    for x in range(rect.x, rect.x2):
        cells += [(x, rect.y), (x, rect.y2 - 1)]
    for y in range(rect.y + 1, rect.y2 - 1):
        cells += [(rect.x, y), (rect.x2 - 1, y)]
    return cells


def openings(game: "Game", rect: Rect) -> list[Pos]:
    """Walkable cells (or doors) in the room's wall ring: where you can get in."""
    gm = game.gmap
    return [p for p in border(rect) if gm.passable(*p)]


def try_lock(game: "Game", rect: Rect, start: Pos) -> list[Pos]:
    """Seal ``rect`` with locked doors if that keeps the rest of the level connected.

    Returns the locked cells (empty if the room is unsuitable; the map is then unchanged).
    """
    gm = game.gmap
    inside = set(rect.inner())
    if start in inside or start in border(rect) or (gm.stairs and (gm.stairs in inside or
                                                                   gm.stairs in border(rect))):
        return []
    holes = openings(game, rect)
    if not holes or len(holes) > MAX_OPENINGS:
        return []
    before = bfs_distances(gm, start)
    old = {p: gm.get(*p) for p in holes}
    for p in holes:
        gm.set(*p, LOCKED_DOOR)
    after = bfs_distances(gm, start)
    lost = [p for p in before if p not in after and p not in inside and p not in old]
    if lost or (gm.stairs and gm.stairs not in after):
        for p, t in old.items():
            gm.set(*p, t)
        return []
    return holes


def key_spots(game: "Game", start: Pos, rooms: list[Rect]) -> list[Pos]:
    """Free floor cells reachable from ``start`` without crossing a locked door."""
    reach = bfs_distances(game.gmap, start)
    gm = game.gmap
    return [p for p in reach if gm.get(*p).name in ("floor", "fungus", "rubble") and p != start
            and not game.items_at(*p) and not game.blocking_at(*p) and p not in game.traps]


def furnish_locks(game: "Game", rooms: list[Rect], start: Pos) -> Rect | None:
    """Maybe lock one room on this level and hide a key for it. Returns the locked room."""
    rng = game.rng
    if game.depth < 2 or len(rooms) < 4 or rng.random() > LOCK_CHANCE:
        return None
    treasuries = [sr.rect for sr in game.special_rooms if sr.kind == "treasury"]
    others = [r for r in rooms[1:-1] if r not in treasuries
              and not any(sr.rect == r for sr in game.special_rooms)]
    rng.shuffle(others)
    for rect in treasuries + others:
        if not try_lock(game, rect, start):
            continue
        if rect not in treasuries:  # a storeroom: extra loot behind the door
            cells = [p for p in rect.inner() if game.gmap.walkable(*p) and not game.items_at(*p)]
            for _ in range(rng.randint(2, 3)):
                if cells:
                    p = cells.pop(rng.randrange(len(cells)))
                    game.place_item(loot.roll_loot(game.depth + 1, rng, game.theme.loot_bias), *p)
        spots = key_spots(game, start, rooms)
        if spots:
            game.place_item(make_item("iron key"), *rng.choice(spots))
        return rect
    return None


def force_chance(power: int) -> float:
    """Chance to force a locked door open, growing with ``power`` and capped at 75%."""
    return min(0.75, FORCE_BASE + FORCE_PER_POWER * max(0, power))


def bump_locked(game: "Game", x: int, y: int) -> bool:
    """The player bumps the locked door at (x, y). Returns True if a turn was spent."""
    from .game import C_BAD, C_GOOD, C_INFO, NOISE

    inv = game.player.pack
    key = next((it for it in inv if it.key == "iron key"), None)
    if key is not None:
        inv.take_one(key)
        game.gmap.set(x, y, OPEN_DOOR)
        game.say("You turn the iron key. The lock clicks open.", C_GOOD)
        game.noise = NOISE["door"]
        game.end_turn()
        return True
    if game._force_confirm != (x, y):
        game._force_confirm = (x, y)
        game.say("The door is locked. Find an iron key, or bump again to force it.", C_INFO)
        return False
    game.noise = NOISE["loud"]
    if game.rng.random() < force_chance(game.player.fight.power):
        game.gmap.set(x, y, OPEN_DOOR)
        game._force_confirm = None
        game.say("With a splintering crash you force the door open!", C_GOOD)
    else:
        game.say("You slam into the door. It holds. (bump again to keep trying)", C_BAD)
    game.end_turn()
    return True
