import { test } from "node:test";
import assert from "node:assert/strict";
import {
  STATUS, addStatus, removeStatus, hasStatus, activeStatuses, attackMultiplier, defenseMultiplier,
  adjustedMp, tick, poisonTick, statusLabel, describeStatuses, POISON_DAMAGE,
} from "../src/status.js";

const unit = () => ({ hp: 20, status: {} });

test("adding keeps the longer duration; removing and querying", () => {
  const u = unit();
  addStatus(u, "poisoned", 2);
  addStatus(u, "poisoned", 1);
  assert.equal(u.status.poisoned, 2);
  addStatus(u, "poisoned", 3);
  assert.equal(u.status.poisoned, 3);
  assert.ok(hasStatus(u, "poisoned"));
  removeStatus(u, "poisoned");
  assert.equal(hasStatus(u, "poisoned"), false);
  assert.throws(() => addStatus(u, "cursed", 1), /unknown status/);
  assert.equal(hasStatus({}, "slowed"), false, "units from old saves have no table");
});

test("multipliers combine rallied, slowed and braced", () => {
  const u = unit();
  assert.equal(attackMultiplier(u), 1);
  addStatus(u, "rallied", 1);
  assert.equal(attackMultiplier(u), 1.2);
  addStatus(u, "slowed", 1);
  assert.ok(Math.abs(attackMultiplier(u) - 0.9) < 1e-9);
  addStatus(u, "braced", 1);
  assert.equal(defenseMultiplier(u), 0.65);
  assert.equal(adjustedMp(u, 5), 3);
  assert.equal(adjustedMp(unit(), 5), 5);
});

test("ticks only count down statuses for the matching phase", () => {
  const u = unit();
  addStatus(u, "poisoned", 2); // start
  addStatus(u, "slowed", 1);   // end
  tick([u], "start");
  assert.deepEqual(u.status, { poisoned: 1, slowed: 1 });
  tick([u], "end");
  assert.deepEqual(u.status, { poisoned: 1 });
  tick([u], "start");
  assert.deepEqual(activeStatuses(u), []);
});

test("poison never kills", () => {
  const u = unit();
  addStatus(u, "poisoned", 3);
  assert.equal(poisonTick(u), POISON_DAMAGE);
  u.hp = 4;
  assert.equal(poisonTick(u), 3);
  assert.equal(u.hp, 1);
  assert.equal(poisonTick(u), 0);
  assert.equal(poisonTick(unit()), 0, "no poison, no damage");
});

test("labels and descriptions follow the table order", () => {
  const u = unit();
  addStatus(u, "braced", 1);
  addStatus(u, "poisoned", 2);
  assert.equal(statusLabel(u), `${STATUS.poisoned.icon}2 ${STATUS.braced.icon}1`);
  assert.equal(describeStatuses(u).length, 2);
  assert.match(describeStatuses(u)[0], /^Poisoned \(2\)/);
});
