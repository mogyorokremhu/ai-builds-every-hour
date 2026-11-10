# ciphers

Classic ciphers, each a runnable stdlib-only script.

- `caesar.py` — Caesar shift with a frequency-scored brute-force `crack`.
- `vigenere.py` — Vigenère polyalphabetic cipher (non-letters skip the key).
- `rail_fence.py` — rail fence zigzag transposition, encrypt and decrypt.
- `atbash.py` — Atbash mirror-alphabet cipher (self-inverse).
- `playfair.py` — Playfair digraph cipher with 5x5 key square (`-d` decrypts).
- `morse.py` — Morse code encoder/decoder (`-d` decodes).
- `affine.py` — affine cipher (a·x+b mod 26), validates a is coprime with 26 (`-d` decrypts).
- `bacon.py` — Bacon's A/B five-bit letter encoding and decoding.
- `columnar.py` — columnar transposition with keyword column ordering (`-d` decrypts).
- `scytale.py` — scytale rod transposition with padding (`-d` decrypts).
- `polybius.py` — Polybius square digit-pair encoding, I/J merged (`-d` decodes).
- `xor_cipher.py` — repeating-key XOR with hex output (`-d` decrypts).
