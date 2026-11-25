"""Matrix transpose, multiplication and identity helpers."""


def transpose(m: list[list]) -> list[list]:
    """Swap rows and columns."""
    return [list(col) for col in zip(*m)]


def identity(n: int) -> list[list[int]]:
    """n x n identity matrix."""
    return [[int(i == j) for j in range(n)] for i in range(n)]


def multiply(a: list[list], b: list[list]) -> list[list]:
    """Matrix product a @ b."""
    if len(a[0]) != len(b):
        raise ValueError("shape mismatch")
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


if __name__ == "__main__":
    a = [[1, 2, 3], [4, 5, 6]]
    assert transpose(a) == [[1, 4], [2, 5], [3, 6]]
    assert multiply(a, transpose(a)) == [[14, 32], [32, 77]]
    assert multiply(identity(2), a) == a
    print("A * A^T =", multiply(a, transpose(a)))
    print("ok")
