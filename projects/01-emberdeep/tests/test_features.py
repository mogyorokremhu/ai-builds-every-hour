"""Phase 7 features: identification, throwing, locked doors, braziers, knockback, the bot."""
import random
import tempfile
import unittest
from pathlib import Path

from emberdeep import bot, knockback, lighting, locks, save
from emberdeep.__main__ import run_text_command
from emberdeep.entities import make_monster
from emberdeep.fov import compute_fov
from emberdeep.game import Game
from emberdeep.gamemap import GameMap
from emberdeep.geometry import Rect
from emberdeep.identify import ALWAYS_KNOWN, Identification, maskable_keys
from emberdeep.items import make_item, plural
from emberdeep.tiles import BRAZIER, FLOOR, LAVA, LOCKED_DOOR, TILES_BY_CODE, WALL
from emberdeep.ui_curses import CursesUI

from tests.helpers import FakeScreen, arena


def add(g, kind, dx, dy, awake=True):
    m = make_monster(kind, g.player.x + dx, g.player.y + dy)
    m.asleep = not awake
    g.entities.append(m)
    g.update_fov()
    return m


class IdentificationTests(unittest.TestCase):
    def test_roll_gives_unique_appearances(self):
        ident = Identification.roll(random.Random(5))
        looks = list(ident.appearances.values())
        self.assertEqual(len(looks), len(set(looks)))
        self.assertEqual(set(ident.appearances), set(maskable_keys()))
        self.assertTrue(ALWAYS_KNOWN <= ident.known)

    def test_rolls_differ_between_seeds_but_are_deterministic(self):
        a = Identification.roll(random.Random(1)).appearances
        b = Identification.roll(random.Random(1)).appearances
        c = Identification.roll(random.Random(2)).appearances
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_floor_items_are_masked_and_identified_together(self):
        g = arena()
        x, y = g.player.pos
        g.place_item(make_item("speed potion"), x + 1, y)
        g.place_item(make_item("speed potion"), x + 2, y)
        names = {e.item.display_name for e in g.items_at(x + 1, y) + g.items_at(x + 2, y)}
        self.assertEqual(len(names), 1)
        self.assertNotIn("speed", names.pop())
        g.identify_kind("speed potion")
        self.assertEqual(g.items_at(x + 1, y)[0].item.display_name, "potion of speed")
        self.assertEqual(g.items_at(x + 2, y)[0].name, "potion of speed")

    def test_healing_is_known_from_the_start(self):
        g = arena()
        g.place_item(make_item("healing potion"), g.player.x + 1, g.player.y)
        self.assertEqual(g.items_at(g.player.x + 1, g.player.y)[0].item.display_name, "potion of healing")

    def test_unknown_item_describes_itself_as_unidentified(self):
        g = arena()
        it = g.ident.mask(make_item("fireball scroll"))
        self.assertEqual(it.describe(), "unidentified")
        self.assertTrue(it.display_name.startswith('scroll labelled "'))

    def test_plural_of_appearances(self):
        self.assertEqual(plural("murky potion"), "murky potions")
        self.assertEqual(plural('scroll labelled "ZUN"'), 'scrolls labelled "ZUN"')

    def test_drinking_an_unknown_potion_identifies_it(self):
        g = arena()
        pot = g.ident.mask(g.give("speed potion"))
        self.assertFalse(pot.identified)
        self.assertTrue(g.use(pot))
        self.assertTrue(g.player.statuses.has("hasted"))
        self.assertTrue(g.ident.is_known("speed potion"))
        self.assertTrue(any("was a potion of speed" in m.text for m in g.log.entries()))

    def test_unknown_potion_is_consumed_even_when_useless(self):
        g = arena()
        g.ident.known.discard("healing potion")
        pot = g.ident.mask(g.give("healing potion"))
        self.assertTrue(g.use(pot))  # full HP: a known one would be refused
        self.assertFalse(any(i.key == "healing potion" for i in g.player.inventory))

    def test_unknown_targeted_scroll_picks_nearest_foe(self):
        g = arena()
        m = add(g, "cave troll", 3, 0)
        scroll = g.ident.mask(g.give("confusion scroll"))
        self.assertTrue(g.use(scroll))
        self.assertGreater(m.confused, 0)

    def test_unknown_confusion_without_foes_confuses_you(self):
        g = arena()
        scroll = g.ident.mask(g.give("confusion scroll"))
        g.use(scroll)
        self.assertTrue(g.player.statuses.has("confused"))

    def test_unknown_fireball_without_foes_singes_you(self):
        g = arena()
        hp = g.player.fighter.hp
        g.use(g.ident.mask(g.give("fireball scroll")))
        self.assertLess(g.player.fighter.hp, hp)

    def test_identification_survives_save_and_old_saves_know_everything(self):
        g = Game(11)
        g.identify_kind("teleport scroll")
        data = save.to_dict(g)
        g2 = save.from_dict(data)
        self.assertEqual(g2.ident.appearances, g.ident.appearances)
        self.assertIn("teleport scroll", g2.ident.known)
        del data["ident"]
        g3 = save.from_dict(data)
        self.assertTrue(all(g3.ident.is_known(k) for k in maskable_keys()))

    def test_drinking_liquid_fire_and_venom(self):
        g = arena()
        g.identify_kind("fire potion")
        g.identify_kind("venom potion")
        hp = g.player.fighter.hp
        g.use(g.give("fire potion"))
        self.assertLess(g.player.fighter.hp, hp)
        g.use(g.give("venom potion"))
        self.assertTrue(g.player.statuses.has("poisoned"))


