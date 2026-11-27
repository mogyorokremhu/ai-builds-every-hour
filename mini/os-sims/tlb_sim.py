"""TLB hit-rate simulation with LRU replacement and effective access time."""
from collections import OrderedDict


def tlb_hit_rate(pages, size):
    tlb, hits = OrderedDict(), 0
    for p in pages:
        if p in tlb:
            hits += 1
            tlb.move_to_end(p)
        else:
            if len(tlb) >= size:
                tlb.popitem(last=False)
            tlb[p] = True
    return hits / len(pages)


def effective_access_time(hit, tlb_ns=10, mem_ns=100):
    return hit * (tlb_ns + mem_ns) + (1 - hit) * (tlb_ns + 2 * mem_ns)


if __name__ == "__main__":
    refs = [1, 2, 3, 1, 2, 4, 1, 2, 3, 4, 1, 2] * 3
    for n in (1, 2, 4, 8):
        h = tlb_hit_rate(refs, n)
        print(f"size={n} hit={h:.2%} EAT={effective_access_time(h):.1f}ns")
    assert tlb_hit_rate([1, 1, 1], 1) == 2 / 3
    assert tlb_hit_rate(refs, 4) > tlb_hit_rate(refs, 1)
