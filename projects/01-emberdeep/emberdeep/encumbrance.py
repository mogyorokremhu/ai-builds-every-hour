"""Item weights, carrying capacity and pack-limit warnings.

Everything in your pack (equipped or not) has a weight. Your carrying capacity grows with
your *base* power (Might boons, shrine blessings), so a strong hero can haul plate armour
and a warhammer while a weakling has to choose:

* up to ``capacity``                → unburdened;
* up to ``capacity * OVERLOAD``     → **burdened**: you move at 3/4 speed;
* beyond that                       → you simply can't pick the item up.

The pack also has 26 letter slots (see :mod:`emberdeep.inventory`); :func:`slot_warning`
warns as they run out.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:  # pragma: no cover
    from .entities import Entity
    from .items import Item

#: Weight of one unit, by item key. Anything not listed falls back to :data:`KIND_WEIGHT`.
ITEM_WEIGHT: dict[str, int] = {
    "dagger": 3, "sword": 6, "warhammer": 11, "war axe": 9,
    "leather armor": 8, "chain mail": 15, "ember plate": 20,
    "ration": 2, "glowcap": 1, "torch": 2, "iron key": 1, "ember heart": 4,
}
KIND_WEIGHT: dict[str, int] = {
    "potion": 2, "scroll": 1, "ring": 0, "weapon": 6, "armor": 10, "food": 2, "tool": 2, "key": 1,
    "artifact": 4,
}

BASE_CAPACITY = 40
CAPACITY_PER_POWER = 4      # each point of base power adds this much capacity
OVERLOAD = 1.5              # can't carry more than capacity * OVERLOAD
BURDENED_SPEED = 0.75       # speed multiplier while burdened
SLOT_WARNING = 3            # warn when this few letter slots are left

UNBURDENED, BURDENED, OVERLOADED = "unburdened", "burdened", "overloaded"


def item_weight(item: "Item") -> int:
    """Weight of the whole stack ``item``."""
    unit = ITEM_WEIGHT.get(item.key, KIND_WEIGHT.get(item.kind, 1))
    return unit * item.count


def unit_weight(item: "Item") -> int:
    """Weight of a single unit of ``item``."""
    return ITEM_WEIGHT.get(item.key, KIND_WEIGHT.get(item.kind, 1))


def total_weight(items: Iterable["Item"]) -> int:
    """Total weight of ``items``, counting full stacks."""
    return sum(item_weight(i) for i in items)


def capacity(player: "Entity") -> int:
    """How much ``player`` can carry without being burdened."""
    return BASE_CAPACITY + CAPACITY_PER_POWER * max(0, player.fight.base_power)


def max_load(player: "Entity") -> int:
    """The heaviest load ``player`` can carry before becoming overloaded."""
    return int(capacity(player) * OVERLOAD)


def carried(player: "Entity") -> int:
    """Total weight of everything in ``player``'s pack."""
    return total_weight(player.pack.items)


def state_for(load: int, cap: int) -> str:
    """Encumbrance state for a ``load`` against carrying capacity ``cap``."""
    if load <= cap:
        return UNBURDENED
    if load <= int(cap * OVERLOAD):
        return BURDENED
    return OVERLOADED


def state(player: "Entity") -> str:
    """The player's current encumbrance state."""
    return state_for(carried(player), capacity(player))


def speed_multiplier(player: "Entity") -> float:
    """Movement-time multiplier from encumbrance (1.0 when unburdened)."""
    return 1.0 if state(player) == UNBURDENED else BURDENED_SPEED


def can_lift(player: "Entity", item: "Item") -> bool:
    """Would picking up ``item`` keep the load within the hard limit?"""
    return carried(player) + item_weight(item) <= max_load(player)


def load_label(player: "Entity") -> str:
    """Sidebar text like ``"23/60"`` (with a marker when burdened)."""
    load, cap = carried(player), capacity(player)
    mark = "" if load <= cap else " (burdened)"
    return f"{load}/{cap}{mark}"


def load_color(player: "Entity") -> str:
    """HUD colour for the load: red when over capacity, yellow above 80%, else white."""
    load, cap = carried(player), capacity(player)
    if load > cap:
        return "bright_red"
    if load > cap * 0.8:
        return "bright_yellow"
    return "white"


def transition_message(before: str, after: str) -> tuple[str, str] | None:
    """(text, colour) to show when the burden state changes, or None."""
    if before == after:
        return None
    if after == BURDENED and before == UNBURDENED:
        return "You are burdened by your load. You move more slowly.", "bright_yellow"
    if after == UNBURDENED:
        return "Your load feels manageable again.", "bright_green"
    return None


def slot_warning(free_slots: int) -> tuple[str, str] | None:
    """A warning when the 26 pack slots are nearly used up."""
    if free_slots <= 0:
        return "Your pack is now full — drop something to make room.", "bright_red"
    if free_slots <= SLOT_WARNING:
        s = "" if free_slots == 1 else "s"
        return f"Your pack is nearly full ({free_slots} slot{s} left).", "bright_yellow"
    return None


def heaviest_spare(player: "Entity") -> "Item | None":
    """The heaviest item that isn't equipped (what a burdened player should drop first)."""
    eq = player.gear
    spare = [i for i in player.pack.items if not eq.is_equipped(i) and i.kind != "artifact"]
    if not spare:
        return None
    return max(spare, key=lambda i: (unit_weight(i), item_weight(i)))
