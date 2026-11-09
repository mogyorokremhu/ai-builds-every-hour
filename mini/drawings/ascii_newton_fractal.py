"""Newton fractal for z^3 - 1: basin of each root gets its own glyph.  python ascii_newton_fractal.py"""

def main(w: int = 72, h: int = 30, iters: int = 20) -> None:
    roots = [1, complex(-0.5, 3 ** 0.5 / 2), complex(-0.5, -(3 ** 0.5) / 2)]
    glyphs = "#o+"
    for j in range(h):
        row = ""
        for i in range(w):
            z = complex(-1.6 + 3.2 * i / w, -1.2 + 2.4 * j / h)
            ch = " "
            for _ in range(iters):
                if z == 0:
                    break
                z -= (z ** 3 - 1) / (3 * z ** 2)
                k = next((n for n, r in enumerate(roots) if abs(z - r) < 1e-3), None)
                if k is not None:
                    ch = glyphs[k]
                    break
            row += ch
        print(row)

if __name__ == "__main__":
    main()
