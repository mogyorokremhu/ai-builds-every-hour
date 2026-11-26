"""Page replacement: FIFO, LRU and Optimal fault counts on a reference string."""

REFS = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]


def fifo(refs, frames):
    mem, faults = [], 0
    for r in refs:
        if r not in mem:
            faults += 1
            if len(mem) == frames:
                mem.pop(0)
            mem.append(r)
    return faults


def lru(refs, frames):
    mem, faults = [], 0
    for r in refs:
        if r in mem:
            mem.remove(r)
        else:
            faults += 1
            if len(mem) == frames:
                mem.pop(0)
        mem.append(r)
    return faults


def optimal(refs, frames):
    mem, faults = [], 0
    for i, r in enumerate(refs):
        if r in mem:
            continue
        faults += 1
        if len(mem) == frames:
            def nxt(p):
                rest = refs[i + 1:]
                return rest.index(p) if p in rest else len(refs) + 1
            mem.remove(max(mem, key=nxt))
        mem.append(r)
    return faults


if __name__ == "__main__":
    print("frames  FIFO  LRU  OPT")
    for f in range(1, 6):
        print(f"{f:6}  {fifo(REFS, f):4}  {lru(REFS, f):3}  {optimal(REFS, f):3}")
