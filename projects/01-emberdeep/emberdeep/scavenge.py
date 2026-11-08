"""Monsters that pick up items lying on the floor.

Creatures tagged ``scavenger`` (kobolds and their shamans) can't resist shiny things.
When they have nothing to hunt they walk to items they can see nearby and pick them up:

* a **healing potion** is stashed for later — cowardly kobolds drink it when hurt
  (see :func:`emberdeep.ai.drink_potion`);
* a **weapon** better than what it already wields is brandished (+power);
* anything else small goes in its sack.

Everything a scavenger carries falls to the floor when it dies. Carried items are stored
in ``ai_state["sack"]`` as plain ``[key, count]`` pairs so saves stay JSON. Iron keys and
the Ember Heart are never taken (that would be too cruel).
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .geometry import chebyshev
from .items import ITEM_TEMPLATES, make_item

if TYPE_CHECKING:  # pragma: no cover
    from .entities import Entity
    from .game import Game

SCAVENGE_RADIUS = 6       # how far a scavenger notices loot
MAX_SACK = 3              # items carried besides a potion / weapon
UNTOUCHABLE_KINDS = ("key", "artifact")


def is_scavenger(m: "Entity") -> bool:
    """True if ``m`` is a scavenger that picks up items."""
    return "scavenger" in m.tags


def wants(m: "Entity", item_ent: "Entity") -> bool:
    """Would ``m`` bother picking up the floor item ``item_ent``?"""
    it = item_ent.item
    if it is None or it.kind in UNTOUCHABLE_KINDS:
        return False
    if it.key == "healing potion":
        return not m.ai_state.get("potion")
    if it.slot == "weapon":
        return it.power_bonus > m.ai_state.get("weapon_bonus", 0)
    return len(m.ai_state.get("sack", [])) < MAX_SACK


def target_item(game: "Game", m: "Entity") -> "Entity | None":
    """The nearest wanted item within reach that the monster can see (shares the player's
    view of the map: a scavenger in the player's sight sees what the player sees)."""
    best: tuple[int, int, int, "Entity"] | None = None
    for e in game.entities:
        if e.item is None or chebyshev(e.pos, m.pos) > SCAVENGE_RADIUS or not wants(m, e):
            continue
        if game.blocking_at(*e.pos) not in (None, m):
            continue
        key = (chebyshev(e.pos, m.pos), e.y, e.x)
        if best is None or key < best[:3]:
            best = (*key, e)
    return best[3] if best else None


def pick_up(game: "Game", m: "Entity", item_ent: "Entity") -> None:
    """``m`` takes ``item_ent`` from the floor."""
    it = item_ent.thing
    game.entities.remove(item_ent)
    seen = game.gmap.visible[m.y][m.x]
    shown = it.display_name
    if it.key == "healing potion" and not m.ai_state.get("potion"):
        m.ai_state["potion"] = True
        if it.count > 1:  # keep one, the rest go in the sack
            m.ai_state.setdefault("sack", []).append([it.key, it.count - 1])
    elif it.slot == "weapon":
        old = m.ai_state.get("weapon")
        if old:
            m.ai_state.setdefault("sack", []).append([old, 1])
        m.fight.bonus_power += it.power_bonus - m.ai_state.get("weapon_bonus", 0)
        m.ai_state["weapon"], m.ai_state["weapon_bonus"] = it.key, it.power_bonus
        if seen:
            game.say(f"The {m.name} picks up {shown} and brandishes it!", "bright_yellow")
        return
    else:
        m.ai_state.setdefault("sack", []).append([it.key, it.count])
    if seen:
        game.say(f"The {m.name} picks up {shown}.", "bright_yellow")


def scavenge(game: "Game", m: "Entity") -> bool:
    """One idle action: walk to (or pick up) loot. Returns True if the monster acted."""
    from .ai import move_towards

    target = target_item(game, m)
    if target is None:
        return False
    if target.pos == m.pos:
        pick_up(game, m, target)
        return True
    return move_towards(game, m, target.pos)


def carried_items(m: "Entity") -> list[tuple[str, int]]:
    """Everything ``m`` carries, as (item key, count)."""
    out: list[tuple[str, int]] = []
    if m.ai_state.get("weapon"):
        out.append((m.ai_state["weapon"], 1))
    out += [(k, n) for k, n in m.ai_state.get("sack", [])]
    return out


def drop_all(game: "Game", m: "Entity") -> list[str]:
    """Drop the scavenger's loot where it stands (on death). Returns the keys dropped.

    The carried healing potion is handled separately by :meth:`Game.on_kill`."""
    dropped: list[str] = []
    for key, count in carried_items(m):
        if key not in ITEM_TEMPLATES:
            continue
        game.place_item(make_item(key, count), m.x, m.y)
        dropped.append(key)
    for k in ("weapon", "weapon_bonus", "sack"):
        m.ai_state.pop(k, None)
    return dropped


def describe(m: "Entity") -> str:
    """Look-mode hint about what a scavenger is carrying."""
    bits = []
    if m.ai_state.get("weapon"):
        bits.append(f"wields a {ITEM_TEMPLATES[m.ai_state['weapon']].name}")
    if m.ai_state.get("sack"):
        bits.append("carries a bulging sack")
    return ("It " + " and ".join(bits) + ".") if bits else ""
