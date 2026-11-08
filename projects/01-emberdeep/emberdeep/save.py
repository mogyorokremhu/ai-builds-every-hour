"""Save files: the whole run as one JSON document, plus permadeath handling.

Emberdeep is a roguelike, so saves are *suspend points*, not checkpoints:

* quitting a live game writes ``save.json``;
* loading a save deletes it straight away (you can't reload after a bad fight);
* dying (or winning) deletes it for good.

The file stores everything needed to continue *exactly* where you left off — including
the random generator's state, so a loaded game plays out identically to the original.
Files live in :func:`data_dir` (``$EMBERDEEP_HOME`` or ``~/.emberdeep``).
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, fields
from pathlib import Path
from typing import Any

from . import explore
from .entities import Entity, Fighter
from .equipment import SLOTS, Equipment
from .gamemap import GameMap
from .geometry import Rect
from .identify import Identification
from .inventory import Inventory
from .items import Item
from .messages import Message, MessageLog
from .progression import Progression
from .resources import Resources
from .status import StatusSet
from .themes import theme_for_depth
from .timeline import Timeline
from .tiles import TILES_BY_CODE
from .traps import Trap
from .vaults import SpecialRoom

SAVE_VERSION = 1
SAVE_NAME = "save.json"


class SaveError(Exception):
    """The save file is missing, corrupt or from an incompatible version."""


def data_dir() -> Path:
    """Where saves, scores and morgue files go (created on demand)."""
    home = os.environ.get("EMBERDEEP_HOME")
    path = Path(home) if home else Path.home() / ".emberdeep"
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_path(directory: Path | None = None) -> Path:
    return (directory or data_dir()) / SAVE_NAME


# ---- encoding ---------------------------------------------------------------
def _item(it: Item) -> dict[str, Any]:
    return asdict(it)


def _decode_item(d: dict[str, Any]) -> Item:
    known = {f.name for f in fields(Item)}
    return Item(**{k: v for k, v in d.items() if k in known})


def _entity(e: Entity) -> dict[str, Any]:
    d: dict[str, Any] = {
        "name": e.name, "glyph": e.glyph, "x": e.x, "y": e.y, "blocks": e.blocks, "ai": e.ai,
        "xp_value": e.xp_value, "tags": sorted(e.tags), "color": e.color, "speed": e.speed,
        "energy": e.energy, "memory": list(e.memory) if e.memory else None,
        "on_hit": list(e.on_hit) if e.on_hit else None, "spell": e.spell,
        "ai_state": e.ai_state, "asleep": e.asleep,
        "statuses": [[s.name, s.turns, s.power] for s in e.statuses._s.values()],
        "fighter": asdict(e.fighter) if e.fighter else None,
        "item": _item(e.item) if e.item else None,
    }
    if e.inventory is not None:
        d["inventory"] = {"capacity": e.inventory.capacity, "items": [_item(i) for i in e.inventory.items]}
    if e.equipment is not None and e.inventory is not None:
        d["equipment"] = {slot: (e.inventory._index(it) if it is not None else None)
                          for slot, it in e.equipment.slots.items()}
    return d


def _decode_entity(d: dict[str, Any]) -> Entity:
    e = Entity(
        name=d["name"], glyph=d["glyph"], x=d["x"], y=d["y"], blocks=d["blocks"], ai=d["ai"],
        xp_value=d["xp_value"], tags=set(d["tags"]), color=d["color"], speed=d["speed"],
        energy=d["energy"], memory=tuple(d["memory"]) if d["memory"] else None,
        on_hit=tuple(d["on_hit"]) if d["on_hit"] else None, spell=d["spell"],
        ai_state=dict(d["ai_state"]), asleep=d["asleep"],
        fighter=Fighter(**d["fighter"]) if d["fighter"] else None,
        item=_decode_item(d["item"]) if d["item"] else None,
    )
    st = StatusSet()
    for name, turns, power in d["statuses"]:
        st.add(name, turns, power)
    e.statuses = st
    if "inventory" in d:
        inv = Inventory(d["inventory"]["capacity"])
        inv.items = [_decode_item(i) for i in d["inventory"]["items"]]
        e.inventory = inv
        if "equipment" in d:  # monsters (scavengers) carry a pack but wear nothing
            eq = Equipment()
            for slot, idx in d["equipment"].items():
                if slot in SLOTS and idx is not None:
                    eq.slots[slot] = inv.items[idx]
            e.equipment = eq
    return e


def _gmap(g: GameMap) -> dict[str, Any]:
    return {
        "width": g.width, "height": g.height,
        "tiles": ["".join(t.save_code for t in row) for row in g.tiles],
        "explored": ["".join("1" if v else "0" for v in row) for row in g.explored],
        "stairs": list(g.stairs) if g.stairs else None,
    }


def _decode_gmap(d: dict[str, Any]) -> GameMap:
    g = GameMap(d["width"], d["height"])
    try:
        g.tiles = [[TILES_BY_CODE[ch] for ch in row] for row in d["tiles"]]
    except KeyError as exc:
        raise SaveError(f"unknown tile glyph {exc}") from None
    g.explored = [[ch == "1" for ch in row] for row in d["explored"]]
    g.stairs = tuple(d["stairs"]) if d["stairs"] else None
    return g


def _rng_state(state: tuple) -> list:
    version, internal, gauss = state
    return [version, list(internal), gauss]


def to_dict(game) -> dict[str, Any]:
    """Serialise a :class:`~emberdeep.game.Game` into plain JSON-able data."""
    if game.player is not game.entities[0]:
        raise SaveError("the player must be the first entity")
    prog, res = game.progression, game.resources
    return {
        "version": SAVE_VERSION,
        "seed": game.seed, "mode": game.mode, "rng": _rng_state(game.rng.getstate()),
        "depth": game.depth, "max_depth": game.max_depth, "turn": game.turn, "kills": game.kills,
        "kill_counts": game.kill_counts, "death_cause": game.death_cause, "victory": game.victory,
        "generator": game.generator,
        "progression": {"xp": prog.xp, "level": prog.level, "pending": prog.pending, "history": prog.history},
        "resources": {"torch": res.torch, "food": res.food, "starving": res._turns_starving},
        "log": [[m.text, m.color, m.count, m.turn] for m in game.log.entries()],
        "map": _gmap(game.gmap),
        "entities": [_entity(e) for e in game.entities],
        "traps": [[t.kind, t.x, t.y, t.hidden, t.triggered] for t in game.traps.values()],
        "special_rooms": [[s.kind, s.rect.x, s.rect.y, s.rect.w, s.rect.h, s.visited]
                          for s in game.special_rooms],
        "altars": [[x, y, used] for (x, y), used in game.altars.items()],
        "ident": game.ident.to_dict(),
        "timeline": game.timeline.to_dict(),
        "explore_deaths": list(game.explore_deaths),
    }


def from_dict(data: dict[str, Any]):
    """Rebuild a Game from :func:`to_dict` output (without generating a level)."""
    from .game import Game

    if not isinstance(data, dict) or data.get("version") != SAVE_VERSION:
        raise SaveError("incompatible save version")
    try:
        g = Game.__new__(Game)
        g.seed, g.mode = data["seed"], data["mode"]
        import random

        g.rng = random.Random()
        v, internal, gauss = data["rng"]
        g.rng.setstate((v, tuple(internal), gauss))
        g.depth, g.max_depth, g.turn, g.kills = data["depth"], data["max_depth"], data["turn"], data["kills"]
        g.kill_counts = dict(data["kill_counts"])
        g.death_cause, g.victory, g.generator = data["death_cause"], data["victory"], data["generator"]
        p = data["progression"]
        g.progression = Progression()
        g.progression.xp, g.progression.level = p["xp"], p["level"]
        g.progression.pending, g.progression.history = p["pending"], list(p["history"])
        r = data["resources"]
        g.resources = Resources(r["torch"], r["food"])
        g.resources._turns_starving = r["starving"]
        g.log = MessageLog()
        for text, color, count, turn in data["log"]:
            g.log._msgs.append(Message(text, color, count, turn))
        g.gmap = _decode_gmap(data["map"])
        g.entities = [_decode_entity(e) for e in data["entities"]]
        g.player = g.entities[0]
        g.traps = {}
        for kind, x, y, hidden, triggered in data["traps"]:
            g.traps[(x, y)] = Trap(kind, x, y, hidden, triggered)
        g.special_rooms = [SpecialRoom(kind, Rect(x, y, w, h), visited)
                           for kind, x, y, w, h, visited in data["special_rooms"]]
        g.altars = {(x, y): used for x, y, used in data["altars"]}
        g.ident = Identification.from_dict(data.get("ident"))
        g.timeline = Timeline.from_dict(data.get("timeline"))
        g.explore_deaths = list(data.get("explore_deaths", []))
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        raise SaveError(f"corrupt save: {exc!r}") from None
    if "player" not in g.player.tags:
        raise SaveError("corrupt save: first entity is not the player")
    g.theme = theme_for_depth(g.depth)
    g.noise = 0
    g.effects = []
    g._trap_confirm = None
    g._force_confirm = None
    from .lighting import compute_lit

    g.lit = compute_lit(g.gmap)
    g.update_fov()
    return g


# ---- files --------------------------------------------------------------------
def save_game(game, path: Path | None = None) -> Path:
    """Write ``game`` to disk atomically. Refuses to save a finished run."""
    if game.game_over:
        raise SaveError("finished runs can't be saved")
    path = path or save_path()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(to_dict(game), separators=(",", ":")), encoding="utf-8")
    tmp.replace(path)
    return path


def has_save(path: Path | None = None) -> bool:
    return (path or save_path()).is_file()


def load_game(path: Path | None = None, consume: bool = True):
    """Load a saved run. With ``consume`` (the default) the file is deleted after reading —
    except for explore-mode runs, whose saves are kept (no permadeath)."""
    path = path or save_path()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SaveError("no saved game") from None
    except (OSError, json.JSONDecodeError) as exc:
        raise SaveError(f"unreadable save: {exc}") from None
    game = from_dict(data)
    if consume and not explore.is_explore(game.mode):
        delete_save(path)
    game.say("Welcome back to Emberdeep.", "bright_cyan")
    return game


def delete_save(path: Path | None = None) -> bool:
    """Remove the save file (permadeath). Returns True if one was deleted."""
    path = path or save_path()
    try:
        path.unlink()
        return True
    except FileNotFoundError:
        return False
