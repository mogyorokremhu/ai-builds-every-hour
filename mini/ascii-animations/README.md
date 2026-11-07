# ASCII animations

Terminal animations in pure Python (no dependencies). Each runs forever until Ctrl+C,
or for a fixed number of frames with `--frames N`. Most accept `--fps`, `--width`,
`--height`, `--seed` and `--no-color`.

| File | What it shows |
|---|---|
| [fire.py](fire.py) | Doom-style fire: heat rises and cools, 256-colour flame ramp |
| [starfield.py](starfield.py) | Stars flying at you with perspective projection |
| [life.py](life.py) | Conway's Game of Life on a torus, half-block cells (random, glider gun, acorn, R-pentomino) |
| [torus.py](torus.py) | Spinning shaded 3D torus with a z-buffer and luminance characters |
| [plasma.py](plasma.py) | Demoscene plasma from interfering sine waves |
| [digital_rain.py](digital_rain.py) | Falling glyph streams with bright heads and fading tails (`--ascii` for plain glyphs) |

```bash
python fire.py
python life.py --pattern glider-gun
python torus.py --frames 200
```
