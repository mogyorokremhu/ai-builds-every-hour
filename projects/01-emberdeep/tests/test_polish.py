"""Phase 7 polish: encumbrance, scavenging monsters, run timeline, explore mode, spell fx."""
import tempfile
import unittest
from pathlib import Path

from emberdeep import encumbrance, explore, fx, save, scavenge, scores
from emberdeep.__main__ import Options, parse_args, run_text_command, start_game
from emberdeep.entities import make_monster
from emberdeep.game import Game
from emberdeep.items import make_item
from emberdeep.morgue import build_morgue, finish_run
from emberdeep.render_ascii import render, render_inventory
from emberdeep.hud import sidebar
from emberdeep.timeline import Timeline, depth_chart, summary_lines
from emberdeep.ui_curses import CursesUI

from tests.helpers import FakeScreen, arena


def add(g, kind, dx, dy, awake=True):
    m = make_monster(kind, g.player.x + dx, g.player.y + dy)
    m.asleep = not awake
    g.entities.append(m)
    g.update_fov()
    return m


class TempHome(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()


# ---- encumbrance --------------------------------------------------------------
class EncumbranceTests(unittest.TestCase):
    def test_weights(self):
        self.assertEqual(encumbrance.item_weight(make_item("chain mail")), 15)
        self.assertEqual(encumbrance.item_weight(make_item("healing potion", 3)), 6)
        self.assertEqual(encumbrance.item_weight(make_item("ring of strength")), 0)
        self.assertEqual(encumbrance.item_weight(make_item("fireball scroll", 4)), 4)

    def test_capacity_grows_with_base_power(self):
        g = arena()
        cap = encumbrance.capacity(g.player)
        self.assertEqual(cap, encumbrance.BASE_CAPACITY + 5 * encumbrance.CAPACITY_PER_POWER)
        g.player.fighter.base_power += 2
        self.assertEqual(encumbrance.capacity(g.player), cap + 2 * encumbrance.CAPACITY_PER_POWER)
        # equipment bonuses don't count, only base power
        g.player.fighter.bonus_power += 10
        self.assertEqual(encumbrance.capacity(g.player), cap + 2 * encumbrance.CAPACITY_PER_POWER)

    def test_states(self):
        self.assertEqual(encumbrance.state_for(10, 20), encumbrance.UNBURDENED)
        self.assertEqual(encumbrance.state_for(25, 20), encumbrance.BURDENED)
        self.assertEqual(encumbrance.state_for(31, 20), encumbrance.OVERLOADED)

    def test_burdened_player_is_slower_and_told_so(self):
        g = arena()
        normal = g.player_speed
        g.give("ember plate")
        g.give("ember plate")
        g.give("chain mail")
        g.give("warhammer")
        g.give("war axe")
        self.assertEqual(encumbrance.state(g.player), encumbrance.BURDENED)
        g.player_wait()
        self.assertLess(g.player_speed, normal)
        self.assertTrue(any("burdened" in m.text for m in g.log.entries()))
        self.assertIn("burdened", encumbrance.load_label(g.player))
        self.assertEqual(encumbrance.load_color(g.player), "bright_red")
        # dropping the heaviest spare item lifts the burden
        junk = encumbrance.heaviest_spare(g.player)
        self.assertEqual(junk.key, "ember plate")
        g.drop(junk)
        g.player_wait()
        self.assertEqual(g.player_speed, normal)
        self.assertTrue(any("manageable" in m.text for m in g.log.entries()))

    def test_burden_makes_monsters_relatively_faster(self):
        g = arena()
        rat = add(g, "rat", 5, 0)
        rat.memory = None
        g.give("ember plate")
        g.give("ember plate")
        g.give("chain mail")
        g.give("warhammer")
        g.give("war axe")
        rat.energy = 0
        g.player_wait()
        self.assertGreater(rat.energy, 0)  # it gained more than one action's worth of energy

    def test_too_heavy_to_pick_up(self):
        g = arena()
        for key in ("ember plate", "ember plate", "ember plate", "chain mail"):
            g.give(key)
        self.assertEqual(encumbrance.state(g.player), encumbrance.BURDENED)
        g.place_item(make_item("ember plate"), *g.player.pos)
        self.assertFalse(g.pickup())
        self.assertTrue(any("too heavy" in m.text for m in g.log.entries()))
        self.assertEqual(len(g.items_at(*g.player.pos)), 1)

    def test_artifact_is_never_too_heavy(self):
        g = arena()
        for key in ("ember plate", "ember plate", "ember plate", "chain mail"):
            g.give(key)
        g.place_item(make_item("ember heart"), *g.player.pos)
        self.assertTrue(g.pickup())
        self.assertTrue(g.victory)

    def test_slot_warnings(self):
        self.assertIsNone(encumbrance.slot_warning(10))
        self.assertIn("3 slots", encumbrance.slot_warning(3)[0])
        self.assertIn("1 slot left", encumbrance.slot_warning(1)[0])
        self.assertIn("full", encumbrance.slot_warning(0)[0])
        g = arena()
        rings = ["ring of strength", "ring of protection", "ring of vitality"]
        for i in range(24):
            g.player.inventory.add(make_item(rings[i % 3]))
        g.place_item(make_item("ring of strength"), *g.player.pos)
        g.pickup()
        self.assertTrue(any("nearly full" in m.text for m in g.log.entries()))

    def test_hud_and_text_render_show_load(self):
        g = arena()
        g.give("sword")
        text = "\n".join(t for t, _ in sidebar(g, 23))
        self.assertIn("Load", text)
        self.assertIn("Pack    1/26", text)
        self.assertIn("Load", render(g))
        inv = render_inventory(g)
        self.assertIn("[wt 6]", inv)
        self.assertIn("Slots 1/26", inv)

    def test_heaviest_spare_skips_equipped(self):
        g = arena()
        plate = g.give("ember plate")
        g.toggle_equip(plate)
        g.give("dagger")
        self.assertEqual(encumbrance.heaviest_spare(g.player).key, "dagger")


# ---- scavengers ---------------------------------------------------------------
class ScavengerTests(unittest.TestCase):
    def setUp(self):
        self.g = arena(w=24, h=12)
        self.g.player.x, self.g.player.y = 2, 2
        self.k = make_monster("kobold", 10, 6)
        self.g.entities.append(self.k)
        self.g.update_fov()

    def run_kobold(self, n):
        for _ in range(n):
            self.k.memory = None
            scavenge.scavenge(self.g, self.k)

    def test_kobolds_are_scavengers(self):
        self.assertTrue(scavenge.is_scavenger(self.k))
        self.assertTrue(scavenge.is_scavenger(make_monster("kobold shaman", 0, 0)))
        self.assertFalse(scavenge.is_scavenger(make_monster("rat", 0, 0)))

    def test_walks_to_and_picks_up_weapon(self):
        self.g.player.x, self.g.player.y = 8, 4
        self.g.update_fov()
        self.g.place_item(make_item("sword"), 13, 6)
        power = self.k.fighter.power
        self.run_kobold(6)
        self.assertEqual(self.k.ai_state.get("weapon"), "sword")
        self.assertEqual(self.k.fighter.power, power + 3)
        self.assertFalse([e for e in self.g.entities if e.item is not None])
        self.assertTrue(any("brandishes" in m.text for m in self.g.log.entries()))
        self.assertIn("wields a sword", scavenge.describe(self.k))

    def test_ignores_worse_weapon_and_keys(self):
        self.k.ai_state.update(weapon="sword", weapon_bonus=3)
        self.g.place_item(make_item("dagger"), 11, 6)
        self.g.place_item(make_item("iron key"), 9, 6)
        self.assertIsNone(scavenge.target_item(self.g, self.k))

    def test_heal_potion_becomes_drinkable(self):
        self.g.place_item(make_item("healing potion"), 10, 6)
        self.run_kobold(1)
        self.assertTrue(self.k.ai_state.get("potion"))

    def test_sack_limit_and_drop_on_death(self):
        for x in range(11, 16):
            self.g.place_item(make_item("ration"), x, 6)
        self.run_kobold(20)
        self.assertEqual(len(self.k.ai_state["sack"]), scavenge.MAX_SACK)
        self.g.place_item(make_item("dagger"), self.k.x, self.k.y)
        self.run_kobold(1)
        self.k.fighter.hp = 0
        self.g.on_kill(self.k)
        here = [e.item.key for e in self.g.items_at(self.k.x, self.k.y)]
        self.assertEqual(here.count("ration"), 3)
        self.assertIn("dagger", here)
        self.assertNotIn("sack", self.k.ai_state)

    def test_dormant_scavenger_uses_take_turn(self):
        from emberdeep import ai

        # out of the player's sight: a wall of darkness via memory=None and hidden player
        self.g.place_item(make_item("sword"), 12, 6)
        self.g.player.x, self.g.player.y = 1, 10
        self.g.update_fov()
        self.k.memory = None
        start = self.k.pos
        for _ in range(4):
            ai.take_turn(self.g, self.k)
        self.assertTrue(self.k.pos != start or self.k.ai_state.get("weapon"))

    def test_scavenged_state_survives_save(self):
        self.g.place_item(make_item("sword"), 10, 6)
        self.run_kobold(1)
        g2 = save.from_dict(save.to_dict(self.g))
        k2 = next(m for m in g2.monsters if m.name == "kobold")
        self.assertEqual(k2.ai_state["weapon"], "sword")
        self.assertEqual(k2.fighter.bonus_power, 3)


# ---- timeline -------------------------------------------------------------------
class TimelineTests(TempHome):
    def test_game_records_descents_levels_and_first_kills(self):
        g = Game(11)
        self.assertEqual(g.timeline.of_kind("depth")[0].depth, 1)
        g.gain_xp(1000)
        self.assertTrue(g.timeline.of_kind("level"))
        m = make_monster("rat", 0, 0)
        g.entities.append(m)
        m.fighter.hp = 0
        g.on_kill(m)
        m2 = make_monster("rat", 0, 0)
        g.entities.append(m2)
        m2.fighter.hp = 0
        g.on_kill(m2)
        self.assertEqual(len(g.timeline.of_kind("first")), 1)
        g.player.x, g.player.y = g.gmap.stairs
        g.turn = 77
        g.descend()
        self.assertEqual(g.timeline.of_kind("depth")[-1].turn, 77)
        self.assertEqual(g.timeline.turns_per_depth(100), {1: 77, 2: 23})

    def test_record_end_once(self):
        g = arena()
        g.record_end()
        self.assertFalse(g.timeline.of_kind("death"))  # still alive
        g.player.fighter.hp = 0
        g.death_cause = "killed by a rat"
        g.record_end()
        g.record_end()
        self.assertEqual([e.text for e in g.timeline.of_kind("death")], ["killed by a rat"])

    def test_chart_shape(self):
        tl = Timeline()
        tl.add(0, 1, "depth", "")
        tl.add(50, 2, "depth", "")
        tl.add(90, 4, "depth", "")
        rows = depth_chart(tl, 100, width=20, height=4)
        self.assertEqual(len(rows), 6)
        self.assertTrue(rows[0].startswith("  4 |"))
        self.assertIn("turn 100", rows[-1])
        # the deepest row is only filled at the end of the run
        self.assertTrue(rows[0].rstrip().endswith("█"))
        self.assertNotIn("█", rows[0][5:15])

    def test_summary_trims_events(self):
        tl = Timeline()
        tl.add(0, 1, "depth", "")
        for i in range(30):
            tl.add(i, 1, "first", f"first thing {i}")
        lines = summary_lines(tl, 40, limit=5)
        self.assertIn("25 earlier events", lines[1])
        self.assertEqual(len(lines), 7)

    def test_timeline_round_trips_through_save(self):
        g = Game(3)
        g.gain_xp(500)
        g2 = save.from_dict(save.to_dict(g))
        self.assertEqual([e.line() for e in g2.timeline.events], [e.line() for e in g.timeline.events])
        old = save.to_dict(g)
        del old["timeline"]
        self.assertEqual(save.from_dict(old).timeline.events, [])

    def test_morgue_contains_timeline(self):
        g = Game(5)
        g.player.fighter.hp = 0
        g.death_cause = "killed by a rat"
        text = build_morgue(g)
        self.assertIn("Timeline", text)
        self.assertIn("Turns per depth", text)
        self.assertIn("x killed by a rat", text)

    def test_end_screen_offers_the_story_of_the_run(self):
        g = arena()
        g.player.fighter.hp = 0
        g.death_cause = "killed by a rat"
        scr = FakeScreen(["T", " "])
        CursesUI(scr, g).run()
        self.assertTrue(scr.seen("perished"))
        self.assertIn("story of your run", scr.text())
        w = arena()
        w.victory = True
        scr = FakeScreen(["x"])
        CursesUI(scr, w).run()
        self.assertIn("VICTORY", scr.text())

    def test_timeline_screen_and_text_command(self):
        g = arena()
        scr = FakeScreen([ord(" ")])
        ui = CursesUI(scr, g)
        ui.handle(ord("T"))
        self.assertTrue(scr.seen("your run so far"))
        run_text_command(g, "T")  # prints; must not crash


# ---- explore mode ---------------------------------------------------------------
class ExploreTests(TempHome):
    def test_parse_and_start(self):
        self.assertTrue(parse_args(["--explore"]).explore)
        g = start_game(Options(explore=True, seed=4), self.home)
        self.assertEqual(g.mode, "explore")
        with self.assertRaises(SystemExit):
            start_game(Options(explore=True, daily=""), self.home)

    def test_explore_save_survives_loading(self):
        g = Game(8, mode="explore")
        path = save.save_game(g, save.save_path(self.home))
        loaded = save.load_game(path)
        self.assertTrue(path.exists())
        self.assertEqual(loaded.mode, "explore")
        normal = Game(8)
        save.save_game(normal, path)
        save.load_game(path)
        self.assertFalse(path.exists())

    def test_death_keeps_explore_save_and_is_unranked(self):
        g = Game(9, mode="explore")
        path = save.save_game(g, save.save_path(self.home))
        g.player.fighter.hp = 0
        g.death_cause = "killed by a rat"
        summary = finish_run(g, self.home)
        self.assertTrue(path.exists())
        self.assertFalse(summary.ranked)
        table = "\n".join(scores.format_table(scores.load_scores(self.home)))
        self.assertIn("[explore]", table)
        self.assertIn("explore mode", build_morgue(g))

    def test_wizard_needs_explore_mode(self):
        g = arena()
        self.assertFalse(explore.wizard(g, "h"))
        g.mode = "explore"
        g.player.fighter.hp = 1
        self.assertTrue(explore.wizard(g, "h"))
        self.assertEqual(g.player.fighter.hp, g.player.fighter.max_hp)
        self.assertFalse(explore.wizard(g, "?"))

    def test_wizard_powers(self):
        g = Game(21, mode="explore")
        self.assertTrue(explore.wizard(g, "m"))
        self.assertTrue(all(all(row) for row in g.gmap.explored))
        self.assertTrue(all(not t.hidden for t in g.traps.values()))
        explore.wizard(g, "i")
        self.assertEqual(g.ident.unknown_kinds(), [])
        explore.wizard(g, "s")
        self.assertEqual(g.player.pos, g.gmap.stairs)
        explore.wizard(g, "d")
        self.assertEqual(g.depth, 2)
        explore.wizard(g, "g")
        self.assertTrue(any(i.key == "greater healing potion" for i in g.player.inventory))
        explore.wizard(g, "g", "sword")
        self.assertTrue(any(i.key == "sword" for i in g.player.inventory))

    def test_wizard_text_and_curses(self):
        g = Game(22, mode="explore")
        run_text_command(g, "Wd")
        self.assertEqual(g.depth, 2)
        scr = FakeScreen([ord("d")])
        ui = CursesUI(scr, g)
        ui.handle(ord("W"))
        self.assertEqual(g.depth, 3)
        self.assertTrue(scr.seen("Wizard powers"))
        self.assertIn("explore mode", "\n".join(t for t, _ in sidebar(g, 23)))


# ---- effects --------------------------------------------------------------------
class FxTests(unittest.TestCase):
    def test_frames(self):
        bolt = fx.Effect("bolt", [(1, 1), (2, 1), (3, 1)], "*", "red")
        frames = fx.frames(bolt)
        self.assertEqual(len(frames), 3)
        self.assertEqual(frames[2][-1][:3], (3, 1, "*"))
        self.assertEqual(frames[2][0][:3], (2, 1, "·"))  # the trail
        beam = fx.frames(fx.Effect("beam", [(1, 1), (2, 2), (3, 3)]), origin=(0, 0))
        self.assertEqual([c[2] for c in beam[0]], ["\\", "\\", "\\"])
        blast = fx.frames(fx.Effect("blast", [(5, 5), (4, 5), (6, 6), (7, 7)]))
        self.assertEqual(len(blast), 3)
        self.assertEqual(len(blast[-1]), 4)
        with self.assertRaises(ValueError):
            fx.frames(fx.Effect("wobble", [(0, 0)]))

    def test_bolt_glyphs(self):
        self.assertEqual(fx.bolt_glyph((0, 0), (1, 0)), "-")
        self.assertEqual(fx.bolt_glyph((0, 0), (0, 1)), "|")
        self.assertEqual(fx.bolt_glyph((0, 0), (1, 1)), "\\")
        self.assertEqual(fx.bolt_glyph((0, 0), (1, -1)), "/")

    def test_queue_is_bounded(self):
        g = arena()
        for _ in range(100):
            fx.emit(g, "bolt", [(1, 1)])
        fx.emit(g, "bolt", [])  # empty paths are ignored
        self.assertEqual(len(fx.drain(g)), fx.MAX_QUEUED)
        self.assertEqual(fx.drain(g), [])

    def test_spells_and_throws_emit_effects(self):
        g = arena()
        imp = add(g, "ember imp", 4, 0)
        g.cast_spell(imp, "ember bolt")
        kinds = [e.kind for e in fx.drain(g)]
        self.assertEqual(kinds, ["bolt"])
        dagger = g.give("dagger")
        g.throw(dagger, imp.pos)
        self.assertEqual(fx.drain(g)[0].glyph, "/")
        scroll = g.give("fireball scroll")
        scroll.unknown_name = None
        g.use(scroll, imp.pos)
        self.assertEqual([e.kind for e in fx.drain(g)], ["bolt", "blast"])

    def test_curses_ui_animates_visible_effects(self):
        g = arena()
        imp = add(g, "ember imp", 4, 0)
        delays = []
        scr = FakeScreen([])
        ui = CursesUI(scr, g, delay=delays.append)
        g.cast_spell(imp, "ember bolt")
        ui.play_fx()
        self.assertGreater(ui.fx_frames, 0)
        self.assertEqual(len(delays), ui.fx_frames)
        # effects out of sight are skipped, and animation can be turned off
        fx.emit(g, "bolt", [(0, 0)])
        g.gmap.visible[0][0] = False
        before = ui.fx_frames
        ui.play_fx()
        self.assertEqual(ui.fx_frames, before)
        ui.animate = False
        g.cast_spell(imp, "ember bolt")
        ui.play_fx()
        self.assertEqual(ui.fx_frames, before)
        self.assertEqual(fx.drain(g), [])


if __name__ == "__main__":
    unittest.main()
