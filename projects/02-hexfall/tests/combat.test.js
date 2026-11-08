import { test } from "node:test";
import assert from "node:assert/strict";
import {
  attackKind, counterKind, damageRolls, forecast, resolveAttack, flankers, effectiveRange, strikeModifiers, ROLLS,
} from "../src/combat.js";
import { hasLineOfSight, sightLines, visibleFrom } from "../src/sight.js";
import { RNG } from "../src/rng.js";
import { key } from "../src/hex.js";
import { arena, plainMap } from "./helpers.js";

test("damage rolls: attack × modifiers × roll − armour, at least 1", () => {
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 4, 3]]);
  const [a, d] = g.units;
  // 11 × {0.8..1.2} = 8.8, 9.9, 11, 12.1, 13.2 → 9, 10, 11, 12, 13 − 2
  assert.deepEqual(damageRolls(g, a, d, "melee"), [7, 8, 9, 10, 11]);
  d.bonus.defense = 50;
  assert.deepEqual(damageRolls(g, a, d, "melee"), [1, 1, 1, 1, 1]);
});

test("terrain defence reduces damage; magic ignores it", () => {
  const map = plainMap(10, 8, { "4,3": "forest" });
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 4, 3], ["mage", "red", 6, 1]], { map });
  const [sw, sp, mage] = g.units;
  assert.equal(strikeModifiers(g, sw, sp, "melee").terrain, 25);
  assert.deepEqual(damageRolls(g, sw, sp, "melee"), [5, 5, 6, 7, 8]); // 11×0.75 = 8.25 × rolls
  assert.equal(strikeModifiers(g, mage, sp, "ranged").terrain, 0);
});

test("spearmen punish cavalry", () => {
  const g = arena([["spearman", "red", 3, 3], ["cavalry", "blue", 4, 3], ["swordsman", "red", 3, 4]]);
  const [sp, cav] = g.units;
  const m = strikeModifiers(g, sp, cav, "melee");
  assert.equal(m.bonus, 1.5);
  assert.equal(strikeModifiers(g, cav, sp, "melee").bonus, 1);
});

test("flanking: each extra adjacent ally adds 10% (melee only, max 3)", () => {
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 4, 3], ["spearman", "red", 5, 3],
    ["spearman", "red", 4, 2], ["archer", "red", 6, 1]]);
  const [sw, target] = g.units;
  assert.equal(flankers(g, sw, target), 2);
  assert.ok(Math.abs(strikeModifiers(g, sw, target, "melee").multiplier - 1.2) < 1e-9);
  assert.equal(strikeModifiers(g, g.units[4], target, "ranged").flank, 0);
});

test("attack kinds, ranges, high ground and counters", () => {
  const map = plainMap(12, 8, { "2,3": "hills" });
  const g = arena([["archer", "red", 3, 3], ["swordsman", "blue", 6, 3], ["archer", "blue", 7, 3],
    ["mage", "red", 4, 4], ["swordsman", "red", 2, 3]], { map });
  const [archer, sw, archer2, mage] = g.units;
  assert.equal(attackKind(g, archer, sw), "ranged");      // distance 3
  assert.equal(attackKind(g, archer, archer2), null);     // distance 4 > range 3
  assert.equal(effectiveRange(g, archer, { q: 2, r: 3 }), 4);
  assert.equal(attackKind(g, archer, archer2, { q: 2, r: 3 }), null, "5 hexes from the hill");
  assert.equal(attackKind(g, archer, sw, { q: 5, r: 3 }), "ranged", "adjacent archer still shoots (8 > 4)");
  assert.equal(attackKind(g, sw, archer, { q: 4, r: 3 }), "melee");
  assert.equal(counterKind(g, sw, archer, "ranged"), null, "swordsmen can't shoot back");
  assert.equal(counterKind(g, archer2, { q: 4, r: 3 }, "ranged"), "ranged");
  assert.equal(attackKind(g, mage, sw), "ranged");        // (4,4)→(6,3) is 2 hexes: mage range
  mage.bonus.range = -1;
  assert.equal(attackKind(g, mage, sw), null);
});

test("forecast enumerates all 25 outcomes exactly", () => {
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 4, 3]]);
  const [a, d] = g.units;
  d.hp = 9; // dies on rolls 3..5 (9, 10, 11)
  const f = forecast(g, a, d);
  assert.equal(f.kind, "melee");
  assert.equal(f.counter, "melee");
  assert.ok(Math.abs(f.killChance - 0.6) < 1e-9);
  assert.deepEqual([f.dealt.min, f.dealt.max], [7, 11]);
  assert.ok(Math.abs(f.expectedDealt - (7 + 8 + 9 + 9 + 9) / 5) < 1e-9);
  // the counter only happens in the 40% of outcomes where the spearman survives
  const counter = damageRolls(g, d, a, "melee");
  const mean = counter.reduce((s, x) => s + x, 0) / 5;
  assert.ok(Math.abs(f.expectedTaken - 0.4 * mean) < 1e-9);
  a.hp = 1;
  assert.ok(Math.abs(forecast(g, a, d).deathChance - 0.4) < 1e-9);
});

