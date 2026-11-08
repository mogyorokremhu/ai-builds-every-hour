import { test } from "node:test";
import assert from "node:assert/strict";
import {
  ABILITIES, abilitiesOf, abilityTargets, abilityPreview, abilityProblem, cooldownLeft,
  CHARGE_MULT, VOLLEY_MULT, FIREBALL_RING, HEAL_BASE, POISON_TURNS,
} from "../src/abilities.js";
import { damageRolls } from "../src/combat.js";
import { UNIT_TYPES, maxHp } from "../src/units.js";
import { hasStatus } from "../src/status.js";
import { key } from "../src/hex.js";
import { arena, plainMap } from "./helpers.js";

test("every unit type has a known ability", () => {
  for (const t of Object.values(UNIT_TYPES)) {
    assert.ok(t.abilities.length >= 1, t.id);
    for (const id of t.abilities) assert.ok(ABILITIES[id], `${t.id}: ${id}`);
  }
  assert.deepEqual(abilitiesOf({ type: "cavalry" }), ["charge"]);
});

test("charge needs a move first and multiplies damage both ways", () => {
  const g = arena([["cavalry", "red", 2, 3], ["swordsman", "blue", 5, 3]]);
  const [cav, foe] = g.units;
  assert.match(abilityProblem(g, cav, "charge"), /move first/);
  g.move(cav, { q: 4, r: 3 });
  assert.equal(abilityProblem(g, cav, "charge"), "");
  assert.deepEqual(abilityTargets(g, cav, "charge"), [{ q: 5, r: 3 }]);
  const p = abilityPreview(g, cav, "charge", foe);
  const plain = damageRolls(g, cav, foe, "melee");
  const charged = damageRolls(g, cav, foe, "melee", CHARGE_MULT);
  assert.ok(charged[2] > plain[2]);
  assert.equal(p.hits[0].max, Math.max(...charged));
  assert.ok(p.counter && p.counter.expected > 0, "the swordsman strikes back, harder");
  const hp = foe.hp;
  const res = g.useAbility(cav, "charge", foe);
  assert.ok(foe.hp < hp || res.killed.includes(foe.id));
  assert.ok(cav.acted);
  assert.equal(cooldownLeft(cav, "charge"), ABILITIES.charge.cooldown);
  assert.match(g.log.at(-2).text + g.log.at(-1).text, /charges/);
});

test("abilities cannot be used twice in a turn, recharge over own turns, and reject bad targets", () => {
  const g = arena([["spearman", "red", 3, 3], ["spearman", "red", 4, 3], ["archer", "blue", 8, 3]]);
  const [sp, ally] = g.units;
  assert.throws(() => g.useAbility(sp, "shieldwall", { q: 0, r: 0 }), /invalid/);
  g.useAbility(sp, "shieldwall", sp);
  assert.ok(hasStatus(sp, "braced") && hasStatus(ally, "braced"));
  assert.match(abilityProblem(g, sp, "shieldwall"), /already acted/);
  g.endTurn(); // blue
  assert.ok(hasStatus(sp, "braced"), "braced through the enemy turn");
  g.endTurn(); // red again: braced wears off, cooldown ticks
  assert.equal(hasStatus(sp, "braced"), false);
  assert.match(abilityProblem(g, sp, "shieldwall"), /recharging \(2 turns\)/);
  g.endTurn(); g.endTurn();
  g.endTurn(); g.endTurn();
  assert.equal(abilityProblem(g, sp, "shieldwall"), "");
  assert.throws(() => g.useAbility(sp, "volley", { q: 8, r: 3 }), /not this unit's ability/);
});

test("braced units take 35% less damage", () => {
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "blue", 4, 3]]);
  const [sw, sp] = g.units;
  const before = damageRolls(g, sw, sp, "melee")[2];
  sp.status.braced = 1;
  const after = damageRolls(g, sw, sp, "melee")[2];
  assert.ok(after < before, `${after} < ${before}`);
});

test("volley hits the target and its neighbours at reduced damage, slows the target, no counter", () => {
  const g = arena([["archer", "red", 2, 3], ["archer", "blue", 5, 3], ["spearman", "blue", 6, 3], ["spearman", "red", 5, 4]]);
  const [ar, foe, nb, friend] = g.units;
  const p = abilityPreview(g, ar, "volley", foe);
  assert.deepEqual(p.hits.map((h) => h.unit.id).sort(), [foe.id, nb.id].sort(), "allies next to the target are spared");
  assert.equal(p.counter, null);
  assert.equal(p.hits[0].max, Math.max(...damageRolls(g, ar, foe, "ranged", VOLLEY_MULT)));
  const arHp = ar.hp, friendHp = friend.hp;
  g.useAbility(ar, "volley", foe);
  assert.equal(ar.hp, arHp, "no counter-attack");
  assert.equal(friend.hp, friendHp);
  assert.ok(foe.hp < UNIT_TYPES.archer.hp && nb.hp < UNIT_TYPES.spearman.hp);
  assert.ok(hasStatus(foe, "slowed"));
  g.endTurn(); // blue's turn: the slowed archer gets half its move points
  assert.equal(foe.mp, Math.ceil(UNIT_TYPES.archer.mp / 2));
  g.endTurn(); g.endTurn();
  assert.equal(foe.mp, UNIT_TYPES.archer.mp, "slow wore off after one turn");
});

