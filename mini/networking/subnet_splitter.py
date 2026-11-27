"""VLSM planner: split a parent network into subnets sized for host counts.

Usage: python subnet_splitter.py 192.168.0.0/24 100 50 20 10
(no args: demo with self-check)
"""
import sys


def ip_to_int(ip: str) -> int:
    a, b, c, d = (int(p) for p in ip.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def int_to_ip(n: int) -> str:
    return ".".join(str((n >> s) & 255) for s in (24, 16, 8, 0))


def plan(parent: str, host_counts: list[int]) -> list[tuple[str, int, int]]:
    """Allocate largest-first; returns (name, base_int, prefix) list."""
    ip, _, bits = parent.partition("/")
    base, size = ip_to_int(ip), 1 << (32 - int(bits))
    base &= ~(size - 1) & 0xFFFFFFFF
    cur, out = base, []
    for need in sorted(host_counts, reverse=True):
        block = 4
        while block - 2 < need:
            block <<= 1
        cur = (cur + block - 1) // block * block  # align
        if cur + block > base + size:
            raise ValueError("parent network too small")
        out.append((f"{need} hosts", cur, 32 - (block.bit_length() - 1)))
        cur += block
    return out


def main(args: list[str]) -> None:
    if args:
        res = plan(args[0], [int(a) for a in args[1:]])
    else:
        res = plan("192.168.0.0/24", [100, 50, 20, 10])
        assert [(int_to_ip(b), p) for _, b, p in res] == [
            ("192.168.0.0", 25), ("192.168.0.128", 26),
            ("192.168.0.192", 27), ("192.168.0.224", 28)]
    for name, b, p in res:
        print(f"{name:>10} -> {int_to_ip(b)}/{p}")


if __name__ == "__main__":
    main(sys.argv[1:])
