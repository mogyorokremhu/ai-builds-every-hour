"""Simulate colour-vision deficiencies on a hex colour (Machado-style linear matrices).

Usage: python color_blind.py [#rrggbb]
"""
import sys

MATRICES = {
    "protanopia": ((0.152, 1.053, -0.205), (0.115, 0.786, 0.099), (-0.004, -0.048, 1.052)),
    "deuteranopia": ((0.367, 0.861, -0.228), (0.280, 0.673, 0.047), (-0.012, 0.043, 0.969)),
    "tritanopia": ((1.256, -0.077, -0.179), (-0.078, 0.931, 0.148), (0.005, 0.691, 0.304)),
}


def simulate(rgb: tuple[int, int, int], kind: str) -> tuple[int, int, int]:
    m = MATRICES[kind]
    out = [sum(row[i] * rgb[i] for i in range(3)) for row in m]
    return tuple(max(0, min(255, round(v))) for v in out)  # type: ignore[return-value]


if __name__ == "__main__":
    h = (sys.argv[1] if len(sys.argv) > 1 else "#ff7f50").lstrip("#")
    rgb = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    assert simulate((255, 255, 255), "deuteranopia")[1] in range(250, 256)
    for kind in MATRICES:
        r, g, b = simulate(rgb, kind)
        print(f"{kind:13} #{r:02x}{g:02x}{b:02x}  \x1b[48;2;{r};{g};{b}m    \x1b[0m")
