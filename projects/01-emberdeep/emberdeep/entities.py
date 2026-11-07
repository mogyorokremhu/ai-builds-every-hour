"""Entities (player, monsters, items on the floor) and their combat stats."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .equipment import Equipment
    from .inventory import Inventory
    from .items import Item


@dataclass
class Fighter:
    """Combat stats. Equipment adds to the ``bonus_*`` fields."""

    base_max_hp: int
    hp: int
    base_power: int
    base_defense: int
    bonus_hp: int = 0
    bonus_power: int = 0
    bonus_defense: int = 0

    @property
    def max_hp(self) -> int:
        return self.base_max_hp + self.bonus_hp

    @property
    def power(self) -> int:
        return self.base_power + self.bonus_power

    @property
    def defense(self) -> int:
        return self.base_defense + self.bonus_defense

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        dealt = max(0, min(amount, self.hp))
        self.hp -= dealt
        return dealt

    def heal(self, amount: int) -> int:
        healed = max(0, min(amount, self.max_hp - self.hp))
        self.hp += healed
        return healed


@dataclass
class Entity:
    name: str
    glyph: str
    x: int
    y: int
    fighter: Fighter | None = None
    blocks: bool = True
    ai: str | None = None  # "chase" for now; more AI kinds coming
    xp_value: int = 0
    tags: set[str] = field(default_factory=set)
    color: str = "white"
    item: "Item | None" = None
    inventory: "Inventory | None" = None
    equipment: "Equipment | None" = None
    confused: int = 0  # turns of confusion left

    @property
    def pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    @property
    def is_player(self) -> bool:
        return "player" in self.tags

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy


MONSTER_TEMPLATES: dict[str, dict] = {
    "rat": dict(glyph="r", color="yellow", hp=4, power=2, defense=0, xp=5, min_depth=1, weight=40),
    "kobold": dict(glyph="k", color="green", hp=8, power=3, defense=0, xp=12, min_depth=1, weight=30),
    "ember imp": dict(glyph="i", color="red", hp=10, power=4, defense=1, xp=20, min_depth=2, weight=20),
    "cave troll": dict(glyph="T", color="magenta", hp=22, power=6, defense=2, xp=55, min_depth=4, weight=8),
}


def make_monster(kind: str, x: int, y: int) -> Entity:
    t = MONSTER_TEMPLATES[kind]
    return Entity(
        name=kind,
        glyph=t["glyph"],
        x=x,
        y=y,
        fighter=Fighter(t["hp"], t["hp"], t["power"], t["defense"]),
        ai="chase",
        xp_value=t["xp"],
        color=t["color"],
    )


def make_player(x: int, y: int) -> Entity:
    from .equipment import Equipment
    from .inventory import Inventory

    return Entity(
        "you", "@", x, y, Fighter(30, 30, 5, 1), tags={"player"}, color="bright_white",
        inventory=Inventory(), equipment=Equipment(),
    )
