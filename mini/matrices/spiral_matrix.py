"""Generate an n x n spiral matrix and read any matrix in spiral order."""


def spiral(n):
    m = [[0] * n for _ in range(n)]
    r = c = 0
    dr, dc = 0, 1
    for k in range(1, n * n + 1):
        m[r][c] = k
        nr, nc = r + dr, c + dc
        if not (0 <= nr < n and 0 <= nc < n) or m[nr][nc]:
            dr, dc = dc, -dr
            nr, nc = r + dr, c + dc
        r, c = nr, nc
    return m


def read_spiral(m):
    out = []
    m = [row[:] for row in m]
    while m:
        out += m.pop(0)
        m = [list(r) for r in zip(*m)][::-1]
    return out


if __name__ == "__main__":
    s = spiral(4)
    assert s[0] == [1, 2, 3, 4] and s[1][3] == 5
    assert read_spiral(s) == list(range(1, 17))
    for row in s:
        print(" ".join(f"{x:2}" for x in row))
