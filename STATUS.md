# Status

- **Runs completed:** 164
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–137 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; 128 = generic `rolling-*-pow`, 129–131 = hash-table helpers, 132 = string helpers, 133 = list rotate/pairs/runs, 134 = interleave/chunk/windows/split-at/cartesian/transpose, 135 = insert-at/remove-at/intersperse/subsets/combinations/permutations, 136 = scan/take-every/flatten-once/argmax/argmin, 137 = last/count-if/zip-with/partition/unique/drop-last). **Put future prelude additions in `prelude129.lisp`** (loaded by `evaluator.py`).
- **Next up:** tick phases 129–137 in ROADMAP (skipped again, file is 19 KB); Phase 138 (more string or list helpers in `prelude129.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 164 done (NEW tilings); run 165 = add to oldest-updated collection
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 666 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-005 started (run 140), holds runs 140–164 (25 entries — FULL; next run creates part-006)
