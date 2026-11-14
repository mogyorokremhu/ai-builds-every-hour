"""Hilbert curve from an L-system, drawn with box characters."""


def expand(n: int) -> str:
    s = "A"
    for _ in range(n):
        s = "".join({"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"}.get(c, c) for c in s)
    return s


def render(n: int = 3) -> str:
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    d, x, y = 0, 0, 0
    visited = [(0, 0)]
    for c in expand(n):
        if c == "+":
            d = (d + 1) % 4
        elif c == "-":
            d = (d - 1) % 4
        elif c == "F":
            x += dirs[d][0]
            y += dirs[d][1]
            visited.append((x, y))
    size = 2 ** n
    # grid cells at even coordinates, connectors between them
    W, H = size * 2 - 1, size * 2 - 1
    g = [[" "] * W for _ in range(H)]
    for (ax, ay), (bx, by) in zip(visited, visited[1:]):
        g[ay * 2][ax * 2] = "+"
        g[by * 2][bx * 2] = "+"
        g[ay + by][ax + bx] = "-" if ay == by else "|"
    return "\n".join("".join(r).rstrip() for r in g)


if __name__ == "__main__":
    print(render(3))
