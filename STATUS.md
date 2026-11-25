# Status

- **Runs completed:** 158
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–131 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; 128 = generic `rolling-*-pow`, 129–131 = hash-table helpers). **Put future prelude additions in `prelude129.lisp`** (loaded by `evaluator.py`).
- **Next up:** tick phases 129–131 in ROADMAP (skipped runs 157–158, file is large); then Phase 132 (more hash/alist helpers or string utils in `prelude129.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 158 done (ascii-animations +3); run 159 = existing collection (oldest-updated first: compression, graphs, interpreters); run 160 = NEW collection
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 636 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-005 started (run 140), holds runs 140–164
