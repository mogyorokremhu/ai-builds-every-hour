"""Look mode: describe what is at a map cell (renderer-independent)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .ai import describe_ai
from .messages import a_an
from .status import STATUS_INFO

if TYPE_CHECKING:  # pragma: no cover
    from .entities import Entity
    from .game import Game


def health_word(e: "Entity") -> str:
    f = e.fighter
    ratio = f.hp / f.max_hp if f.max_hp else 0
    if ratio >= 1:
        return "unhurt"
    if ratio > 0.66:
        return "lightly wounded"
    if ratio > 0.33:
        return "wounded"
    return "badly wounded"


def speed_word(e: "Entity") -> str:
    s = e.effective_speed
    if s >= 180:
        return "very fast"
    if s > 110:
        return "fast"
    if s < 60:
        return "very slow"
    if s < 90:
        return "slow"
    return ""


def describe_creature(e: "Entity") -> str:
    bits = [f"{'You' if e.is_player else a_an(e.name).capitalize()} ({health_word(e)}"]
    sp = speed_word(e)
    if sp:
        bits.append(f", {sp}")
    adjs = [STATUS_INFO[n][2] for n in e.statuses.names()]
    if adjs:
        bits.append(", " + ", ".join(adjs))
    bits.append(")")
    text = "".join(bits)
    if not e.is_player:
        text += ". " + describe_ai(e)
    return text


def describe_cell(game: "Game", x: int, y: int) -> list[str]:
    """Lines describing the cell at (x, y), from the player's point of view."""
    gmap = game.gmap
    if not gmap.in_bounds(x, y) or not gmap.explored[y][x]:
        return ["You don't know what is there."]
    tile = gmap.tiles[y][x]
    if not gmap.visible[y][x]:
        return [f"You remember {_article(tile.name)} here."]
    lines: list[str] = []
    for e in game.entities:
        if e.pos != (x, y):
            continue
        if e.fighter is not None and e.fighter.alive and (e.ai or e.is_player):
            lines.append(describe_creature(e))
    for e in game.entities:
        if e.pos == (x, y) and e.item is not None:
            desc = e.item.describe()
            lines.append(f"{e.item.display_name}" + (f" ({desc})" if desc else ""))
    for e in game.entities:
        if e.pos == (x, y) and e.fighter is not None and not e.fighter.alive and not e.is_player:
            lines.append(a_an(e.name))
    lines.append(_article(tile.name).capitalize() + ".")
    return lines


def _article(name: str) -> str:
    if name.startswith("stairs"):
        return f"a flight of {name}"
    return a_an(name)
