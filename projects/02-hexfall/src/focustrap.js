// Focus trap logic for the menu dialog (pure: works on arrays of focusable ids/elements).

export const FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

/** Index to focus after Tab / Shift+Tab inside a trap of `count` items; `current` is -1 when focus is outside. */
export function nextIndex(current, count, shift = false) {
  if (count <= 0) return -1;
  if (current < 0) return shift ? count - 1 : 0;
  return shift ? (current - 1 + count) % count : (current + 1) % count;
}

/** Should the Tab key be intercepted? Only when it would leave the trap. */
export function wouldEscape(current, count, shift = false) {
  if (count <= 0) return false;
  if (current < 0) return true;
  return shift ? current === 0 : current === count - 1;
}

/** Install a trap on `root`; returns { release }. `doc` defaults to the global document. */
export function trapFocus(root, doc = globalThis.document) {
  const prev = doc.activeElement;
  const items = () => [...root.querySelectorAll(FOCUSABLE)].filter((e) => !e.hidden);
  const onKey = (ev) => {
    if (ev.key !== "Tab") return;
    const list = items();
    const cur = list.indexOf(doc.activeElement);
    if (!wouldEscape(cur, list.length, ev.shiftKey)) return;
    ev.preventDefault();
    list[nextIndex(cur, list.length, ev.shiftKey)]?.focus();
  };
  root.addEventListener("keydown", onKey);
  items()[0]?.focus();
  return {
    release() {
      root.removeEventListener("keydown", onKey);
      prev?.focus?.();
    },
  };
}
