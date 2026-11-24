"""Levy C curve drawn in ASCII from an L-system (F -> +F--F+, angle 45 snapped to a grid)."""
RULES = {"F": "+F--F+"}


def expand(n: int) -> str:
    s = "F"
    for _ in range(n):
        s = "".join(RULES.get(c, c) for c in s)
    return s


def draw(n: int = 8) -> str:
    # 8 headings on a grid; diagonal steps move both axes
    dirs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    x = y = h = 0
    pts = {(0, 0)}
    for c in expand(n):
        if c == "F":
            dx, dy = dirs[h]
            x, y = x + dx, y + dy
            pts.add((x, y))
        elif c == "+":
            h = (h + 1) % 8
        elif c == "-":
            h = (h - 1) % 8
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    rows = []
    for yy in range(min(ys), max(ys) + 1):
        rows.append("".join("#" if (xx, yy) in pts else " " for xx in range(min(xs), max(xs) + 1)))
    return "\n".join(rows)


if __name__ == "__main__":
    print(draw(8))
