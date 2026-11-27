# Status

- **Runs completed:** 200
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–173 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–168 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers; 169–171 = twenty-seventh/…/twenty-ninth; 172 = thirtieth/…; 173 = thirty-first/sum-eighteenth-powers/multiples-of-sixteen/product-multiples-of-fifteen). **Put future prelude additions in `lispling/prelude162.lisp`** (small, loaded last by `evaluator.py`; append there, don't resend prelude149/129). Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. ROADMAP's last line ("Phases 129–160") is several phases behind (phases 161–173 ticks not pushed either); it's a 19KB file, tick it when convenient.
- **Next up:** Phase 174 (more string or list helpers in `prelude162.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 200 done (NEW music-theory); run 201 = existing collection (oldest-updated first)
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 845 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-007 (holds runs 190–214, 11 entries)
