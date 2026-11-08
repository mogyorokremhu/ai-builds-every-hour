"""Special rooms ("vaults") that make some levels memorable.

* **treasury** — a pile of better-than-usual loot, guarded by sleeping monsters.
* **shrine**   — an altar (``_``); pray at it (``p``) once for healing and a blessing.
* **trap room** — bait in the middle of a floor riddled with hidden traps.
* **library**  — shelves of scrolls.

Special rooms are only carved into room-based levels, never the start or stairs room.
Entering one for the first time prints a hint.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from . import loot, traps
from .entities import make_monster
from .geometry import Rect
from .items import make_item
from .tiles import ALTAR

if TYPE_CHECKING:  # pragma: no cover
    from .game import Game

#: kind -> (weight, minimum depth, entry message)
VAULT_KINDS: dict[str, tuple[int, int, str]] = {
    "treasury": (3, 2, "Gold glints in the dark: a treasury! Something guards it."),
    "shrine": (3, 1, "A quiet shrine. An altar of black stone stands here (p to pray)."),
    "trap room": (2, 2, "The floor here is suspiciously clean..."),
    "library": (2, 1, "Shelves of crumbling scrolls line the walls of this library."),
}

VAULT_CHANCE = 0.6        # chance a room level gets at least one special room
SECOND_VAULT_CHANCE = 0.25

BLESSINGS = ("might", "guard", "vigor")


@dataclass
class SpecialRoom:
    """A special room (vault) on the level, of a given kind, and whether it has been entered."""
    kind: str
    rect: Rect
    visited: bool = False

    def contains(self, x: int, y: int) -> bool:
        """True if (x, y) is inside the room."""
        return self.rect.contains(x, y)


def _free(game: "Game", room: Rect) -> list[tuple[int, int]]:
    return [p for p in room.inner() if game.gmap.walkable(*p) and not game.blocking_at(*p)
            and not game.items_at(*p) and p not in game.traps and p != game.gmap.stairs]


def pick_kind(game: "Game") -> str:
    """Pick a random vault kind available at the current depth, by weight."""
    pool = [(k, w) for k, (w, lo, _) in VAULT_KINDS.items() if game.depth >= lo]
    kinds, weights = zip(*pool)
    return game.rng.choices(kinds, weights=weights)[0]


def build(game: "Game", kind: str, room: Rect) -> SpecialRoom:
    """Furnish ``room`` as a special room of ``kind``."""
    rng = game.rng
    cells = _free(game, room)
    if kind == "treasury":
        for _ in range(rng.randint(3, 5)):
            free = _free(game, room)
            if free:
                game.place_item(loot.roll_loot(game.depth + 2, rng), *rng.choice(free))
        for _ in range(rng.randint(1, 2)):
            free = _free(game, room)
            if free:
                m = make_monster(game.pick_monster(), *rng.choice(free))
                m.asleep = True
                game.entities.append(m)
    elif kind == "shrine":
        cx, cy = room.center
        game.gmap.set(cx, cy, ALTAR)
        game.altars[(cx, cy)] = False  # not yet used
    elif kind == "trap room":
        cx, cy = room.center
        if game.gmap.walkable(cx, cy):
            game.place_item(loot.roll_loot(game.depth + 1, rng), cx, cy)
        bait = (cx, cy)
        traps.place(game, [c for c in cells if c != bait], max(3, len(cells) // 4))
    elif kind == "library":
        for _ in range(rng.randint(2, 4)):
            free = _free(game, room)
            if free:
                key = rng.choice(["lightning scroll", "confusion scroll", "teleport scroll",
                                  "fireball scroll" if game.depth >= 3 else "lightning scroll"])
                game.place_item(make_item(key), *rng.choice(free))
    sr = SpecialRoom(kind, room)
    game.special_rooms.append(sr)
    return sr


def furnish(game: "Game", rooms: list[Rect]) -> list[SpecialRoom]:
    """Maybe turn one or two of ``rooms`` (excluding start and stairs rooms) into vaults."""
    candidates = [r for r in rooms[1:-1] if r.w >= 5 and r.h >= 5]
    built: list[SpecialRoom] = []
    if not candidates or game.rng.random() > VAULT_CHANCE:
        return built
    count = 2 if len(candidates) > 3 and game.rng.random() < SECOND_VAULT_CHANCE else 1
    for room in game.rng.sample(candidates, min(count, len(candidates))):
        built.append(build(game, pick_kind(game), room))
    return built


def check_enter(game: "Game") -> SpecialRoom | None:
    """Announce a special room the first time the player steps into it."""
    for sr in game.special_rooms:
        if not sr.visited and sr.contains(*game.player.pos):
            sr.visited = True
            from .game import C_MAGIC

            game.say(VAULT_KINDS[sr.kind][2], C_MAGIC)
            return sr
    return None


def pray(game: "Game") -> bool:
    """Pray at the altar under the player. Returns True if a turn was spent."""
    from .game import C_GOOD, C_INFO

    pos = game.player.pos
    if pos not in game.altars:
        game.say("There is no altar here.")
        return False
    if game.altars[pos]:
        game.say("The altar is cold and silent.", C_INFO)
        return False
    game.altars[pos] = True
    f = game.player.fight
    f.hp = f.max_hp
    for name in ("burning", "poisoned", "slowed", "confused"):
        game.player.statuses.remove(name)
    blessing = game.rng.choice(BLESSINGS)
    if blessing == "might":
        f.base_power += 1
        text = "You feel the strength of the deep in your arms. (+1 power)"
    elif blessing == "guard":
        f.base_defense += 1
        text = "A warm glow settles over your skin. (+1 defense)"
    else:
        f.base_max_hp += 5
        f.hp = f.max_hp
        text = "Your heart beats stronger. (+5 max HP)"
    game.say("You kneel and pray. Warmth floods through you.", C_GOOD)
    game.say(text, C_GOOD)
    game.resources.refuel(200)
    return True
