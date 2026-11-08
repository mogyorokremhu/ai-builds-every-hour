"""Plain-text renderer: turns a Game into a printable frame (used by text mode and tests)."""
from __future__ import annotations

from . import encumbrance
from .game import Game
from .hud import bar


def render(game: Game, log_lines: int = 5) -> str:
    """Render the map, status lines and recent log as plain text."""
    gmap = game.gmap
    grid = [[" "] * gmap.width for _ in range(gmap.height)]
    for y in range(gmap.height):
        for x in range(gmap.width):
            if gmap.visible[y][x]:
                grid[y][x] = gmap.tiles[y][x].glyph
            elif gmap.explored[y][x]:
                g = gmap.tiles[y][x].glyph
                grid[y][x] = ":" if g == "." else g  # dim remembered floor
            if grid[y][x] != " " and game.known_trap_at(x, y):
                grid[y][x] = "^"
    # items, then corpses, then the living
    def order(e) -> int:
        """Draw order: items first, then corpses, then living creatures and the player."""
        return 2 if e.is_player else 1 if e.blocks else 0

    for e in sorted(game.entities, key=order):
        if gmap.visible[e.y][e.x]:
            grid[e.y][e.x] = e.glyph
    f = game.player.fight
    status = (f"HP {f.hp}/{f.max_hp} [{bar(f.hp, f.max_hp, 10, '#', '-')}]  Pow {f.power} Def {f.defense}  "
              f"Depth {game.depth}  Lv {game.level} XP {game.xp}  Turn {game.turn}\n"
              f"Torch {game.resources.torch_label}  Food {game.resources.hunger_label}  "
              f"Load {encumbrance.load_label(game.player)}  [{game.theme.name}]")
    if game.pending_levels:
        status += "  ** LEVEL UP: +v vitality, +m might, +g guard **"
    effects = game.player.statuses.labels()
    if effects:
        status += "  [" + " ".join(label for label, _ in effects) + "]"
    lines = ["".join(r) for r in grid] + [status, "-" * gmap.width] + game.log.last(log_lines)
    return "\n".join(lines)


def render_inventory(game: Game) -> str:
    """Plain-text listing of the pack with equipped marks, weights, slots and load."""
    inv, eq = game.player.pack, game.player.gear
    if not len(inv):
        return "Your pack is empty."
    out = ["Inventory:"]
    for letter, it in inv.listing():
        worn = " (equipped)" if eq.is_equipped(it) else ""
        out.append(f"  {letter}) {it.display_name}{worn}  {it.describe()}  [wt {encumbrance.item_weight(it)}]")
    p = game.player
    out.append(f"Slots {len(inv)}/{inv.capacity}  Load {encumbrance.load_label(p)}")
    return "\n".join(out)
