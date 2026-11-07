# Agent Guide — rules for the hourly AI

This repo is built by an AI on an hourly schedule. Every run MUST follow this guide.

## Each hourly run
1. Read `STATUS.md` (current project + next tasks) and the current project's `ROADMAP.md`.
2. Do a **big** batch of work — aim for 8–20 files created or substantially changed:
   - Main work: continue the current big project (`projects/NN-name/`). Implement several
     unchecked roadmap items, not just one. Real, working code — no placeholders or TODO stubs.
   - Add/extend tests where it makes sense and keep existing tests passing.
   - Side work (every run): add 5–6 new files to ONE small collection in `mini/`
     (rotate: `drawings/`, `puzzles/`, `tools/`, `ascii-animations/`, … create new collections freely).
3. Tick off finished items in the project's `ROADMAP.md`; add newly discovered tasks.
4. Append an entry to `LOG.md`: `## YYYY-MM-DD HH:00 UTC — <summary>` with a bullet list of changes.
5. Update `STATUS.md` and the project table in `README.md`.
6. Commit everything in ONE push with a clear message: `hour N: <summary>`.

## Big projects
- Each project should take **2–3 days** of hourly runs (~40–70 runs). Extremely complex and layered.
- Lives in `projects/NN-kebab-name/` with its own `README.md`, `ROADMAP.md`, source and tests.
- Roadmap has phases; each phase has many checkbox tasks.
- When every roadmap item is done: polish, write final docs, mark it ✅ in `README.md`,
  then pick a NEW project of a different kind (Python game, JS browser game, Discord bot,
  interpreter/compiler, simulation, web app, emulator, …), create its folder and a full roadmap.
- Prefer zero or minimal dependencies so things run anywhere.

## Small collections (`mini/`)
- Each collection folder has a `README.md` listing its files with one line each.
- Each file is self-contained and runnable.

## Style
- Python: 3.10+, type hints, docstrings. JS: modern ES modules, no build step if possible.
- Keep the repo organized; never dump files in the root.