test("forecast from another hex and null when out of reach", () => {
  const g = arena([["swordsman", "red", 2, 3], ["spearman", "blue", 5, 3]]);
  const [a, d] = g.units;
  assert.equal(forecast(g, a, d), null);
  assert.equal(forecast(g, a, d, { q: 4, r: 3 }).kind, "melee");
});

test("resolveAttack is seeded, applies the counter and removes the dead", () => {
  const run = (seed) => {
    const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 4, 3]], { seed });
    g.rng = new RNG(seed);
    const res = resolveAttack(g, g.units[0], g.units[1]);
    return { res, hp: g.units.map((u) => u.hp) };
  };
  assert.deepEqual(run(5), run(5));
  const { res, hp } = run(5);
  assert.ok(res.dealt >= 7 && res.dealt <= 11);
  assert.ok(res.taken >= 1);
  assert.deepEqual(hp, [40 - res.taken, 34 - res.dealt]);
});

test("kills grant 8 XP per level and can promote", () => {
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 4, 3]]);
  const [a, d] = g.units;
  d.hp = 1;
  a.xp = 15;
  const res = resolveAttack(g, a, d);
  assert.deepEqual(res.killed, [d.id]);
  assert.equal(res.counter, null);
  assert.equal(g.units.length, 1);
  assert.equal(a.level, 2);
  assert.equal(a.kills, 1);
  assert.deepEqual(res.promotions, [{ id: a.id, perks: ["Blademaster"] }]);
  assert.ok(res.lines.some((l) => l.includes("promoted")));
});

test("surviving an exchange gives 1 XP per enemy level to both sides", () => {
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 4, 3]]);
  const [a, d] = g.units;
  d.level = 2;
  resolveAttack(g, a, d);
  assert.equal(a.xp, 2);
  assert.equal(d.xp, 1);
});

test("line of sight: forests and villages block unless you stand higher; mountains always block", () => {
  const map = plainMap(12, 8, { "4,3": "forest" });
  assert.equal(hasLineOfSight(map, { q: 3, r: 3 }, { q: 5, r: 3 }), false);
  assert.equal(hasLineOfSight(map, { q: 3, r: 3 }, { q: 4, r: 3 }), true, "adjacent always visible");
  map.set({ q: 3, r: 3 }, "hills");
  assert.equal(hasLineOfSight(map, { q: 3, r: 3 }, { q: 5, r: 3 }), true, "from the hill over the trees");
  map.set({ q: 4, r: 3 }, "mountain");
  assert.equal(hasLineOfSight(map, { q: 3, r: 3 }, { q: 5, r: 3 }), false);
});

test("edge-aligned lines are clear if either side is clear", () => {
  // (2,3) → (4,2) runs along the edge between (3,2) and (3,3)
  const lines = sightLines({ q: 2, r: 3 }, { q: 4, r: 2 });
  const mids = lines.map((l) => key(l[0]));
  assert.deepEqual(new Set(mids), new Set(["3,2", "3,3"]));
  const map = plainMap(12, 8, { "3,2": "forest" });
  assert.equal(hasLineOfSight(map, { q: 2, r: 3 }, { q: 4, r: 2 }), true);
  map.set({ q: 3, r: 3 }, "forest");
  assert.equal(hasLineOfSight(map, { q: 2, r: 3 }, { q: 4, r: 2 }), false);
});

test("line of sight on flat ground is symmetric", () => {
  const map = plainMap(12, 8, { "5,3": "forest", "4,4": "village", "6,2": "forest" });
  const hexes = [...map].filter((t) => t.terrain === "plains").slice(0, 60);
  for (const a of hexes) for (const b of hexes) {
    assert.equal(hasLineOfSight(map, a, b), hasLineOfSight(map, b, a), `${key(a)} ↔ ${key(b)}`);
  }
});

test("visibleFrom includes the viewer and excludes hidden hexes", () => {
  const map = plainMap(12, 8, { "4,3": "forest" });
  const seen = visibleFrom(map, { q: 3, r: 3 }, 3);
  assert.ok(seen.has("3,3") && seen.has("4,3"));
  assert.ok(!seen.has("5,3"));
  assert.ok(seen.size > 20);
});

test("ROLLS are symmetric around 1", () => {
  assert.equal(ROLLS.reduce((s, x) => s + x, 0) / ROLLS.length, 1);
});
