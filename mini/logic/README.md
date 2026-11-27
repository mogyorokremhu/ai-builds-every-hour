# logic

Boolean logic tools, each self-contained with a built-in check.

- `truth_table.py` — truth table / tautology check for an expression (`and or not ^ ->`).
- `dpll_sat.py` — DPLL SAT solver with unit propagation and a pigeonhole test.
- `quine_mccluskey.py` — minimizes minterms to a minimal sum-of-products.
- `gray_code.py` — Gray code conversion and cyclic single-bit-change check.
- `half_full_adder.py` — gate-level half/full adders chained into a ripple-carry adder.
- `boolean_simplify.py` — verifies boolean-law identities by exhaustive evaluation.
- `nand_universal.py` — builds NOT/AND/OR/XOR from NAND alone and verifies them.
- `two_bit_comparator.py` — gate-level 2-bit comparator checked on all 16 inputs.
- `mux_decoder.py` — 4:1 multiplexer built on a 2:4 decoder, exhaustively verified.
