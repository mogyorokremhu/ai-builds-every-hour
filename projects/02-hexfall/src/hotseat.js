// Hot-seat "pass the device" curtain logic: when two humans share a screen under fog of war,
// the board must be hidden between turns so the incoming player does not see the outgoing player's view.

/** Number of human-controlled sides given the two controller values ("human" or an AI level). */
export function humanCount(controllers) {
  return controllers.filter((c) => !c || c === "human").length;
}

/** Does a hot-seat curtain make sense at all? Needs fog and at least two humans. */
export function hotseatActive({ fog, controllers }) {
  return !!fog && humanCount(controllers) >= 2;
}

/**
 * Tracks the curtain. `arm()` is called after a turn ends; the curtain is raised only when the
 * side now to move is human and no winner exists. `reveal()` lowers it.
 */
export class Curtain {
  constructor() { this.up = false; this.side = null; this.turn = 0; }

  arm({ fog, controllers, active, turn, winner }) {
    const humans = controllers.map((c) => !c || c === "human");
    const on = hotseatActive({ fog, controllers }) && winner == null && humans[active];
    this.up = on;
    this.side = on ? active : null;
    this.turn = turn;
    return on;
  }

  reveal() { const was = this.up; this.up = false; return was; }

  /** Text for the curtain card. */
  message(sideNames) {
    if (!this.up) return "";
    return `Turn ${this.turn}: pass the device to ${sideNames[this.side]}. Press Ready when only they are looking.`;
  }
}