class ThrowingTests(unittest.TestCase):
    def test_thrown_dagger_hits_and_lands(self):
        g = arena()
        m = add(g, "cave troll", 3, 0)
        dagger = g.give("dagger")
        hp, spot = m.fighter.hp, m.pos
        self.assertTrue(g.throw(dagger, spot))
        self.assertLess(m.fighter.hp, hp)
        self.assertTrue(any(e.item.key == "dagger" for e in g.items_at(*spot)))
        self.assertFalse(any(i.key == "dagger" for i in g.player.inventory))

    def test_projectile_stops_at_first_creature(self):
        g = arena()
        near = add(g, "rat", 2, 0)
        far = add(g, "cave troll", 4, 0)
        hp, spot = far.fighter.hp, near.pos
        g.throw(g.give("torch"), far.pos)
        self.assertEqual(far.fighter.hp, hp)
        self.assertTrue(any(e.item.key == "torch" for e in g.items_at(*spot)))

    def test_liquid_fire_bursts_and_identifies(self):
        g = arena()
        a = add(g, "cave troll", 4, 0)
        b = add(g, "cave troll", 4, 1)
        pot = g.ident.mask(g.give("fire potion"))
        hp = a.fighter.hp
        self.assertTrue(g.throw(pot, a.pos))
        self.assertLess(a.fighter.hp, hp)
        self.assertLess(b.fighter.hp, hp)
        self.assertTrue(g.ident.is_known("fire potion"))
        self.assertFalse(g.items_at(*a.pos))  # shattered, nothing lands

    def test_fire_creatures_bask_in_liquid_fire(self):
        g = arena()
        imp = add(g, "fire beetle", 3, 0)
        hp = imp.fighter.hp
        g.throw(g.give("fire potion"), imp.pos)
        self.assertEqual(imp.fighter.hp, hp)

    def test_venom_splash_poisons(self):
        g = arena()
        m = add(g, "cave troll", 3, 0)
        g.throw(g.give("venom potion"), m.pos)
        self.assertTrue(m.statuses.has("poisoned"))

    def test_throw_validation(self):
        g = arena()
        dagger = g.give("dagger")
        self.assertFalse(g.throw(dagger, g.player.pos))
        self.assertFalse(g.throw(dagger, (g.player.x + 9, g.player.y)))  # too far / unseen
        heart = g.give("ember heart")
        self.assertFalse(g.throw(heart, (g.player.x + 2, g.player.y)))

    def test_throwing_equipped_weapon_unequips_it(self):
        g = arena()
        dagger = g.give("dagger")
        g.toggle_equip(dagger)
        power = g.player.fighter.power
        g.throw(dagger, (g.player.x + 3, g.player.y))
        self.assertEqual(g.player.fighter.power, power - 1)
        self.assertIsNone(g.player.equipment.slots["weapon"])

    def test_curses_throw_command(self):
        g = arena()
        m = add(g, "cave troll", 3, 0)
        g.give("dagger")
        hp = m.fighter.hp
        ui = CursesUI(FakeScreen(["t", "a", 10, "Q"]), g)
        ui.run()
        self.assertLess(m.fighter.hp, hp)

    def test_text_mode_throw(self):
        g = arena()
        m = add(g, "cave troll", 3, 0)
        g.give("dagger")
        hp = m.fighter.hp
        run_text_command(g, "ta")
        self.assertLess(m.fighter.hp, hp)


