"""Projectile motion: range, peak height and flight time, plus an ASCII trajectory."""
import math
import sys

G = 9.81


def trajectory(speed: float, angle_deg: float, h0: float = 0.0) -> dict[str, float]:
    """Return flight time, range and max height for a launch (no air drag)."""
    a = math.radians(angle_deg)
    vx, vy = speed * math.cos(a), speed * math.sin(a)
    t = (vy + math.sqrt(vy * vy + 2 * G * h0)) / G
    return {"time": t, "range": vx * t, "peak": h0 + vy * vy / (2 * G)}


def plot(speed: float, angle_deg: float, width: int = 60, height: int = 14) -> str:
    """Draw the path as ASCII art."""
    info = trajectory(speed, angle_deg)
    a = math.radians(angle_deg)
    grid = [[" "] * width for _ in range(height)]
    for i in range(width):
        t = info["time"] * i / (width - 1)
        y = speed * math.sin(a) * t - 0.5 * G * t * t
        row = height - 1 - round(y / max(info["peak"], 1e-9) * (height - 1))
        if 0 <= row < height:
            grid[row][i] = "*"
    return "\n".join("".join(r) for r in grid) + "\n" + "-" * width


if __name__ == "__main__":
    v = float(sys.argv[1]) if len(sys.argv) > 1 else 30.0
    ang = float(sys.argv[2]) if len(sys.argv) > 2 else 45.0
    print(plot(v, ang))
    for k, val in trajectory(v, ang).items():
        print(f"{k:>5}: {val:.2f}")
