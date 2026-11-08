// Unit types and unit records. Units are plain objects so the whole game state is JSON.

/**
 * @typedef {object} UnitType
 * @property {string} id
 * @property {string} name
 * @property {string} glyph      letter drawn on the token
 * @property {number} hp         max hit points at level 1
 * @property {number} attack     melee attack (0 = cannot fight in melee)
 * @property {number} ranged     ranged attack (0 = no ranged attack)
 * @property {number} range      max ranged distance (ranged units; melee is always distance 1)
 * @property {number} defense    flat damage reduction per hit
 * @property {number} mp         move points per turn
 * @property {number} cost       recruit cost in gold
 * @property {string[]} traits   rule tags: mounted, antiCavalry, magic, healer, ...
 * @property {string} perk       perk gained when promoted to veteran
 * @property {string} blurb
 */

/** @type {Record<string, UnitType>} */
export const UNIT_TYPES = Object.freeze({
  spearman: {
    id: "spearman", name: "Spearman", glyph: "S", hp: 34, attack: 9, ranged: 0, range: 1, defense: 2,
    mp: 5, cost: 14, traits: ["antiCavalry"], perk: "phalanx",
    blurb: "Cheap line infantry. Spears deal ×1.5 damage to mounted units.",
  },
  swordsman: {
    id: "swordsman", name: "Swordsman", glyph: "W", hp: 40, attack: 11, ranged: 0, range: 1, defense: 3,
    mp: 5, cost: 17, traits: [], perk: "blademaster",
    blurb: "Tough, hard-hitting melee fighter.",
  },
  archer: {
    id: "archer", name: "Archer", glyph: "A", hp: 28, attack: 4, ranged: 8, range: 3, defense: 1,
    mp: 5, cost: 15, traits: [], perk: "longshot",
    blurb: "Shoots up to 3 hexes (4 from high ground). Needs a clear line of sight.",
  },
  cavalry: {
    id: "cavalry", name: "Cavalry", glyph: "C", hp: 38, attack: 10, ranged: 0, range: 1, defense: 2,
    mp: 8, cost: 20, traits: ["mounted"], perk: "outrider",
    blurb: "Fast raider. Forests and swamps cost it 1 extra move point.",
  },
  mage: {
    id: "mage", name: "Mage", glyph: "M", hp: 24, attack: 3, ranged: 11, range: 2, defense: 0,
    mp: 5, cost: 20, traits: ["magic"], perk: "arcanist",
    blurb: "Fragile caster. Magic ignores terrain defence.",
  },
  healer: {
    id: "healer", name: "Healer", glyph: "H", hp: 26, attack: 4, ranged: 0, range: 1, defense: 1,
    mp: 5, cost: 16, traits: ["healer"], perk: "medic",
    blurb: "Heals adjacent allies at the start of each of its turns.",
  },
});

/** What each perk does when a unit becomes a veteran. */
export const PERKS = Object.freeze({
  phalanx: { name: "Phalanx", text: "+2 defence", apply: (u) => { u.bonus.defense += 2; } },
  blademaster: { name: "Blademaster", text: "+3 melee attack", apply: (u) => { u.bonus.attack += 3; } },
  longshot: { name: "Longshot", text: "+1 range", apply: (u) => { u.bonus.range += 1; } },
  outrider: { name: "Outrider", text: "+1 move point", apply: (u) => { u.bonus.mp += 1; } },
  arcanist: { name: "Arcanist", text: "+3 ranged attack", apply: (u) => { u.bonus.ranged += 3; } },
  medic: { name: "Medic", text: "heals 4 more", apply: (u) => { u.bonus.heal += 4; } },
  elite: { name: "Elite", text: "+1 attack, +1 defence", apply: (u) => {
    u.bonus.attack += 1;
    u.bonus.defense += 1;
    if (unitType(u).ranged) u.bonus.ranged += 1;
  } },
});

/** XP needed to reach the next level (index = current level). Level 3 is the cap. */
export const XP_TO_LEVEL = Object.freeze([0, 20, 45]);
export const MAX_LEVEL = 3;
export const LEVEL_NAMES = Object.freeze(["", "Recruit", "Veteran", "Elite"]);

export function unitType(u) {
  const t = UNIT_TYPES[typeof u === "string" ? u : u.type];
  if (!t) throw new Error(`unknown unit type ${typeof u === "string" ? u : u.type}`);
  return t;
}

/** A fresh level-1 unit of `type` for `side` at hex `h`. */
export function createUnit(id, type, side, h) {
  const t = unitType(type);
  return {
    id, type, side, q: h.q, r: h.r,
    hp: t.hp, mp: t.mp, acted: false, xp: 0, level: 1, kills: 0,
    perks: [],
    bonus: { hp: 0, attack: 0, ranged: 0, range: 0, defense: 0, mp: 0, heal: 0 },
  };
}

// Derived stats (type + promotion bonuses).
export const maxHp = (u) => unitType(u).hp + u.bonus.hp;
export const meleeAttack = (u) => (unitType(u).attack ? unitType(u).attack + u.bonus.attack : 0);
export const rangedAttack = (u) => (unitType(u).ranged ? unitType(u).ranged + u.bonus.ranged : 0);
export const attackRange = (u) => (unitType(u).ranged ? unitType(u).range + u.bonus.range : 1);
export const defenseOf = (u) => unitType(u).defense + u.bonus.defense;
export const maxMp = (u) => unitType(u).mp + u.bonus.mp;
export const healAmount = (u) => (hasTrait(u, "healer") ? 4 + u.bonus.heal : 0);
export const hasTrait = (u, trait) => unitType(u).traits.includes(trait);
export const xpToNext = (u) => (u.level >= MAX_LEVEL ? Infinity : XP_TO_LEVEL[u.level]);

/**
 * Add XP and promote as many times as earned. Each promotion raises max HP by 15% of the
 * base, heals fully and grants a perk (the type's perk at veteran, "elite" after that).
 * @returns {string[]} names of the perks gained (empty if no promotion)
 */
export function gainXp(u, amount) {
  u.xp += amount;
  const gained = [];
  while (u.level < MAX_LEVEL && u.xp >= xpToNext(u)) {
    u.xp -= xpToNext(u);
    u.level += 1;
    const perk = u.level === 2 ? unitType(u).perk : "elite";
    u.bonus.hp += Math.round(unitType(u).hp * 0.15);
    PERKS[perk].apply(u);
    u.perks.push(perk);
    u.hp = maxHp(u);
    gained.push(PERKS[perk].name);
  }
  if (u.level >= MAX_LEVEL) u.xp = 0;
  return gained;
}

/** One-line description for tooltips and the roster. */
export function describeUnit(u) {
  const t = unitType(u);
  const parts = [`${LEVEL_NAMES[u.level]} ${t.name}`, `HP ${u.hp}/${maxHp(u)}`];
  if (meleeAttack(u)) parts.push(`melee ${meleeAttack(u)}`);
  if (rangedAttack(u)) parts.push(`ranged ${rangedAttack(u)} (range ${attackRange(u)})`);
  parts.push(`def ${defenseOf(u)}`, `MP ${u.mp}/${maxMp(u)}`);
  if (u.level < MAX_LEVEL) parts.push(`XP ${u.xp}/${xpToNext(u)}`);
  if (u.perks.length) parts.push(u.perks.map((p) => PERKS[p].name).join(", "));
  return parts.join(" · ");
}

/** The army each side gets in a default skirmish. */
export const DEFAULT_ARMY = Object.freeze(["swordsman", "spearman", "archer", "cavalry", "mage", "healer"]);