def locked_room_game(seed: int = 4) -> Game:
    """An arena split by a wall with a locked door into a west and east half."""
    g = arena(seed, w=20, h=9)
    for y in range(9):
        g.gmap.set(12, y, WALL)
    g.gmap.set(12, 4, LOCKED_DOOR)
    g.player.x, g.player.y = 11, 4
    g.update_fov()
    return g


class LockTests(unittest.TestCase):
    def test_key_unlocks_and_is_used_up(self):
        g = locked_room_game()
        g.give("iron key")
        self.assertTrue(g.player_move(1, 0))
        self.assertEqual(g.gmap.get(12, 4).name, "open door")
        self.assertFalse(any(i.key == "iron key" for i in g.player.inventory))

    def test_locked_door_needs_confirmation_to_force(self):
        g = locked_room_game()
        self.assertFalse(g.player_move(1, 0))  # first bump: just a message
        self.assertEqual(g.turn, 0)
        for _ in range(200):
            g.player_move(1, 0)
            if g.gmap.get(12, 4).name == "open door":
                break
        self.assertEqual(g.gmap.get(12, 4).name, "open door")
        self.assertGreater(g.turn, 0)

    def test_force_chance_grows_with_power(self):
        self.assertLess(locks.force_chance(2), locks.force_chance(10))
        self.assertLessEqual(locks.force_chance(100), 0.75)

    def test_locked_doors_block_monsters_and_sight(self):
        g = locked_room_game()
        m = make_monster("rat", 14, 4)
        g.entities.append(m)
        g.update_fov()
        self.assertFalse(g.gmap.visible[4][14])
        self.assertFalse(g.gmap.passable(12, 4))

    def test_try_lock_keeps_level_connected(self):
        for seed in range(25):
            g = Game(seed)
            if not g.generator.startswith(("rooms", "bsp")):
                continue
            start = g.player.pos
            for gx in range(g.gmap.width):
                for gy in range(g.gmap.height):
                    if g.gmap.get(gx, gy).name == "locked door":
                        g.gmap.set(gx, gy, FLOOR)  # undo the level's own locks for a clean check
            from emberdeep.gen_caves import bfs_distances

            base = bfs_distances(g.gmap, start)
            for x in range(1, 50, 7):
                rect = Rect(x, 2, 8, 7)
                locked = locks.try_lock(g, rect, start)
                if locked:
                    after = bfs_distances(g.gmap, start)
                    inside = set(rect.inner())
                    self.assertTrue(all(p in after for p in base if p not in inside and p not in locked))
                    for p in locked:
                        g.gmap.set(*p, FLOOR)

    def test_some_levels_get_locked_rooms_with_reachable_keys(self):
        from emberdeep.gen_caves import bfs_distances

        found = 0
        for seed in range(40):
            g = Game(seed)
            g.new_level()  # depth 2
            doors = [(x, y) for y in range(g.gmap.height) for x in range(g.gmap.width)
                     if g.gmap.get(x, y).name == "locked door"]
            if not doors:
                continue
            found += 1
            reach = bfs_distances(g.gmap, g.player.pos)
            keys = [e for e in g.entities if e.item is not None and e.item.key == "iron key"]
            self.assertTrue(keys)
            self.assertTrue(any(k.pos in reach for k in keys))
            self.assertIn(g.gmap.stairs, reach)
        self.assertGreater(found, 3)

    def test_locked_door_survives_save(self):
        g = locked_room_game()
        g2 = save.from_dict(save.to_dict(g))
        self.assertEqual(g2.gmap.get(12, 4).name, "locked door")
        self.assertIn("L", TILES_BY_CODE)


