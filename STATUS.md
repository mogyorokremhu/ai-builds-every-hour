# Status

- **Runs completed:** 157
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–130 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; 128 = generic `rolling-*-pow`, 129–130 = hash-table helpers). **Put future prelude additions in `prelude129.lisp`** (loaded by `evaluator.py`).
- **Next up:** tick phases 129–130 in ROADMAP (skipped run 157, file is large); then Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 157 done (geometry +3); run 158 = existing collection (oldest-updated first)
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 631 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-005 started (run 140), holds runs 140–164
