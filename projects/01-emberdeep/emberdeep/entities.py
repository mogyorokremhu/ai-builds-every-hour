"""Entities (player, monsters, items on the floor) and their combat stats."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .status import StatusSet

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
    ai: str | None = None  # chase | coward | caster | pack (see ai.py)
    xp_value: int = 0
    tags: set[str] = field(default_factory=set)
    color: str = "white"
    item: "Item | None" = None
    inventory: "Inventory | None" = None
    equipment: "Equipment | None" = None
    statuses: StatusSet = field(default_factory=StatusSet)
    speed: int = 100            # 100 = normal; 200 acts twice per normal turn
    energy: int = 0             # accumulates speed; acts at ENERGY_PER_ACTION
    memory: tuple[int, int] | None = None  # last place the player was seen
    on_hit: tuple[str, int, int, float] | None = None  # (status, turns, power, chance)
    spell: str | None = None    # key into ai.SPELLS for casters
    ai_state: dict[str, Any] = field(default_factory=dict)
    asleep: bool = False        # sleeping monsters ignore you until noise wakes them

    @property
    def confused(self) -> int:
        """Turns of confusion left (backed by the status system)."""
        return self.statuses.turns("confused")

    @confused.setter
    def confused(self, turns: int) -> None:
        self.statuses.set_turns("confused", turns)

    @property
    def effective_speed(self) -> int:
        return max(1, int(self.speed * self.statuses.speed_multiplier()))

    @property
    def pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    @property
    def is_player(self) -> bool:
        return "player" in self.tags

    def immune_to(self, status: str) -> bool:
        return f"immune:{status}" in self.tags

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy


#: Monster templates. Optional keys: ai (default "chase"), speed (default 100),
#: on_hit (status, turns, power, chance), spell (see ai.SPELLS), max_depth,
#: immune (statuses that can't affect it, stored as ``immune:<name>`` tags), tags.
MONSTER_TEMPLATES: dict[str, dict] = {
    "rat": dict(glyph="r", color="yellow", hp=4, power=2, defense=0, xp=5, min_depth=1, weight=40,
                max_depth=4),
    "kobold": dict(glyph="k", color="green", hp=8, power=3, defense=0, xp=12, min_depth=1, weight=30,
                   ai="coward"),
    "jackal": dict(glyph="j", color="yellow", hp=5, power=2, defense=0, xp=8, min_depth=2, weight=18,
                   ai="pack", speed=150, pack=(2, 4)),
    "ember imp": dict(glyph="i", color="red", hp=10, power=4, defense=1, xp=20, min_depth=2, weight=14,
                      ai="caster", spell="ember bolt", immune=("burning",)),
    "cave spider": dict(glyph="s", color="bright_green", hp=9, power=3, defense=1, xp=22, min_depth=3,
                        weight=14, speed=120, on_hit=("poisoned", 5, 1, 0.5)),
    "kobold shaman": dict(glyph="k", color="bright_cyan", hp=9, power=2, defense=0, xp=28, min_depth=3,
                          weight=10, ai="caster", spell="hex of slowness"),
    "fire beetle": dict(glyph="b", color="bright_red", hp=16, power=4, defense=3, xp=30, min_depth=3,
                        weight=12, speed=70, on_hit=("burning", 3, 2, 0.4), immune=("burning",)),
    "myconid": dict(glyph="m", color="bright_magenta", hp=12, power=3, defense=1, xp=26, min_depth=4,
                    weight=8, speed=80, on_hit=("confused", 3, 0, 0.35)),
    "magma hound": dict(glyph="h", color="bright_red", hp=14, power=5, defense=1, xp=40, min_depth=7,
                        weight=10, ai="pack", speed=140, pack=(2, 3), on_hit=("burning", 3, 2, 0.3),
                        immune=("burning",)),
    # the final boss (never spawned randomly: see boss.py)
    "Ember Guardian": dict(glyph="&", color="bright_red", hp=150, power=9, defense=3, xp=400, min_depth=99,
                           weight=0, ai="boss", spell="magma burst", immune=("burning", "confused"),
                           tags=("boss",)),
    "cave troll": dict(glyph="T", color="magenta", hp=22, power=6, defense=2, xp=55, min_depth=4, weight=8,
                       tags=("knockback",)),
}


def make_monster(kind: str, x: int, y: int) -> Entity:
    t = MONSTER_TEMPLATES[kind]
    return Entity(
        name=kind,
        glyph=t["glyph"],
        x=x,
        y=y,
        fighter=Fighter(t["hp"], t["hp"], t["power"], t["defense"]),
        ai=t.get("ai", "chase"),
        xp_value=t["xp"],
        color=t["color"],
        speed=t.get("speed", 100),
        on_hit=t.get("on_hit"),
        spell=t.get("spell"),
        tags=set(t.get("tags", ())) | {f"immune:{s}" for s in t.get("immune", ())},
    )


def make_player(x: int, y: int) -> Entity:
    from .equipment import Equipment
    from .inventory import Inventory

    return Entity(
        "you", "@", x, y, Fighter(30, 30, 5, 1), tags={"player"}, color="bright_white",
        inventory=Inventory(), equipment=Equipment(),
    )