class LightingTests(unittest.TestCase):
    def lit_room(self):
        g = arena(w=40, h=11)
        g.gmap.set(35, 0, BRAZIER)
        g.lit = lighting.compute_lit(g.gmap)
        g.resources.torch = 0  # torch out: radius 2
        g.player.x, g.player.y = 16, 5
        g.update_fov()
        return g

    def test_brazier_lights_cells_around_it(self):
        g = self.lit_room()
        self.assertIn((35, 1), g.lit)
        self.assertNotIn((16, 5), g.lit)

    def test_you_can_see_lit_cells_from_the_dark(self):
        g = self.lit_room()
        self.assertTrue(g.gmap.visible[2][34])
        self.assertFalse(g.gmap.visible[9][12])  # dark and beyond the torch: unseen

    def test_monsters_in_light_dont_see_you_in_the_dark(self):
        g = self.lit_room()
        m = make_monster("rat", 34, 2)
        g.entities.append(m)
        g.update_fov()
        self.assertTrue(g.gmap.visible[2][34])
        self.assertFalse(g.monster_sees_player(m))
        g.player.x, g.player.y = 33, 3
        g.update_fov()
        self.assertTrue(g.monster_sees_player(m))

    def test_compute_lit_leaves_exploration_alone(self):
        g = self.lit_room()
        explored = [row[:] for row in g.gmap.explored]
        lighting.compute_lit(g.gmap)
        self.assertEqual(g.gmap.explored, explored)

    def test_brazier_spots_never_open_walls(self):
        for seed in range(10):
            g = Game(seed)
            for (x, y) in lighting.braziers(g.gmap):
                fronts = [(dx, dy) for dx, dy in lighting.ORTHO
                          if g.gmap.get(x + dx, y + dy).name in ("floor", "fungus", "rubble", "stairs down")]
                self.assertLessEqual(len(fronts), 1)

    def test_magma_levels_have_braziers(self):
        total = 0
        for seed in range(6):
            g = Game(seed)
            while g.depth < 7:
                g.new_level()
            total += len(lighting.braziers(g.gmap))
        self.assertGreater(total, 0)

    def test_lit_is_rebuilt_on_load(self):
        g = self.lit_room()
        g2 = save.from_dict(save.to_dict(g))
        self.assertEqual(g2.lit, g.lit)

    def test_fov_without_lit_matches_plain(self):
        gm = GameMap(30, 30)
        for y in range(1, 29):
            for x in range(1, 29):
                gm.set(x, y, FLOOR)
        compute_fov(gm, 15, 15, 5)
        plain = [row[:] for row in gm.visible]
        compute_fov(gm, 15, 15, 5, frozenset())
        self.assertEqual(plain, gm.visible)


