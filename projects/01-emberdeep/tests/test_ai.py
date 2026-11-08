"""Tests for pathfinding, status effects, the energy system, monster AI and look mode."""
import random
import unittest

from emberdeep import ai
from emberdeep.entities import MONSTER_TEMPLATES, make_monster
from emberdeep.gamemap import GameMap
from emberdeep.geometry import chebyshev
from emberdeep.look import describe_cell
from emberdeep.messages import a_an
from emberdeep.pathfinding import astar, dijkstra_map, downhill_step, flee_map, heuristic
from emberdeep.status import StatusSet
from emberdeep.tiles import FLOOR, WALL
from emberdeep.ui_curses import CursesUI

from tests.helpers import FakeScreen, arena


def open_map(w: int, h: int, walls: set[tuple[int, int]] = frozenset()) -> GameMap:
    gm = GameMap(w, h)
    for y in range(h):
        for x in range(w):
            border = x in (0, w - 1) or y in (0, h - 1)
            gm.set(x, y, WALL if border or (x, y) in walls else FLOOR)
    return gm


def add(g, kind, dx, dy):
    m = make_monster(kind, g.player.x + dx, g.player.y + dy)
    g.entities.append(m)
    g.update_fov()
    return m


class PathfindingTests(unittest.TestCase):
    def test_straight_path(self):
        gm = open_map(12, 5)
        path = astar(gm, (1, 2), (8, 2))
        self.assertEqual(len(path), 7)
        self.assertEqual(path[-1], (8, 2))
        self.assertTrue(all(y == 2 for _, y in path))

    def test_routes_around_wall(self):
        wall = {(5, y) for y in range(1, 8)}  # gap at y=8
        gm = open_map(11, 10, wall)
        path = astar(gm, (2, 2), (8, 2))
        self.assertTrue(path)
        self.assertNotIn((5, 2), path)
        self.assertIn((5, 8), path)
        for a, b in zip([(2, 2)] + path, path):
            self.assertEqual(chebyshev(a, b), 1)
            self.assertTrue(gm.walkable(*b))

    def test_no_path(self):
        wall = {(5, y) for y in range(1, 9)}
        gm = open_map(11, 10, wall)
        self.assertEqual(astar(gm, (2, 2), (8, 2)), [])
        self.assertEqual(astar(gm, (2, 2), (2, 2)), [])

    def test_extra_cost_detours(self):
        gm = open_map(12, 7)
        blocked = {(5, 3)}
        path = astar(gm, (2, 3), (8, 3), extra_cost=lambda x, y: 100 if (x, y) in blocked else 0)
        self.assertNotIn((5, 3), path)
        self.assertEqual(len(path), 6)  # a diagonal sidestep costs no extra moves

    def test_heuristic_admissible(self):
        gm = open_map(15, 15)
        dist = dijkstra_map(gm, [(7, 7)])
        for pos, d in dist.items():
            self.assertLessEqual(heuristic(pos, (7, 7)), d)

    def test_dijkstra_and_flee(self):
        gm = open_map(20, 7)
        dist = dijkstra_map(gm, [(1, 3)])
        self.assertEqual(dist[(1, 3)], 0)
        self.assertEqual(dist[(4, 3)], 30)
        field = flee_map(gm, (5, 3))
        step = downhill_step(gm, (7, 3), field)
        self.assertIsNotNone(step)
        self.assertEqual(step[0], 1)  # moves away (to the right)
        self.assertIsNone(downhill_step(gm, (50, 50), field))


class StatusTests(unittest.TestCase):
    def test_add_refresh_tick_expire(self):
        s = StatusSet()
        self.assertTrue(s.add("burning", 2, 3))
        self.assertFalse(s.add("burning", 1, 1))  # keeps longer/stronger
        self.assertEqual(s.turns("burning"), 2)
        r = s.tick()
        self.assertEqual(r.total_damage, 3)
        r = s.tick()
        self.assertEqual(r.expired, ["burning"])
        self.assertFalse(s.has("burning"))
        with self.assertRaises(KeyError):
            s.add("petrified", 3)

    def test_haste_and_slow_cancel(self):
        s = StatusSet()
        s.add("hasted", 5)
        self.assertEqual(s.speed_multiplier(), 2.0)
        s.add("slowed", 5)
        self.assertEqual(len(s), 0)
        s.add("slowed", 5)
        self.assertEqual(s.speed_multiplier(), 0.5)
        self.assertEqual(s.labels(), [("Slow", "cyan")])

    def test_confused_property_backed_by_status(self):
        m = make_monster("rat", 1, 1)
        m.confused = 4
        self.assertTrue(m.statuses.has("confused"))
        m.confused = 0
        self.assertFalse("confused" in m.statuses)

    def test_burning_kills_monster_and_counts(self):
        g = arena()
        rat = add(g, "rat", 5, 0)
        g.apply_status(rat, "burning", 5, 10)
        g.player_wait()
        self.assertFalse(rat.fighter.alive)
        self.assertEqual(g.kills, 1)

    def test_player_poison_ticks_and_potion_cures(self):
        g = arena()
        g.apply_status(g.player, "poisoned", 4, 1)
        hp = g.player.fighter.hp
        g.player_wait()
        self.assertEqual(g.player.fighter.hp, hp - 1)
        self.assertTrue(g.use(g.give("healing potion")))
        self.assertFalse(g.player.statuses.has("poisoned"))

    def test_status_death_sets_cause(self):
        g = arena()
        g.player.fighter.hp = 1
        g.apply_status(g.player, "burning", 3, 5)
        g.player_wait()
        self.assertTrue(g.game_over)
        self.assertEqual(g.death_cause, "burned to death")

    def test_speed_potion(self):
        g = arena()
        self.assertTrue(g.use(g.give("speed potion")))
        self.assertTrue(g.player.statuses.has("hasted"))
        self.assertEqual(g.player.effective_speed, 200)


