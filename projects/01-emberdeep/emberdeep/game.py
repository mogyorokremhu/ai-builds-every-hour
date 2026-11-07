"""Game state and turn logic, independent of any renderer."""
from __future__ import annotations

import random

from . import ai, levelgen, loot, traps, vaults
from .combat import attack
from .entities import MONSTER_TEMPLATES, Entity, make_monster, make_player
from .fov import compute_fov
from .geometry import chebyshev
from .items import TARGET_CELL, Item, make_item, make_item_entity
from .messages import MessageLog, a_an
from .progression import CHOICES, Progression
from .resources import Resources
from .status import STATUS_INFO
from .targeting import blast_area, projectile_path
from .themes import Theme, theme_for_depth

MAP_W, MAP_H = 70, 24
FOV_RADIUS = 8           # radius with a bright torch (see resources.TORCH_STAGES)
SLEEP_CHANCE = 0.45      # chance a freshly spawned monster (or pack) is asleep

#: Noise made by player actions: monsters within ``noise * NOISE_RANGE`` may hear it.
NOISE = {"move": 1, "wait": 0, "attack": 4, "pickup": 1, "item": 2, "loud": 8, "search": 0}
NOISE_RANGE = 2
ENERGY_PER_ACTION = 100  # a creature acts each time its energy reaches this
ACTION_COST = 100        # time a normal-speed action takes

# message colours (names resolved by the UI's colour table)
C_INFO, C_GOOD, C_BAD, C_ITEM, C_MAGIC = "white", "bright_green", "bright_red", "bright_yellow", "bright_cyan"


