"""Bounding box and aspect ratio of an L-system turtle path per generation."""
import math

RULES = {"F": "F+F-F-F+F"}  # quadratic Koch variant
ANGLE = 90


def expand(axiom: str, rules: dict[str, str], n: int) -> str:
    for _ in range(n):
        axiom = "".join(rules.get(c, c) for c in axiom)
    return axiom


def bbox(s: str, angle: float) -> tuple[float, float, float, float]:
    x = y = 0.0
    heading = 0.0
    stack = []
    xs, ys = [0.0], [0.0]
    for c in s:
        if c in "FG":
            x += math.cos(math.radians(heading))
            y += math.sin(math.radians(heading))
            xs.append(x)
            ys.append(y)
        elif c == "+":
            heading += angle
        elif c == "-":
            heading -= angle
        elif c == "[":
            stack.append((x, y, heading))
        elif c == "]":
            x, y, heading = stack.pop()
    return min(xs), min(ys), max(xs), max(ys)


if __name__ == "__main__":
    print("gen  width  height  aspect")
    for g in range(0, 5):
        x0, y0, x1, y1 = bbox(expand("F", RULES, g), ANGLE)
        w, h = x1 - x0, y1 - y0
        print(f"{g:>3} {w:>6.1f} {h:>7.1f} {w / h if h else float('inf'):>7.2f}")
