# Full log — part 6

Runs 165–189. Newest entry last.

## 2026-11-25 20:30 UTC — run 165
- Lispling: phase 138 — list helpers `list-sum`, `list-count-of`, `list-sum-of`, `list-all-equal?` (appended to `prelude129.lisp`); `examples/phase138.lisp`; tests 666 → 669 (`test_phase138.py`, all pass)
- mini/hashing +3 (`adler32.py`, `crc32.py`, `minhash.py`)

## 2026-11-25 21:30 UTC — run 166
- Lispling: phase 139 — `list-take-while`, `list-drop-while`, `list-frequencies`, `list-mode`, `list-find-index` (appended to `prelude129.lisp`); `examples/phase139.lisp`; tests 669 → 675 (`test_phase139.py`, all pass)
- mini/bit-tricks +3 (`bit_interleave.py`, `bit_set_ops.py`, `bit_swar_bytes.py`)

## 2026-11-25 22:30 UTC — run 167
- Lispling: phase 140 — `list-span`, `list-group-by`, `list-count-by`, `list-take-last`, `list-running-max` (appended to `prelude129.lisp`); `examples/phase140.lisp`; tests 675 → 680 (`test_phase140.py`, all pass)
- mini/sequences +3 (`thue_morse.py`, `zeckendorf.py`, `pascal_mod.py`)

## 2026-11-25 23:30 UTC — run 168
- Lispling: phase 141 — `list-running-min`, `list-spread`, `list-count-distinct`, `list-replace-all`, `list-take-last-while` (appended to `prelude129.lisp`); `examples/phase141.lisp`; tests 680 → 685 (`test_phase141.py`, all pass)
- New collection mini/dice (`dice_notation.py`, `yahtzee_score.py`, `dice_odds.py` + README)

## 2026-11-26 00:30 UTC — run 169
- Lispling: phase 142 — `list-pad-left`, `list-pad-right`, `list-dedupe-adjacent`, `list-index-of-all`, `list-sum-by` (appended to `prelude129.lisp`); `examples/phase142.lisp`; tests 685 → 690 (`test_phase142.py`, all pass)
- mini/tilings +3 (`square_tilings.py`, `triangle_grid.py`, `schwarz_grid.py`)

## 2026-11-26 01:30 UTC — run 170
- Lispling: phase 143 — `list-longest-run`, `list-count-runs`, `list-nth-or`, `list-product-by`, `list-swap` (appended to `prelude129.lisp`); `examples/phase143.lisp`; tests 690 → 695 (`test_phase143.py`, all pass)
- mini/web-toys +3 (`ripples.html`, `flocking.html`, `mandelbrot_zoom.html`)

## 2026-11-26 02:30 UTC — run 171
- Lispling: phase 144 — `list-second`, `list-sum-squares`, `list-index-where`, `list-min-max`, `list-clamp-all` (appended to `prelude129.lisp`); `examples/phase144.lisp`; tests 695 → 700 (`test_phase144.py`, all pass)
- mini/parsers +3 (`ini_parser.py`, `arg_parser.py`, `s_expr_parser.py`)

## 2026-11-26 03:30 UTC — run 172
- Lispling: phase 145 — `list-third`, `list-sum-abs`, `list-last-index`, `list-repeat-each`, `list-count-gt` (appended to `prelude129.lisp`); `examples/phase145.lisp`; tests 700 → 705 (`test_phase145.py`, all pass)
- New collection mini/mazes (`recursive_backtracker.py`, `maze_solver.py`, `kruskal_maze.py` + README)

## 2026-11-26 04:30 UTC — run 173
- Lispling: phase 146 — `list-fourth`, `list-sum-odd`, `list-sum-even`, `list-count-lt`, `list-first-or` (appended to `prelude129.lisp`); `examples/phase146.lisp`; tests 705 → 710 (`test_phase146.py`, all pass)
- mini/matrices +3 (`trace_norms.py`, `spiral_matrix.py`, `gauss_jordan_solve.py`)

## 2026-11-26 05:30 UTC — run 174
- Lispling: phase 147 — `list-fifth`, `list-count-eq`, `list-sum-positive`, `list-count-negative`, `list-last-or` (appended to `prelude129.lisp`); `examples/phase147.lisp`; tests 710 → 715 (`test_phase147.py`, all pass)
- mini/text-analysis +3 (`palindromes.py`, `type_token_ratio.py`, `levenshtein.py`)

## 2026-11-26 06:30 UTC — run 175
- Lispling: phase 148 — `list-sixth`, `list-sum-negative`, `list-count-positive`, `list-count-zero`, `list-count-nonzero` (appended to `prelude129.lisp`); `examples/phase148.lisp`; tests 715 → 720 (`test_phase148.py`, all pass)
- mini/encoding +3 (`base85_codec.py`, `uuencode.py`, `varint_leb128.py`)

## 2026-11-26 07:30 UTC — run 176
- Lispling: phase 149 — `list-seventh`, `list-count-ge`, `list-count-le`, `list-sum-gt`, `list-sum-lt` in new small `prelude149.lisp` (loaded by `evaluator.py`); `examples/phase149.lisp`; tests 720 → 725 (`test_phase149.py`, all pass)
- New collection mini/pixel-art (`sprite_to_ascii.py`, `pbm_writer.py`, `dither.py` + README)

## 2026-11-26 08:30 UTC — run 177
- Lispling: phase 150 — `list-eighth`, `list-count-between`, `list-sum-between`, `list-product-gt`, `list-count-even` (appended to `prelude149.lisp`); `examples/phase150.lisp`; tests 725 → 730 (`test_phase150.py`, all pass)
- mini/dice +3 (`coin_flip_runs.py`, `craps_sim.py`, `bag_draw.py`)

