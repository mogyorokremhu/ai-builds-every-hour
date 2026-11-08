# Agent Guide — rules for the scheduled AI

This repo is built by an AI on a schedule (every 2 hours). Every run MUST follow this guide.
Runs should be **moderate and efficient**: steady progress, not huge batches.

## Each run
1. Read `STATUS.md`, the latest `LOG.md` entry and the current project's `ROADMAP.md`.
   Only open the other files you actually need.
2. Do a **small-to-medium** batch — about 3–6 files created or changed:
   - Main work: continue the current big project (`projects/NN-name/`). Implement 1–2
     unchecked roadmap items. Real, working code — no placeholders or TODO stubs.
   - Prefer adding new files over rewriting big existing ones.
   - Add tests where it makes sense; run only the relevant tests, no long debugging loops.
   - Side work: add 2–3 new small files to ONE collection in `mini/`
     (rotate: `puzzles/`, `tools/`, `ascii-animations/`, `drawings/`, … create new collections freely).
3. Tick off finished items in the project's `ROADMAP.md`; add newly discovered tasks.
4. Append a short entry to `LOG.md`: `## YYYY-MM-DD HH:MM UTC — run N: <summary>`.
5. Update `STATUS.md` (run count) and the tables in `README.md` if something changed.
6. Commit everything in ONE push with a clear message: `run N: <summary>`.

## Big projects
- Each project is complex and layered, built up over many runs.
- Lives in `projects/NN-kebab-name/` with its own `README.md`, `ROADMAP.md`, source and tests.
- Roadmap has phases; each phase has several checkbox tasks.
- When every roadmap item is done: write final docs, mark it ✅ in `README.md`,
  then pick a NEW project of a different kind (Python game, JS browser game, Discord bot,
  interpreter/compiler, simulation, web app, emulator, …), create its folder and a roadmap.
- Prefer zero or minimal dependencies so things run anywhere.

## Small collections (`mini/`)
- Each collection folder has a `README.md` listing its files with one line each.
- Each file is self-contained and runnable.

## Style
- Python: 3.10+, type hints, docstrings. JS: modern ES modules, no build step if possible.
- Keep the repo organized; never dump files in the root.
