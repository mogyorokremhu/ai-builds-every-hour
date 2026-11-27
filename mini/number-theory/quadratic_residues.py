"""Quadratic residues mod n: list them, count them and show the multiplication pattern."""
import sys


def residues(n: int) -> list[int]:
    """Sorted distinct squares mod n."""
    return sorted({(x * x) % n for x in range(n)})


def is_primitive_root(g: int, p: int) -> bool:
    """True if g generates all of (Z/pZ)* for prime p."""
    seen, x = set(), 1
    for _ in range(p - 1):
        x = x * g % p
        seen.add(x)
    return len(seen) == p - 1


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 23
    r = residues(n)
    print(f"squares mod {n}: {r} ({len(r)} of {n})")
    if all(n % d for d in range(2, int(n ** 0.5) + 1)) and n > 2:
        assert len(r) == (n + 1) // 2  # 0 plus (n-1)/2 non-zero residues
        roots = [g for g in range(2, n) if is_primitive_root(g, n)]
        print("primitive roots:", roots)
        print("Euler criterion check:", all(pow(a, (n - 1) // 2, n) == 1 for a in r if a))
