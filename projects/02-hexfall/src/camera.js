// Camera: zoom and pan on top of the base "fit the whole map" layout. Pure functions so
// the maths can be tested in node; main.js wires them to the mouse wheel and dragging.

export const MIN_ZOOM = 1;
export const MAX_ZOOM = 4;

/** A camera over `base` (from render.fitLayout): zoom factor and pan offset in pixels. */
export function camera(base) {
  return { base, zoom: 1, panX: 0, panY: 0 };
}

/** The effective layout ({size, ox, oy}) the renderer should use. */
export function view(cam) {
  const { base, zoom } = cam;
  return { size: base.size * zoom, ox: base.ox * zoom + cam.panX, oy: base.oy * zoom + cam.panY };
}

/**
 * Zoom by `factor` keeping the screen point (px, py) fixed under the cursor.
 * Returns a new camera (zoom clamped to [MIN_ZOOM, MAX_ZOOM]).
 */
export function zoomAt(cam, factor, px, py, viewport) {
  const zoom = Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, cam.zoom * factor));
  const k = zoom / cam.zoom;
  // world point under the cursor stays put: p = o + w*z  =>  o' = p - (p - o) * k
  const v = view(cam);
  const ox = px - (px - v.ox) * k;
  const oy = py - (py - v.oy) * k;
  const next = { ...cam, zoom, panX: ox - cam.base.ox * zoom, panY: oy - cam.base.oy * zoom };
  return viewport ? clamp(next, viewport) : next;
}

export function panBy(cam, dx, dy, viewport) {
  const next = { ...cam, panX: cam.panX + dx, panY: cam.panY + dy };
  return viewport ? clamp(next, viewport) : next;
}

/**
 * Keep the map on screen: at zoom 1 there is no panning; zoomed in, the scaled map
 * (viewport × zoom) may slide only until its edge meets the viewport edge.
 */
export function clamp(cam, viewport) {
  const { width, height } = viewport;
  const minX = width - width * cam.zoom, minY = height - height * cam.zoom;
  return {
    ...cam,
    panX: Math.min(0, Math.max(minX, cam.panX)),
    panY: Math.min(0, Math.max(minY, cam.panY)),
  };
}

/** The visible part of the map as a rectangle in base (zoom 1) pixel coordinates — the
 *  box the minimap draws. */
export function visibleRect(cam, viewport) {
  return {
    x: -cam.panX / cam.zoom,
    y: -cam.panY / cam.zoom,
    w: viewport.width / cam.zoom,
    h: viewport.height / cam.zoom,
  };
}

/** Centre the camera on base-pixel point (bx, by) — used when clicking the minimap. */
export function centerOn(cam, bx, by, viewport) {
  const next = { ...cam, panX: viewport.width / 2 - bx * cam.zoom, panY: viewport.height / 2 - by * cam.zoom };
  return clamp(next, viewport);
}
