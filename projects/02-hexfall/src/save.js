// Saving and loading games: JSON text, storage slots (localStorage or any Storage-like object).
import { Game } from "./game.js";

export const SLOT_PREFIX = "hexfall.save.";

/** Serialise a game to pretty JSON text (also the export file format). */
export function serialize(game) {
  return JSON.stringify(game.toJSON());
}

/** Parse save text back into a Game; throws a readable Error for bad input. */
export function deserialize(text) {
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error("not a Hexfall save (invalid JSON)");
  }
  return Game.fromJSON(data);
}

/**
 * Write `game` to `slot` of `storage` (anything with getItem/setItem/removeItem/key/length,
 * e.g. window.localStorage). Stores a small header for the slot list.
 */
export function saveToSlot(storage, slot, game) {
  const meta = { slot, savedAt: new Date().toISOString(), turn: game.turn, side: game.side, seed: game.seed, winner: game.winner };
  storage.setItem(SLOT_PREFIX + slot, JSON.stringify({ meta, game: game.toJSON() }));
  return meta;
}

/** Load the game in `slot`, or null when the slot is empty. */
export function loadFromSlot(storage, slot) {
  const raw = storage.getItem(SLOT_PREFIX + slot);
  if (raw == null) return null;
  return Game.fromJSON(JSON.parse(raw).game);
}

export function deleteSlot(storage, slot) {
  storage.removeItem(SLOT_PREFIX + slot);
}

/** Headers of every saved slot, newest first. */
export function listSlots(storage) {
  const out = [];
  for (let i = 0; i < storage.length; i++) {
    const k = storage.key(i);
    if (!k || !k.startsWith(SLOT_PREFIX)) continue;
    try {
      out.push(JSON.parse(storage.getItem(k)).meta);
    } catch {
      // ignore corrupt slots
    }
  }
  return out.sort((a, b) => (a.savedAt < b.savedAt ? 1 : -1));
}

/** A tiny in-memory Storage (for tests and when localStorage is unavailable). */
export class MemoryStorage {
  constructor() {
    this.data = new Map();
  }
  get length() {
    return this.data.size;
  }
  key(i) {
    return [...this.data.keys()][i] ?? null;
  }
  getItem(k) {
    return this.data.has(k) ? this.data.get(k) : null;
  }
  setItem(k, v) {
    this.data.set(k, String(v));
  }
  removeItem(k) {
    this.data.delete(k);
  }
}
