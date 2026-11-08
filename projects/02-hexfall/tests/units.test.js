import { test } from "node:test";
import assert from "node:assert/strict";
import {
  UNIT_TYPES, PERKS, createUnit, gainXp, maxHp, meleeAttack, rangedAttack, attackRange, defenseOf,
  maxMp, healAmount, describeUnit, xpToNext, MAX_LEVEL, DEFAULT_ARMY,
} from "../src/units.js";

test("every unit type is complete and has a valid perk", () => {
  for (const t of Object.values(UNIT_TYPES)) {
    for (const f of ["hp", "attack", "ranged", "range", "defense", "mp", "cost"]) assert.equal(typeof t[f], "number", `${t.id}.${f}`);
    assert.ok(t.hp > 0 && t.mp > 0 && t.cost > 0);
    assert.ok(t.attack > 0 || t.ranged > 0, `${t.id} can fight`);
    assert.ok(PERKS[t.perk], `${t.id} perk`);
    assert.equal(t.glyph.length, 1);
  }
  assert.equal(new Set(Object.values(UNIT_TYPES).map((t) => t.glyph)).size, Object.keys(UNIT_TYPES).length);
  for (const t of DEFAULT_ARMY) assert.ok(UNIT_TYPES[t]);
});

test("createUnit starts fresh at level 1", () => {
  const u = createUnit(1, "archer", "red", { q: 2, r: 3 });
  assert.deepEqual([u.q, u.r, u.hp, u.mp, u.level, u.xp, u.acted], [2, 3, 28, 5, 1, 0, false]);
  assert.equal(meleeAttack(u), 4);
  assert.equal(rangedAttack(u), 8);
  assert.equal(attackRange(u), 3);
  assert.equal(rangedAttack(createUnit(2, "swordsman", "red", { q: 0, r: 0 })), 0);
  assert.equal(attackRange(createUnit(2, "swordsman", "red", { q: 0, r: 0 })), 1);
  assert.throws(() => createUnit(3, "dragon", "red", { q: 0, r: 0 }));
});

test("promotion: veteran perk, then elite, then capped", () => {
  const u = createUnit(1, "spearman", "blue", { q: 0, r: 0 });
  u.hp = 5;
  assert.deepEqual(gainXp(u, 19), []);
  assert.equal(u.level, 1);
  assert.deepEqual(gainXp(u, 1), ["Phalanx"]);
  assert.equal(u.level, 2);
  assert.equal(defenseOf(u), UNIT_TYPES.spearman.defense + 2);
  assert.equal(maxHp(u), 34 + 5);
  assert.equal(u.hp, maxHp(u), "promotion heals fully");
  assert.deepEqual(gainXp(u, 100), ["Elite"]);
  assert.equal(u.level, MAX_LEVEL);
  assert.equal(xpToNext(u), Infinity);
  assert.equal(meleeAttack(u), 9 + 1);
  assert.deepEqual(gainXp(u, 100), []);
});

test("a big XP gain can promote twice at once", () => {
  const u = createUnit(1, "mage", "red", { q: 0, r: 0 });
  assert.deepEqual(gainXp(u, 70), ["Arcanist", "Elite"]);
  assert.equal(rangedAttack(u), 11 + 3 + 1);
});

test("type perks", () => {
  const mk = (t) => { const u = createUnit(1, t, "red", { q: 0, r: 0 }); gainXp(u, 20); return u; };
  assert.equal(attackRange(mk("archer")), 4);
  assert.equal(maxMp(mk("cavalry")), 9);
  assert.equal(meleeAttack(mk("swordsman")), 14);
  assert.equal(healAmount(mk("healer")), 8);
  assert.equal(healAmount(createUnit(1, "healer", "red", { q: 0, r: 0 })), 4);
  assert.equal(healAmount(mk("swordsman")), 0);
});

test("describeUnit mentions the essentials", () => {
  const u = createUnit(1, "archer", "red", { q: 0, r: 0 });
  const d = describeUnit(u);
  for (const s of ["Recruit Archer", "HP 28/28", "ranged 8 (range 3)", "MP 5/5", "XP 0/20"]) assert.ok(d.includes(s), s);
});
