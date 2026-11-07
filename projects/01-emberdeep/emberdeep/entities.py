"""Entities (player, monsters) and their combat stats."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Fighter:
    max_hp: int
    hp: int
    power: int
    defense: int

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        dealt = max(0, min(amount, self.hp))
        self.hp -= dealt
        return dealt

    def heal(self, amount: int) -> int:
        healed = min(amount, self.max_hp - self.hp)
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

    @property
    def pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy


MONSTER_TEMPLATES: dict[str, dict] = {
    "rat": dict(glyph="r", hp=4, power=2, defense=0, xp=5, min_depth=1, weight=40),
    "kobold": dict(glyph="k", hp=8, power=3, defense=0, xp=12, min_depth=1, weight=30),
    "ember imp": dict(glyph="i", hp=10, power=4, defense=1, xp=20, min_depth=2, weight=20),
    "cave troll": dict(glyph="T", hp=22, power=6, defense=2, xp=55, min_depth=4, weight=8),
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
    )


def make_player(x: int, y: int) -> Entity:
    return Entity("you", "@", x, y, Fighter(30, 30, 5, 1), tags={"player"})