class KnockbackTests(unittest.TestCase):
    def test_shove_moves_target(self):
        g = arena()
        m = add(g, "cave troll", 1, 0)
        self.assertEqual(knockback.shove(g, g.player, m), "moved")
        self.assertEqual(m.pos, (g.player.x + 2, g.player.y))

    def test_shove_into_lava_kills(self):
        g = arena()
        m = add(g, "cave troll", 1, 0)
        g.gmap.set(g.player.x + 2, g.player.y, LAVA)
        self.assertEqual(knockback.shove(g, g.player, m), "lava")
        self.assertNotIn(m, g.entities)
        self.assertEqual(g.kill_counts.get("cave troll"), 1)

    def test_fire_creatures_climb_out(self):
        g = arena()
        m = add(g, "fire beetle", 1, 0)
        g.gmap.set(g.player.x + 2, g.player.y, LAVA)
        self.assertEqual(knockback.shove(g, g.player, m), "climbed")
        self.assertTrue(m.fighter.alive)

    def test_walls_and_boss(self):
        g = arena()
        m = add(g, "cave troll", 1, 0)
        g.gmap.set(g.player.x + 2, g.player.y, WALL)
        self.assertEqual(knockback.shove(g, g.player, m), "blocked")
        m.tags.add("boss")
        self.assertEqual(knockback.shove(g, g.player, m), "immovable")

    def test_player_scorched_at_lava_edge(self):
        g = arena()
        troll = add(g, "cave troll", 1, 0)
        g.gmap.set(g.player.x - 1, g.player.y, LAVA)
        hp = g.player.fighter.hp
        self.assertEqual(knockback.shove(g, troll, g.player), "scorched")
        self.assertLess(g.player.fighter.hp, hp)
        self.assertTrue(g.player.statuses.has("burning"))

    def test_warhammer_knocks_back_sometimes(self):
        moved = 0
        for seed in range(30):
            g = arena(seed)
            hammer = g.give("warhammer")
            g.toggle_equip(hammer)
            g.player.fighter.base_power = 1  # keep the troll alive
            m = add(g, "cave troll", 1, 0)
            m.fighter.hp = m.fighter.base_max_hp = 500
            g.player_move(1, 0)
            moved += any("knocked back" in msg.text for msg in g.log.entries())
        self.assertGreater(moved, 0)

    def test_trolls_carry_the_knockback_tag(self):
        self.assertIn("knockback", make_monster("cave troll", 0, 0).tags)


class KoboldPotionTests(unittest.TestCase):
    def test_hurt_kobold_drinks_its_potion(self):
        drank = 0
        for seed in range(20):
            g = arena(seed)
            k = add(g, "kobold", 2, 0)
            k.ai_state["potion"] = True
            k.fighter.hp = 1
            g.player_wait()
            drank += k.fighter.hp > 1 and "potion" not in k.ai_state
        self.assertGreater(drank, 5)

    def test_kobold_drops_unused_potion(self):
        g = arena()
        k = add(g, "kobold", 1, 0)
        k.ai_state["potion"] = True
        k.fighter.hp = 0
        g.on_kill(k)
        self.assertTrue(any(e.item.key == "healing potion" for e in g.items_at(*k.pos)))


class BotTests(unittest.TestCase):
    def test_bot_plays_without_crashing(self):
        for seed in (1, 2):
            r = bot.play(seed, max_actions=600)
            self.assertGreaterEqual(r.depth, 1)
            self.assertGreater(r.turns, 0)

    def test_bot_makes_progress(self):
        r = bot.play(3, max_actions=2500)
        self.assertTrue(r.depth >= 2 or r.cause != "timeout")

    def test_report_format(self):
        results = [bot.RunResult(1, True, 10, 15, 4000, 200, "victory"),
                   bot.RunResult(2, False, 3, 4, 900, 30, "killed by an ember imp's ember bolt"),
                   bot.RunResult(3, False, 3, 5, 800, 25, "killed by a jackal")]
        text = bot.report(results, 1.0)
        self.assertIn("Victories | 1 (33.3%)", text)
        self.assertIn("killed by ember imp", text)
        self.assertIn("| 3 | 2 |", text)

    def test_bot_runs_are_deterministic(self):
        a = bot.play(5, max_actions=400)
        b = bot.play(5, max_actions=400)
        self.assertEqual(a, b)


class SaveRoundTripTests(unittest.TestCase):
    def test_new_items_round_trip(self):
        g = arena()
        g.give("warhammer")
        g.give("iron key", 2)
        g.ident.mask(g.give("venom potion"))
        with tempfile.TemporaryDirectory() as d:
            path = save.save_game(g, Path(d) / "s.json")
            g2 = save.load_game(path)
        keys = {i.key: i for i in g2.player.inventory}
        self.assertEqual(keys["iron key"].count, 2)
        self.assertAlmostEqual(keys["warhammer"].knockback, 0.35)
        self.assertFalse(keys["venom potion"].identified)


if __name__ == "__main__":
    unittest.main()