test("fireball blasts a hex and its ring, friends included, and sets dry ground alight", () => {
  const map = plainMap(10, 8, { "6,3": "forest", "6,4": "village" });
  const g = arena([["mage", "red", 3, 3], ["swordsman", "blue", 5, 3], ["spearman", "blue", 6, 3], ["spearman", "red", 4, 3]], { map });
  const [mage, center, ring, friend] = g.units;
  const targets = abilityTargets(g, mage, "fireball");
  assert.ok(targets.some((h) => key(h) === "5,3"));
  assert.ok(targets.every((h) => Math.abs(h.q - 3) + Math.abs(h.r - 3) + Math.abs(h.q + h.r - 6) <= 4));
  const p = abilityPreview(g, mage, "fireball", center);
  const ids = p.hits.map((h) => h.unit.id).sort();
  assert.deepEqual(ids, [center.id, ring.id, friend.id].sort());
  assert.equal(p.hits.find((h) => h.unit === ring).max, Math.max(...damageRolls(g, mage, ring, "ranged", FIREBALL_RING)));
  assert.ok(p.fires >= 3);
  const fHp = friend.hp;
  g.useAbility(mage, "fireball", center);
  assert.ok(friend.hp < fHp, "friendly fire");
  assert.ok(g.map.get({ q: 5, r: 3 }).fire > 0, "plains burn");
  assert.ok(g.map.get({ q: 6, r: 3 }).fire > 0, "forest burns");
  assert.ok(!g.map.get({ q: 6, r: 4 }).fire, "villages do not");
  assert.ok(!g.map.get({ q: 3, r: 3 }).fire, "never under the caster");
});

test("burning hexes cost extra to enter, hurt units that start a turn there and burn out", () => {
  const map = plainMap(10, 8, { "5,3": "forest" });
  const g = arena([["swordsman", "red", 2, 3], ["spearman", "blue", 5, 3]], { map });
  const [sw, sp] = g.units;
  g.map.get({ q: 5, r: 3 }).fire = 1;
  g.map.get({ q: 3, r: 3 }).fire = 2;
  assert.equal(g.area(sw).get("3,3").cost, 3, "1 + 2 for the flames");
  g.endTurn(); // blue starts on fire
  assert.equal(sp.hp, UNIT_TYPES.spearman.hp - 6);
  g.rules.weather = false;
  g.endTurn(); // new round: fires burn down; the forest burns out to plains
  assert.equal(g.map.get({ q: 5, r: 3 }).terrain, "plains");
  assert.ok(!(g.map.get({ q: 5, r: 3 }).fire > 0));
});

test("heal restores HP to an adjacent hurt ally and cures poison", () => {
  const g = arena([["healer", "red", 3, 3], ["swordsman", "red", 4, 3], ["spearman", "red", 7, 3]]);
  const [h, sw, far] = g.units;
  assert.deepEqual(abilityTargets(g, h, "heal"), [], "nobody hurt yet");
  sw.hp = 10;
  sw.status.poisoned = 2;
  far.hp = 5;
  assert.deepEqual(abilityTargets(g, h, "heal"), [{ q: 4, r: 3 }]);
  const p = abilityPreview(g, h, "heal", sw);
  assert.equal(p.heal, HEAL_BASE);
  assert.equal(p.cures, 1);
  g.useAbility(h, "heal", sw);
  assert.equal(sw.hp, 10 + HEAL_BASE);
  assert.equal(hasStatus(sw, "poisoned"), false);
  sw.hp = maxHp(sw) - 3;
  assert.equal(abilityPreview({ ...g, side: "red" }, { ...h, acted: false }, "heal", sw)?.heal ?? 3, 3);
});

test("envenom poisons a survivor, poison ticks at its turn start and villages cure it", () => {
  const map = plainMap(10, 8, { "6,3": "village" });
  const g = arena([["rogue", "red", 4, 3], ["swordsman", "blue", 5, 3], ["swordsman", "blue", 6, 3]], { map });
  const [rogue, a, b] = g.units;
  g.useAbility(rogue, "envenom", a);
  assert.ok(hasStatus(a, "poisoned"));
  assert.equal(a.status.poisoned, POISON_TURNS);
  const hp = a.hp;
  g.endTurn();
  assert.equal(a.hp, hp - 6);
  assert.equal(a.status.poisoned, POISON_TURNS - 1);
  b.status.poisoned = 2;
  const bhp = b.hp;
  g.endTurn(); g.endTurn();
  assert.equal(hasStatus(b, "poisoned"), false, "the village cured it");
  assert.equal(b.hp, bhp, "...instead of healing");
});

test("rally gives +20% damage this turn and the next", () => {
  const g = arena([["swordsman", "red", 3, 3], ["spearman", "red", 3, 4], ["spearman", "blue", 4, 4]]);
  const [sw, sp, foe] = g.units;
  const before = damageRolls(g, sp, foe, "melee")[2];
  g.useAbility(sw, "rally", sw);
  assert.ok(hasStatus(sp, "rallied") && hasStatus(sw, "rallied"));
  assert.ok(damageRolls(g, sp, foe, "melee")[2] > before);
  g.endTurn(); g.endTurn();
  assert.ok(hasStatus(sp, "rallied"), "still rallied on the next turn");
  g.endTurn();
  assert.equal(hasStatus(sp, "rallied"), false);
});

test("statuses and cooldowns survive a save round trip", async () => {
  const { Game } = await import("../src/game.js");
  const g = arena([["spearman", "red", 3, 3], ["archer", "blue", 8, 3]]);
  g.useAbility(g.units[0], "shieldwall", g.units[0]);
  g.units[1].status.poisoned = 2;
  const back = Game.fromJSON(JSON.parse(JSON.stringify(g.toJSON())));
  assert.deepEqual(back.units[0].status, { braced: 1 });
  assert.deepEqual(back.units[0].cd, { shieldwall: 3 });
  assert.deepEqual(back.units[1].status, { poisoned: 2 });
});
