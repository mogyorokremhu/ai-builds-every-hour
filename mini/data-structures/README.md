# data-structures

Classic data structures from scratch, standard library only. Each file runs a small demo.

- `heap.py` — array-backed binary min-heap plus heap sort.
- `trie.py` — prefix tree with autocomplete (`python trie.py car`).
- `bloom_filter.py` — Bloom filter sized from n and target false-positive rate.
- `union_find.py` — disjoint-set with path compression and union by rank.
- `lru_cache.py` — LRU cache via hash map + doubly linked list.
- `skip_list.py` — probabilistic sorted set with O(log n) add/remove/lookup.
- `ring_buffer.py` — fixed-capacity circular buffer that overwrites the oldest item.
- `segment_tree.py` — iterative segment tree for range sums with point updates.
- `fenwick_tree.py` — binary indexed tree for prefix/range sums with point updates.
- `linked_deque.py` — doubly linked deque with O(1) operations at both ends.
- `avl_tree.py` — self-balancing AVL BST (rotations), stays O(log n) on sorted input.
- `min_stack.py` — stack that reports its minimum in O(1).
- `monotonic_queue.py` — sliding-window maximum via a monotonic deque.
- `sparse_table.py` — O(1) range-minimum queries after an O(n log n) build.
