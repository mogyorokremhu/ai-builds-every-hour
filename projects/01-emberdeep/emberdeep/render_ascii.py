"""Plain-text renderer: turns a Game into a printable frame."""
from __future__ import annotations

from .game import Game


def render(game: Game, log_lines: int = 5) -> str:
    gmap = game.gmap
    grid = [[" "] * gmap.width for _ in range(gmap.height)]
    for y in range(gmap.height):
        for x in range(gmap.width):
            if gmap.visible[y][x]:
                grid[y][x] = gmap.tiles[y][x].glyph
            elif gmap.explored[y][x]:
                g = gmap.tiles[y][x].glyph
                grid[y][x] = ":" if g == "." else g  # dim remembered floor
    # corpses first so living things draw on top
    for e in sorted(game.entities, key=lambda e: e.blocks):
        if gmap.visible[e.y][e.x]:
            grid[e.y][e.x] = e.glyph
    f = game.player.fighter
    status = f"HP {f.hp}/{f.max_hp}  Depth {game.depth}  XP {game.xp}  Turn {game.turn}  Seed {game.seed}"
    lines = ["".join(r) for r in grid] + [status, "-" * gmap.width] + game.log.last(log_lines)
    return "\n".join(lines)
