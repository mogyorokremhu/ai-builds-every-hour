"""Scavengers: kobolds (and their shamans) pick up items lying on the floor.

* A scavenger standing on an item picks it up (that takes its action). It carries at
  most :data:`CARRY_LIMIT` items in a small pack of its own.
* When it doesn't see you, it wanders toward shiny things within :data:`SNIFF_RADIUS`.
* A picked-up **weapon** is wielded: the kobold gains the weapon's power bonus.
* A picked-up **healing potion** is drunk when the kobold is hurt (see ``ai.drink_potion``).
* Everything it carries drops when it dies — you get your stuff back.

Artifacts (the Ember Heart) and iron keys are never taken: keys must stay reachable so
locked rooms remain solvable, and the Heart is far too hot to hold.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .geometry import chebyshev
from .inventory import Inventory

if TYPE_CHECKING:  # pragma: no cover
    from .entities import Entity
    from .game import Game
    from .items import Item

SCAVENGERS = frozenset({"kobold", "kobold shaman"})
CARRY_LIMIT = 3
SNIFF_RADIUS = 5
NEVER_TAKE = frozenset({"artifact"})
NEVER_TAKE_KEYS = frozenset({"iron key", "ember heart"})


def is_scavenger(m: "Entity") -> bool:
    return m.name in SCAVENGERS and m.ai is not None


def wants(item: "Item") -> bool:
    return item.kind not in NEVER_TAKE and item.key not in NEVER_TAKE_KEYS


def carried(m: "Entity") -> list["Item"]:
    return list(m.inventory.items) if m.inventory is not None else []


def has_room(m: "Entity") -> bool:
    return m.inventory is None or not m.inventory.full


def try_pickup(game: "Game", m: "Entity") -> bool:
    """Pick up a wanted item under ``m``. Returns True if that used the monster's action."""
    if not is_scavenger(m) or not has_room(m):
        return False
    here = [e for e in game.items_at(*m.pos) if wants(e.item)]
    if not here:
        return False
    ent = here[0]
    if m.inventory is None:
        m.inventory = Inventory(CARRY_LIMIT)
    item = ent.item
    m.inventory.add(item)
    game.entities.remove(ent)
    seen = game.gmap.visible[m.y][m.x]
    if seen:
        game.say(f"The {m.name} picks up {item.display_name}.", "yellow")
    if item.slot == "weapon" and item.power_bonus > 0 and "armed" not in m.ai_state:
        m.ai_state["armed"] = item.power_bonus
        m.fighter.bonus_power += item.power_bonus
        if seen:
            game.say(f"The {m.name} brandishes the {item.shown_name}!", "bright_red")
    return True


def has_potion(m: "Entity") -> bool:
    """Does ``m`` have a healing potion to drink (spawned with one, or picked one up)?"""
    return bool(m.ai_state.get("potion")) or any(it.key == "healing potion" for it in carried(m))


def nearest_loot(game: "Game", m: "Entity") -> tuple[int, int] | None:
    """The closest wanted floor item within sniffing range, if any."""
    best: tuple[int, tuple[int, int]] | None = None
    for e in game.entities:
        if e.item is None or not wants(e.item):
            continue
        d = chebyshev(e.pos, m.pos)
        if d <= SNIFF_RADIUS and (best is None or d < best[0]):
            best = (d, e.pos)
    return best[1] if best else None


def forage(game: "Game", m: "Entity") -> bool:
    """When idle (not hunting): walk toward loot. Returns True if it moved."""
    from .ai import move_towards

    if not is_scavenger(m) or not has_room(m) or m.ai_state.get("fleeing"):
        return False
    goal = nearest_loot(game, m)
    if goal is None or goal == m.pos:
        return False
    return move_towards(game, m, goal)


def use_potion(m: "Entity") -> bool:
    """Remove one carried healing potion (it is being drunk). Returns True if one was found."""
    if m.inventory is None:
        return False
    for it in m.inventory.items:
        if it.key == "healing potion":
            m.inventory.take_one(it)
            return True
    return False


def drop_all(game: "Game", m: "Entity") -> list["Item"]:
    """On death: everything the scavenger carried falls to the floor."""
    items = carried(m)
    for it in items:
        game.place_item(it, m.x, m.y)
    if m.inventory is not None:
        m.inventory.items = []
    return items
