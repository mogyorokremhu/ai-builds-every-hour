"""Tests for items, inventory, equipment, loot and targeting."""
import random
import unittest

from emberdeep import loot
from emberdeep.entities import make_monster
from emberdeep.equipment import Equipment
from emberdeep.inventory import Inventory
from emberdeep.items import ITEM_TEMPLATES, make_item, plural
from emberdeep.targeting import Cursor, blast_area, projectile_path
from emberdeep.tiles import WALL

from tests.helpers import arena


class InventoryTests(unittest.TestCase):
    def test_stacking_and_letters(self):
        inv = Inventory()
        inv.add(make_item("healing potion"))
        inv.add(make_item("dagger"))
        inv.add(make_item("healing potion"))
        self.assertEqual(len(inv), 2)
        self.assertEqual(inv.get("a").count, 2)
        self.assertEqual(inv.get("b").key, "dagger")
        self.assertIsNone(inv.get("z"))

    def test_identical_equipment_does_not_stack(self):
        inv = Inventory()
        d1, d2 = make_item("dagger"), make_item("dagger")
        inv.add(d1)
        inv.add(d2)
        self.assertEqual(len(inv), 2)
        self.assertEqual(inv.letter_of(d2), "b")
        inv.remove(d2)
        self.assertIs(inv.get("a"), d1)

    def test_capacity(self):
        inv = Inventory(capacity=2)
        self.assertTrue(inv.add(make_item("dagger")))
        self.assertTrue(inv.add(make_item("sword")))
        self.assertFalse(inv.add(make_item("war axe")))
        self.assertTrue(inv.can_add(make_item("dagger")) is False)

    def test_take_one_splits_stack(self):
        inv = Inventory()
        inv.add(make_item("healing potion", 3))
        stack = inv.get("a")
        one = inv.take_one(stack)
        self.assertEqual(one.count, 1)
        self.assertEqual(stack.count, 2)

    def test_plural(self):
        self.assertEqual(plural("potion of healing"), "potions of healing")
        self.assertEqual(plural("dagger"), "daggers")
        self.assertEqual(make_item("lightning scroll", 3).display_name, "3 scrolls of lightning")


class EquipmentTests(unittest.TestCase):
    def test_bonuses_apply_and_clamp(self):
        g = arena()
        f = g.player.fighter
        ring = g.give("ring of vitality")
        g.toggle_equip(ring)
        self.assertEqual(f.max_hp, 40)
        f.hp = 40
        g.toggle_equip(ring)
        self.assertEqual(f.max_hp, 30)
        self.assertEqual(f.hp, 30)

    def test_swap_weapon(self):
        g = arena()
        base = g.player.fighter.power
        dagger, sword = g.give("dagger"), g.give("sword")
        g.toggle_equip(dagger)
        self.assertEqual(g.player.fighter.power, base + 1)
        g.toggle_equip(sword)
        self.assertEqual(g.player.fighter.power, base + 3)
        self.assertFalse(g.player.equipment.is_equipped(dagger))

    def test_equip_rejects_non_equipment(self):
        with self.assertRaises(ValueError):
            Equipment().equip(make_item("healing potion"))

    def test_drop_unequips(self):
        g = arena()
        armor = g.give("chain mail")
        g.toggle_equip(armor)
        self.assertEqual(g.player.fighter.defense, 3)
        g.drop(armor)
        self.assertEqual(g.player.fighter.defense, 1)
        self.assertEqual(len(g.items_at(*g.player.pos)), 1)


class PickupTests(unittest.TestCase):
    def test_pickup_and_drop_roundtrip(self):
        g = arena()
        g.place_item(make_item("healing potion"), *g.player.pos)
        self.assertTrue(g.pickup())
        self.assertEqual(g.items_at(*g.player.pos), [])
        self.assertEqual(g.player.inventory.get("a").key, "healing potion")
        self.assertFalse(g.pickup())

    def test_walking_onto_item_reports_it(self):
        g = arena()
        x, y = g.player.pos
        g.place_item(make_item("sword"), x + 1, y)
        g.player_move(1, 0)
        self.assertIn("sword", g.log.last(1)[0])


