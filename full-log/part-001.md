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
