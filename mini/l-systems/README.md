# l-systems

Lindenmayer systems: string rewriting plus a turtle interpreter. Pure standard library.

- `expand.py` — expand algae/koch/dragon/plant systems and print each generation.
- `turtle_svg.py` — turtle interpreter that writes an SVG (`python turtle_svg.py plant 4`).
- `ascii_tree.py` — draws a branching plant in the terminal.
- `lsystem_stats.py` — growth statistics (length, ratio, symbol counts) per generation.
- `sierpinski_ascii.py` — Sierpinski triangle from an L-system, drawn in ASCII.
- `lsystem_random.py` — stochastic L-system with weighted rules and seeded variants.
- `koch_snowflake_svg.py` — Koch snowflake written as an SVG.
- `hilbert_ascii.py` — Hilbert curve from an L-system, drawn in ASCII.
- `dragon_unfold.py` — dragon curve turns by paper folding, verified against the L-system.
- `gosper_ascii.py` — Gosper (flowsnake) curve drawn in ASCII.
- `lsystem_grammar_check.py` — validates rules: bracket balance and unknown symbols.
- `lsystem_bracket_depth.py` — max branching depth and branch counts per generation.
- `lsystem_bbox.py` — bounding box and aspect ratio of the turtle path per generation.
- `levy_c_ascii.py` — Lévy C curve drawn in ASCII on an 8-direction grid.
- `lsystem_rle.py` — run-length compression ratio of L-system strings (round-trip checked).
- `penrose_counts.py` — thin/thick rhombus substitution counts converging to the golden ratio.
- `lsystem_symmetry.py` — palindrome and mirror-symmetry checks on expanded strings.
- `lsystem_turn_balance.py` — net turning angle and closed-heading check per generation.
