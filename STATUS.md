# Status

- **Runs completed:** 203
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–176 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–168 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers; 169–171 = twenty-seventh/…/twenty-ninth; 172 = thirtieth/…; 173 = thirty-first/…/multiples-of-sixteen; 174 = thirty-second/sum-nineteenth-powers/multiples-of-seventeen/product-multiples-of-sixteen; 175 = thirty-third/…; 176 = thirty-fourth/sum-twenty-first-powers/multiples-of-nineteen/product-multiples-of-eighteen). **Put future prelude additions in `lispling/prelude162.lisp`** (small, loaded last by `evaluator.py`; append there, don't resend prelude149/129). Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. ROADMAP's last line ("Phases 129–160") is several phases behind (phases 161–176 ticks not pushed; 19KB file).
- **Next up:** Phase 177 (more string or list helpers in `prelude162.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 203 done (logic +3); run 204 = NEW collection (run number divisible by 4)
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 860 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-007 (holds runs 190–214, 14 entries)
