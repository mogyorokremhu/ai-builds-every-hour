// Pure helper: turn continuous pinch scale factors into discrete wheel-zoom steps (main.js zooms ×1.15 per wheel tick).
export const WHEEL_STEP = 1.15;

/** acc is the accumulated log-scale so far. Returns { steps, acc }: steps > 0 zoom in, < 0 zoom out (integers). */
export function pinchSteps(acc, factor, step = WHEEL_STEP) {
  if (!(factor > 0)) return { steps: 0, acc };
  const unit = Math.log(step);
  let a = acc + Math.log(factor);
  const steps = Math.trunc(a / unit);
  a -= steps * unit;
  return { steps, acc: a };
}
