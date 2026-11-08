// Touch support without touching main.js: recognise gestures with TouchGestures and replay them as the
// synthetic mouse / wheel events main.js already understands (tap = click, pan = drag, pinch = wheel zoom,
// long-press = hover tooltip).
import { TouchGestures } from "./touch.js";
import { pinchSteps } from "./pinch.js";

const canvas = document.getElementById("board");
if (canvas) {
  canvas.style.touchAction = "none";
  const g = new TouchGestures();
  const pos = new Map();
  let dragging = false, last = { x: 0, y: 0 }, acc = 0;

  const mouse = (type, x, y, target = canvas) =>
    target.dispatchEvent(new MouseEvent(type, { bubbles: true, clientX: x, clientY: y, button: 0 }));
  const wheel = (x, y, dir) =>
    canvas.dispatchEvent(new WheelEvent("wheel", { bubbles: true, cancelable: true, clientX: x, clientY: y, deltaY: dir }));
  const isTouch = (ev) => ev.pointerType === "touch" || ev.pointerType === "pen";

  canvas.addEventListener("pointerdown", (ev) => {
    if (!isTouch(ev)) return;
    canvas.setPointerCapture?.(ev.pointerId);
    pos.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
    last = { x: ev.clientX, y: ev.clientY };
    g.down(ev.pointerId, ev.clientX, ev.clientY, ev.timeStamp);
  });
  canvas.addEventListener("pointermove", (ev) => {
    if (!isTouch(ev) || !pos.has(ev.pointerId)) return;
    pos.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
    const r = g.move(ev.pointerId, ev.clientX, ev.clientY);
    if (!r) return;
    if (r.type === "pan") {
      if (!dragging) { mouse("mousedown", last.x, last.y); dragging = true; }
      mouse("mousemove", ev.clientX, ev.clientY);
    } else if (r.type === "pinch") {
      const pts = [...pos.values()];
      const cx = (pts[0].x + pts[1].x) / 2, cy = (pts[0].y + pts[1].y) / 2;
      const s = pinchSteps(acc, r.factor);
      acc = s.acc;
      for (let i = 0; i < Math.abs(s.steps); i++) wheel(cx, cy, s.steps > 0 ? -1 : 1);
    }
    last = { x: ev.clientX, y: ev.clientY };
  });
  const end = (ev) => {
    if (!isTouch(ev)) return;
    const r = g.up(ev.pointerId, ev.clientX, ev.clientY, ev.timeStamp);
    pos.delete(ev.pointerId);
    if (dragging && pos.size === 0) { mouse("mouseup", ev.clientX, ev.clientY); dragging = false; }
    if (pos.size === 0) acc = 0;
    if (!r) return;
    if (r.type === "tap") { mouse("mousedown", r.x, r.y); mouse("mouseup", r.x, r.y); }
    else if (r.type === "longpress") mouse("mousemove", r.x, r.y);
  };
  canvas.addEventListener("pointerup", end);
  canvas.addEventListener("pointercancel", (ev) => {
    if (!isTouch(ev)) return;
    g.cancel(); pos.clear(); acc = 0;
    if (dragging) { mouse("mouseup", ev.clientX, ev.clientY); dragging = false; }
  });
}
