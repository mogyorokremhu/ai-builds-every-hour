"""Tests for Phase 5: levels, torch/hunger, generators, themes, vaults, traps, stealth."""
import random
import unittest

from emberdeep import ai, gen_bsp, gen_caves, levelgen, progression, resources, themes, traps, vaults
from emberdeep.__main__ import run_text_command
from emberdeep.entities import Fighter, make_monster
from emberdeep.game import Game
from emberdeep.geometry import Rect
from emberdeep.hud import sidebar
from emberdeep.items import make_item, plural
from emberdeep.look import describe_cell
from emberdeep.render_ascii import render
from emberdeep.ui_curses import CursesUI

from tests.helpers import FakeScreen, arena


def connected(gmap, start):
    return set(gen_caves.bfs_distances(gmap, start))


class ProgressionTests(unittest.TestCase):
    def test_thresholds_increase(self):
        self.assertEqual(progression.xp_for_level(1), 0)
        self.assertEqual(progression.xp_for_level(2), 40)
        steps = [progression.xp_to_next(lv) for lv in range(1, 6)]
        self.assertEqual(steps, sorted(steps))
        self.assertEqual(progression.level_for_xp(39), 1)
        self.assertEqual(progression.level_for_xp(40), 2)

    def test_gain_queues_pending_levels(self):
        p = progression.Progression()
        self.assertEqual(p.gain(10), 0)
        self.assertEqual(p.gain(200), 2)  # 210 XP -> level 3 (level 4 needs 225)
        self.assertEqual((p.level, p.pending), (3, 2))
        into, span = p.progress
        self.assertTrue(0 <= into < span)

    def test_apply_choices(self):
        p = progression.Progression()
        p.gain(500)
        f = Fighter(30, 10, 5, 1)
        p.apply("v", f)
        self.assertEqual((f.max_hp, f.hp), (40, 40))
        p.apply("m", f)
        self.assertEqual(f.power, 6)
        p.apply("g", f)
        self.assertEqual(f.defense, 2)
        self.assertEqual(p.history, ["v", "m", "g"])
        with self.assertRaises(ValueError):
            p.apply("x", f)

    def test_apply_without_pending_fails(self):
        with self.assertRaises(ValueError):
            progression.Progression().apply("m", Fighter(1, 1, 1, 1))

    def test_kills_level_up_player_in_game(self):
        g = arena()
        troll = make_monster("cave troll", g.player.x + 1, g.player.y)
        g.entities.append(troll)
        g.damage_monster(troll, 999, "smitten")
        self.assertEqual(g.level, 2)
        self.assertEqual(g.pending_levels, 1)
        self.assertTrue(g.choose_level_up("m"))
        self.assertEqual(g.player.fighter.power, 6)
        self.assertFalse(g.choose_level_up("m"))

    def test_level_up_survives_equipment_change(self):
        g = arena()
        g.progression.gain(100)
        g.choose_level_up("g")
        g.toggle_equip(g.give("leather armor"))
        self.assertEqual(g.player.fighter.defense, 3)


class ResourceTests(unittest.TestCase):
    def test_torch_stages_shrink_view(self):
        r = resources.Resources(torch=resources.TORCH_MAX)
        self.assertEqual(r.fov_radius, 8)
        r.torch = 100
        self.assertEqual((r.fov_radius, r.torch_label), (4, "Guttering"))
        r.torch = 0
        self.assertEqual(r.fov_radius, 2)

    def test_tick_messages_on_stage_change(self):
        r = resources.Resources(torch=351, food=401)
        ev = r.tick(2)
        texts = [t for t, _ in ev.messages]
        self.assertIn("Your torch is growing dim.", texts)
        self.assertIn("You are getting hungry.", texts)

    def test_starvation_damage(self):
        r = resources.Resources(food=0)
        ev = r.tick(resources.STARVE_INTERVAL * 2)
        self.assertEqual(ev.starve_damage, 2)
        self.assertFalse(r.can_regenerate)

    def test_refuel_and_eat_clamp(self):
        r = resources.Resources(torch=1400, food=2300)
        self.assertEqual(r.refuel(500), resources.TORCH_MAX - 1400)
        self.assertEqual(r.eat(999), resources.FOOD_MAX - 2300)

    def test_game_torch_and_food_items(self):
        g = arena()
        g.resources.torch = 50
        g.update_fov()
        self.assertTrue(g.use(g.give("torch")))
        self.assertGreater(g.resources.torch, 700)
        self.assertGreaterEqual(g.fov_radius, 7)
        g.resources.food = 2350
        ration = g.give("ration")
        self.assertFalse(g.use(ration))  # too full to eat
        g.resources.food = 100
        self.assertTrue(g.use(ration))
        self.assertGreater(g.resources.food, 1000)

    def test_starving_player_dies(self):
        g = arena()
        g.resources.food = 0
        g.player.fighter.hp = 1
        for _ in range(resources.STARVE_INTERVAL):
            g.player_wait()
        self.assertTrue(g.game_over)
        self.assertEqual(g.death_cause, "starved to death")

    def test_hungry_player_does_not_regenerate(self):
        g = arena()
        g.player.fighter.hp = 10
        g.resources.food = 200
        for _ in range(9):
            g.player_wait()
        self.assertEqual(g.player.fighter.hp, 10)

    def test_plural_es(self):
        self.assertEqual(plural("torch"), "torches")
        self.assertEqual(make_item("torch", 2).display_name, "2 torches")


