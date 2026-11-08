// Status effects on units: poisoned, slowed, rallied, braced. Statuses are stored on the unit
// as {id: turnsLeft} so they survive saves. Each status counts down either at the start or at
// the end of its bearer's own turn.

/**
 * @typedef {object} StatusDef
 * @property {string} id
 * @property {string} name
 * @property {string} icon
 * @property {"start"|"end"} expires   when the counter ticks down (bearer's turn start/end)
 * @property {string} text
 */

/** @type {Record<string, StatusDef>} */
export const STATUS = Object.freeze({
  poisoned: { id: "poisoned", name: "Poisoned", icon: "☠", expires: "start", text: "Loses 6 HP at the start of each of its turns (never below 1). Villages and healers cure it instead of healing." },
  slowed: { id: "slowed", name: "Slowed", icon: "🐌", expires: "end", text: "Half move points and −25% damage until the end of its next turn." },
  rallied: { id: "rallied", name: "Rallied", icon: "⚑", expires: "end", text: "+20% damage." },
  braced: { id: "braced", name: "Braced", icon: "🛡", expires: "start", text: "Takes 35% less damage until its next turn." },
});

export const POISON_DAMAGE = 6;
export const RALLY_BONUS = 0.2;
export const SLOW_PENALTY = 0.25;
export const BRACE_REDUCTION = 0.35;

/** The unit's status table (created on demand; older saves have none). */
export function statuses(u) {
  if (!u.status) u.status = {};
  return u.status;
}

export function hasStatus(u, id) {
  return (u.status?.[id] ?? 0) > 0;
}

/** Give `u` status `id` for `turns` (keeps the longer duration if it already has it). */
export function addStatus(u, id, turns) {
  if (!STATUS[id]) throw new Error(`unknown status ${id}`);
  const s = statuses(u);
  s[id] = Math.max(s[id] ?? 0, turns);
}

export function removeStatus(u, id) {
  if (u.status) delete u.status[id];
}

/** Active status ids of `u`, in table order. */
export function activeStatuses(u) {
  return Object.keys(STATUS).filter((id) => hasStatus(u, id));
}

/** Multiplier on the damage `u` deals (rallied +20%, slowed −25%). */
export function attackMultiplier(u) {
  let m = 1;
  if (hasStatus(u, "rallied")) m *= 1 + RALLY_BONUS;
  if (hasStatus(u, "slowed")) m *= 1 - SLOW_PENALTY;
  return m;
}

/** Multiplier on the damage `u` takes (braced −35%). */
export function defenseMultiplier(u) {
  return hasStatus(u, "braced") ? 1 - BRACE_REDUCTION : 1;
}

/** Move points `u` gets at the start of its turn given its statuses. */
export function adjustedMp(u, mp) {
  return hasStatus(u, "slowed") ? Math.ceil(mp / 2) : mp;
}

/** Count down statuses of `units` that expire at `when` ("start" | "end"). */
export function tick(units, when) {
  for (const u of units) {
    if (!u.status) continue;
    for (const [id, left] of Object.entries(u.status)) {
      if (STATUS[id]?.expires !== when) continue;
      if (left <= 1) delete u.status[id];
      else u.status[id] = left - 1;
    }
  }
}

/**
 * Poison damage for one unit at its turn start (never kills: stops at 1 HP).
 * @returns {number} HP lost
 */
export function poisonTick(u) {
  if (!hasStatus(u, "poisoned")) return 0;
  const lost = Math.min(POISON_DAMAGE, u.hp - 1);
  u.hp -= lost;
  return lost;
}

/** Short label like "☠2 🐌1" for tooltips and the roster. */
export function statusLabel(u) {
  return activeStatuses(u).map((id) => `${STATUS[id].icon}${u.status[id]}`).join(" ");
}

/** Description lines for a unit's statuses. */
export function describeStatuses(u) {
  return activeStatuses(u).map((id) => `${STATUS[id].name} (${u.status[id]}): ${STATUS[id].text}`);
}
