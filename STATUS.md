# Status

- **Runs completed:** 193
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–166 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–166 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers; 166 = twenty-fourth/sum-eleventh-powers/count-multiples-of-nine/sum-multiples-of-nine/product-multiples-of-eight). **Put future prelude additions in `lispling/prelude162.lisp`** (small, loaded last by `evaluator.py`; append there, don't resend prelude149/129). Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. ROADMAP's last line ("Phases 129–160") is several phases behind; it's a 19KB file, tick it when convenient.
- **Next up:** Phase 167 (more string or list helpers in `prelude162.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 193 done (mini/voting +3); run 194 = oldest-updated collection (os-sims or finance); run 196 = new collection
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 810 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-007 (holds runs 190–214)
