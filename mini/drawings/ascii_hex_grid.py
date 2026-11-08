"""Draw a hexagonal grid of ASCII cells with axial coordinates. Usage: python ascii_hex_grid.py [radius]"""
import sys


def hexagon_rows(radius):
    """Yield text rows of a hexagon-shaped board made of pointy-top cells ('/ \\' roofs)."""
    n = radius
    rows = []
    for r in range(-n, n + 1):
        cells = [q for q in range(-n, n + 1) if abs(q) <= n and abs(r) <= n and abs(q + r) <= n]
        indent = " " * (abs(r) * 2)
        rows.append(indent + "".join(f"<{q:+d},{r:+d}>" for q in cells))
    return rows


def main():
    radius = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    for line in hexagon_rows(radius):
        print(line)
    count = 3 * radius * (radius + 1) + 1
    print(f"\nradius {radius}: {count} hexes")


if __name__ == "__main__":
    main()
