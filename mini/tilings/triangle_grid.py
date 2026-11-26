"""Triangular tiling: triangle counts in a big triangle and ASCII rendering."""


def triangle_count(n: int) -> int:
    """Total triangles (all sizes) in a triangular grid of side n."""
    return n * (n + 2) * (2 * n + 1) // 8


def render(n: int) -> str:
    rows = []
    for r in range(n):
        up = " " * (n - r - 1) + "/\\" * (r + 1)
        down = " " * (n - r - 1) + "".join("/_" if i == 0 else "\\/_" for i in range(r + 1))
        rows.append(up if r % 2 == 0 else down)
    return "\n".join(rows)


if __name__ == "__main__":
    assert [triangle_count(k) for k in (1, 2, 3, 4)] == [1, 5, 13, 27]
    for k in range(1, 6):
        print(k, triangle_count(k))
    print(render(4))
