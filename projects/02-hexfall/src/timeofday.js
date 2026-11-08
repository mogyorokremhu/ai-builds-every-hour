// Day/night cycle: six phases of one turn each. Lawful units hit harder by day, chaotic
// units by night; neutral units do not care.

/**
 * @typedef {object} TimeOfDay
 * @property {string} id
 * @property {string} name
 * @property {number} lawful   % damage bonus for lawful units (chaotic get the opposite)
 * @property {string} icon
 * @property {string} tint     translucent colour laid over the map in this phase ("" = none)
 */

/** @type {ReadonlyArray<TimeOfDay>} */
export const CYCLE = Object.freeze([
  { id: "dawn", name: "Dawn", lawful: 0, icon: "🌅", tint: "rgba(255,170,120,0.08)" },
  { id: "morning", name: "Morning", lawful: 25, icon: "☀️", tint: "" },
  { id: "afternoon", name: "Afternoon", lawful: 25, icon: "🌞", tint: "" },
  { id: "dusk", name: "Dusk", lawful: 0, icon: "🌇", tint: "rgba(200,110,80,0.12)" },
  { id: "first-watch", name: "First watch", lawful: -25, icon: "🌙", tint: "rgba(20,30,90,0.30)" },
  { id: "second-watch", name: "Second watch", lawful: -25, icon: "🌌", tint: "rgba(10,15,70,0.36)" },
]);

/** The phase in effect on game turn `turn` (turn 1 = dawn). */
export function timeOfDay(turn) {
  const n = CYCLE.length;
  return CYCLE[(((turn - 1) % n) + n) % n];
}

/** % damage bonus for a unit of `alignment` at time `tod` (negative = penalty). */
export function alignmentBonus(alignment, tod) {
  if (alignment === "lawful") return tod.lawful;
  if (alignment === "chaotic") return -tod.lawful;
  return 0;
}

/** Damage multiplier (e.g. 1.25) for `alignment` on game turn `turn`. */
export function todMultiplier(alignment, turn) {
  return 1 + alignmentBonus(alignment, timeOfDay(turn)) / 100;
}

/** The next `count` phases starting at `turn` (for the UI's day/night strip). */
export function upcoming(turn, count = CYCLE.length) {
  return Array.from({ length: count }, (_, i) => ({ turn: turn + i, ...timeOfDay(turn + i) }));
}
