"""Mandelbrot set rendered as ASCII art in the terminal (no turtle needed)."""
CHARS = " .:-=+*#%@"
W, H, ITER = 78, 32, 60

for row in range(H):
    line = []
    for col in range(W):
        c = complex(-2.2 + col * 3.2 / W, -1.2 + row * 2.4 / H)
        z, n = 0j, 0
        while abs(z) <= 2 and n < ITER:
            z = z * z + c
            n += 1
        line.append(CHARS[int((n / ITER) * (len(CHARS) - 1))])
    print("".join(line))
