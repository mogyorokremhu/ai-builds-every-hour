# Agent Guide — rules for the scheduled AI

This repo is built by an AI on a schedule (every hour). Every run MUST follow this guide.
Runs should be **moderate and efficient**: steady progress, not huge batches.

## Each run
1. Read `STATUS.md`, today's log file in `logs/` (if it exists) and the current project's
   `ROADMAP.md`. Only open the other files you actually need.
2. Do a **small-to-medium** batch — about 3–6 files created or changed:
   - Main work: continue the current big project (`projects/NN-name/`). Implement 1–2
     unchecked roadmap items. Real, working code — no placeholders or TODO stubs.
   - Prefer adding new files over rewriting big existing ones.
   - Add tests where it makes sense; run only the relevant tests, no long debugging loops.
   - Side work: add 2–3 new small files to ONE collection in `mini/` (see below).
3. Tick off finished items in the project's `ROADMAP.md`; add newly discovered tasks.
4. **Log the run — this is required every run, never skip it:**
   - Add an entry to `logs/YYYY-MM-DD.md` for today's UTC date:
     `## YYYY-MM-DD HH:MM UTC — run N` followed by 1–3 bullets.
   - If today's file doesn't exist yet, create it (title `# Build log — YYYY-MM-DD`) and
     add a link to it at the end of the list in `LOG.md`.
   - Never put run summaries in `STATUS.md` and never append to `LOG.md` itself; it is only an index.
5. Update `STATUS.md` (run count, current state, next steps — keep it short) and the tables
   in `README.md` if something changed (including mini file counts).
6. Commit everything in ONE push with a clear message: `run N: <summary>`.

## Big projects
- Each project is complex and layered, built up over many runs.
- Lives in `projects/NN-kebab-name/` with its own `README.md`, `ROADMAP.md`, source and tests.
- Roadmap has phases; each phase has several checkbox tasks.
- When every roadmap item is done: write final docs, mark it ✅ in `README.md`,
  then pick a NEW project of a different kind (Python game, JS browser game, Discord bot,
  interpreter/compiler, simulation, web app, emulator, …), create its folder and a roadmap.
- Prefer zero or minimal dependencies so things run anywhere.

## Mini collections (`mini/`)
- **Every 4th run (run number divisible by 4), start a brand-new collection** instead of
  adding to an existing one. Pick a theme that doesn't exist yet. Ideas: `games/` (tiny
  terminal games), `sorting-visualizers/`, `cellular-automata/`, `ciphers/`, `math-art/`,
  `sound/` (WAV generators), `web-toys/` (single-file HTML), `generators/` (names, mazes,
  poems), `simulations/`, `data-structures/`, `quizzes/`, `l-systems/`, … invent your own too.
  Start it with 3 files plus its `README.md`, and add a row for it to `README.md`.
- Other runs: add 2–3 files to an existing collection, rotating through ALL collections
  (oldest-updated first), not just the original four.
- Each collection folder has a `README.md` listing its files with one line each.
- Each file is self-contained and runnable.

## Website (`website/`)
- `website/` is a hand-maintained Cloudflare site that lets people register, browse this repo and play it
  in the browser. **Never edit it during scheduled runs.**
- It detects playable projects automatically: a folder with `index.html` (web game), a Python package with
  `__main__.py` (run as `python -m`; it passes `--text` if `__main__.py` mentions that flag), or a
  `repl.py` / `main.py` / `app.py` / `play.py` in the project folder.
- Python runs in the browser (Pyodide): standard library only, no network, and no `curses`, `turtle`,
  `tkinter` or `pygame`. So give new Python projects a plain text mode, and prefer JS web games with an
  `index.html` when the project is visual. Mini scripts under `mini/` get a ▶ Run button the same way.

## Style
- Python: 3.10+, type hints, docstrings. JS: modern ES modules, no build step if possible.
- Keep the repo organized; never dump files in the root.
