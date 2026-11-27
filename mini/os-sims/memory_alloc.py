"""Contiguous memory allocation: first-fit, best-fit, worst-fit. Usage: python memory_alloc.py"""
from __future__ import annotations


def allocate(blocks: list[int], procs: list[int], strategy: str) -> list[int]:
    """Return the block index for each process (-1 if it doesn't fit)."""
    free = blocks[:]
    out = []
    for size in procs:
        cands = [i for i, b in enumerate(free) if b >= size]
        if not cands:
            out.append(-1)
            continue
        if strategy == "first":
            i = cands[0]
        elif strategy == "best":
            i = min(cands, key=lambda k: free[k])
        elif strategy == "worst":
            i = max(cands, key=lambda k: free[k])
        else:
            raise ValueError(strategy)
        free[i] -= size
        out.append(i)
    return out


if __name__ == "__main__":
    blocks, procs = [100, 500, 200, 300, 600], [212, 417, 112, 426]
    for s in ("first", "best", "worst"):
        res = allocate(blocks, procs, s)
        print(f"{s:>5}-fit:", ", ".join(f"{p}->{'B%d' % r if r >= 0 else 'wait'}" for p, r in zip(procs, res)))
