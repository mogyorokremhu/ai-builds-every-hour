"""Three interfering sine waves and their sum, drawn in ASCII. Usage: python ascii_sine_waves.py"""
import math

W, H = 72, 21
WAVES = [(1.0, 0.07, 0.0, "."), (0.6, 0.19, 1.0, ":"), (0.35, 0.41, 2.0, "-")]


def render():
    grid = [[" "] * W for _ in range(H)]
    for x in range(W):
        grid[H // 2][x] = "·"
    for amp, freq, phase, ch in WAVES:
        for x in range(W):
            y = H // 2 - round(amp * math.sin(x * freq * 2 * math.pi + phase) * (H // 2 - 1) / 1.95)
            if 0 <= y < H:
                grid[y][x] = ch
    for x in range(W):
        total = sum(a * math.sin(x * f * 2 * math.pi + p) for a, f, p, _ in WAVES)
        y = H // 2 - round(total * (H // 2 - 1) / 1.95)
        if 0 <= y < H:
            grid[y][x] = "#"
    return "\n".join("".join(r) for r in grid)


if __name__ == "__main__":
    print(render())
