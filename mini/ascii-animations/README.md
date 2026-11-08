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
| [double_pendulum.py](double_pendulum.py) | Chaotic double pendulum (RK4) with a fading trail; `--twin` races two started 0.01° apart |
| [sorting.py](sorting.py) | Seven sorting algorithms as animated bars, driven by their real compare/write events |
| [maze.py](maze.py) | A maze carves itself (DFS or Prim, `--loops`), then a BFS wavefront solves it |
| [ripples.py](ripples.py) | Raindrops on a pond: the damped 2D wave equation with slope shading |
| [bouncing.py](bouncing.py) | Balls with gravity and momentum-conserving collisions, drawn in half-block pixels |
| [dna_helix.py](dna_helix.py) | A rotating DNA double helix with A–T / C–G base pairs scrolling past |

```bash
python fire.py
python life.py --pattern glider-gun
python torus.py --frames 200
python double_pendulum.py --twin
python sorting.py --algo quick --size 80
python maze.py --algo prim --loops
```
