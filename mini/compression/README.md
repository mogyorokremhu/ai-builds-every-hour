# compression

Tiny lossless compression algorithms, each self-contained with a round-trip demo.

- `rle.py` — run-length encoding (count+char).
- `huffman.py` — Huffman prefix codes built with a heap.
- `lzw.py` — LZW dictionary compression.
- `delta.py` — delta encoding of integer sequences.
- `bwt.py` — Burrows-Wheeler transform and inverse.
- `lz77.py` — LZ77 sliding-window (offset, length, char) triples.
- `mtf.py` — move-to-front transform (pairs well with BWT).
- `lz78.py` — LZ78 phrase dictionary, (index, char) pairs.
- `golomb.py` — Golomb-Rice coding of small integers.
