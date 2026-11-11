"""Draw a branching L-system plant on a character grid."""
import math

from expand import expand

W, H = 61, 28


def render(s: str, angle: float = 22.0) -> str:
    grid = [[" "] * W for _ in range(H)]
    x, y, heading = W / 2, H - 1.0, -90.0
    stack = []
    for c in s:
        if c == "F":
            for _ in range(2):
                x += math.cos(math.radians(heading)) * 0.6
                y += math.sin(math.radians(heading)) * 0.6 * 0.5 * 2
                ix, iy = int(round(x)), int(round(y))
                if 0 <= ix < W and 0 <= iy < H:
                    grid[iy][ix] = "|" if abs(math.sin(math.radians(heading))) > 0.8 else "/" if math.cos(math.radians(heading)) > 0 else "\\"
        elif c == "+":
            heading += angle
        elif c == "-":
            heading -= angle
        elif c == "[":
            stack.append((x, y, heading))
        elif c == "]":
            x, y, heading = stack.pop()
    return "\n".join("".join(r).rstrip() for r in grid)


if __name__ == "__main__":
    print(render(expand("X", {"X": "F[+X][-X]FX", "F": "FF"}, 4)))
