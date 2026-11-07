"""Phase 6 tests: the Ember Guardian, victory, scores, morgue files, daily seeds, doors."""
import datetime as dt
import random
import tempfile
import unittest
from pathlib import Path

from emberdeep import ai, boss, daily, morgue, scores
from emberdeep.__main__ import Options, end_session, parse_args, run_text_command, start_game
from emberdeep.entities import make_monster
from emberdeep.game import Game
from emberdeep.gen_bsp import generate as bsp_generate
from emberdeep.gen_caves import bfs_distances
from emberdeep.tiles import DOOR, OPEN_DOOR, WALL
from emberdeep.ui_curses import CursesUI

from tests.helpers import FakeScreen, arena


def to_boss_level(seed: int = 3) -> Game:
    g = Game(seed)
    while g.depth < boss.BOSS_DEPTH:
        g.new_level()
    return g


def the_boss(g: Game):
    return next(m for m in g.monsters if m.name == boss.BOSS_KIND)


class ArenaTests(unittest.TestCase):
    def test_arena_is_connected_and_stairless(self):
        for seed in range(8):
            layout, sanctum = boss.build_arena(70, 24, random.Random(seed))
            self.assertIsNone(layout.gmap.stairs)
            reach = bfs_distances(layout.gmap, layout.start)
            self.assertIn(sanctum, reach)
            self.assertTrue(any(t.name == "lava" for row in layout.gmap.tiles for t in row))
            self.assertTrue(layout.areas[0])

    def test_boss_level_spawns_guardian(self):
        g = to_boss_level()
        self.assertEqual(g.depth, 10)
        b = the_boss(g)
        self.assertIn("boss", b.tags)
        self.assertTrue(b.immune_to("burning"))
        self.assertFalse(g.descend())
        self.assertEqual(g.theme.key, "heart")

    def test_guardian_never_spawns_randomly(self):
        g = Game(1)
        g.depth = 50
        for _ in range(300):
            self.assertNotEqual(g.pick_monster(), boss.BOSS_KIND)


class GuardianTests(unittest.TestCase):
    def setUp(self):
        self.g = arena(seed=4, w=30, h=15)
        self.b = make_monster(boss.BOSS_KIND, self.g.player.x + 5, self.g.player.y)
        self.g.entities.append(self.b)
        self.g.update_fov()

    def test_wakes_when_it_sees_you(self):
        ai.take_turn(self.g, self.b)
        self.assertTrue(self.b.ai_state["awake"])
        self.assertIn("rises from the magma", self.g.log.last(1)[0])

    def test_casts_magma_burst_at_range(self):
        self.b.ai_state["awake"] = True
        hp = self.g.player.fighter.hp
        ai.take_turn(self.g, self.b)
        self.assertLess(self.g.player.fighter.hp, hp)
        self.assertGreater(self.b.ai_state["cooldown"], 0)

    def test_phase_two_summons_minions(self):
        self.b.ai_state["awake"] = True
        self.b.fighter.hp = self.b.fighter.max_hp // 2
        ai.take_turn(self.g, self.b)
        self.assertEqual(self.b.ai_state["phase"], 2)
        self.assertTrue(boss.minions(self.g))
        self.assertTrue(all(m.name in boss.MINION_KINDS for m in boss.minions(self.g)))

    def test_phase_three_enrages(self):
        self.b.ai_state.update(awake=True, summon=50)
        self.b.fighter.hp = 10
        power = self.b.fighter.power
        ai.take_turn(self.g, self.b)
        self.assertEqual(self.b.ai_state["phase"], 3)
        self.assertEqual(self.b.speed, boss.ENRAGE_SPEED)
        self.assertEqual(self.b.fighter.power, power + boss.ENRAGE_POWER)

    def test_fire_nova_hits_adjacent_player(self):
        self.b.x, self.b.y = self.g.player.x + 1, self.g.player.y
        self.b.ai_state.update(awake=True, phase=2, summon=50)
        self.b.fighter.hp = self.b.fighter.max_hp // 2
        hp = self.g.player.fighter.hp
        ai.take_turn(self.g, self.b)
        self.assertLess(self.g.player.fighter.hp, hp)
        self.assertTrue(self.g.player.statuses.has("burning"))

    def test_immune_to_confusion_and_fire(self):
        scroll = self.g.give("confusion scroll")
        self.assertTrue(self.g.use(scroll, self.b.pos))
        self.assertEqual(self.b.confused, 0)
        self.g.apply_status(self.b, "burning", 5, 3)
        self.assertFalse(self.b.statuses.has("burning"))

    def test_killing_guardian_drops_heart_and_wins(self):
        self.b.ai_state["awake"] = True
        boss.summon(self.g, self.b, 2)
        self.b.x, self.b.y = self.g.player.x + 1, self.g.player.y
        self.b.fighter.hp = 1
        self.g.player.fighter.base_power = 50
        self.g.player_move(1, 0)
        self.assertFalse(boss.minions(self.g))
        self.assertEqual(self.g.kill_counts.get(boss.BOSS_KIND), 1)
        heart = [e for e in self.g.items_at(*self.b.pos) if e.item.key == "ember heart"]
        self.assertEqual(len(heart), 1)
        self.g.player_move(1, 0)
        self.assertFalse(self.g.game_over)
        self.assertTrue(self.g.pickup())
        self.assertTrue(self.g.victory)
        self.assertTrue(self.g.game_over)
        self.assertFalse(self.g.dead)
        turn = self.g.turn
        self.assertFalse(self.g.player_move(1, 0))
        self.assertEqual(self.g.turn, turn)