class GeneratorTests(unittest.TestCase):
    def test_caves_connected_and_deterministic(self):
        for seed in range(5):
            gmap, cells = gen_caves.generate(70, 24, random.Random(seed))
            self.assertGreater(len(cells), 70 * 24 * 0.25)
            self.assertEqual(connected(gmap, cells[0]), set(cells))
        a, _ = gen_caves.generate(50, 20, random.Random(3))
        b, _ = gen_caves.generate(50, 20, random.Random(3))
        self.assertEqual([[t.name for t in r] for r in a.tiles], [[t.name for t in r] for r in b.tiles])

    def test_cave_border_is_wall(self):
        gmap, _ = gen_caves.generate(40, 16, random.Random(1))
        for x in range(40):
            self.assertFalse(gmap.walkable(x, 0) or gmap.walkable(x, 15))

    def test_sectors_partition(self):
        cells = [(x, y) for x in range(30) for y in range(10)]
        secs = gen_caves.sectors(cells)
        self.assertEqual(sum(len(s) for s in secs), len(cells))

    def test_bsp_connected_with_rooms_and_doors(self):
        doors = 0
        for seed in range(8):
            gmap, rooms = gen_bsp.generate(70, 24, random.Random(seed))
            self.assertGreaterEqual(len(rooms), 4)
            reach = connected(gmap, rooms[0].center)
            for r in rooms:
                self.assertIn(r.center, reach)
            self.assertEqual(gmap.stairs, rooms[-1].center)
            doors += sum(t.name == "door" for row in gmap.tiles for t in row)
        self.assertGreater(doors, 0)

    def test_bsp_rooms_inside_map_and_disjoint(self):
        gmap, rooms = gen_bsp.generate(70, 24, random.Random(4))
        for i, a in enumerate(rooms):
            self.assertTrue(a.x >= 0 and a.y >= 0 and a.x2 <= 70 and a.y2 <= 24)
            for b in rooms[i + 1:]:
                self.assertFalse(a.intersects(b))


class ThemeAndLevelTests(unittest.TestCase):
    def test_theme_bands(self):
        self.assertEqual(themes.theme_for_depth(1).key, "cellars")
        self.assertEqual(themes.theme_for_depth(5).key, "fungal")
        self.assertEqual(themes.theme_for_depth(8).key, "magma")
        self.assertEqual(themes.theme_for_depth(12).key, "heart")

    def test_theme_colors(self):
        t = themes.theme_for_depth(8)
        self.assertEqual(t.tile_colors("wall", ("x", "y"))[0], "red")
        self.assertEqual(t.tile_colors("lava", ("a", "b")), ("a", "b"))

    def test_every_theme_level_is_connected(self):
        for theme in themes.THEMES:
            for seed in range(6):
                lay = levelgen.generate_level(70, 24, random.Random(seed), theme)
                reach = connected(lay.gmap, lay.start)
                self.assertIn(lay.gmap.stairs, reach, (theme.key, seed))
                opens = set(levelgen.open_cells(lay.gmap))
                self.assertTrue(opens <= reach, (theme.key, seed))
                self.assertIn(lay.start, lay.areas[0])

    def test_decorations_appear(self):
        names = {th.key: set() for th in themes.THEMES}
        for th in themes.THEMES:
            for seed in range(4):
                lay = levelgen.generate_level(70, 24, random.Random(seed), th)
                names[th.key] |= {t.name for row in lay.gmap.tiles for t in row}
        self.assertIn("fungus", names["fungal"])
        self.assertIn("lava", names["magma"])
        self.assertIn("rubble", names["cellars"])

    def test_deep_game_uses_themes(self):
        g = Game(seed=11)
        for _ in range(6):
            g.player.x, g.player.y = g.gmap.stairs
            g.descend()
        self.assertEqual(g.theme.key, "magma")
        self.assertIn(g.theme.intro, " ".join(m.text for m in g.log.entries()))

    def test_theme_bias_affects_monsters(self):
        g = Game(seed=2)
        g.depth = 5
        g.theme = themes.theme_for_depth(5)
        rolls = [g.pick_monster() for _ in range(400)]
        self.assertGreater(rolls.count("myconid"), 20)


