# 🧩 Puzzles

Self-contained Python puzzle solvers and toys. Each runs with `python <file>.py`
(no dependencies) and most accept optional command-line arguments.

| File | What it does |
|---|---|
| `sudoku_solver.py` | Solves any sudoku with constraint propagation + MRV backtracking |
| `n_queens.py` | Counts all N-Queens solutions with bitmasks and draws one |
| `fifteen_puzzle.py` | Shuffles a 15-puzzle and solves it optimally with IDA* + linear conflict |
| `knights_tour.py` | Knight's tour via Warnsdorff's rule with tie-break lookahead |
| `hanoi.py` | Animated Towers of Hanoi in the terminal |
| `nonogram.py` | Picross solver: line arrangements + propagation + backtracking |
| `lights_out.py` | Lights Out solver: Gaussian elimination over GF(2), fewest presses |
| `mastermind.py` | Knuth's minimax codebreaker (≤ 5 guesses), or `--play` to guess yourself |
| `peg_solitaire.py` | Solves English peg solitaire (33 holes) with symmetry-pruned DFS, replays 31 jumps |
| `cryptarithm.py` | SEND + MORE = MONEY style solver with weighted sums and bound pruning |
| `magic_square.py` | Magic squares of any order: Siamese, doubly-even and Strachey constructions |
| `water_jugs.py` | Shortest pour sequence for jug puzzles via BFS (any number of jugs) |
