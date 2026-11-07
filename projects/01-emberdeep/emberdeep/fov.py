"""Recursive shadowcasting field of view (8 octants)."""
from __future__ import annotations

from .gamemap import GameMap

_OCTANTS = (
    (1, 0, 0, 1), (0, 1, 1, 0), (0, -1, 1, 0), (-1, 0, 0, 1),
    (-1, 0, 0, -1), (0, -1, -1, 0), (0, 1, -1, 0), (1, 0, 0, -1),
)


def compute_fov(gmap: GameMap, ox: int, oy: int, radius: int) -> None:
    """Recompute gmap.visible from origin (ox, oy)."""
    gmap.clear_visibility()
    gmap.mark_visible(ox, oy)
    for xx, xy, yx, yy in _OCTANTS:
        _cast(gmap, ox, oy, 1, 1.0, 0.0, radius, xx, xy, yx, yy)


def _cast(gmap, cx, cy, row, start, end, radius, xx, xy, yx, yy) -> None:
    if start < end:
        return
    r2 = radius * radius
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
            if dx * dx + dy * dy < r2:
                gmap.mark_visible(mx, my)
            if blocked:
                if not gmap.transparent(mx, my):
                    new_start = r_slope
                    continue
                blocked = False
                start = new_start
            elif not gmap.transparent(mx, my) and j < radius:
                blocked = True
                _cast(gmap, cx, cy, j + 1, start, l_slope, radius, xx, xy, yx, yy)
                new_start = r_slope
        if blocked:
            break
