"""Modular times-table string art: chords i -> k*i mod n. k=2 gives a cardioid, k=3 a nephroid."""
import math
import sys


def build(n: int = 200, k: int = 2, size: int = 400) -> str:
    r = size / 2 - 10
    c = size / 2
    pts = [(c + r * math.cos(2 * math.pi * i / n), c + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    lines = [f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="#888"/>']
    for i in range(n):
        j = (i * k) % n
        lines.append(f'<line x1="{pts[i][0]:.1f}" y1="{pts[i][1]:.1f}" x2="{pts[j][0]:.1f}" y2="{pts[j][1]:.1f}" '
                     f'stroke="hsl({360 * i / n:.0f},70%,50%)" stroke-width="0.6"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
            f'<rect width="100%" height="100%" fill="#111"/>' + "".join(lines) + "</svg>")


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    path = sys.argv[2] if len(sys.argv) > 2 else f"times_table_{k}.svg"
    with open(path, "w") as f:
        f.write(build(k=k))
    print("wrote", path)
