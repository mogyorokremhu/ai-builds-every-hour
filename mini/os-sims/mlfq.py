"""Multi-level feedback queue scheduler simulation."""
from collections import deque


def mlfq(jobs, quanta=(2, 4, 8)):
    """jobs: list of (name, arrival, burst). Returns {name: finish_time}.

    Jobs start in the top queue; using a full quantum demotes them one level.
    Higher queues always run first (non-preemptive within a quantum).
    """
    jobs = sorted(jobs, key=lambda j: j[1])
    queues = [deque() for _ in quanta]
    remaining = {n: b for n, _, b in jobs}
    finish, t, i = {}, 0, 0
    while len(finish) < len(jobs):
        while i < len(jobs) and jobs[i][1] <= t:
            queues[0].append(jobs[i][0])
            i += 1
        level = next((l for l, q in enumerate(queues) if q), None)
        if level is None:
            t = jobs[i][1]
            continue
        name = queues[level].popleft()
        run = min(quanta[level], remaining[name])
        t += run
        remaining[name] -= run
        while i < len(jobs) and jobs[i][1] <= t:
            queues[0].append(jobs[i][0])
            i += 1
        if remaining[name] == 0:
            finish[name] = t
        else:
            queues[min(level + 1, len(quanta) - 1)].append(name)
    return finish


if __name__ == "__main__":
    res = mlfq([("A", 0, 10), ("B", 1, 3), ("C", 2, 6)])
    assert res == {"B": 11, "C": 15, "A": 19}, res
    print(res)
