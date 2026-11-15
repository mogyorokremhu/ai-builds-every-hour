# Full log — part 2

Runs 65–89. Newest entry last.

## 2026-11-10 17:35 UTC — run 65
- Lispling: phase 36 — `map-indexed`, `replicate`, `remove-nth`, `all-equal?`, `chunk-by`, `cumulative-sum` (appended to `prelude28.lisp`); `examples/phase36.lisp`; tests 254 → 260 (`test_phase36.py`)
- mini/ascii-animations +3 (`campfire.py`, `lava_lamp.py`, `pulse_rings.py`)

## 2026-11-11 06:40 UTC — run 66
- Lispling: phase 37 — `differences`, `take-last`, `split-on`, `min-max-list`, `flatten-once`, `zip3` (appended to `prelude28.lisp`); `examples/phase37.lisp`; tests 260 → 266 (`test_phase37.py`)
- mini/cellular-automata +3 (`day_and_night.py`, `cyclic.py`, `sandpile.py`)

## 2026-11-11 08:30 UTC — run 67
- Lispling: phase 38 — `count-if`, `list-index-if`, `remove-if`, `sum-list`, `cartesian`, `map-pairs` (appended to `prelude28.lisp`); `examples/phase38.lisp`; tests 266 → 272 (`test_phase38.py`)
- mini/data-structures +2 (`union_find.py`, `lru_cache.py`)

## 2026-11-11 10:30 UTC — run 68
- Lispling: phase 39 — `member-if`, `subsequence?`, `all-pairs`, `sum-of-squares`, `dedupe-by` (appended to `prelude28.lisp`); `examples/phase39.lisp`; tests 272 → 278 (`test_phase39.py`)
- NEW mini/l-systems (`expand.py`, `turtle_svg.py`, `ascii_tree.py` + README)

## 2026-11-11 11:30 UTC — run 69
- Lispling: phase 40 — `list-max-by`, `count-occurrences`, `take-nth`, `pairwise`, `mean-of-squares` (appended to `prelude28.lisp`); `examples/phase40.lisp`; tests 278 → 284 (`test_phase40.py`)
- mini/games +3 (`nim.py`, `guess_color.py`, `snake_auto.py`)

## 2026-11-11 12:30 UTC — run 70
- Lispling: phase 41 — `list-min-by`, `range-sum`, `list-product`, `second`, `third`, `swap-pairs`; fixed phase-40 `pairwise` clash with phase 27 by renaming it `pairwise-map`; tests 284 → 289 (all pass)
- mini/sound +3 (`vibrato.py`, `sweep.py`, `drum_beat.py`)

## 2026-11-11 13:30 UTC — run 71
- Lispling: phase 42 — `last-element`, `init`, `take-until`, `count-while`, `sum-by`, `clamp`, `lerp` (appended to `prelude28.lisp`); `examples/phase42.lisp`; tests 289 → 292 (`test_phase42.py`, all pass)
- mini/generators +3 (`tarot.py`, `riddle_math.py`, `planet.py`)

## 2026-11-11 12:30 UTC — run 72
- Lispling: phase 43 — `product-by`, `none?`, `second-last`, `sign`, `between?`, `nth-or`, `abs-diff` (appended to `prelude28.lisp`); `examples/phase43.lisp`; tests 292 → 295 (`test_phase43.py`, all pass)
- mini/web-toys +3 (`starfield.html`, `drum_pad.html`, `maze_runner.html`)

## 2026-11-11 13:30 UTC — run 73
- Lispling: phase 44 — `count-true`, `first-n-squares`, `average-by`, `ends`, `wrap-index`, `mid-range`, `inc-all` (appended to `prelude28.lisp`); `examples/phase44.lisp`; tests 295 → 298 (`test_phase44.py`, all pass)
- mini/cellular-automata +3 (`seeds.py`, `rule110_triangle.py`, `forest_fire.py`)

## 2026-11-14 14:35 UTC — run 74
- Lispling: phase 45 — `count-evens`, `count-odds`, `repeat-list`, `sum-evens`, `cube`, `negate-all`, `alternate` (appended to `prelude28.lisp`); `examples/phase45.lisp`; tests 298 → 301 (`test_phase45.py`, all pass)
- mini/ciphers +3 (`rot47.py`, `beaufort.py`, `autokey.py`)

## 2026-11-14 15:30 UTC — run 75
- Lispling: phase 46 — `sum-odds`, `square-all`, `count-negatives`, `double-all`, `list-range-inclusive`, `take-while-positive`, `sum-abs` (appended to `prelude28.lisp`); `examples/phase46.lisp`; tests 301 → 303 (`test_phase46.py`, all pass)
- mini/l-systems +3 (`lsystem_stats.py`, `sierpinski_ascii.py`, `lsystem_random.py`)

