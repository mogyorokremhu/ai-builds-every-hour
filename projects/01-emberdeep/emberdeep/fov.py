"""Recursive shadowcasting field of view (8 octants)."""
from __future__ import annotations

from .gamemap import GameMap

_OCTANTS = (
    (1, 0, 0, 1), (0, 1, 1, 0), (0, -1, 1, 0), (-1, 0, 0, 1),
    (-1, 0, 0, -1), (0, -1, -1, 0), (0, 1, -1, 0), (1, 0, 0, -1),
)


#: How far you can see into a lit area (braziers) beyond your own torchlight.
LIT_SIGHT = 20


def compute_fov(gmap: GameMap, ox: int, oy: int, radius: int,
                lit: "set[tuple[int, int]] | frozenset | None" = None) -> None:
    """Recompute gmap.visible from origin (ox, oy).

    Cells within ``radius`` (your light) are visible when in line of sight. If ``lit`` is
    given, cells in that set are also visible up to :data:`LIT_SIGHT` away — you can see
    into a brightly lit room from the dark.
    """
    gmap.clear_visibility()
    gmap.mark_visible(ox, oy)
    reach = max(radius, LIT_SIGHT) if lit else radius
    for xx, xy, yx, yy in _OCTANTS:
        _cast(gmap, ox, oy, 1, 1.0, 0.0, reach, xx, xy, yx, yy, radius, lit)


def _cast(gmap, cx, cy, row, start, end, radius, xx, xy, yx, yy, light=None, lit=None) -> None:
    if start < end:
        return
    r2 = radius * radius
    l2 = (radius if light is None else light) ** 2
    new_start = start
    for j in range(row, radius + 1):
        dx, dy = -j - 1, -j
        blocked = False
        while dx <= 0:
            dx += 1
            mx, my = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
            l_slope = (dx - 0.5) / (dy + 0.5)
            r_slope = (dx + 0.5) / (dy - 0.5)
            if start < r_slope:
                continue
            if end > l_slope:
                break
            d2 = dx * dx + dy * dy
            if d2 < r2 and (d2 < l2 or (lit is not None and (mx, my) in lit)):
                gmap.mark_visible(mx, my)
            if blocked:
                if not gmap.transparent(mx, my):
                    new_start = r_slope
                    continue
                blocked = False
                start = new_start
            elif not gmap.transparent(mx, my) and j < radius:
                blocked = True
                _cast(gmap, cx, cy, j + 1, start, l_slope, radius, xx, xy, yx, yy, light, lit)
                new_start = r_slope
        if blocked:
            break