class DoorTests(unittest.TestCase):
    def setUp(self):
        self.g = arena(seed=2)
        px, py = self.g.player.pos
        self.door = (px + 1, py)
        for y in range(1, self.g.gmap.height - 1):
            self.g.gmap.set(px + 1, y, WALL)
        self.g.gmap.set(*self.door, DOOR)
        self.g.update_fov()

    def test_closed_door_blocks_and_bump_opens(self):
        self.assertFalse(self.g.gmap.walkable(*self.door))
        self.assertTrue(self.g.gmap.passable(*self.door))
        self.assertFalse(self.g.gmap.visible[self.g.player.y][self.g.player.x + 3])
        pos = self.g.player.pos
        self.assertTrue(self.g.player_move(1, 0))
        self.assertEqual(self.g.player.pos, pos)  # opening took the turn
        self.assertEqual(self.g.gmap.get(*self.door).name, "open door")
        self.assertTrue(self.g.gmap.visible[self.g.player.y][self.g.player.x + 3])
        self.g.player_move(1, 0)
        self.assertEqual(self.g.player.pos, self.door)

    def test_close_door(self):
        self.g.gmap.set(*self.door, OPEN_DOOR)
        self.assertEqual(self.g.closable_doors(), [self.door])
        self.assertTrue(self.g.close_door())
        self.assertEqual(self.g.gmap.get(*self.door).name, "door")
        self.assertFalse(self.g.close_door())  # nothing left to close

    def test_cannot_close_on_a_monster(self):
        self.g.gmap.set(*self.door, OPEN_DOOR)
        self.g.entities.append(make_monster("rat", *self.door))
        self.assertFalse(self.g.close_door(1, 0))

    def test_monsters_open_doors(self):
        rat = make_monster("rat", self.door[0] + 2, self.door[1])
        rat.memory = self.g.player.pos
        self.g.entities.append(rat)
        for _ in range(3):
            ai.take_turn(self.g, rat)
        self.assertEqual(self.g.gmap.get(*self.door).name, "open door")

    def test_bsp_has_both_door_states_and_stays_connected(self):
        closed = opened = 0
        for seed in range(10):
            gmap, rooms = bsp_generate(70, 24, random.Random(seed))
            names = [t.name for row in gmap.tiles for t in row]
            closed += names.count("door")
            opened += names.count("open door")
            reach = bfs_distances(gmap, rooms[0].center)
            self.assertIn(gmap.stairs, reach)
        self.assertGreater(closed, 0)
        self.assertGreater(opened, 0)

    def test_ui_close_key(self):
        self.g.gmap.set(*self.door, OPEN_DOOR)
        CursesUI(FakeScreen(["c", "Q"]), self.g).run()
        self.assertEqual(self.g.gmap.get(*self.door).name, "door")

    def test_text_mode_close(self):
        self.g.gmap.set(*self.door, OPEN_DOOR)
        run_text_command(self.g, "k")
        self.assertEqual(self.g.gmap.get(*self.door).name, "door")


class DailyTests(unittest.TestCase):
    def test_seed_is_stable_and_date_dependent(self):
        d1, d2 = dt.date(2026, 11, 7), dt.date(2026, 11, 8)
        self.assertEqual(daily.daily_seed(d1), daily.daily_seed(d1))
        self.assertNotEqual(daily.daily_seed(d1), daily.daily_seed(d2))
        self.assertLess(daily.daily_seed(d1), 1 << 30)
        self.assertEqual(daily.mode_date(daily.daily_mode(d1)), "2026-11-07")
        self.assertIsNone(daily.mode_date("normal"))

    def test_same_day_same_dungeon(self):
        seed = daily.daily_seed(dt.date(2026, 1, 1))
        a, b = Game(seed, "daily:2026-01-01"), Game(seed, "daily:2026-01-01")
        self.assertEqual([[t.glyph for t in r] for r in a.gmap.tiles], [[t.glyph for t in r] for r in b.gmap.tiles])

    def test_cli_parsing(self):
        o = parse_args(["--daily=2026-02-03", "--text"])
        self.assertEqual(o.daily, "2026-02-03")
        self.assertTrue(o.text)
        self.assertEqual(parse_args(["42"]).seed, 42)
        with self.assertRaises(SystemExit):
            parse_args(["--bogus"])


class ScoreAndMorgueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def dead_game(self, seed=7, mode="normal") -> Game:
        g = Game(seed, mode)
        g.kill_counts = {"rat": 3, "kobold": 1}
        g.kills = 4
        g.player.fighter.hp = 0
        g.death_cause = "killed by a rat"
        return g

    def test_score_rewards_depth_and_victory(self):
        g = self.dead_game()
        base = scores.compute_score(g)
        g.max_depth = 5
        self.assertGreater(scores.compute_score(g), base)
        g.victory = True
        self.assertGreater(scores.compute_score(g), base + scores.VICTORY_BONUS)

    def test_table_sorted_and_capped(self):
        for i in range(scores.MAX_ENTRIES + 5):
            e = scores.ScoreEntry(i * 10, "died", 1, 1, 0, 0, 10, i)
            scores.add_score(self.home, e)
        table = scores.load_scores(self.home)
        self.assertEqual(len(table), scores.MAX_ENTRIES)
        self.assertEqual(table[0].score, (scores.MAX_ENTRIES + 4) * 10)
        self.assertEqual(scores.add_score(self.home, scores.ScoreEntry(0, "died", 1, 1, 0, 0, 1, 0)), 0)
        rows = scores.format_table(table, limit=3)
        self.assertEqual(len(rows), 4)

    def test_corrupt_scores_file(self):
        scores.scores_path(self.home).write_text("{not json")
        self.assertEqual(scores.load_scores(self.home), [])
        self.assertIn("No runs", scores.format_table([])[0])

    def test_repeat_daily_is_practice(self):
        mode = "daily:2026-11-07"
        e1 = scores.entry_for(self.dead_game(mode=mode))
        e2 = scores.entry_for(self.dead_game(mode=mode))
        scores.add_score(self.home, e1)
        scores.add_score(self.home, e2)
        self.assertTrue(e1.ranked)
        self.assertFalse(e2.ranked)
        self.assertIn("practice", "\n".join(scores.format_table(scores.load_scores(self.home))))

    def test_morgue_contents(self):
        g = self.dead_game()
        g.give("healing potion", 2)
        text = morgue.build_morgue(g)
        for needle in ("killed by a rat", "Kills (4)", "rat", "potions of healing", "Map", "@"):
            self.assertIn(needle, text)

    def test_finish_run_writes_files_and_deletes_save(self):
        from emberdeep import save

        alive = Game(9)
        save.save_game(alive, save.save_path(self.home))
        g = self.dead_game()
        summary = morgue.finish_run(g, self.home)
        self.assertTrue(summary.morgue.exists())
        self.assertEqual(summary.rank, 1)
        self.assertFalse(save.has_save(save.save_path(self.home)))
        self.assertIn("Hall of fame:  #1", "\n".join(summary.lines()))
        # a second identical-second run gets a distinct morgue filename
        self.assertNotEqual(morgue.finish_run(self.dead_game(), self.home).morgue, summary.morgue)

    def test_session_flow_save_then_resume(self):
        from emberdeep import save

        g = start_game(Options(seed=11), self.home)
        g.player_wait()
        report = end_session(g, self.home, recorded=False)
        self.assertIn("saved", report[0])
        resumed = start_game(Options(), self.home)
        self.assertEqual(resumed.seed, 11)
        self.assertEqual(resumed.turn, 1)
        self.assertFalse(save.has_save(save.save_path(self.home)))  # consumed on load
        end_session(resumed, self.home, recorded=False)
        fresh = start_game(Options(new=True), self.home)
        self.assertEqual(fresh.turn, 0)
        self.assertTrue(save.has_save(save.save_path(self.home)))  # --new leaves the save alone

    def test_session_records_death_once(self):
        g = self.dead_game()
        self.assertTrue(end_session(g, self.home, recorded=False))
        self.assertEqual(end_session(g, self.home, recorded=True), [])
        self.assertEqual(len(scores.load_scores(self.home)), 1)

    def test_daily_start(self):
        g = start_game(Options(daily="2026-03-04"), self.home)
        self.assertEqual(g.mode, "daily:2026-03-04")
        self.assertEqual(g.seed, daily.daily_seed(dt.date(2026, 3, 4)))

    def test_ui_end_screens_and_scores_screen(self):
        g = self.dead_game()
        scr = FakeScreen([ord("x")])
        CursesUI(scr, g, on_finish=lambda game: ["Score:         123"]).run()
        self.assertIn("Score:         123", scr.text())
        w = arena()
        w.victory = True
        scr = FakeScreen([ord("x")])
        CursesUI(scr, w).run()
        self.assertIn("VICTORY", scr.text())
        scores.add_score(self.home, scores.entry_for(self.dead_game()))
        scr = FakeScreen(["H", "Q"])
        ui = CursesUI(scr, arena(), home=self.home)
        ui.handle(ord("H"))
        self.assertIn("hall of fame", scr.text())


if __name__ == "__main__":
    unittest.main()
