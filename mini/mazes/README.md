# mazes

Maze generation and solving in the terminal (standard library only).

- `recursive_backtracker.py` — perfect maze via randomized DFS: `python recursive_backtracker.py [w h seed]`.
- `maze_solver.py` — generates a maze and draws the BFS shortest path with dots.
- `kruskal_maze.py` — perfect maze via randomized Kruskal with union-find.
- `wilson_maze.py` — perfect maze via Wilson's loop-erased random walks.
- `braid_maze.py` — braid maze (loops) by removing dead ends from a Wilson maze.
- `maze_stats.py` — dead-end statistics for both kinds.
