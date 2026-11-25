# hashing

Small hash-based algorithms, each self-contained (run from this folder, e.g. `python bloom.py`).

- `fnv.py` — FNV-1a 32/64-bit hash with known-vector checks.
- `bloom.py` — Bloom filter with sized bit array and measured false-positive rate.
- `consistent_hash.py` — consistent hashing ring with virtual nodes.
- `adler32.py` — Adler-32 checksum verified against zlib.
- `crc32.py` — table-driven CRC-32 (IEEE) verified against zlib.
- `minhash.py` — MinHash signatures estimating Jaccard similarity.
