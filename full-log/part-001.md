# Full log — part 1

Runs 40–64. Newest entry last.

## 2026-11-09 16:35 UTC — run 40
- Lispling VM: inlined binary primitive ops (`PRIM2` for + - * < > <= >= =, runtime guard if redefined/shadowed); tests 94 → 101 (`test_phase11.py`)
- NEW mini/ciphers collection: `caesar.py` (with crack), `vigenere.py`, `rail_fence.py` + README

## 2026-11-09 17:40 UTC — run 41
- Lispling VM: inlined unary primitives (`PRIM1` for car cdr null? not zero? pair?, runtime guard like PRIM2); tests 101 → 109 (`test_phase12.py`)
- mini/puzzles +3 (`zebra_puzzle.py`, `pancake_sort.py`, `kaprekar.py`)

## 2026-11-09 18:35 UTC — run 42
- Lispling VM: inlined env-chain lookup for LOAD and the PRIM1/PRIM2 guards (`_lookup`, one walk instead of two); tests 109 → 116 (`test_phase13.py`); bench shows no measurable change, so real speedup still needs slot-resolved locals
- mini/ascii-animations +3 (`cube.py`, `metronome.py`, `sandpile.py`)

## 2026-11-09 19:35 UTC — run 43
- Lispling VM: fused `PRIM2LC` superinstruction (LOAD var + CONST + PRIM2, jump-target-safe via `Code.targets`, same redefinition guard); tests 116 → 125 (`test_phase14.py`); loop bench 1.69x vs tree-walker
- mini/drawings +3 (`ascii_sunflower.py`, `ascii_rule30.py`, `ascii_lissajous_knot.py`)

## 2026-11-09 20:35 UTC — run 44
- Lispling: new `case` special form (expander in forms.py, works in tree-walker and VM, key evaluated once, tail-safe); tests 125 → 132 (`test_phase15.py`)
- NEW mini/generators collection: `maze.py`, `names.py`, `markov.py` + README

## 2026-11-09 21:31 UTC — run 45
- Lispling: lazy evaluation — `delay`/`force`/`cons-stream` + stream library (map/filter/take/ref, `integers-from`) in the prelude, `examples/streams.lisp` (stream sieve); tests 132 → 140 (`test_phase16.py`)
- mini/ciphers +3 (`atbash.py`, `playfair.py`, `morse.py`)

## 2026-11-09 22:35 UTC — run 46
- Lispling: error handling — `error`, `try` (thunk + handler), `assert`, plus `when`/`unless` forms (tree-walker + VM); `examples/errors.lisp`; tests 140 → 149 (`test_phase17.py`)
- mini/puzzles +3 (`collatz_records.py`, `nim_game.py`, `josephus_closed_form.py`)

## 2026-11-09 23:35 UTC — run 47
- Lispling: mutable vectors (`vectors.py`: vector/make-vector/vector-ref/set!/fill!/->list/list->vector, `#(..)` printing) + `define-record-type` expander (tagged-vector records, predicate, getters/setters, type-checked); `examples/records.lisp`; tests 149 → 160 (`test_phase18.py`)
- mini/tools +3 (`humansize.py`, `jsonfmt.py`, `lineno.py`)

## 2026-11-10 00:30 UTC — run 48
- Lispling: phase 19 prelude library — `sort` (stable merge sort), `list-ref`, `list-tail`, `remove`, `delete`, `partition`, `list-index`, `vector-map`/`vector-for-each`/`vector-sort`; `examples/sorting.lisp`; tests 160 → 166 (`test_phase19.py`)
- NEW mini/cellular-automata (`life.py`, `elementary.py`, `langton.py` + README)

## 2026-11-10 01:35 UTC — run 49
- Lispling: phase 20 prelude — `fold-left`/`fold-right`, `append-map`, `iota`/`iota-from`, `any`/`every`/`count`, `zip`, `remove-duplicates`; `examples/folds.lisp`; tests 166 → 170 (`test_phase20.py`)
- mini/generators +3 (`password.py`, `dungeon.py`, `haiku.py`)

## 2026-11-10 02:35 UTC — run 50
- Lispling: phase 21 — prelude `take-while`/`drop-while`/`filter-map`/`list-set`/`last-pair`/`alist-set`/`alist-ref`/`hash-update!`/`group-by` + native `string-pad-left/right`, `string-prefix?/suffix?`; `examples/utils.lisp`; tests 170 → 175 (`test_phase21.py`)
- mini/ciphers +3 (`affine.py`, `bacon.py`, `columnar.py`)

## 2026-11-10 03:35 UTC — run 51
- Lispling: phase 22 numeric library — `gcd`/`lcm`/`quotient`/`remainder`/`modulo`/`expt`/`floor`/`ceiling`/`round`/`truncate`/`number->string-radix` + prelude `square`/`digits`/`memq`/`list-copy`/`delete-duplicates`; `examples/numbers.lisp`; tests 175 → 181 (`test_phase22.py`)
- mini/ascii-animations +3 (`boids.py`, `hourglass.py`, `aurora.py`)

## 2026-11-10 04:30 UTC — run 52
- Lispling: phase 23 functional helpers — prelude `butlast`/`curry`/`flip`/`max-by`/`min-by`/`interleave`/`transpose`/`chunk`/`frequencies`; `examples/functional.lisp`; tests 181 → 187 (`test_phase23.py`; variadic params not yet supported by the interpreter, so `curry` is 2-arg)
- NEW mini/sound (`tones.py`, `melody.py`, `chord.py` + README) — stdlib WAV generators

## 2026-11-10 05:30 UTC — run 53
- Lispling: phase 24 variadic parameters — `(define (f . rest))`, `(lambda args ...)`, `(lambda (a . r) ...)` in tree-walker and VM via shared `split_params`/`bind_params`; `examples/variadic.lisp`; tests 187 → 194 (`test_phase24.py`)
- mini/drawings +3 (`ascii_apollonian.py`, `ascii_cantor_dust.py`, `ascii_flow_field.py`)

## 2026-11-10 06:35 UTC — run 54
- Lispling: phase 25 combinators — variadic `curry`/`partial` (any number of pre-supplied args), `constantly`, `complement`, `juxt`, `compose*`; `examples/combinators.lisp`; tests 194 → 201 (`test_phase25.py`)
- mini/puzzles +3 (`subset_sum.py`, `coin_change.py`, `lis.py`)

## 2026-11-10 07:35 UTC — run 55
- Lispling: phase 26 strings & chars — char predicates/conversion, `string>?`/`<=?`/`>=?`/`-ci=?`, trim-left/right, titlecase, `string-count`, prelude `string-map`/`for-each`/`filter`/`take`/`drop`/`capitalize`, `palindrome?`, `caesar-shift`, `word-count`; `examples/strings2.lisp`; tests 201 → 211 (`test_phase26.py`)
- mini/tools +3 (`rle.py`, `sumlines.py`, `fizzlist.py`)

## 2026-11-10 08:35 UTC — run 56
- Lispling: phase 27 — `list-union/intersection/difference`, `subset?`, `take-right`/`drop-right`, `rotate`, `pairwise`, `cartesian-product`, `power-set`, `combinations`, `permutations`, `subvector`/`vector-append`/`vector-reverse`/`vector-count`/`vector-index`/`vector-binary-search`; `examples/sets_combinatorics.lisp`; tests 211 → 219 (`test_phase27.py`)
- NEW mini/web-toys (`bouncing_balls.html`, `color_mixer.html`, `typing_speed.html` + README)
