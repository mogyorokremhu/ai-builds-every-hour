"""Save/load: JSON round trips, deterministic continuation, permadeath and corruption."""
import json
import random
import tempfile
import unittest
from pathlib import Path

from emberdeep import boss, save
from emberdeep.game import Game

ACTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def play_randomly(g: Game, steps: int, rng: random.Random) -> None:
    for _ in range(steps):
        if g.game_over:
            return
        if g.pending_levels:
            g.choose_level_up(rng.choice("vmg"))
        r = rng.random()
        if r < 0.05:
            g.pickup()
        elif r < 0.08:
            g.player_wait()
        elif r < 0.1 and len(g.player.inventory):
            g.use(g.player.inventory.items[0], g.player.pos)
        elif g.player.pos == g.gmap.stairs:
            g.descend()
        else:
            g.player_move(*rng.choice(ACTIONS))


def fingerprint(g: Game) -> dict:
    """Everything observable about a game, for comparing two runs."""
    d = save.to_dict(g)
    d.pop("rng")
    return d


class RoundTripTests(unittest.TestCase):
    def test_round_trip_is_lossless(self):
        g = Game(21)
        play_randomly(g, 150, random.Random(1))
        if g.game_over:
            self.skipTest("bot died too early")
        data = save.to_dict(g)
        clone = save.from_dict(json.loads(json.dumps(data)))
        self.assertEqual(save.to_dict(clone), data)
        self.assertEqual(clone.player.pos, g.player.pos)
        self.assertEqual(clone.theme.key, g.theme.key)

    def test_loaded_game_continues_identically(self):
        for seed in (3, 8, 13):
            g = Game(seed)
            g.give("healing potion", 2)
            g.give("sword")
            g.toggle_equip(next(i for i in g.player.inventory if i.key == "sword"))
            play_randomly(g, 60, random.Random(seed))
            if g.game_over:
                continue
            clone = save.from_dict(json.loads(json.dumps(save.to_dict(g))))
            play_randomly(g, 120, random.Random(99))
            play_randomly(clone, 120, random.Random(99))
            self.assertEqual(fingerprint(clone), fingerprint(g), f"seed {seed} diverged")

    def test_equipment_and_stacks_survive(self):
        g = Game(5)
        g.give("healing potion", 3)
        ring = g.give("ring of vitality")
        g.toggle_equip(ring)
        clone = save.from_dict(save.to_dict(g))
        inv = clone.player.inventory
        potions = next(i for i in inv if i.key == "healing potion")
        self.assertEqual(potions.count, 3)
        worn = clone.player.equipment.slots["ring"]
        self.assertIsNotNone(worn)
        self.assertTrue(any(i is worn for i in inv.items))
        self.assertEqual(clone.player.fighter.max_hp, g.player.fighter.max_hp)

    def test_statuses_traps_altars_and_boss_state_survive(self):
        g = Game(6)
        while g.depth < boss.BOSS_DEPTH:
            g.new_level()
        g.player.statuses.add("burning", 4, 2)
        b = next(m for m in g.monsters if m.name == boss.BOSS_KIND)
        b.ai_state.update(awake=True, phase=2)
        g.altars[(1, 1)] = True
        clone = save.from_dict(json.loads(json.dumps(save.to_dict(g))))
        self.assertEqual(clone.player.statuses.turns("burning"), 4)
        cb = next(m for m in clone.monsters if m.name == boss.BOSS_KIND)
        self.assertEqual(cb.ai_state["phase"], 2)
        self.assertTrue(cb.immune_to("burning"))
        self.assertIsNone(clone.gmap.stairs)
        self.assertEqual(clone.altars, {(1, 1): True})

    def test_messages_survive(self):
        g = Game(2)
        g.say("hello", "bright_red")
        g.say("hello", "bright_red")
        clone = save.from_dict(save.to_dict(g))
        last = clone.log.entries(1)[0]
        self.assertEqual((last.text, last.count, last.color), ("hello", 2, "bright_red"))


class FileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "save.json"

    def tearDown(self):
        self.tmp.cleanup()

    def test_save_load_consumes_file(self):
        g = Game(4)
        g.player_wait()
        save.save_game(g, self.path)
        self.assertTrue(save.has_save(self.path))
        loaded = save.load_game(self.path)
        self.assertFalse(save.has_save(self.path))
        self.assertEqual(loaded.turn, 1)
        self.assertIn("Welcome back", loaded.log.last(1)[0])

    def test_keep_file_when_not_consuming(self):
        save.save_game(Game(4), self.path)
        save.load_game(self.path, consume=False)
        self.assertTrue(save.has_save(self.path))

    def test_finished_runs_cannot_be_saved(self):
        g = Game(4)
        g.player.fighter.hp = 0
        with self.assertRaises(save.SaveError):
            save.save_game(g, self.path)

    def test_missing_and_corrupt(self):
        with self.assertRaises(save.SaveError):
            save.load_game(self.path)
        self.path.write_text("{oops")
        with self.assertRaises(save.SaveError):
            save.load_game(self.path)
        self.path.write_text(json.dumps({"version": 999}))
        with self.assertRaises(save.SaveError):
            save.load_game(self.path)
        data = save.to_dict(Game(1))
        del data["map"]
        self.path.write_text(json.dumps(data))
        with self.assertRaises(save.SaveError):
            save.load_game(self.path)

    def test_delete_save(self):
        self.assertFalse(save.delete_save(self.path))
        save.save_game(Game(1), self.path)
        self.assertTrue(save.delete_save(self.path))

    def test_data_dir_env(self):
        import os

        old = os.environ.get("EMBERDEEP_HOME")
        os.environ["EMBERDEEP_HOME"] = str(Path(self.tmp.name) / "home")
        try:
            self.assertTrue(save.data_dir().is_dir())
            self.assertEqual(save.save_path().parent, Path(self.tmp.name) / "home")
        finally:
            if old is None:
                del os.environ["EMBERDEEP_HOME"]
            else:
                os.environ["EMBERDEEP_HOME"] = old


if __name__ == "__main__":
    unittest.main()
