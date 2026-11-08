// "Show all" spectator toggle: lets a hot-seat reviewer see through fog without changing the game state.

/** Effective fog viewer: the real viewer unless show-all is on. */
export function effectiveViewer(viewer, showAll) {
  return showAll ? null : viewer;
}

/** Label for the toggle depending on whether fog is even enabled. */
export function toggleLabel(fogOn, showAll) {
  if (!fogOn) return "Show all (fog off)";
  return showAll ? "Fog: showing all" : "Fog: normal view";
}

/** Ask for confirmation only when turning show-all on mid human-vs-human battle (it reveals the other side). */
export function needsConfirm(humanSides, showAll) {
  return !showAll && humanSides >= 2;
}
