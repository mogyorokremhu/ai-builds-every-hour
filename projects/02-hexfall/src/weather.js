// Weather: seeded fronts that last a few turns. Rain dulls ranged attacks and puts out fires,
// fog shortens sight and bow range, storms do a little of everything. Weather is derived
// from the game seed and the turn number, so it needs no saved state and replays exactly.

/**
 * @typedef {object} Weather
 * @property {string} id
 * @property {string} name
 * @property {string} icon
 * @property {number} ranged        multiplier on ranged damage
 * @property {number} rangePenalty  hexes taken off ranged reach (never below 1)
 * @property {number} sightPenalty  hexes taken off sight radius (fog of war)
 * @property {boolean} wet          puts out burning hexes and stops new fires
 * @property {string} tint          translucent colour laid over the map ("" = none)
 * @property {string} text
 */

/** @type {Record<string, Weather>} */
export const WEATHER = Object.freeze({
  clear: { id: "clear", name: "Clear", icon: "🌤️", ranged: 1, rangePenalty: 0, sightPenalty: 0, wet: false, tint: "", text: "No effect." },
  rain: { id: "rain", name: "Rain", icon: "🌧️", ranged: 0.8, rangePenalty: 0, sightPenalty: 1, wet: true, tint: "rgba(60,80,120,0.16)", text: "Ranged damage −20%, sight −1, fires go out." },
  fog: { id: "fog", name: "Fog", icon: "🌫️", ranged: 1, rangePenalty: 1, sightPenalty: 2, wet: false, tint: "rgba(220,225,230,0.22)", text: "Ranged reach −1, sight −2." },
  storm: { id: "storm", name: "Storm", icon: "⛈️", ranged: 0.7, rangePenalty: 1, sightPenalty: 2, wet: true, tint: "rgba(40,45,80,0.26)", text: "Ranged damage −30%, reach −1, sight −2, fires go out." },
});

/** How likely each weather is when a new front arrives. */
export const FRONT_WEIGHTS = Object.freeze([["clear", 50], ["rain", 22], ["fog", 17], ["storm", 11]]);
/** Turns per weather front. The first front (turns 1–3) is always clear. */
export const FRONT_LENGTH = 3;

/** A well-mixed 32-bit hash of two integers (deterministic weather rolls). */
export function hash2(a, b) {
  let h = (Math.imul(a | 0, 0x9e3779b1) ^ Math.imul(b | 0, 0x85ebca77)) >>> 0;
  h = Math.imul(h ^ (h >>> 16), 0x7feb352d) >>> 0;
  h = Math.imul(h ^ (h >>> 15), 0x846ca68b) >>> 0;
  return (h ^ (h >>> 16)) >>> 0;
}

/** Weather on game turn `turn` for battle seed `seed`. */
export function weatherFor(seed, turn) {
  const front = Math.floor((Math.max(1, turn) - 1) / FRONT_LENGTH);
  if (front === 0) return WEATHER.clear;
  const total = FRONT_WEIGHTS.reduce((s, [, w]) => s + w, 0);
  let roll = (hash2(seed, front) / 4294967296) * total;
  for (const [id, w] of FRONT_WEIGHTS) {
    if ((roll -= w) < 0) return WEATHER[id];
  }
  return WEATHER.clear;
}

/** Weather in effect in `game` right now (always clear when the weather rule is off). */
export function currentWeather(game) {
  if (!game || game.rules?.weather === false) return WEATHER.clear;
  return weatherFor(game.seed ?? 1, game.turn ?? 1);
}

/** The next `count` turns of weather from `turn` (forecast strip in the UI). */
export function weatherForecast(game, count = 6) {
  return Array.from({ length: count }, (_, i) => ({
    turn: (game.turn ?? 1) + i,
    ...(game.rules?.weather === false ? WEATHER.clear : weatherFor(game.seed ?? 1, (game.turn ?? 1) + i)),
  }));
}
