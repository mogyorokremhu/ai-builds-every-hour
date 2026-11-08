"""Morgue files: a plain-text post-mortem of every finished run, plus run finishing.

:func:`finish_run` is what the front-ends call when a game ends: it writes the morgue
file, records the high score and deletes the save (permadeath), returning a short summary
for the death/victory screen.
"""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from . import daily, save, scores
from .progression import CHOICES

if TYPE_CHECKING:  # pragma: no cover
    from .game import Game

MORGUE_DIR = "morgue"


def map_dump(game: "Game") -> list[str]:
    """The explored map as text (unexplored = blank), with creatures you can see."""
    gmap = game.gmap
    grid = [[gmap.tiles[y][x].glyph if gmap.explored[y][x] else " " for x in range(gmap.width)]
            for y in range(gmap.height)]
    for (x, y), t in game.traps.items():
        if not t.hidden and gmap.explored[y][x]:
            grid[y][x] = "^"
    for e in sorted(game.entities, key=lambda e: (e.is_player, e.blocks)):
        if gmap.visible[e.y][e.x] or e.is_player:
            grid[e.y][e.x] = e.glyph
    rows = ["".join(r).rstrip() for r in grid]
    while rows and not rows[0]:
        rows.pop(0)
    while rows and not rows[-1]:
        rows.pop()
    return rows


def build_morgue(game: "Game", when: _dt.datetime | None = None) -> str:
    """The full morgue text for ``game``."""
    when = when or _dt.datetime.now(_dt.timezone.utc)
    f = game.player.fighter
    p = game.player
    lines = [
        "EMBERDEEP — morgue file",
        "=" * 40,
        f"Date:     {when.replace(microsecond=0).isoformat()}",
        f"Seed:     {game.seed}" + (f"  (daily run {daily.mode_date(game.mode)})" if daily.is_daily(game.mode) else ""),
        "",
        "VICTORY! You carried off the Ember Heart." if game.victory
        else f"You died on depth {game.depth}: {game.death_cause or 'unknown causes'}.",
        f"Score:    {scores.compute_score(game)}",
        f"Depth:    {game.depth} (deepest {game.max_depth}), {game.theme.name}",
        f"Turns:    {game.turn}",
        "",
        "Character",
        "-" * 40,
        f"Level {game.level} ({game.xp} XP)   HP {f.hp}/{f.max_hp}   Power {f.power}   Defense {f.defense}",
    ]
    hist = game.progression.history
    if hist:
        counts = {k: hist.count(k) for k in CHOICES}
        lines.append("Boons:    " + ", ".join(f"{CHOICES[k].label} x{n}" for k, n in counts.items() if n))
    effects = p.statuses.names()
    if effects:
        lines.append("Statuses: " + ", ".join(effects))
    lines += [f"Torch:    {game.resources.torch_label}   Food: {game.resources.hunger_label}", ""]
    lines += ["Equipment", "-" * 40]
    for slot, item in p.equipment.slots.items():
        lines.append(f"{slot.title():<7} {item.name if item else '-'}")
    lines += ["", "Pack", "-" * 40]
    if len(p.inventory):
        for letter, it in p.inventory.listing():
            desc = it.describe()
            lines.append(f"{letter}) {it.display_name}" + (f"  ({desc})" if desc else ""))
    else:
        lines.append("(empty)")
    found = game.ident.discoveries() if hasattr(game, "ident") else []
    if found:
        lines += ["", "Discoveries", "-" * 40]
        lines += [f"{look:<36} {name}" for look, name in found]
    lines += ["", f"Kills ({game.kills})", "-" * 40]
    for name, n in sorted(game.kill_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"{n:>4}  {name}")
    if not game.kill_counts:
        lines.append("(none — a pacifist run?)")
    lines += ["", "Last messages", "-" * 40]
    lines += [f"[{m.turn:>5}] {m.full_text}" for m in game.log.entries(15)]
    lines += ["", "Map", "-" * 40] + map_dump(game)
    return "\n".join(lines) + "\n"


def write_morgue(game: "Game", directory: Path, when: _dt.datetime | None = None) -> Path:
    when = when or _dt.datetime.now(_dt.timezone.utc)
    folder = directory / MORGUE_DIR
    folder.mkdir(parents=True, exist_ok=True)
    stamp = when.strftime("%Y%m%d-%H%M%S")
    path = folder / f"emberdeep-{stamp}-{game.seed}.txt"
    n = 2
    while path.exists():
        path = folder / f"emberdeep-{stamp}-{game.seed}-{n}.txt"
        n += 1
    path.write_text(build_morgue(game, when), encoding="utf-8")
    return path


@dataclass
class RunSummary:
    score: int
    rank: int
    ranked: bool
    morgue: Path

    def lines(self) -> list[str]:
        out = [f"Score:         {self.score}"]
        if self.rank:
            out.append(f"Hall of fame:  #{self.rank}" + ("" if self.ranked else " (practice run)"))
        out.append(f"Morgue file:   {self.morgue.name}")
        return out


def finish_run(game: "Game", directory: Path | None = None) -> RunSummary:
    """Record a finished run: morgue file + high score, and delete any save (permadeath)."""
    directory = directory or save.data_dir()
    when = _dt.datetime.now(_dt.timezone.utc)
    path = write_morgue(game, directory, when)
    entry = scores.entry_for(game, when)
    rank = scores.add_score(directory, entry)
    save.delete_save(save.save_path(directory))
    return RunSummary(entry.score, rank, entry.ranked, path)
