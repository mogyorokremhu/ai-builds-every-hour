"""Dijkstra's shortest paths on a small weighted graph."""
import heapq

GRAPH = {
    "A": {"B": 7, "C": 9, "F": 14},
    "B": {"A": 7, "C": 10, "D": 15},
    "C": {"A": 9, "B": 10, "D": 11, "F": 2},
    "D": {"B": 15, "C": 11, "E": 6},
    "E": {"D": 6, "F": 9},
    "F": {"A": 14, "C": 2, "E": 9},
}


def dijkstra(graph, src):
    """Return (distance, predecessor) dicts from src."""
    dist = {n: float("inf") for n in graph}
    dist[src] = 0
    prev = {}
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u].items():
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev


def path(prev, dst):
    out = [dst]
    while out[-1] in prev:
        out.append(prev[out[-1]])
    return out[::-1]


if __name__ == "__main__":
    dist, prev = dijkstra(GRAPH, "A")
    for n in sorted(dist):
        print(n, dist[n], "->".join(path(prev, n)))