class TrapTests(unittest.TestCase):
    def setUp(self):
        self.g = arena(w=24)
        self.g.depth = 3

    def put(self, kind, dx=1):
        p = self.g.player
        t = traps.Trap(kind, p.x + dx, p.y)
        self.g.traps[t.pos] = t
        return t

    def test_hidden_trap_triggers(self):
        t = self.put("dart")
        self.g.player_move(1, 0)
        self.assertFalse(t.hidden)
        self.assertTrue(self.g.player.statuses.has("poisoned"))

    def test_known_trap_needs_confirmation(self):
        t = self.put("fire")
        t.hidden = False
        start = self.g.player.pos
        self.assertFalse(self.g.player_move(1, 0))
        self.assertEqual(self.g.player.pos, start)
        self.assertTrue(self.g.player_move(1, 0))
        self.assertTrue(self.g.player.statuses.has("burning"))

    def test_net_alarm_teleport(self):
        self.put("net")
        self.g.player_move(1, 0)
        self.assertTrue(self.g.player.statuses.has("slowed"))
        g = arena(w=40, h=20)
        g.depth = 3
        m = make_monster("rat", 2, 2)
        m.asleep = True
        g.entities.append(m)
        g.traps[(g.player.x + 1, g.player.y)] = traps.Trap("alarm", g.player.x + 1, g.player.y)
        g.player_move(1, 0)
        self.assertFalse(m.asleep)
        g2 = arena(w=40, h=20)
        start = (g2.player.x + 1, g2.player.y)
        g2.traps[start] = traps.Trap("teleport", *start)
        g2.player_move(1, 0)
        self.assertNotEqual(g2.player.pos, start)

    def test_search_finds_traps(self):
        t = self.put("dart", dx=2)
        for _ in range(20):
            self.g.search()
        self.assertFalse(t.hidden)
        self.assertIn("^", render(self.g))
        self.assertIn("poison dart trap", " ".join(describe_cell(self.g, *t.pos)))

    def test_roll_kind_respects_depth(self):
        kinds = {traps.roll_kind(1, random.Random(s)) for s in range(200)}
        self.assertNotIn("teleport", kinds)

    def test_place_avoids_player_and_stairs(self):
        cells = [(x, y) for x in range(1, 23) for y in range(1, 11)]
        placed = traps.place(self.g, cells, 30)
        for t in placed:
            self.assertGreater(max(abs(t.x - self.g.player.x), abs(t.y - self.g.player.y)), 2)


