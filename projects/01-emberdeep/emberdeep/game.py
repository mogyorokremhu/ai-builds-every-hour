"""Game state and turn logic, independent of any renderer."""
from __future__ import annotations

import random

from . import dungeon, loot
from .combat import attack
from .entities import MONSTER_TEMPLATES, Entity, make_monster, make_player
from .fov import compute_fov
from .geometry import chebyshev
from .items import TARGET_CELL, Item, make_item, make_item_entity
from .messages import MessageLog
from .targeting import blast_area, projectile_path

MAP_W, MAP_H = 70, 24
FOV_RADIUS = 8

# message colours (names resolved by the UI's colour table)
C_INFO, C_GOOD, C_BAD, C_ITEM, C_MAGIC = "white", "bright_green", "bright_red", "bright_yellow", "bright_cyan"


class Game:
    def __init__(self, seed: int | None = None) -> None:
        self.seed = seed if seed is not None else random.randrange(1 << 30)
        self.rng = random.Random(self.seed)
        self.log = MessageLog()
        self.depth = 0
        self.turn = 0
        self.xp = 0
        self.kills = 0
        self.player = make_player(0, 0)
        self.entities: list[Entity] = []
        self.new_level()
        self.say("You descend into Emberdeep. Find the stairs (>).", C_MAGIC)

    def say(self, text: str, color: str = C_INFO) -> None:
        self.log.add(text, color, self.turn)

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
        for room in rooms:
            for _ in range(loot.items_per_room(self.depth, self.rng)):
                spots = [p for p in room.inner() if not self.items_at(*p) and p != self.player.pos]
                if spots:
                    x, y = self.rng.choice(spots)
                    self.place_item(loot.roll_loot(self.depth, self.rng), x, y)
        self.update_fov()

    def pick_monster(self) -> str:
        pool = [(k, t["weight"]) for k, t in MONSTER_TEMPLATES.items() if t["min_depth"] <= self.depth]
        kinds, weights = zip(*pool)
        return self.rng.choices(kinds, weights=weights)[0]

    def place_item(self, item: Item, x: int, y: int) -> Entity:
        ent = make_item_entity(item, x, y)
        # items go first so monsters/player draw over them
        self.entities.insert(1, ent)
        return ent

    # ---- queries ------------------------------------------------------
    def blocking_at(self, x: int, y: int) -> Entity | None:
        for e in self.entities:
            if e.blocks and e.x == x and e.y == y and (e.fighter is None or e.fighter.alive):
                return e
        return None

    def items_at(self, x: int, y: int) -> list[Entity]:
        return [e for e in self.entities if e.item is not None and e.x == x and e.y == y]

    @property
    def monsters(self) -> list[Entity]:
        return [e for e in self.entities if e.ai and e.fighter and e.fighter.alive]

    def visible_monsters(self) -> list[Entity]:
        """Living monsters in view, nearest first."""
        vis = [m for m in self.monsters if self.gmap.visible[m.y][m.x]]
        return sorted(vis, key=lambda m: (chebyshev(m.pos, self.player.pos), m.y, m.x))

    def visible_items(self) -> list[Entity]:
        return [e for e in self.entities if e.item is not None and self.gmap.visible[e.y][e.x]]

    def monster_at(self, x: int, y: int) -> Entity | None:
        for m in self.monsters:
            if m.pos == (x, y):
                return m
        return None

    @property
    def game_over(self) -> bool:
        return not self.player.fighter.alive

    def update_fov(self) -> None:
        compute_fov(self.gmap, self.player.x, self.player.y, FOV_RADIUS)

    # ---- movement & combat --------------------------------------------
    def player_move(self, dx: int, dy: int) -> bool:
        """Try to move/attack. Returns True if a turn was spent."""
        if self.game_over:
            return False
        tx, ty = self.player.x + dx, self.player.y + dy
        target = self.blocking_at(tx, ty)
        if target and target.fighter:
            _, msg = attack(self.player, target, self.rng)
            self.say(msg)
            if not target.fighter.alive:
                self.on_kill(target)
        elif self.gmap.walkable(tx, ty):
            self.player.move(dx, dy)
            here = self.items_at(tx, ty)
            if len(here) == 1:
                self.say(f"You see here {here[0].item.display_name}.")
            elif here:
                self.say(f"There are {len(here)} items here.")
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
            self.say("There are no stairs here.")
            return False
        self.new_level()
        self.say(f"You descend to depth {self.depth}. The air grows hotter.", C_MAGIC)
        return True

    def on_kill(self, monster: Entity) -> None:
        monster.glyph, monster.blocks, monster.ai = "%", False, None
        monster.color = "red"
        monster.name = f"{monster.name} corpse"
        self.xp += monster.xp_value
        self.kills += 1

    def damage_monster(self, monster: Entity, amount: int, how: str) -> None:
        dealt = monster.fighter.take_damage(amount)
        msg = f"The {monster.name} is {how} for {dealt}."
        if not monster.fighter.alive:
            msg += f" The {monster.name} dies!"
            self.on_kill(monster)
        self.say(msg, C_MAGIC)

    # ---- items --------------------------------------------------------
    def pickup(self) -> bool:
        here = self.items_at(*self.player.pos)
        if not here:
            self.say("There is nothing here to pick up.")
            return False
        inv = self.player.inventory
        picked = False
        for ent in here:
            if not inv.can_add(ent.item):
                self.say("Your pack is full.", C_BAD)
                break
            inv.add(ent.item)
            self.entities.remove(ent)
            stored = next((i for i in inv if i is ent.item), None) or next(
                i for i in inv if i.key == ent.item.key and i.stackable)
            letter = inv.letter_of(stored)
            self.say(f"You pick up {ent.item.display_name} ({letter}).", C_ITEM)
            picked = True
        if picked:
            self.end_turn()
        return picked

    def drop(self, item: Item) -> bool:
        inv, eq = self.player.inventory, self.player.equipment
        if not any(i is item for i in inv.items):
            return False
        if eq.is_equipped(item):
            eq.unequip(item)
            eq.apply_to(self.player.fighter)
        inv.remove(item)
        self.place_item(item, *self.player.pos)
        self.say(f"You drop {item.display_name}.")
        self.end_turn()
        return True

    def toggle_equip(self, item: Item) -> bool:
        eq = self.player.equipment
        if eq.is_equipped(item):
            eq.unequip(item)
            self.say(f"You remove the {item.name}.")
        else:
            old = eq.equip(item)
            if old is not None:
                self.say(f"You remove the {old.name}.")
            verb = "wield" if item.slot == "weapon" else "put on"
            self.say(f"You {verb} the {item.name}.", C_ITEM)
        eq.apply_to(self.player.fighter)
        self.end_turn()
        return True

    def use(self, item: Item, target: tuple[int, int] | None = None) -> bool:
        """Use/equip an inventory item. Returns True if a turn was spent.

        Items with ``targeting == "cell"`` need ``target``; ``"auto"`` items pick the nearest
        visible monster themselves.
        """
        if self.game_over or not any(i is item for i in self.player.inventory.items):
            return False
        if item.is_equipment:
            return self.toggle_equip(item)
        handler = getattr(self, f"_effect_{item.effect}", None)
        if handler is None:
            self.say(f"You can't use the {item.name}.")
            return False
        if item.targeting == TARGET_CELL and target is None:
            self.say("That needs a target.")
            return False
        if not handler(item, target):
            return False
        self.player.inventory.take_one(item)
        self.end_turn()
        return True

    def _effect_heal(self, item: Item, _target) -> bool:
        f = self.player.fighter
        if f.hp >= f.max_hp:
            self.say("You are already at full health.")
            return False
        healed = f.heal(item.magnitude)
        self.say(f"You drink the {item.name} and recover {healed} HP.", C_GOOD)
        return True

    def _effect_lightning(self, item: Item, _target) -> bool:
        candidates = [m for m in self.visible_monsters() if chebyshev(m.pos, self.player.pos) <= item.range]
        if not candidates:
            self.say("No enemy is close enough to strike.")
            return False
        m = candidates[0]
        self.say("A bolt of lightning leaps from the scroll!", C_MAGIC)
        self.damage_monster(m, item.magnitude, "struck by lightning")
        return True

    def _check_target(self, item: Item, target: tuple[int, int]) -> bool:
        if not self.gmap.in_bounds(*target) or not self.gmap.visible[target[1]][target[0]]:
            self.say("You can't see that spot.")
            return False
        if chebyshev(target, self.player.pos) > item.range:
            self.say("That is out of range.")
            return False
        return True

    def _effect_fireball(self, item: Item, target) -> bool:
        if not self._check_target(item, target):
            return False
        path = projectile_path(self.gmap, self.player.pos, target)
        center = path[-1] if path else self.player.pos
        self.say("The scroll erupts into a roaring fireball!", C_MAGIC)
        for cell in blast_area(self.gmap, center, item.radius):
            if cell == self.player.pos:
                dealt = self.player.fighter.take_damage(item.magnitude // 2)
                self.say(f"You are singed by your own fireball for {dealt}!", C_BAD)
                continue
            m = self.monster_at(*cell)
            if m is not None:
                self.damage_monster(m, item.magnitude, "burned")
        return True

    def _effect_confuse(self, item: Item, target) -> bool:
        if not self._check_target(item, target):
            return False
        m = self.monster_at(*target)
        if m is None:
            self.say("There is no creature there.")
            return False
        m.confused = item.magnitude
        self.say(f"The {m.name}'s eyes glaze over.", C_MAGIC)
        return True

    def _effect_teleport(self, item: Item, _target) -> bool:
        spots = [(x, y) for y in range(self.gmap.height) for x in range(self.gmap.width)
                 if self.gmap.walkable(x, y) and not self.blocking_at(x, y)
                 and chebyshev((x, y), self.player.pos) > FOV_RADIUS]
        if not spots:
            self.say("The scroll fizzles.")
            return True
        self.player.x, self.player.y = self.rng.choice(spots)
        self.say("Space folds around you!", C_MAGIC)
        return True

    # ---- monsters -----------------------------------------------------
    def end_turn(self) -> None:
        self.turn += 1
        self.update_fov()
        for m in self.monsters:
            self.monster_act(m)
            if self.game_over:
                break
        self.update_fov()

    def monster_act(self, m: Entity) -> None:
        if m.confused > 0:
            m.confused -= 1
            dx, dy = self.rng.choice([(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)])
            nx, ny = m.x + dx, m.y + dy
            other = self.blocking_at(nx, ny)
            if other is not None and other is not m and other.fighter:
                _, msg = attack(m, other, self.rng)
                self.say(f"(confused) {msg}", C_BAD if other.is_player else C_INFO)
                if not other.is_player and not other.fighter.alive:
                    self.on_kill(other)
            elif self.gmap.walkable(nx, ny):
                m.move(dx, dy)
            if m.confused == 0:
                self.say(f"The {m.name} is no longer confused.")
            return
        if not self.gmap.visible[m.y][m.x]:
            return  # only hunts what it can see (sight is symmetric)
        if chebyshev(m.pos, self.player.pos) <= 1:
            _, msg = attack(m, self.player, self.rng)
            self.say(msg, C_BAD)
            return
        dx = (self.player.x > m.x) - (self.player.x < m.x)
        dy = (self.player.y > m.y) - (self.player.y < m.y)
        for step in ((dx, dy), (dx, 0), (0, dy)):
            nx, ny = m.x + step[0], m.y + step[1]
            if step != (0, 0) and self.gmap.walkable(nx, ny) and not self.blocking_at(nx, ny):
                m.move(*step)
                return

    # ---- debug helpers --------------------------------------------------
    def give(self, key: str, count: int = 1) -> Item:
        """Put an item straight into the player's pack (used by tests and wizard mode)."""
        item = make_item(key, count)
        self.player.inventory.add(item)
        return next(i for i in self.player.inventory if i.key == key)
