# bit-tricks

Bit manipulation toys, standard library only.

- `popcount_tricks.py` — popcount (loop and SWAR), power-of-two, lowest set bit, bit reversal, with self-checks.
- `gray_code.py` — Gray code encode/decode table that verifies one-bit-per-step (`python gray_code.py 5`).
- `bitset_sieve.py` — prime sieve that uses a single Python int as its bit array.
- `gosper_hack.py` — Gosper's hack: enumerate all n-bit values with exactly k set bits.
- `xorshift_rng.py` — xorshift32/64 generators with a bit-balance check.
- `parity_tricks.py` — parity via loop/fold plus Hamming(7,4) syndrome decoding.
- `bit_permutations.py` — next same-popcount permutation and submask enumeration.
- `bit_matrix.py` — 8x8 bit matrix in one 64-bit int: transpose and rotate.
- `bit_run_lengths.py` — longest run of ones, run count, leading/trailing zeros.
- `bit_interleave.py` — Morton/Z-order codes: spread, compact, encode, decode.
- `bit_set_ops.py` — sets as bitmasks, submask enumeration, subset-sum DP in one int.
- `bit_swar_bytes.py` — SWAR zero-byte detection, broadcast and lane-safe byte addition.
- `bit_reverse.py` — reverse bits by loop and 32-bit mask swaps; FFT bit-reversal order.
- `bit_next_pow2.py` — power-of-two test, round up/down, lowest set bit, floor log2.
- `bit_saturating.py` — wrapping vs saturating add/sub and signed overflow detection.
