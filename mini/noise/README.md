# noise

Procedural noise in pure Python (standard library only), rendered as ASCII.

- `value_noise.py` — lattice value noise with smoothstep interpolation.
- `perlin.py` — classic gradient Perlin noise plus fractal octave layering.
- `island_map.py` — ASCII island generator: fractal noise with radial falloff (imports `perlin.py`).