class Game:
    def __init__(self, seed: int | None = None) -> None:
        self.seed = seed if seed is not None else random.randrange(1 << 30)
        self.rng = random.Random(self.seed)
        self.log = MessageLog()
        self.depth = 0
        self.turn = 0
        self.kills = 0
        self.player = make_player(0, 0)
        self.progression = Progression()
        self.resources = Resources()
        self.death_cause: str | None = None
        self.entities: list[Entity] = []
        self.traps: dict[tuple[int, int], traps.Trap] = {}
        self.special_rooms: list[vaults.SpecialRoom] = []
        self.altars: dict[tuple[int, int], bool] = {}
        self.theme: Theme = theme_for_depth(1)
        self.generator = "rooms"
        self.noise = 0
        self._trap_confirm: tuple[int, int] | None = None
        self.new_level()
        self.say("You descend into Emberdeep. Find the stairs (>).", C_MAGIC)

    def say(self, text: str, color: str = C_INFO) -> None:
        self.log.add(text, color, self.turn)

    # ---- level setup -------------------------------------------------
    @property
    def xp(self) -> int:
        return self.progression.xp

    @property
    def level(self) -> int:
        return self.progression.level

    def new_level(self) -> None:
        self.depth += 1
        old_theme = self.theme
        self.theme = theme_for_depth(self.depth)
        layout = levelgen.generate_level(MAP_W, MAP_H, self.rng, self.theme)
        self.gmap, self.generator = layout.gmap, layout.generator
        self.player.x, self.player.y = layout.start
        self.entities = [self.player]
        self.traps, self.special_rooms, self.altars = {}, [], {}
        self._trap_confirm = None
        for area in layout.areas[1:]:
            self._spawn_monsters(area)
        for area in layout.areas:
            for _ in range(loot.items_per_room(self.depth, self.rng)):
                spots = [p for p in area if not self.items_at(*p) and p != self.player.pos
                         and p != self.gmap.stairs]
                if spots:
                    x, y = self.rng.choice(spots)
                    self.place_item(loot.roll_loot(self.depth, self.rng, self.theme.loot_bias), x, y)
        if layout.rooms:
            vaults.furnish(self, layout.rooms)
        loose = [p for area in layout.areas[1:] for p in area]
        traps.place(self, loose, traps.traps_for_depth(self.depth, self.rng))
        if self.depth > 1 and self.theme is not old_theme:
            self.say(self.theme.intro, C_MAGIC)
        self.update_fov()

    def _spawn_monsters(self, area: list[tuple[int, int]]) -> None:
        for _ in range(self.rng.randint(0, 2 + self.depth // 2)):
            if not [p for p in area if not self.blocking_at(*p)]:
                return
            kind = self.pick_monster()
            lo, hi = MONSTER_TEMPLATES[kind].get("pack", (1, 1))
            asleep = self.rng.random() < SLEEP_CHANCE
            for _ in range(self.rng.randint(lo, hi)):
                spots = [p for p in area if not self.blocking_at(*p) and p != self.gmap.stairs]
                if not spots:
                    break
                x, y = self.rng.choice(spots)
                m = make_monster(kind, x, y)
                m.asleep = asleep
                self.entities.append(m)

    def pick_monster(self) -> str:
        bias = self.theme.monster_bias
        pool = [(k, t["weight"] * bias.get(k, 1.0)) for k, t in MONSTER_TEMPLATES.items()
                if t["min_depth"] <= self.depth <= t.get("max_depth", 99)]
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

    @property
    def fov_radius(self) -> int:
        return self.resources.fov_radius

    def update_fov(self) -> None:
        compute_fov(self.gmap, self.player.x, self.player.y, self.fov_radius)

    def known_trap_at(self, x: int, y: int) -> "traps.Trap | None":
        t = self.traps.get((x, y))
        return t if t is not None and not t.hidden else None

    # ---- movement & combat --------------------------------------------
    def player_move(self, dx: int, dy: int) -> bool:
        """Try to move/attack. Returns True if a turn was spent."""
        if self.game_over:
            return False
        if self.player.confused and self.rng.random() < 0.5:
            dx, dy = self.rng.choice(ai.DIRS8)
            self.say("You stumble around in confusion.", C_BAD)
        tx, ty = self.player.x + dx, self.player.y + dy
        target = self.blocking_at(tx, ty)
        if target and target.fighter:
            self.noise = NOISE["attack"]
            bonus = 0
            if target.asleep:
                bonus = self.player.fighter.power
                target.asleep = False
                self.say(f"You strike the sleeping {target.name}!", C_GOOD)
            _, msg = attack(self.player, target, self.rng, bonus)
            self.say(msg)
            if not target.fighter.alive:
                self.on_kill(target)
        elif self.gmap.walkable(tx, ty):
            known = self.known_trap_at(tx, ty)
            if known is not None and self._trap_confirm != (tx, ty) and not self.player.confused:
                self._trap_confirm = (tx, ty)
                self.say(f"There is a {known.name} there. Move again to step on it.", C_BAD)
                return False
            self._trap_confirm = None
            self.player.move(dx, dy)
            self.noise = NOISE["move"]
            here = self.items_at(tx, ty)
            if len(here) == 1:
                self.say(f"You see here {here[0].item.display_name}.")
            elif here:
                self.say(f"There are {len(here)} items here.")
            if self.gmap.get(tx, ty).name == "altar":
                used = self.altars.get((tx, ty), True)
                self.say("The altar is cold." if used else "An altar. Press p to pray.", C_MAGIC)
            vaults.check_enter(self)
            trap = self.traps.get((tx, ty))
            if trap is not None:
                traps.trigger(self, trap)
                if self.game_over:
                    return True
        elif self.player.confused:
            self.say("You bump into the wall.")  # a confused stumble still costs the turn
        else:
            return False
        self.end_turn()
        return True

    def player_wait(self) -> None:
        f = self.player.fighter
        if f.hp < f.max_hp and self.turn % 3 == 0 and self.resources.can_regenerate:
            f.heal(1)
        self.noise = NOISE["wait"]
        self.end_turn()

    def search(self) -> None:
        """Spend a turn searching carefully for hidden traps nearby."""
        found = traps.search(self)
        for t in found:
            self.say(f"You find a {t.name}!", C_ITEM)
        if not found:
            self.say("You search carefully but find nothing.")
        self.noise = NOISE["search"]
        self.end_turn()

    def pray(self) -> bool:
        if vaults.pray(self):
            self.end_turn()
            return True
        return False

    # ---- progression ----------------------------------------------------
    def gain_xp(self, amount: int) -> None:
        gained = self.progression.gain(amount)
        if gained:
            self.say(f"Welcome to level {self.progression.level}! Choose a boon.", C_GOOD)

    @property
    def pending_levels(self) -> int:
        return self.progression.pending

    def choose_level_up(self, key: str) -> bool:
        """Spend a pending level-up on choice ``key`` (see progression.CHOICES)."""
        if key not in CHOICES or self.progression.pending <= 0:
            return False
        choice = self.progression.apply(key, self.player.fighter)
        self.say(f"{choice.label}: {choice.description}.", C_GOOD)
        return True

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
        monster.statuses = type(monster.statuses)()
        monster.memory = None
        monster.name = f"{monster.name} corpse"
        monster.asleep = False
        self.kills += 1
        self.gain_xp(monster.xp_value)

    def damage_monster(self, monster: Entity, amount: int, how: str) -> None:
        dealt = monster.fighter.take_damage(amount)
        monster.asleep = False
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
            self.noise = NOISE["pickup"]
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
        self.noise = NOISE["loud"] if item.effect in ("fireball", "lightning") else NOISE["item"]
        self.end_turn()
        return True

    def _effect_eat(self, item: Item, _target) -> bool:
        res = self.resources
        if res.food >= 2300:
            self.say("You are too full to eat.")
            return False
        res.eat(item.magnitude)
        self.say(f"You eat the {item.name}. {'Delicious!' if item.key == 'ration' else 'It tastes earthy.'}",
                 C_GOOD)
        return True

    def _effect_refuel(self, item: Item, _target) -> bool:
        res = self.resources
        if res.torch >= 1400:
            self.say("Your torch is already burning brightly.")
            return False
        res.refuel(item.magnitude)
        self.say("You light a fresh torch from the embers of the old one.", C_ITEM)
        self.update_fov()
        return True

    def _effect_heal(self, item: Item, _target) -> bool:
        f = self.player.fighter
        poisoned = self.player.statuses.has("poisoned")
        if f.hp >= f.max_hp and not poisoned:
            self.say("You are already at full health.")
            return False
        healed = f.heal(item.magnitude)
        self.say(f"You drink the {item.name} and recover {healed} HP.", C_GOOD)
        if poisoned:
            self.player.statuses.remove("poisoned")
            self.say("The poison leaves your veins.", C_GOOD)
        return True

    def _effect_haste(self, item: Item, _target) -> bool:
        st = self.player.statuses
        was_slow = st.has("slowed")
        st.add("hasted", item.magnitude)
        self.say("You feel sluggishness fade." if was_slow else "You feel yourself speed up!", C_GOOD)
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

    def _effect_teleport(self, item: Item | None, _target) -> bool:
        spots = [(x, y) for y in range(self.gmap.height) for x in range(self.gmap.width)
                 if self.gmap.walkable(x, y) and not self.blocking_at(x, y)
                 and chebyshev((x, y), self.player.pos) > FOV_RADIUS]
        if not spots:
            self.say("The scroll fizzles.")
            return True
        self.player.x, self.player.y = self.rng.choice(spots)
        self.say("Space folds around you!", C_MAGIC)
        return True

    # ---- time, statuses & monsters ---------------------------------------
    def end_turn(self, cost: int = ACTION_COST) -> None:
        """Advance time after a player action of ``cost`` and let monsters act.

        Energy system: the time an action takes is ``cost`` scaled by the player's speed;
        every monster gains energy proportional to its own speed for that time and acts
        once per ``ENERGY_PER_ACTION`` energy. Fast monsters act several times per player
        turn, slow ones skip turns.
        """
        self.turn += 1
        self.tick_statuses(self.player)
        if self.game_over:
            return
        self.tick_resources()
        if self.game_over:
            return
        self.update_fov()
        for t in traps.passive_detect(self):
            self.say(f"You notice a {t.name}.", C_ITEM)
        elapsed = cost * 100 // self.player.effective_speed
        for m in self.monsters:
            if not m.fighter.alive:
                continue
            m.energy += m.effective_speed * elapsed // 100
            while m.energy >= ENERGY_PER_ACTION and m.ai and m.fighter.alive and not self.game_over:
                m.energy -= ENERGY_PER_ACTION
                ai.take_turn(self, m)
                if m.fighter.alive and m.ai:
                    self.tick_statuses(m)
            if self.game_over:
                break
        self.noise = 0
        self.update_fov()

    def tick_resources(self) -> None:
        events = self.resources.tick()
        for text, color in events.messages:
            self.say(text, color)
        if events.starve_damage:
            self.player.fighter.take_damage(events.starve_damage)
            self.say("Hunger gnaws at you.", C_BAD)
            if not self.player.fighter.alive:
                self.death_cause = "starved to death"
                self.say("You die...", C_BAD)

    def tick_statuses(self, e: Entity) -> None:
        """Apply damage-over-time and expire statuses for one creature action."""
        if not len(e.statuses):
            return
        res = e.statuses.tick()
        for name, amount in res.damage:
            dealt = e.fighter.take_damage(amount)
            if e.is_player:
                verb = "burn" if name == "burning" else "suffer from poison"
                self.say(f"You {verb} for {dealt}.", C_BAD)
                if not e.fighter.alive:
                    self.death_cause = "burned to death" if name == "burning" else "succumbed to poison"
                    self.say("You die...", C_BAD)
                    return
            elif self.gmap.visible[e.y][e.x]:
                self.say(f"The {e.name} takes {dealt} {'fire' if name == 'burning' else 'poison'} damage.")
            if not e.is_player and not e.fighter.alive:
                if self.gmap.visible[e.y][e.x]:
                    self.say(f"The {e.name} dies!", C_GOOD)
                self.on_kill(e)
                return
        for name in res.expired:
            adj = STATUS_INFO[name][2]
            if e.is_player:
                self.say(f"You are no longer {adj}.", C_GOOD)
            elif self.gmap.visible[e.y][e.x]:
                self.say(f"The {e.name} is no longer {adj}.")

    def apply_status(self, e: Entity, name: str, turns: int, power: int = 0) -> None:
        new = e.statuses.add(name, turns, power)
        if not new:
            return
        adj = STATUS_INFO[name][2]
        if e.is_player:
            self.say(f"You are {adj}!", C_BAD if name != "hasted" else C_GOOD)
        elif self.gmap.visible[e.y][e.x]:
            self.say(f"The {e.name} is {adj}!")

    def monster_attack(self, m: Entity, target: Entity, prefix: str = "") -> None:
        """Melee attack by a monster (on the player or, when confused, anyone)."""
        dealt, msg = attack(m, target, self.rng)
        self.say(prefix + msg, C_BAD if target.is_player else C_INFO)
        if not target.fighter.alive:
            if target.is_player:
                self.death_cause = f"killed by {a_an(m.name)}"
            else:
                self.on_kill(target)
            return
        if dealt > 0 and m.on_hit is not None:
            name, turns, power, chance = m.on_hit
            if self.rng.random() < chance:
                self.apply_status(target, name, turns, power)

    def cast_spell(self, m: Entity, spell_key: str) -> None:
        """A monster casts a spell at the player (line of fire already checked)."""
        spell = ai.SPELLS[spell_key]
        p = self.player
        self.say(f"The {m.name} {spell['verb']} you!", spell["color"])
        if spell["damage"]:
            dmg = max(1, spell["damage"] + self.rng.randint(-1, 1) - p.fighter.defense // 2)
            dealt = p.fighter.take_damage(dmg)
            self.say(f"It hits you for {dealt}.", C_BAD)
            if not p.fighter.alive:
                self.death_cause = f"killed by {a_an(m.name)}'s {spell_key}"
                self.say("You die...", C_BAD)
                return
        if spell["status"] is not None:
            name, turns, power, chance = spell["status"]
            if self.rng.random() < chance:
                self.apply_status(p, name, turns, power)

    def monster_act(self, m: Entity) -> None:
        """Kept for compatibility: run one AI action for ``m``."""
        ai.take_turn(self, m)

    # ---- debug helpers --------------------------------------------------
    def give(self, key: str, count: int = 1) -> Item:
        """Put an item straight into the player's pack (used by tests and wizard mode)."""
        item = make_item(key, count)
        self.player.inventory.add(item)
        return next(i for i in self.player.inventory if i.key == key)
