"""Disk head scheduling: FCFS, SSTF and SCAN total head movement."""

REQUESTS = [98, 183, 37, 122, 14, 124, 65, 67]
HEAD = 53
MAX_CYL = 199


def movement(path):
    return sum(abs(a - b) for a, b in zip(path, path[1:]))


def fcfs(reqs, head):
    return [head] + list(reqs)


def sstf(reqs, head):
    left, path = list(reqs), [head]
    while left:
        nxt = min(left, key=lambda r: abs(r - path[-1]))
        left.remove(nxt); path.append(nxt)
    return path


def scan(reqs, head, max_cyl=MAX_CYL):
    up = sorted(r for r in reqs if r >= head)
    down = sorted((r for r in reqs if r < head), reverse=True)
    return [head] + up + [max_cyl] + down


if __name__ == "__main__":
    for name, fn in (("FCFS", fcfs), ("SSTF", sstf), ("SCAN", scan)):
        p = fn(REQUESTS, HEAD)
        print(f"{name:5} {movement(p):4} cylinders  path: {p}")
