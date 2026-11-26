# Status

- **Runs completed:** 189
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–162 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–162 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers; 161 = nineteenth/sum-sixth-powers/count-multiples-of-four/sum-multiples-of-four/product-multiples-of-three, 162 = twentieth/sum-seventh-powers/count-multiples-of-five/sum-multiples-of-five/product-multiples-of-four). **Put future prelude additions in `lispling/prelude162.lisp`** (small, loaded last by `evaluator.py`; append there, don't resend prelude149/129). Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. ROADMAP's last line ("Phases 129–160") is two phases behind; it's a 19KB file, tick it when convenient.
- **Next up:** Phase 163 (more string or list helpers in `prelude162.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 189 done (puzzles +3); run 190 = tools next (run 192 = new collection)
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 790 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-006 started (run 165) and is now full (runs 165–189); run 190 starts part-007 (create it + link it in full-log/README.md)