class VaultTests(unittest.TestCase):
    def make(self):
        g = arena(w=30, h=14)
        g.depth = 3
        room = Rect(15, 2, 10, 8)
        return g, room

    def test_treasury_has_loot_and_guards(self):
        g, room = self.make()
        vaults.build(g, "treasury", room)
        items = [e for e in g.entities if e.item and room.contains(e.x, e.y)]
        guards = [m for m in g.monsters if room.contains(m.x, m.y)]
        self.assertGreaterEqual(len(items), 3)
        self.assertTrue(guards and all(m.asleep for m in guards))

    def test_shrine_prayer_once(self):
        g, room = self.make()
        vaults.build(g, "shrine", room)
        g.player.x, g.player.y = room.center
        g.player.fighter.hp = 5
        stats = (g.player.fighter.power, g.player.fighter.defense, g.player.fighter.base_max_hp)
        self.assertTrue(g.pray())
        f = g.player.fighter
        self.assertEqual(f.hp, f.max_hp)
        self.assertNotEqual((f.power, f.defense, f.base_max_hp), stats)
        self.assertFalse(g.pray())
        g.player.x += 1
        self.assertFalse(g.pray())

    def test_trap_room_and_library(self):
        g, room = self.make()
        vaults.build(g, "trap room", room)
        self.assertGreaterEqual(len(g.traps), 3)
        g2, room2 = self.make()
        vaults.build(g2, "library", room2)
        self.assertTrue(all(e.item.kind == "scroll" for e in g2.entities if e.item))

    def test_entering_announces_once(self):
        g, room = self.make()
        vaults.build(g, "library", room)
        g.player.x, g.player.y = room.x + 1, room.y + 2
        self.assertIsNotNone(vaults.check_enter(g))
        self.assertIsNone(vaults.check_enter(g))

    def test_levels_get_special_rooms(self):
        kinds = set()
        for s in range(40):
            kinds |= {sr.kind for sr in Game(seed=s).special_rooms}
        self.assertTrue({"shrine", "library"} <= kinds)


class StealthTests(unittest.TestCase):
    def test_sleeping_monster_stays_put_when_quiet(self):
        g = arena(w=40, h=20)
        m = make_monster("cave troll", 34, 3)
        m.asleep = True
        g.entities.append(m)
        g.rng.seed(1)
        start = m.pos
        for _ in range(3):
            g.player_wait()
        self.assertTrue(m.asleep and m.pos == start or not m.asleep)

    def test_noise_wakes(self):
        g = arena(w=20)
        m = make_monster("rat", g.player.x + 3, g.player.y)
        m.asleep = True
        g.entities.append(m)
        g.noise = 8
        self.assertGreaterEqual(ai.wake_chance(g, m), 0.9)
        g.noise = 0
        self.assertLess(ai.wake_chance(g, m), 0.2)

    def test_sneak_attack_bonus_and_wakes(self):
        g = arena()
        m = make_monster("cave troll", g.player.x + 1, g.player.y)
        m.asleep = True
        g.entities.append(m)
        g.player_move(1, 0)
        self.assertFalse(m.asleep)
        # power 5 + bonus 5 + roll(-1..2) - defense 2 >= 7
        self.assertLessEqual(m.fighter.hp, 22 - 7)

    def test_spawns_include_sleepers(self):
        sleepers = sum(m.asleep for s in range(10) for m in Game(seed=s).monsters)
        self.assertGreater(sleepers, 3)

    def test_look_says_asleep(self):
        g = arena()
        m = make_monster("rat", g.player.x + 2, g.player.y)
        m.asleep = True
        g.entities.append(m)
        g.update_fov()
        self.assertIn("asleep", " ".join(describe_cell(g, *m.pos)))


class UITests(unittest.TestCase):
    def test_level_up_popup(self):
        g = arena()
        g.progression.gain(40)
        scr = FakeScreen(["g", "Q"])
        CursesUI(scr, g).run()
        self.assertEqual(g.player.fighter.defense, 2)
        self.assertEqual(g.pending_levels, 0)

    def test_search_and_pray_keys(self):
        g = arena()
        turn = g.turn
        CursesUI(FakeScreen(["S", "p", "Q"]), g).run()
        self.assertEqual(g.turn, turn + 1)  # search spends a turn, failed prayer does not

    def test_sidebar_shows_resources(self):
        g = arena()
        g.progression.gain(40)
        text = "\n".join(t for t, _ in sidebar(g))
        self.assertIn("Torch", text)
        self.assertIn("Food", text)
        self.assertIn("Level 2", text)
        self.assertIn("level-up", text)
        self.assertTrue(all(len(t) <= 22 for t, _ in sidebar(g)))

    def test_themed_frames_render(self):
        g = Game(seed=5)
        for _ in range(9):
            g.player.x, g.player.y = g.gmap.stairs
            g.descend()
            scr = FakeScreen([])
            CursesUI(scr, g).draw()
            self.assertIn("@", scr.text())

    def test_text_mode_commands(self):
        g = arena()
        g.progression.gain(40)
        run_text_command(g, "+m")
        self.assertEqual(g.player.fighter.power, 6)
        turn = g.turn
        run_text_command(g, "f")
        self.assertEqual(g.turn, turn + 1)
        self.assertIn("Torch", render(g))


if __name__ == "__main__":
    unittest.main()
