"""The final level: the Ember Heart arena and its guardian.

Depth :data:`BOSS_DEPTH` replaces the normal generator with a hand-shaped arena: a wide
molten cavern, basalt pillars for cover, and the guardian's sanctum ringed by lava with
three narrow bridges. There are no stairs down — the only way out is through the
**Ember Guardian**. Killing it drops the Ember Heart (``*``); picking it up wins the game.

The guardian fights in three phases (by remaining HP):

1. **Awakened** — melee and *magma burst* (a ranged bolt that sets you alight).
2. **Kindled** (≤ 66 %) — also summons fire creatures and unleashes *fire novas*
   on anyone within two tiles.
3. **Enraged** (≤ 33 %) — faster and stronger; everything comes more often.
"""
from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING

from . import ai, fx
from .entities import make_monster
from .gamemap import GameMap
from .gen_caves import bfs_distances, sectors
from .geometry import chebyshev
from .levelgen import Layout
from .targeting import blast_area
from .tiles import FLOOR, LAVA, RUBBLE, WALL

if TYPE_CHECKING:  # pragma: no cover
    from .entities import Entity
    from .game import Game

Pos = tuple[int, int]

BOSS_DEPTH = 10
BOSS_KIND = "Ember Guardian"
MINION_KINDS = ("magma hound", "fire beetle", "ember imp")
MAX_MINIONS = 3

PHASES = {1: "awakened", 2: "kindled", 3: "enraged"}
PHASE_MESSAGES = {
    2: "The Ember Guardian's core flares white-hot! The cavern trembles.",
    3: "The Ember Guardian roars in fury and blazes brighter than ever!",
}
NOVA_RADIUS = 2
ENRAGE_SPEED = 140
ENRAGE_POWER = 2

#: cooldowns (in guardian actions) per phase: (spell, summon, nova)
COOLDOWNS = {1: (4, 99, 99), 2: (4, 14, 6), 3: (3, 10, 4)}


