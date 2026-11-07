"""Item definitions: consumables (potions, scrolls) and equipment.

Items are plain data. Their *effects* are applied by :mod:`emberdeep.game`, which keeps
this module free of game-state imports and easy to test.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

from .entities import Entity

#: Targeting modes for usable items.
TARGET_NONE = None      # used on yourself (potions, teleport)
TARGET_AUTO = "auto"    # automatically hits the nearest visible monster (lightning)
TARGET_CELL = "cell"    # player picks a cell with the targeting cursor (fireball, confusion)


@dataclass
class Item:
    key: str
    name: str
    glyph: str
    color: str
    kind: str                       # potion | scroll | weapon | armor | ring
    effect: str | None = None       # heal | lightning | fireball | confuse | teleport
    targeting: str | None = TARGET_NONE
    magnitude: int = 0              # healing amount / damage / turns
    radius: int = 0                 # area of effect (fireball)
    range: int = 0                  # max distance for targeted items
    slot: str | None = None         # weapon | armor | ring
    power_bonus: int = 0
    defense_bonus: int = 0
    hp_bonus: int = 0
    stackable: bool = False
    count: int = 1

    @property
    def is_equipment(self) -> bool:
        return self.slot is not None

    @property
    def display_name(self) -> str:
        if self.count > 1:
            return f"{self.count} {plural(self.name)}"
        return self.name

    def describe(self) -> str:
        """One-line description used by the inventory screen."""
        bits: list[str] = []
        if self.power_bonus:
            bits.append(f"{self.power_bonus:+d} power")
        if self.defense_bonus:
            bits.append(f"{self.defense_bonus:+d} defense")
        if self.hp_bonus:
            bits.append(f"{self.hp_bonus:+d} max HP")
        if self.effect == "heal":
            bits.append(f"heals {self.magnitude}")
        elif self.effect in ("lightning", "fireball"):
            bits.append(f"{self.magnitude} damage")
            if self.radius:
                bits.append(f"radius {self.radius}")
        elif self.effect == "confuse":
            bits.append(f"confuses for {self.magnitude} turns")
        elif self.effect == "teleport":
            bits.append("random teleport")
        return ", ".join(bits)


def plural(name: str) -> str:
    """Pluralise 'potion of healing' -> 'potions of healing'."""
    head, sep, tail = name.partition(" of ")
    return f"{head}s{sep}{tail}" if sep else f"{name}s"


def _c(key: str, name: str, glyph: str, color: str, kind: str, **kw) -> Item:
    return Item(key=key, name=name, glyph=glyph, color=color, kind=kind, **kw)


ITEM_TEMPLATES: dict[str, Item] = {
    # consumables
    "healing potion": _c("healing potion", "potion of healing", "!", "magenta", "potion",
                         effect="heal", magnitude=12, stackable=True),
    "greater healing potion": _c("greater healing potion", "potion of greater healing", "!", "bright_magenta",
                                 "potion", effect="heal", magnitude=30, stackable=True),
    "lightning scroll": _c("lightning scroll", "scroll of lightning", "?", "bright_yellow", "scroll",
                           effect="lightning", targeting=TARGET_AUTO, magnitude=14, range=7, stackable=True),
    "fireball scroll": _c("fireball scroll", "scroll of fireball", "?", "red", "scroll",
                          effect="fireball", targeting=TARGET_CELL, magnitude=10, radius=2, range=9,
                          stackable=True),
    "confusion scroll": _c("confusion scroll", "scroll of confusion", "?", "cyan", "scroll",
                           effect="confuse", targeting=TARGET_CELL, magnitude=8, range=8, stackable=True),
    "teleport scroll": _c("teleport scroll", "scroll of teleportation", "?", "bright_cyan", "scroll",
                          effect="teleport", stackable=True),
    # weapons
    "dagger": _c("dagger", "dagger", "/", "bright_white", "weapon", slot="weapon", power_bonus=1),
    "sword": _c("sword", "sword", "/", "bright_cyan", "weapon", slot="weapon", power_bonus=3),
    "war axe": _c("war axe", "war axe", "/", "bright_red", "weapon", slot="weapon", power_bonus=5,
                  defense_bonus=-1),
    # armor
    "leather armor": _c("leather armor", "leather armor", "[", "yellow", "armor", slot="armor", defense_bonus=1),
    "chain mail": _c("chain mail", "chain mail", "[", "bright_white", "armor", slot="armor", defense_bonus=2),
    "ember plate": _c("ember plate", "ember plate", "[", "bright_red", "armor", slot="armor", defense_bonus=4,
                      hp_bonus=5),
    # rings
    "ring of strength": _c("ring of strength", "ring of strength", "=", "bright_yellow", "ring", slot="ring",
                           power_bonus=2),
    "ring of protection": _c("ring of protection", "ring of protection", "=", "bright_blue", "ring",
                             slot="ring", defense_bonus=2),
    "ring of vitality": _c("ring of vitality", "ring of vitality", "=", "bright_green", "ring", slot="ring",
                           hp_bonus=10),
}


def make_item(key: str, count: int = 1) -> Item:
    """Return a fresh copy of an item template."""
    return replace(ITEM_TEMPLATES[key], count=count)


def make_item_entity(item: Item, x: int, y: int) -> Entity:
    """Wrap an item in a non-blocking map entity so it can lie on the floor."""
    return Entity(name=item.display_name, glyph=item.glyph, x=x, y=y, blocks=False,
                  color=item.color, item=item, tags={"item"})