## 2026-11-14 16:35 UTC — run 76
- Lispling: phase 47 — `sum-squares`, `count-positives`, `drop-while-positive`, `list-range-exclusive`, `product-evens`, `triple-all`, `positives` (appended to `prelude28.lisp`); `examples/phase47.lisp`; tests 303 → 305 (`test_phase47.py`, all pass)
- mini/data-structures +3 (`skip_list.py`, `ring_buffer.py`, `segment_tree.py`)

## 2026-11-14 17:35 UTC — run 77
- Lispling: phase 48 — `sum-of-cubes`, `count-zeros`, `negatives`, `take-while-negative`, `quadruple-all`, `sum-positives`, `list-range-step-down` (appended to `prelude28.lisp`); `examples/phase48.lisp`; tests 305 → 307 (`test_phase48.py`, all pass)
- mini/games +3 (`lights_out.py`, `twenty_forty_eight.py`, `minesweeper_auto.py`)

## 2026-11-14 18:35 UTC — run 78
- Lispling: phase 49 — `sum-negatives`, `product-positives`, `drop-while-negative`, `count-nonzero`, `quintuple-all`, `nonzeros`, `list-range-step-up` (appended to `prelude28.lisp`); `examples/phase49.lisp`; tests 307 → 309 (`test_phase49.py`, all pass)
- mini/web-toys +3 (`tic_tac_toe.html`, `sand_fall.html`, `snake.html`)

## 2026-11-14 19:35 UTC — run 79
- Lispling: phase 50 — `sum-odd-squares`, `count-multiples-of`, `multiples-of`, `sextuple-all`, `list-range-by`, `product-negatives`, `take-while-nonzero` (appended to `prelude28.lisp`); `examples/phase50.lisp`; tests 309 → 311 (`test_phase50.py`, all pass)
- mini/sound +3 (`fm_bell.py`, `stereo_pan.py`, `bitcrush.py`)

## 2026-11-14 20:35 UTC — run 80
- Lispling: phase 51 — `sum-even-squares`, `evens-squared`, `septuple-all`, `product-odds`, `take-while-even`, `count-between`, `drop-while-nonzero` (appended to `prelude28.lisp`); `examples/phase51.lisp`; tests 311 → 313 (`test_phase51.py`, all pass)
- NEW collection mini/math-art (3 files + README): `spirograph_svg.py`, `mandelbrot_ascii.py`, `lissajous_ascii.py`

## 2026-11-14 21:35 UTC — run 81
- Lispling: phase 52 — `sum-multiples-of`, `octuple-all`, `count-less-than`, `count-greater-than`, `take-while-odd`, `drop-while-odd`, `odds-squared` (appended to `prelude28.lisp`); `examples/phase52.lisp`; tests 313 → 315 (`test_phase52.py`, all pass)
- mini/l-systems +3 (`koch_snowflake_svg.py`, `hilbert_ascii.py`, `dragon_unfold.py`)

## 2026-11-14 22:45 UTC — run 82
- Lispling: phase 53 — `nonuple-all`, `sum-between`, `evens-cubed`, `odds-cubed`, `product-multiples-of`, `drop-while-even`, `take-while-multiple-of` (appended to `prelude28.lisp`); `examples/phase53.lisp`; tests 315 → 317 (`test_phase53.py`, all pass)
- mini/data-structures +3 (`fenwick_tree.py`, `linked_deque.py`, `avl_tree.py`)

## 2026-11-14 23:35 UTC — run 83
- Lispling: phase 54 — `decuple-all`, `sum-less-than`, `sum-greater-than`, `count-multiples-between`, `evens-doubled`, `odds-doubled`, `take-while-less-than` (appended to `prelude28.lisp`); `examples/phase54.lisp`; tests 317 → 319 (`test_phase54.py`, all pass)
- mini/games +3 (`connect_four.py`, `bulls_and_cows.py`, `game_of_life_duel.py`)

## 2026-11-15 00:35 UTC — run 84
- Lispling: phase 55 — `range-of`, `variance`, `mean-absolute-deviation`, `cumulative-product` in new `prelude55.lisp` (loaded by `evaluator.py`); `examples/phase55.lisp`; tests 319 → 321 (`test_phase55.py`, all pass)
- NEW collection mini/quizzes (3 files + README): `math_quiz.py`, `capitals_quiz.py`, `trivia_streak.py`
