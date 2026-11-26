# Status

- **Runs completed:** 188
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–161 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–161 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers; 160 = eighteenth/sum-fifth-powers/product-nonzero/count-multiples-of-three/sum-multiples-of-three, 161 = nineteenth/sum-sixth-powers/count-multiples-of-four/sum-multiples-of-four/product-multiples-of-three). **Put future prelude additions in `lispling/prelude149.lisp`** (small, loaded by `evaluator.py`; append there, don't resend prelude129). Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. ROADMAP's last line ("Phases 129–160") is one phase behind; it's a 19KB file, tick it when convenient.
- **Next up:** Phase 162 (more string or list helpers in `prelude149.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 188 done (new mini/os-sims); run 189 = puzzles/tools next
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 785 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-006 started (run 165), holds runs 165–189 (run 188 included)
