"""Game state and turn logic, independent of any renderer."""
from __future__ import annotations

import random

from . import dungeon
from .combat import attack
from .entities import MONSTER_TEMPLATES, Entity, make_monster, make_player
from .fov import compute_fov
from .geometry import chebyshev
from .messages import MessageLog

MAP_W, MAP_H = 70, 24
FOV_RADIUS = 8


class Game:
    def __init__(self, seed: int | None = None) -> None:
        self.seed = seed if seed is not None else random.randrange(1 << 30)
        self.rng = random.Random(self.seed)
        self.log = MessageLog()
        self.depth = 0
        self.turn = 0
        self.xp = 0
        self.player = make_player(0, 0)
        self.entities: list[Entity] = []
        self.new_level()
        self.log.add("You descend into Emberdeep. Find the stairs (>).")

    # ---- level setup -------------------------------------------------
    def new_level(self) -> None:
        self.depth += 1
        self.gmap, rooms = dungeon.generate(MAP_W, MAP_H, self.rng)
        self.player.x, self.player.y = rooms[0].center
        self.entities = [self.player]
        for room in rooms[1:]:
            for _ in range(self.rng.randint(0, 2 + self.depth // 2)):
                spots = [p for p in room.inner() if not self.blocking_at(*p)]
                if spots:
                    x, y = self.rng.choice(spots)
                    self.entities.append(make_monster(self.pick_monster(), x, y))
        self.update_fov()

    def pick_monster(self) -> str:
        pool = [(k, t["weight"]) for k, t in MONSTER_TEMPLATES.items() if t["min_depth"] <= self.depth]
        kinds, weights = zip(*pool)
        return self.rng.choices(kinds, weights=weights)[0]

    # ---- queries ------------------------------------------------------
    def blocking_at(self, x: int, y: int) -> Entity | None:
        for e in self.entities:
            if e.blocks and e.x == x and e.y == y and (e.fighter is None or e.fighter.alive):
                return e
        return None

    @property
    def monsters(self) -> list[Entity]:
        return [e for e in self.entities if e.ai and e.fighter and e.fighter.alive]

    @property
    def game_over(self) -> bool:
        return not self.player.fighter.alive

    def update_fov(self) -> None:
        compute_fov(self.gmap, self.player.x, self.player.y, FOV_RADIUS)

    # ---- actions ------------------------------------------------------
    def player_move(self, dx: int, dy: int) -> bool:
        """Try to move/attack. Returns True if a turn was spent."""
        if self.game_over:
            return False
        tx, ty = self.player.x + dx, self.player.y + dy
        target = self.blocking_at(tx, ty)
        if target and target.fighter:
            _, msg = attack(self.player, target, self.rng)
            self.log.add(msg)
            if not target.fighter.alive:
                self.on_kill(target)
        elif self.gmap.walkable(tx, ty):
            self.player.move(dx, dy)
        else:
            return False
        self.end_turn()
        return True

    def player_wait(self) -> None:
        if self.player.fighter.hp < self.player.fighter.max_hp and self.turn % 3 == 0:
            self.player.fighter.heal(1)
        self.end_turn()

    def descend(self) -> bool:
        if self.player.pos != self.gmap.stairs:
            self.log.add("There are no stairs here.")
            return False
        self.new_level()
        self.log.add(f"You descend to depth {self.depth}. The air grows hotter.")
        return True

    def on_kill(self, monster: Entity) -> None:
        monster.glyph, monster.blocks, monster.ai = "%", False, None
        monster.name = f"{monster.name} corpse"
        self.xp += monster.xp_value

    # ---- monsters -----------------------------------------------------
    def end_turn(self) -> None:
        self.turn += 1
        for m in self.monsters:
            self.monster_act(m)
            if self.game_over:
                break
        self.update_fov()

    def monster_act(self, m: Entity) -> None:
        if not self.gmap.visible[m.y][m.x]:
            return  # only hunts what it can see (sight is symmetric)
        if chebyshev(m.pos, self.player.pos) <= 1:
            _, msg = attack(m, self.player, self.rng)
            self.log.add(msg)
            return
        dx = (self.player.x > m.x) - (self.player.x < m.x)
        dy = (self.player.y > m.y) - (self.player.y < m.y)
        for step in ((dx, dy), (dx, 0), (0, dy)):
            nx, ny = m.x + step[0], m.y + step[1]
            if step != (0, 0) and self.gmap.walkable(nx, ny) and not self.blocking_at(nx, ny):
                m.move(*step)
                return
