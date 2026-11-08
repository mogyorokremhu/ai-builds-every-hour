"""Monster behaviour.

Every monster has an ``ai`` kind:

* ``chase``  — hunts the player with A*, remembers where it last saw them.
* ``coward`` — like chase, but flees along a safety map when badly hurt and slowly
  recovers its nerve (and HP) when out of sight.
* ``caster`` — keeps its distance and casts a spell with a cooldown when it has a clear
  line of fire (see :data:`SPELLS`).
* ``pack``   — howls to alert pack-mates, lurks at a distance until enough of the pack
  has gathered, then rushes in together.
* ``boss``   — the Ember Guardian (registered by :mod:`emberdeep.boss`).

All behaviours share: confusion (random stumbling), memory of the player's last seen
position, and A* movement that routes around other monsters and opens closed doors.
Sleeping monsters do nothing until noise or proximity wakes them (see :func:`wake_chance`).
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from .geometry import chebyshev
from .pathfinding import astar, downhill_step, flee_map
from .targeting import projectile_path

if TYPE_CHECKING:  # pragma: no cover
    from .entities import Entity
    from .game import Game

#: Spells used by casters. ``status`` is (name, turns, power, chance) or None.
SPELLS: dict[str, dict] = {
    "ember bolt": dict(range=6, cooldown=4, damage=4, status=("burning", 3, 1, 0.35),
                       verb="hurls an ember bolt at", color="bright_red"),
    "hex of slowness": dict(range=7, cooldown=6, damage=0, status=("slowed", 6, 0, 1.0),
                            verb="chants a hex of slowness at", color="cyan"),
}

CASTER_KITE_CHANCE = 0.6  # chance a caster backs away when you get close (balance-tuned)
COWARD_THRESHOLD = 0.35   # flee below this fraction of max HP
PACK_ALERT_RADIUS = 8
PACK_GATHER = 2           # pack members (incl. self) near the player before rushing in
PACK_LURK_DIST = 4
CROWD_PENALTY = 40        # extra A* cost for walking through another monster

DIRS8 = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


# ---- shared helpers ------------------------------------------------------
def move_towards(game: "Game", m: "Entity", goal: tuple[int, int]) -> bool:
    """Take one A* step toward ``goal``. Returns True if the monster moved."""
    def crowd(x: int, y: int) -> int:
        return CROWD_PENALTY if game.blocking_at(x, y) is not None else 0

    path = astar(game.gmap, m.pos, goal, extra_cost=crowd, max_nodes=1500)
    if not path:
        return False
    nx, ny = path[0]
    if game.blocking_at(nx, ny) is not None:
        return False
    return step_into(game, m, nx, ny)


def step_into(game: "Game", m: "Entity", nx: int, ny: int) -> bool:
    """Move ``m`` onto (nx, ny), or open the closed door there (which takes the action)."""
    if game.gmap.is_closed_door(nx, ny):
        game.open_door(nx, ny, m)
        return True
    if not game.gmap.walkable(nx, ny):
        return False
    m.move(nx - m.x, ny - m.y)
    return True


def step_away(game: "Game", m: "Entity", threat: tuple[int, int]) -> bool:
    """Walk downhill on a safety map away from ``threat``."""
    field = flee_map(game.gmap, threat, radius=12)
    step = downhill_step(game.gmap, m.pos, field, blocked=lambda x, y: game.blocking_at(x, y) is not None)
    if step is None:
        return False
    return step_into(game, m, m.x + step[0], m.y + step[1])


def wander(game: "Game", m: "Entity") -> None:
    """Stumble in a random direction, attacking whatever is there (confusion)."""
    dx, dy = game.rng.choice(DIRS8)
    nx, ny = m.x + dx, m.y + dy
    other = game.blocking_at(nx, ny)
    if other is not None and other is not m and other.fighter:
        game.monster_attack(m, other, prefix="(confused) ")
    elif game.gmap.walkable(nx, ny):
        m.move(dx, dy)


def clear_shot(game: "Game", m: "Entity", target: tuple[int, int]) -> bool:
    """True if a projectile from ``m`` reaches ``target`` without hitting walls or creatures."""
    path = projectile_path(game.gmap, m.pos, target)
    if not path or path[-1] != target:
        return False
    return all(game.blocking_at(*p) is None for p in path[:-1])


def hunt(game: "Game", m: "Entity", sees: bool) -> None:
    """Basic chase: attack if adjacent, otherwise path to the player or their memory."""
    player = game.player
    if sees and chebyshev(m.pos, player.pos) <= 1:
        game.monster_attack(m, player)
        return
    goal = player.pos if sees else m.memory
    if goal is None:
        return
    moved = move_towards(game, m, goal)
    if not sees and (m.pos == goal or not moved):
        m.memory = None  # reached the spot (or can't get there) and found nothing


# ---- behaviours ------------------------------------------------------------
def act_chase(game: "Game", m: "Entity", sees: bool) -> None:
    hunt(game, m, sees)


def act_coward(game: "Game", m: "Entity", sees: bool) -> None:
    f = m.fighter
    hurt = f.hp <= f.max_hp * COWARD_THRESHOLD
    if not sees:
        if hurt and m.ai_state.get("fleeing"):
            # catch its breath out of sight
            m.ai_state["rest"] = m.ai_state.get("rest", 0) + 1
            if m.ai_state["rest"] % 3 == 0:
                f.heal(1)
            if f.hp > f.max_hp * 0.6:
                m.ai_state["fleeing"] = False
            return
        hunt(game, m, sees)
        return
    if hurt and m.ai_state.get("potion") and game.rng.random() < 0.6:
        drink_potion(game, m)
        return
    if hurt:
        if not m.ai_state.get("fleeing"):
            m.ai_state["fleeing"] = True
            game.say(f"The {m.name} turns to flee!")
        if step_away(game, m, game.player.pos):
            return
        # cornered: fight back
    hunt(game, m, sees)


def drink_potion(game: "Game", m: "Entity") -> None:
    """A monster quaffs the healing potion it carries (kobolds)."""
    m.ai_state.pop("potion", None)
    healed = m.fighter.heal(12)
    if game.gmap.visible[m.y][m.x]:
        game.say(f"The {m.name} drinks a potion of healing! (+{healed})", "bright_yellow")
        game.identify_kind("healing potion")


def act_caster(game: "Game", m: "Entity", sees: bool) -> None:
    spell = SPELLS[m.spell or "ember bolt"]
    cd = m.ai_state.get("cooldown", 0)
    if cd > 0:
        m.ai_state["cooldown"] = cd - 1
    if not sees:
        hunt(game, m, sees)
        return
    player = game.player
    dist = chebyshev(m.pos, player.pos)
    if cd == 0 and dist <= spell["range"] and clear_shot(game, m, player.pos):
        game.cast_spell(m, m.spell or "ember bolt")
        m.ai_state["cooldown"] = spell["cooldown"]
        return
    if dist <= 2 and game.rng.random() < CASTER_KITE_CHANCE and step_away(game, m, player.pos):
        return  # keep casting distance (casters aren't perfect at it)
    if dist <= 1:
        game.monster_attack(m, player)
        return
    if dist > spell["range"] or not clear_shot(game, m, player.pos):
        move_towards(game, m, player.pos)
    # otherwise: in range, waiting for the cooldown — hold position


def pack_mates(game: "Game", m: "Entity", radius: int) -> list["Entity"]:
    return [o for o in game.monsters
            if o is not m and o.ai == "pack" and o.name == m.name and chebyshev(o.pos, m.pos) <= radius]


def act_pack(game: "Game", m: "Entity", sees: bool) -> None:
    player = game.player
    if sees:
        # howl: share the player's position with the pack
        for o in pack_mates(game, m, PACK_ALERT_RADIUS):
            o.memory = player.pos
    if not sees:
        hunt(game, m, sees)
        return
    dist = chebyshev(m.pos, player.pos)
    if dist <= 1:
        game.monster_attack(m, player)
        return
    mates = pack_mates(game, m, 12)
    if not mates:
        hunt(game, m, sees)  # a lone pack animal just attacks
        return
    near = 1 + sum(1 for o in mates if chebyshev(o.pos, player.pos) <= PACK_LURK_DIST + 1)
    hurt_player = player.fighter.hp <= player.fighter.max_hp // 2
    if near >= min(PACK_GATHER, 1 + len(mates)) or hurt_player or m.ai_state.get("rushing"):
        m.ai_state["rushing"] = True
        hunt(game, m, sees)
        return
    # lurk at the edge of the player's reach until the pack gathers
    if dist < PACK_LURK_DIST:
        step_away(game, m, player.pos)
    elif dist > PACK_LURK_DIST + 1:
        move_towards(game, m, player.pos)


BEHAVIOURS: dict[str, Callable[["Game", "Entity", bool], None]] = {
    "chase": act_chase,
    "coward": act_coward,
    "caster": act_caster,
    "pack": act_pack,
}


def wake_chance(game: "Game", m: "Entity") -> float:
    """Chance a sleeping monster wakes this action, from player noise and proximity."""
    from .game import NOISE_RANGE

    d = chebyshev(m.pos, game.player.pos)
    chance = 0.0
    if game.noise and d <= game.noise * NOISE_RANGE:
        chance += min(0.9, 0.12 * game.noise)
    if game.gmap.visible[m.y][m.x]:
        chance += 0.2 if d <= 2 else 0.06 if d <= 5 else 0.015
    return min(1.0, chance)


def take_turn(game: "Game", m: "Entity") -> None:
    """Run one action for monster ``m``."""
    if m.asleep:
        if game.rng.random() < wake_chance(game, m):
            m.asleep = False
            m.memory = game.player.pos
            if game.gmap.visible[m.y][m.x]:
                game.say(f"The {m.name} wakes up!", "bright_yellow")
        return
    if m.confused > 0:
        wander(game, m)
        return
    # FOV is symmetric for our purposes (if you see it, it sees you) unless you lurk in the dark
    sees = game.monster_sees_player(m)
    if sees:
        m.memory = game.player.pos
    elif m.memory is None:
        return  # dormant: nothing to hunt
    BEHAVIOURS.get(m.ai or "chase", act_chase)(game, m, sees)


def describe_ai(m: "Entity") -> str:
    """Short behaviour hint for look mode."""
    if m.asleep:
        return "It is asleep."
    if m.ai == "boss":
        from .boss import describe

        return describe(m)
    if m.ai == "coward":
        return "It looks skittish." if not m.ai_state.get("fleeing") else "It is fleeing!"
    if m.ai == "caster":
        return f"It knows {m.spell}."
    if m.ai == "pack":
        return "It hunts in packs."
    return "It looks hungry."
