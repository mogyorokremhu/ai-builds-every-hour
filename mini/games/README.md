# games

Tiny terminal games, standard library only. Each supports `--auto` so it can run unattended.

- `hangman.py` — guess the word letter by letter; `--auto` plays by letter frequency.
- `higher_lower.py` — guess 1–100 in 7 tries; `--auto` binary-searches.
- `tictactoe.py` — play against an unbeatable minimax AI; `--auto` is AI vs AI.
- `nim.py` — 21-stick Nim; `--auto` pits the mod-4 strategy against random play.
- `guess_color.py` — Mastermind-lite with 6 colors; `--auto` solves it by elimination.
- `snake_auto.py` — self-steering snake on a small grid, prints the final board.
- `lights_out.py` — 5x5 Lights Out; `--auto` solves it with GF(2) elimination.
- `twenty_forty_eight.py` — 2048; `--auto` plays greedily by empty cells.
- `minesweeper_auto.py` — 9x9 Minesweeper; `--auto` deduces safe cells and guesses when stuck.
- `connect_four.py` — Connect Four vs a minimax AI; `--auto` is AI vs random.
- `bulls_and_cows.py` — 4-digit code breaker; `--auto` solves by elimination.
- `game_of_life_duel.py` — two-colour Life; prints which colour wins.
- `dice_poker.py` — five-dice poker with one reroll; `--auto` simulates 1000 rounds.
- `word_ladder.py` — word ladder solved by BFS over a built-in word list.
- `battleship_auto.py` — 8x8 Battleship with a hunt/target AI; prints board and average shots.
- `mastermind_solver.py` — Mastermind minimax solver; prints each guess and feedback.
- `tower_of_hanoi.py` — Tower of Hanoi solved with ASCII pegs drawn after every move.
- `rock_paper_scissors_ai.py` — RPS against a Markov predictor; `--auto` simulates 300 rounds.
- `pig.py` — Pig dice game; hold-at-N strategies play each other in a win-rate table.
- `blackjack_basic.py` — blackjack simulation comparing a dealer-mimic player with a basic strategy.
- `memory_match.py` — Memory card game; average turns for AIs with different recall.
