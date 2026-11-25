"""Hexagonal tiling math: axial coordinates, distance, neighbours and ring sizes."""

DIRS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]


def neighbors(q: int, r: int) -> list[tuple[int, int]]:
    return [(q + dq, r + dr) for dq, dr in DIRS]


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    dq, dr = a[0] - b[0], a[1] - b[1]
    return (abs(dq) + abs(dr) + abs(dq + dr)) // 2


def ring(radius: int) -> list[tuple[int, int]]:
    if radius == 0:
        return [(0, 0)]
    q, r = -radius, radius  # start at direction 4 * radius
    out = []
    for dq, dr in DIRS:
        for _ in range(radius):
            out.append((q, r))
            q, r = q + dq, r + dr
    return out


if __name__ == "__main__":
    for k in range(5):
        cells = ring(k)
        assert all(distance((0, 0), c) == k for c in cells)
        print(f"ring {k}: {len(cells)} cells")
    assert distance((0, 0), (3, -1)) == 3
    print("checks passed")
