"""CPU scheduling simulator: FCFS, SJF (non-preemptive) and Round Robin."""
from collections import deque

JOBS = [("A", 0, 8), ("B", 1, 4), ("C", 2, 9), ("D", 3, 5)]  # name, arrival, burst


def fcfs(jobs):
    t, done = 0, {}
    for n, a, b in sorted(jobs, key=lambda j: j[1]):
        t = max(t, a) + b
        done[n] = t
    return done


def sjf(jobs):
    pending, t, done = list(jobs), 0, {}
    while pending:
        ready = [j for j in pending if j[1] <= t] or [min(pending, key=lambda j: j[1])]
        j = min(ready, key=lambda j: j[2])
        pending.remove(j)
        t = max(t, j[1]) + j[2]
        done[j[0]] = t
    return done


def round_robin(jobs, quantum=3):
    jobs = sorted(jobs, key=lambda j: j[1])
    rem = {n: b for n, _, b in jobs}
    q, t, i, done = deque(), 0, 0, {}
    while len(done) < len(jobs):
        while i < len(jobs) and jobs[i][1] <= t:
            q.append(jobs[i][0]); i += 1
        if not q:
            t = jobs[i][1]; continue
        n = q.popleft()
        run = min(quantum, rem[n])
        t += run; rem[n] -= run
        while i < len(jobs) and jobs[i][1] <= t:
            q.append(jobs[i][0]); i += 1
        if rem[n]:
            q.append(n)
        else:
            done[n] = t
    return done


def report(name, done, jobs):
    tat = {n: done[n] - a for n, a, _ in jobs}
    wait = {n: tat[n] - b for n, _, b in jobs}
    print(f"{name:12} avg turnaround {sum(tat.values())/len(jobs):5.2f}  avg wait {sum(wait.values())/len(jobs):5.2f}")


if __name__ == "__main__":
    for name, fn in (("FCFS", fcfs), ("SJF", sjf), ("RR (q=3)", round_robin)):
        report(name, fn(JOBS), JOBS)