class EnergyTests(unittest.TestCase):
    def count_actions(self, g, m, player_turns):
        acted = []
        orig = ai.take_turn

        def spy(game, mon):
            if mon is m:
                acted.append(1)
            orig(game, mon)

        ai.take_turn = spy
        try:
            for _ in range(player_turns):
                g.player_wait()
        finally:
            ai.take_turn = orig
        return len(acted)

    def test_fast_and_slow_monsters(self):
        g = arena(w=40)
        jackal = add(g, "jackal", 8, 0)   # speed 150
        self.assertEqual(self.count_actions(g, jackal, 10), 15)
        g = arena(w=40)
        beetle = add(g, "fire beetle", 8, 0)  # speed 70
        self.assertEqual(self.count_actions(g, beetle, 10), 7)

    def test_hasted_player_gets_double_turns(self):
        g = arena(w=40)
        troll = add(g, "cave troll", 9, 0)
        g.player.statuses.add("hasted", 50)
        self.assertEqual(self.count_actions(g, troll, 10), 5)

    def test_slowed_player_monsters_act_twice(self):
        g = arena(w=40)
        rat = add(g, "rat", 9, 0)
        g.player.statuses.add("slowed", 50)
        self.assertEqual(self.count_actions(g, rat, 4), 8)


class AITests(unittest.TestCase):
    def test_chaser_closes_in_and_attacks(self):
        g = arena(w=30)
        troll = add(g, "cave troll", 6, 0)
        for _ in range(6):
            g.player_wait()
        self.assertLessEqual(chebyshev(troll.pos, g.player.pos), 1)
        self.assertLess(g.player.fighter.hp, g.player.fighter.max_hp)

    def test_memory_leads_monster_to_last_seen_spot(self):
        g = arena(w=30)
        troll = add(g, "cave troll", 6, 0)
        g.player_wait()
        self.assertEqual(troll.memory, g.player.pos)
        # player vanishes from the troll's sight: it walks to the remembered spot
        last = g.player.pos
        g.player.x, g.player.y = 1, 1
        g.gmap.visible = [[False] * g.gmap.width for _ in range(g.gmap.height)]
        for _ in range(10):
            ai.take_turn(g, troll)
            if troll.memory is None:
                break
        self.assertIsNone(troll.memory)
        self.assertLessEqual(chebyshev(troll.pos, last), 1)

    def test_dormant_without_memory(self):
        g = arena(w=30)
        rat = add(g, "rat", 6, 0)
        g.gmap.visible = [[False] * g.gmap.width for _ in range(g.gmap.height)]
        start = rat.pos
        ai.take_turn(g, rat)
        self.assertEqual(rat.pos, start)

    def test_coward_flees_when_hurt(self):
        g = arena(w=40, h=12)
        g.player.x, g.player.y = 10, 6
        kobold = add(g, "kobold", 2, 0)
        kobold.fighter.hp = 2
        d0 = chebyshev(kobold.pos, g.player.pos)
        ai.take_turn(g, kobold)
        self.assertTrue(kobold.ai_state.get("fleeing"))
        self.assertGreater(chebyshev(kobold.pos, g.player.pos), d0)
        self.assertTrue(any("flee" in m.text for m in g.log.entries()))

    def test_caster_casts_with_cooldown(self):
        g = arena(w=30)
        g.rng = random.Random(0)
        imp = add(g, "ember imp", 4, 0)
        hp = g.player.fighter.hp
        ai.take_turn(g, imp)
        self.assertLess(g.player.fighter.hp, hp)
        self.assertEqual(imp.ai_state["cooldown"], ai.SPELLS["ember bolt"]["cooldown"])
        hp = g.player.fighter.hp
        ai.take_turn(g, imp)  # on cooldown: no second bolt
        self.assertEqual(g.player.fighter.hp, hp)

    def test_caster_needs_clear_shot(self):
        g = arena(w=30)
        add(g, "cave troll", 2, 0)
        imp = add(g, "ember imp", 4, 0)
        self.assertFalse(ai.clear_shot(g, imp, g.player.pos))

    def test_shaman_slows_player(self):
        g = arena(w=30)
        shaman = add(g, "kobold shaman", 5, 0)
        ai.take_turn(g, shaman)
        self.assertTrue(g.player.statuses.has("slowed"))

    def test_on_hit_status(self):
        g = arena()
        spider = add(g, "cave spider", 1, 0)
        spider.on_hit = ("poisoned", 5, 1, 1.0)
        spider.fighter.base_power = 20
        g.player.fighter.base_max_hp = g.player.fighter.hp = 100
        g.monster_attack(spider, g.player)
        self.assertTrue(g.player.statuses.has("poisoned"))

    def test_pack_lurks_until_gathered_then_rushes(self):
        g = arena(w=40, h=14)
        g.player.x, g.player.y = 20, 7
        a = add(g, "jackal", 3, 0)
        b = add(g, "jackal", 9, 3)  # near a, but too far from the player to count
        g.gmap.visible[b.y][b.x] = True
        ai.take_turn(g, a)
        self.assertEqual(b.memory, g.player.pos)  # howl alerted the pack
        self.assertFalse(a.ai_state.get("rushing"))
        self.assertGreaterEqual(chebyshev(a.pos, g.player.pos), 3)
        b.x, b.y = g.player.x - 3, g.player.y
        ai.take_turn(g, a)
        self.assertTrue(a.ai_state.get("rushing"))

    def test_lone_pack_animal_attacks(self):
        g = arena()
        j = add(g, "jackal", 1, 0)
        hp = g.player.fighter.hp
        g.player.fighter.base_defense = -10
        ai.take_turn(g, j)
        self.assertLess(g.player.fighter.hp, hp)

    def test_confused_monster_wanders(self):
        g = arena(w=30)
        troll = add(g, "cave troll", 6, 0)
        troll.confused = 3
        g.rng = random.Random(4)
        start = troll.pos
        ai.take_turn(g, troll)
        self.assertNotEqual(troll.pos, start)  # stumbled somewhere (not straight at us)

    def test_every_template_spawns_and_acts(self):
        for kind in MONSTER_TEMPLATES:
            g = arena(w=30)
            m = add(g, kind, 5, 0)
            for _ in range(5):
                g.player_wait()
            self.assertTrue(m.ai is None or m.ai in ai.BEHAVIOURS, kind)

    def test_packs_spawn_together(self):
        from emberdeep.game import Game
        found = False
        for seed in range(30):
            g = Game(seed)
            for _ in range(2):
                g.new_level()
            if sum(1 for m in g.monsters if m.name == "jackal") >= 2:
                found = True
                break
        self.assertTrue(found)