class EffectTests(unittest.TestCase):
    def test_heal_consumes_only_when_hurt(self):
        g = arena()
        pot = g.give("healing potion", 2)
        self.assertFalse(g.use(pot))
        g.player.fighter.hp = 10
        self.assertTrue(g.use(pot))
        self.assertEqual(g.player.fighter.hp, 22)
        self.assertEqual(pot.count, 1)

    def test_lightning_hits_nearest(self):
        g = arena()
        x, y = g.player.pos
        near = make_monster("cave troll", x + 2, y)
        far = make_monster("cave troll", x + 5, y)
        g.entities += [near, far]
        g.update_fov()
        self.assertTrue(g.use(g.give("lightning scroll")))
        self.assertLess(near.fighter.hp, near.fighter.max_hp)
        self.assertEqual(far.fighter.hp, far.fighter.max_hp)

    def test_lightning_without_target_not_consumed(self):
        g = arena()
        scroll = g.give("lightning scroll")
        self.assertFalse(g.use(scroll))
        self.assertIn(scroll, g.player.inventory.items)

    def test_fireball_area(self):
        g = arena()
        x, y = g.player.pos
        rats = [make_monster("rat", x + 4, y), make_monster("rat", x + 5, y), make_monster("rat", x + 4, y + 1)]
        g.entities += rats
        g.update_fov()
        self.assertTrue(g.use(g.give("fireball scroll"), (x + 4, y)))
        self.assertTrue(all(not r.fighter.alive for r in rats))
        self.assertEqual(g.kills, 3)
        self.assertEqual(g.player.fighter.hp, g.player.fighter.max_hp)

    def test_fireball_needs_target_and_range(self):
        g = arena(w=30)
        scroll = g.give("fireball scroll")
        self.assertFalse(g.use(scroll))
        self.assertFalse(g.use(scroll, (g.player.x + 12, g.player.y)))

    def test_confusion_makes_monster_wander(self):
        g = arena()
        x, y = g.player.pos
        troll = make_monster("cave troll", x + 3, y)
        g.entities.append(troll)
        g.update_fov()
        self.assertTrue(g.use(g.give("confusion scroll"), troll.pos))
        self.assertEqual(troll.confused, 7)  # one turn already spent wandering
        for _ in range(7):
            g.player_wait()
        self.assertEqual(troll.confused, 0)

    def test_teleport_moves_far(self):
        g = arena(w=40)
        start = g.player.pos
        self.assertTrue(g.use(g.give("teleport scroll")))
        self.assertGreater(max(abs(g.player.x - start[0]), abs(g.player.y - start[1])), 8)


class LootTests(unittest.TestCase):
    def test_tables_respect_depth(self):
        shallow = {k for k, _ in loot.table_for(1)}
        self.assertNotIn("ember plate", shallow)
        self.assertIn("ember plate", {k for k, _ in loot.table_for(8)})
        for key, *_ in loot.LOOT_TABLE:
            self.assertIn(key, ITEM_TEMPLATES)

    def test_levels_contain_items(self):
        from emberdeep.game import Game
        total = sum(len([e for e in Game(seed=s).entities if e.item]) for s in range(10))
        self.assertGreater(total, 10)

    def test_roll_is_deterministic(self):
        a = [loot.roll_loot(3, random.Random(9)).key for _ in range(1)]
        b = [loot.roll_loot(3, random.Random(9)).key for _ in range(1)]
        self.assertEqual(a, b)


class TargetingTests(unittest.TestCase):
    def test_projectile_stops_at_wall(self):
        g = arena()
        x, y = g.player.pos
        g.gmap.set(x + 2, y, WALL)
        self.assertEqual(projectile_path(g.gmap, (x, y), (x + 5, y)), [(x + 1, y)])

    def test_blast_area_shape(self):
        g = arena()
        cells = blast_area(g.gmap, g.player.pos, 1)
        self.assertEqual(len(cells), 9)

    def test_cursor_range_and_cycle(self):
        c = Cursor((5, 5), 5, 5, 2, 20, 20)
        for _ in range(5):
            c.move(1, 0)
        self.assertEqual(c.pos, (7, 5))
        c.cycle([(1, 1), (2, 2)])
        self.assertEqual(c.pos, (1, 1))
        c.cycle([(1, 1), (2, 2)])
        self.assertEqual(c.pos, (2, 2))


if __name__ == "__main__":
    unittest.main()
