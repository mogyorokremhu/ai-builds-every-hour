"""Depth themes: each band of depths has its own generator, colours, decorations and fauna.

=========  ======  ==========================================================
Theme      Depths  Character
=========  ======  ==========================================================
cellars    1–3     old storerooms: rooms & corridors or BSP halls, rubble
fungal     4–6     cellular-automata caves carpeted with glowing fungus
magma      7–9     BSP halls split by lava pools; fire creatures abound
heart      10+     a vast molten cavern around the Ember Heart
=========  ======  ==========================================================
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Theme:
    """A depth band's look and feel: generators, colours, decoration and spawn/loot biases."""
    key: str
    name: str
    min_depth: int
    generators: tuple[tuple[str, int], ...]   # (generator key, weight)
    wall_color: str
    floor_color: str
    intro: str
    decoration: str | None = None             # "rubble" | "fungus" | "lava"
    decoration_amount: float = 0.0
    monster_bias: dict[str, float] = field(default_factory=dict)
    loot_bias: dict[str, float] = field(default_factory=dict)

    def tile_colors(self, tile_name: str, default: tuple[str, str]) -> tuple[str, str]:
        """(lit, remembered) colour for a tile, with theme overrides for walls/floors."""
        if tile_name == "wall":
            return self.wall_color, "blue"
        if tile_name == "floor":
            return self.floor_color, "blue"
        return default


THEMES: tuple[Theme, ...] = (
    Theme("cellars", "the Old Cellars", 1, (("rooms", 2), ("bsp", 1)), "yellow", "white",
          "Dusty cellars stretch out before you.", decoration="rubble", decoration_amount=0.03,
          monster_bias={"rat": 1.5, "kobold": 1.3}, loot_bias={"ration": 1.5}),
    Theme("fungal", "the Fungal Caves", 4, (("caves", 3), ("rooms", 1)), "green", "white",
          "Pale fungus glows on the walls of a damp cave.", decoration="fungus",
          decoration_amount=0.12, monster_bias={"cave spider": 1.8, "myconid": 2.5, "rat": 0.5},
          loot_bias={"glowcap": 3.0}),
    Theme("magma", "the Magma Halls", 7, (("bsp", 3), ("caves", 1)), "red", "yellow",
          "Heat shimmers over rivers of molten rock.", decoration="lava", decoration_amount=0.05,
          monster_bias={"fire beetle": 2.0, "ember imp": 1.6, "magma hound": 2.0},
          loot_bias={"torch": 1.5}),
    Theme("heart", "the Ember Heart", 10, (("caves", 1),), "bright_red", "yellow",
          "You stand in the burning heart of the deep.", decoration="lava", decoration_amount=0.07,
          monster_bias={"magma hound": 2.0, "cave troll": 1.5}),
)


def theme_for_depth(depth: int) -> Theme:
    """The deepest theme whose ``min_depth`` is at most ``depth``."""
    chosen = THEMES[0]
    for theme in THEMES:
        if depth >= theme.min_depth:
            chosen = theme
    return chosen
