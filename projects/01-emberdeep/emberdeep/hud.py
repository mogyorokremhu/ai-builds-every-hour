"""Renderer-independent HUD content: HP bar, stats sidebar, monster list."""
from __future__ import annotations

from typing import TYPE_CHECKING

from . import encumbrance
from .resources import TORCH_MAX
from .status import STATUS_INFO

if TYPE_CHECKING:  # pragma: no cover
    from .game import Game

Line = tuple[str, str]  # (text, colour name)


def bar(current: int, maximum: int, width: int, fill: str = "█", empty: str = "░") -> str:
    """Return a text progress bar like '██████░░░░'."""
    if maximum <= 0 or width <= 0:
        return ""
    filled = round(width * max(0, min(current, maximum)) / maximum)
    return fill * filled + empty * (width - filled)


def hp_color(current: int, maximum: int) -> str:
    """HUD colour for an HP value: green above 60%, yellow above 30%, else red."""
    ratio = current / maximum if maximum else 0
    if ratio > 0.6:
        return "bright_green"
    if ratio > 0.3:
        return "bright_yellow"
    return "bright_red"


def torch_color(fuel: int) -> str:
    """HUD colour for torch fuel: bright yellow above 50%, yellow above 20%, else red."""
    ratio = fuel / TORCH_MAX
    if ratio > 0.5:
        return "bright_yellow"
    if ratio > 0.2:
        return "yellow"
    return "bright_red"


def sidebar(game: "Game", width: int = 22, max_monsters: int = 8) -> list[Line]:
    """Build the sidebar as a list of (text, colour) lines."""
    p = game.player
    f = p.fight
    res = game.resources
    into, span = game.progression.progress
    lines: list[Line] = [
        ("EMBERDEEP", "bright_red"),
        (f"Depth {game.depth}: {game.theme.name.replace('the ', '')}", "bright_yellow"),
        ("", "white"),
        (f"HP {f.hp}/{f.max_hp}", hp_color(f.hp, f.max_hp)),
        (bar(f.hp, f.max_hp, width - 2), hp_color(f.hp, f.max_hp)),
        (f"Level {game.level}  XP {game.xp}", "bright_white"),
        (bar(into, span, width - 2, "▰", "▱"), "bright_cyan"),
        (f"Power   {f.power}", "white"),
        (f"Defense {f.defense}", "white"),
        (f"Torch   {res.torch_label}", torch_color(res.torch)),
        (bar(res.torch, TORCH_MAX, width - 2, "▮", "▯"), torch_color(res.torch)),
        (f"Food    {res.hunger_label}", res.hunger_color),
        (f"Load    {encumbrance.load_label(p)}", encumbrance.load_color(p)),
        (f"Pack    {len(p.pack)}/{p.pack.capacity}",
         "bright_red" if p.pack.full else
         "bright_yellow" if p.pack.capacity - len(p.pack) <= encumbrance.SLOT_WARNING else "white"),
        (f"Turn    {game.turn}", "white"),
    ]
    if game.mode == "explore":
        lines.insert(2, ("[explore mode]", "bright_magenta"))
    if game.pending_levels:
        lines.insert(7, (f"** {game.pending_levels} level-up(s)! **", "bright_green"))
    for name in p.statuses.names():
        label, color = STATUS_INFO[name][0], STATUS_INFO[name][1]
        lines.append((f"* {label} ({p.statuses.turns(name)})", color))
    lines.append(("", "white"))
    eq = p.gear
    if eq is not None:
        for slot, item in eq.slots.items():
            name = item.name if item else "-"
            lines.append((f"{slot[:3].title()}: {name}"[:width], "cyan" if item else "blue"))
        lines.append(("", "white"))
    mons = game.visible_monsters()
    lines.append(("In view:" if mons else "Nothing in view", "bright_white"))
    for m in mons[:max_monsters]:
        mf = m.fight
        label = f"{m.glyph} {m.name}"
        tags = ("z" if m.asleep else "") + "".join(STATUS_INFO[n][0][0] for n in m.statuses.names())
        if tags:
            label += f" [{tags}]"
        lines.append((label[:width], m.color))
        lines.append(("  " + bar(mf.hp, mf.max_hp, min(10, width - 4)), hp_color(mf.hp, mf.max_hp)))
    if len(mons) > max_monsters:
        lines.append((f"  ...and {len(mons) - max_monsters} more", "white"))
    items = game.visible_items()
    if items:
        lines.append(("", "white"))
        lines.append((f"Items in view: {len(items)}", "bright_yellow"))
    return [(t[:width], c) for t, c in lines]
