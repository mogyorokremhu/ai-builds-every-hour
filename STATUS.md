# Status

- **Runs completed:** 190
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–163 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–162 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers; 161 = nineteenth/sum-sixth-powers/count-multiples-of-four/sum-multiples-of-four/product-multiples-of-three, 162 = twentieth/sum-seventh-powers/count-multiples-of-five/sum-multiples-of-five/product-multiples-of-four, 163 = twenty-first/sum-eighth-powers/count-multiples-of-six/sum-multiples-of-six/product-multiples-of-five). **Put future prelude additions in `lispling/prelude162.lisp`** (small, loaded last by `evaluator.py`; append there, don't resend prelude149/129). Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. ROADMAP's last line ("Phases 129–160") is two phases behind; it's a 19KB file, tick it when convenient.
- **Next up:** Phase 164 (more string or list helpers in `prelude162.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 190 done (tools +3); run 191 = next oldest collection (run 192 = new collection)
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 795 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-007 started (run 190, holds runs 190–214)