# ---- arena -------------------------------------------------------------------
def build_arena(width: int, height: int, rng: random.Random) -> tuple[Layout, Pos]:
    """Carve the boss arena. Returns the layout and the guardian's starting position."""
    gmap = GameMap(width, height)
    cx, cy = width / 2 - 0.5, height / 2 - 0.5
    rx, ry = width / 2 - 2.5, height / 2 - 1.5
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            wobble = 0.08 * math.sin(x * 0.7 + rng.random()) + 0.06 * math.cos(y * 1.3)
            if d < 1.0 + wobble:
                gmap.set(x, y, FLOOR)
    start = (4, height // 2)
    sanctum = (width - 14, height // 2)
    for p in (start, sanctum):
        gmap.set(*p, FLOOR)
    # lava ring around the sanctum with three bridges (west, north, south)
    sx, sy = sanctum
    for y in range(sy - 7, sy + 8):
        for x in range(sx - 9, sx + 10):
            r = math.hypot((x - sx) / 1.6, y - sy)
            if 3.6 <= r <= 4.9 and gmap.get(x, y).name == "floor":
                bridge = (abs(y - sy) <= 0 and x < sx) or (abs(x - sx) <= 0)
                if not bridge:
                    gmap.set(x, y, LAVA)
    # basalt pillars and rubble in the outer cavern, never cutting it apart
    target = len(bfs_distances(gmap, start))
    for _ in range(26):
        px, py = rng.randrange(8, sx - 9), rng.randrange(2, height - 2)
        if gmap.get(px, py).name != "floor" or chebyshev((px, py), start) < 3:
            continue
        gmap.set(px, py, WALL)
        reach = bfs_distances(gmap, start)
        if sanctum not in reach or len(reach) < target - 1:
            gmap.set(px, py, FLOOR)
        else:
            target = len(reach)
    for _ in range(30):
        px, py = rng.randrange(1, width - 1), rng.randrange(1, height - 1)
        if gmap.get(px, py).name == "floor" and (px, py) not in (start, sanctum):
            gmap.set(px, py, RUBBLE)
    gmap.stairs = None
    cells = sorted(bfs_distances(gmap, start), key=lambda p: (p[1], p[0]))
    cells = [c for c in cells if gmap.walkable(*c)]
    near_start = [c for c in cells if chebyshev(c, start) <= 4]
    outer = [c for c in cells if chebyshev(c, start) > 8 and chebyshev(c, sanctum) > 6]
    areas = [near_start] + sectors(outer)
    return Layout(gmap, start, areas, [], "arena"), sanctum


def populate(game: "Game", sanctum: Pos) -> "Entity":
    """Place the guardian (awake but dormant until it sees you) and two sleeping hounds."""
    boss = make_monster(BOSS_KIND, *sanctum)
    boss.ai_state.update(phase=1, cooldown=0, summon=0, nova=0, awake=False)
    game.entities.append(boss)
    for dx, dy in ((-2, -1), (-2, 1)):
        x, y = sanctum[0] + dx, sanctum[1] + dy
        if game.gmap.walkable(x, y) and not game.blocking_at(x, y):
            hound = make_monster("magma hound", x, y)
            hound.asleep = True
            game.entities.append(hound)
    return boss


# ---- behaviour ------------------------------------------------------------
def phase_for(m: "Entity") -> int:
    """The boss's fight phase (1-3) from its remaining HP fraction."""
    ratio = m.fight.hp / m.fight.max_hp
    return 3 if ratio <= 1 / 3 else 2 if ratio <= 2 / 3 else 1


def minions(game: "Game") -> list["Entity"]:
    """All living monsters tagged as boss minions."""
    return [e for e in game.monsters if "minion" in e.tags]


def summon(game: "Game", m: "Entity", count: int = 2) -> list["Entity"]:
    """Call fire creatures out of the lava next to the guardian."""
    free = [(m.x + dx, m.y + dy) for dx, dy in ai.DIRS8]
    free += [(m.x + dx, m.y + dy) for dx in range(-2, 3) for dy in range(-2, 3) if max(abs(dx), abs(dy)) == 2]
    free = [p for p in free if game.gmap.walkable(*p) and not game.blocking_at(*p)]
    made = []
    for p in free[:count]:
        kind = game.rng.choice(MINION_KINDS)
        e = make_monster(kind, *p)
        e.tags.add("minion")
        e.memory = game.player.pos
        game.entities.append(e)
        made.append(e)
    if made:
        names = ", ".join(sorted({e.name for e in made}))
        game.say(f"The {m.name} calls forth fire from the deep: {names}!", "bright_red")
    return made


def fire_nova(game: "Game", m: "Entity") -> None:
    """Burst of flame around the guardian. Hurts everything nearby that isn't fireproof."""
    phase = m.ai_state.get("phase", 1)
    game.say(f"The {m.name} erupts in a nova of flame!", "bright_red")
    area = blast_area(game.gmap, m.pos, NOVA_RADIUS)
    fx.emit(game, "blast", [m.pos] + [c for c in area if c != m.pos], "*", "bright_red")
    for cell in area:
        if cell == m.pos:
            continue
        target = game.blocking_at(*cell)
        if target is None or target.fighter is None:
            continue
        if target.is_player:
            dmg = max(1, 4 + phase - target.fight.defense // 2)
            dealt = target.fight.take_damage(dmg)
            game.say(f"The flames sear you for {dealt}!", "bright_red")
            if not target.fight.alive:
                game.death_cause = f"incinerated by the {m.name}"
                game.say("You die...", "bright_red")
                return
            game.apply_status(target, "burning", 3, 1)
        elif "immune:burning" not in target.tags:
            game.damage_monster(target, 5, "scorched")


def act_boss(game: "Game", m: "Entity", sees: bool) -> None:
    """Boss AI: wake on sight, escalate phases, then summon, nova, cast or melee by cooldown."""
    st = m.ai_state
    for key, default in (("phase", 1), ("cooldown", 0), ("summon", 0), ("nova", 0)):
        st.setdefault(key, default)
    if not st.get("awake"):
        if not sees:
            return
        st["awake"] = True
        game.say(f"The {m.name} rises from the magma, eyes blazing!", "bright_red")
        return
    phase = phase_for(m)
    if phase > st.get("phase", 1):
        st["phase"] = phase
        game.say(PHASE_MESSAGES[phase], "bright_red")
        if phase == 3:
            m.speed = ENRAGE_SPEED
            m.fight.base_power += ENRAGE_POWER
        st["summon"] = 0  # summon right away on a phase change
    for key in ("cooldown", "summon", "nova"):
        st[key] = max(0, st.get(key, 0) - 1)
    spell_cd, summon_cd, nova_cd = COOLDOWNS[st["phase"]]
    player = game.player
    dist = chebyshev(m.pos, player.pos)
    if st["phase"] >= 2 and st["summon"] == 0 and len(minions(game)) < MAX_MINIONS:
        summon(game, m, 2 if st["phase"] == 2 else 3)
        st["summon"] = summon_cd
        return
    if not sees:
        ai.hunt(game, m, sees)
        return
    if st["phase"] >= 2 and st["nova"] == 0 and dist <= NOVA_RADIUS:
        fire_nova(game, m)
        st["nova"] = nova_cd
        return
    spell = ai.SPELLS[m.spell or "magma burst"]
    if st["cooldown"] == 0 and 2 <= dist <= spell["range"] and ai.clear_shot(game, m, player.pos):
        game.cast_spell(m, m.spell or "magma burst")
        st["cooldown"] = spell_cd
        return
    ai.hunt(game, m, sees)


ai.BEHAVIOURS["boss"] = act_boss
ai.SPELLS["magma burst"] = dict(range=7, cooldown=4, damage=6, status=("burning", 3, 2, 0.6),
                                verb="hurls a gout of magma at", color="bright_red")


def describe(m: "Entity") -> str:
    """Look-mode hint for the guardian."""
    st = m.ai_state
    if not st.get("awake"):
        return "It slumbers in the magma, waiting."
    return f"It is {PHASES[st.get('phase', 1)]}."
