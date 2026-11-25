"""Prim's minimum spanning tree with a heap."""
import heapq

GRAPH = {
    "A": {"B": 4, "H": 8}, "B": {"A": 4, "C": 8, "H": 11}, "C": {"B": 8, "D": 7, "F": 4, "I": 2},
    "D": {"C": 7, "E": 9, "F": 14}, "E": {"D": 9, "F": 10}, "F": {"C": 4, "D": 14, "E": 10, "G": 2},
    "G": {"F": 2, "H": 1, "I": 6}, "H": {"A": 8, "B": 11, "G": 1, "I": 7}, "I": {"C": 2, "G": 6, "H": 7},
}


def prim(graph: dict, start: str) -> list[tuple[str, str, int]]:
    """Return MST edges (u, v, weight)."""
    seen = {start}
    heap = [(w, start, v) for v, w in graph[start].items()]
    heapq.heapify(heap)
    edges = []
    while heap and len(seen) < len(graph):
        w, u, v = heapq.heappop(heap)
        if v in seen:
            continue
        seen.add(v)
        edges.append((u, v, w))
        for x, wx in graph[v].items():
            if x not in seen:
                heapq.heappush(heap, (wx, v, x))
    return edges


if __name__ == "__main__":
    mst = prim(GRAPH, "A")
    for u, v, w in mst:
        print(f"{u}-{v} ({w})")
    print("total weight:", sum(w for _, _, w in mst))
