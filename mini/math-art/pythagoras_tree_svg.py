"""Pythagoras tree: recursive squares with right-triangle branching, written to an SVG file."""
import math
import sys


def square(p, q, out, depth, max_depth, angle):
    """Draw the square on edge p->q (left to right, drawn upward) then recurse."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    p4 = (p[0] - dy, p[1] + dx)
    q4 = (q[0] - dy, q[1] + dx)
    g = int(80 + 150 * depth / max_depth)
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in (p, q, q4, p4))
    out.append(f'<polygon points="{pts}" fill="rgb(60,{g},50)" stroke="#222" stroke-width="0.3"/>')
    if depth >= max_depth:
        return
    # apex of the right triangle sitting on the top edge p4->q4
    c = math.cos(angle)
    ex, ey = q4[0] - p4[0], q4[1] - p4[1]
    apex = (p4[0] + c * (c * ex - math.sin(angle) * ey), p4[1] + c * (math.sin(angle) * ex + c * ey))
    square(p4, apex, out, depth + 1, max_depth, angle)
    square(apex, q4, out, depth + 1, max_depth, angle)


def build(max_depth: int = 10, angle_deg: float = 40.0) -> str:
    out = []
    square((-50.0, 0.0), (50.0, 0.0), out, 0, max_depth, math.radians(angle_deg))
    body = "\n".join(out)
    # y points up in the maths; flip it for SVG
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-200 -260 400 300">'
            f'<g transform="scale(1,-1)">{body}</g></svg>')


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "pythagoras_tree.svg"
    with open(path, "w") as f:
        f.write(build())
    print("wrote", path)
