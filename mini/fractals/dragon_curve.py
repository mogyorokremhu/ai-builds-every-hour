"""Heighway dragon curve: paper-folding turn sequence plotted in ASCII."""


def turns(order: int) -> list[int]:
    """Return the turn sequence (+1 left, -1 right) after `order` folds."""
    seq: list[int] = []
    for _ in range(order):
        seq = seq + [1] + [-t for t in reversed(seq)]
    return seq


def path(order: int) -> list[tuple[int, int]]:
    x = y = 0
    dx, dy = 1, 0
    pts = [(x, y)]
    x, y = x + dx, y + dy
    pts.append((x, y))
    for t in turns(order):
        dx, dy = (-dy, dx) if t == 1 else (dy, -dx)
        x, y = x + dx, y + dy
        pts.append((x, y))
    return pts


def render(order: int = 9) -> str:
    pts = path(order)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, y0 = min(xs), min(ys)
    w, h = max(xs) - x0 + 1, max(ys) - y0 + 1
    grid = [[" "] * (2 * w - 1) for _ in range(h)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        ax, ay, bx, by = ax - x0, ay - y0, bx - x0, by - y0
        grid[ay][2 * ax] = grid[by][2 * bx] = "+"
        if ay == by:
            grid[ay][ax + bx] = "-"
        else:
            grid[(ay + by) // 2][2 * ax] = "|"
    return "\n".join("".join(r).rstrip() for r in grid)


if __name__ == "__main__":
    print(render(8))
