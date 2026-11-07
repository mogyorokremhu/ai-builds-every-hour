"""Core tests for Emberdeep. Run from the project folder:  python -m unittest"""
import random
import unittest

from emberdeep import dungeon
from emberdeep.entities import Fighter
from emberdeep.fov import compute_fov
from emberdeep.game import Game
from emberdeep.geometry import Rect, bresenham, chebyshev
from emberdeep.messages import MessageLog
from emberdeep.render_ascii import render


class GeometryTests(unittest.TestCase):
    def test_rect_intersect(self):
        self.assertTrue(Rect(0, 0, 5, 5).intersects(Rect(4, 4, 3, 3)))
        self.assertFalse(Rect(0, 0, 5, 5).intersects(Rect(5, 5, 3, 3)))

    def test_bresenham_endpoints(self):
        line = bresenham(0, 0, 5, 3)
        self.assertEqual(line[0], (0, 0))
        self.assertEqual(line[-1], (5, 3))

    def test_chebyshev(self):
        self.assertEqual(chebyshev((0, 0), (3, -2)), 3)


class DungeonTests(unittest.TestCase):
    def test_deterministic(self):
        a, _ = dungeon.generate(60, 20, random.Random(7))
        b, _ = dungeon.generate(60, 20, random.Random(7))
        self.assertEqual([[t.glyph for t in r] for r in a.tiles], [[t.glyph for t in r] for r in b.tiles])

    def test_has_rooms_and_stairs(self):
        gmap, rooms = dungeon.generate(70, 24, random.Random(1))
        self.assertGreater(len(rooms), 3)
        self.assertIsNotNone(gmap.stairs)
        self.assertTrue(gmap.walkable(*rooms[0].center))

    def test_all_rooms_connected(self):
        gmap, rooms = dungeon.generate(70, 24, random.Random(3))
        start = rooms[0].center
        seen, stack = {start}, [start]
        while stack:
            x, y = stack.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n not in seen and gmap.walkable(*n):
                    seen.add(n)
                    stack.append(n)
        for r in rooms:
            self.assertIn(r.center, seen)


class FovTests(unittest.TestCase):
    def test_origin_visible_and_walls_block(self):
        gmap, rooms = dungeon.generate(70, 24, random.Random(2))
        cx, cy = rooms[0].center
        compute_fov(gmap, cx, cy, 8)
        self.assertTrue(gmap.visible[cy][cx])
        self.assertTrue(gmap.explored[cy][cx])
        # far corner of the map should not be visible
        self.assertFalse(gmap.visible[0][0] and gmap.visible[23][69])


class CombatAndGameTests(unittest.TestCase):
    def test_fighter_damage_clamped(self):
        f = Fighter(10, 10, 3, 0)
        self.assertEqual(f.take_damage(50), 10)
        self.assertFalse(f.alive)

    def test_game_runs_many_turns(self):
        g = Game(seed=42)
        rng = random.Random(0)
        for _ in range(400):
            if g.game_over:
                break
            g.player_move(rng.choice([-1, 0, 1]), rng.choice([-1, 0, 1]))
        self.assertGreater(g.turn, 0)

    def test_render_contains_player(self):
        g = Game(seed=5)
        self.assertIn("@", render(g))

    def test_message_stacking(self):
        log = MessageLog()
        for _ in range(3):
            log.add("The rat bites you.")
        self.assertEqual(log.last(1), ["The rat bites you. (x3)"])


if __name__ == "__main__":
    unittest.main()