class LookTests(unittest.TestCase):
    def test_describe_monster_item_and_tile(self):
        g = arena()
        x, y = g.player.pos
        m = add(g, "fire beetle", 2, 0)
        m.statuses.add("burning", 3, 1)
        text = " ".join(describe_cell(g, *m.pos))
        self.assertIn("A fire beetle (unhurt, slow, on fire)", text)
        self.assertIn("A floor", text)
        from emberdeep.items import make_item
        g.identify_kind("speed potion")
        g.place_item(make_item("speed potion"), x + 1, y + 1)
        self.assertIn("potion of speed (haste for 15 turns)", describe_cell(g, x + 1, y + 1))
        self.assertEqual(describe_cell(g, 0, 0)[0][:3], "You")

    def test_unknown_and_remembered(self):
        g = arena()
        g.gmap.explored[1][1] = False
        g.gmap.visible[1][1] = False
        self.assertEqual(describe_cell(g, 1, 1), ["You don't know what is there."])
        g.gmap.explored[1][1] = True
        self.assertEqual(describe_cell(g, 1, 1), ["You remember a floor here."])

    def test_look_mode_in_ui(self):
        g = arena()
        add(g, "kobold", 3, 0)
        scr = FakeScreen(["x", 9, 27, "Q"], rows=24, cols=80)  # look, Tab to kobold, Esc
        ui = CursesUI(scr, g)
        ui.handle(ord("x"))
        self.assertTrue(ui.running)

    def test_a_an(self):
        self.assertEqual(a_an("ember imp"), "an ember imp")
        self.assertEqual(a_an("rat"), "a rat")


if __name__ == "__main__":
    unittest.main()