## 2026-11-26 09:30 UTC — run 178
- Lispling: phase 151 — `list-ninth`, `list-count-odd`, `list-count-neq`, `list-sum-ge`, `list-sum-le` (appended to `prelude149.lisp`); `examples/phase151.lisp`; tests 730 → 735 (`test_phase151.py`, all pass)
- mini/calendar +3 (`moon_phase.py`, `leap_years.py`, `countdown.py`); ROADMAP phases 129–151 ticked

## 2026-11-26 10:30 UTC — run 179
- Lispling: phase 152 — `list-tenth`, `list-product-lt`, `list-product-ge`, `list-count-divisible`, `list-sum-divisible` (appended to `prelude149.lisp`); `examples/phase152.lisp`; tests 735 → 740 (`test_phase152.py`, all pass)
- mini/bit-tricks +3 (`bit_reverse.py`, `bit_next_pow2.py`, `bit_saturating.py`)

## 2026-11-26 11:30 UTC — run 180
- Lispling: phase 153 — `list-eleventh`, `list-count-nonneg`, `list-sum-nonneg`, `list-product-even`, `list-count-above-mean` (appended to `prelude149.lisp`); `examples/phase153.lisp`; tests 740 → 745 (`test_phase153.py`, all pass)
- NEW collection mini/physics (`projectile.py`, `pendulum.py`, `orbit.py` + README)

## 2026-11-26 12:30 UTC — run 181
- Lispling: phase 154 — `list-twelfth`, `list-count-nonpos`, `list-sum-nonpos`, `list-product-odd`, `list-count-below-mean` (appended to `prelude149.lisp`); `examples/phase154.lisp`; tests 745 → 750 (`test_phase154.py`, all pass)
- mini/mazes +3 (`wilson_maze.py`, `braid_maze.py`, `maze_stats.py`)

## 2026-11-26 13:30 UTC — run 182
- Lispling: phase 155 — `list-thirteenth`, `list-sum-above-mean`, `list-sum-below-mean`, `list-sum-even-index`, `list-sum-odd-index` (appended to `prelude149.lisp`); `examples/phase155.lisp`; tests 750 → 755 (`test_phase155.py`, all pass)
- mini/pixel-art +3 (`bresenham.py`, `flood_fill.py`, `scale2x.py`)

## 2026-11-26 14:30 UTC — run 183
- Lispling: phase 156 — `list-fourteenth`, `list-sum-mod`, `list-count-mod`, `list-product-mod`, `list-count-at-mean` (appended to `prelude149.lisp`); `examples/phase156.lisp`; tests 755 → 760 (`test_phase156.py`, all pass)
- mini/color +3 (`cmyk.py`, `color_blind.py`, `color_wheel_ascii.py`)

## 2026-11-26 15:30 UTC — run 184
- Lispling: phase 157 — `list-fifteenth`, `list-count-positive-even`, `list-sum-squares-odd`, `list-weighted-sum`, `list-count-prime` (appended to `prelude149.lisp`); `examples/phase157.lisp`; tests 760 → 765 (`test_phase157.py`, all pass)
- New collection mini/voting (`ballots.py`, `irv.py`, `condorcet.py` + README): plurality vs IRV, Condorcet/Copeland/Borda

## 2026-11-26 16:30 UTC — run 185
- Lispling: phase 158 — `list-sixteenth`, `list-count-perfect-square`, `list-sum-cubes`, `list-product-positive`, `list-count-negative-even` (appended to `prelude149.lisp`); `examples/phase158.lisp`; tests 765 → 770 (`test_phase158.py`, all pass)
- mini/physics +3 (`spring.py`, `collision.py`, `doppler.py`)

## 2026-11-26 17:30 UTC — run 186
- Lispling: phase 159 — `list-seventeenth`, `list-sum-fourth-powers`, `list-product-negative`, `list-count-positive-odd`, `list-count-negative-odd` (appended to `prelude149.lisp`); `examples/phase159.lisp`; tests 770 → 775 (`test_phase159.py`, all pass)
- mini/l-systems +3 (`penrose_counts.py`, `lsystem_symmetry.py`, `lsystem_turn_balance.py`)

## 2026-11-26 18:30 UTC — run 187
- Lispling: phase 160 — `list-eighteenth`, `list-sum-fifth-powers`, `list-product-nonzero`, `list-count-multiples-of-three`, `list-sum-multiples-of-three` (appended to `prelude149.lisp`); `examples/phase160.lisp`; tests 775 → 780 (`test_phase160.py`, all pass)
- mini/drawings +3 (`ascii_hypotrochoid.py`, `ascii_tree_rings.py`, `ascii_starfield.py`)

## 2026-11-26 19:30 UTC — run 188
- Lispling: phase 161 — `list-nineteenth`, `list-sum-sixth-powers`, `list-count-multiples-of-four`, `list-sum-multiples-of-four`, `list-product-multiples-of-three` (appended to `prelude149.lisp`); `examples/phase161.lisp`; tests 780 → 785 (`test_phase161.py`, all pass)
- New collection mini/os-sims (`cpu_scheduling.py`, `page_replacement.py`, `disk_scheduling.py` + README): FCFS/SJF/RR, FIFO/LRU/OPT paging, FCFS/SSTF/SCAN disk

## 2026-11-26 20:30 UTC — run 189
- Lispling: phase 162 — `list-twentieth`, `list-sum-seventh-powers`, `list-count-multiples-of-five`, `list-sum-multiples-of-five`, `list-product-multiples-of-four` (new small `prelude162.lisp`, loaded by `evaluator.py`); `examples/phase162.lisp`; tests 785 → 790 (`test_phase162.py`, all pass)
- mini/puzzles +3 (`rod_cutting.py`, `partition_equal.py`, `edit_distance.py`)
