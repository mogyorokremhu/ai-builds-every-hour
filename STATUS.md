# Status

- **Runs completed:** 206
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–180 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–180 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers; 178–180 = thirty-sixth…thirty-eighth, sum-twenty-third…twenty-fifth-powers, multiples-of-twenty-one…twenty-three, product-multiples-of-twenty…twenty-two). **Put future prelude additions in `lispling/prelude178.lisp` (loaded last by `evaluator.py`; append there, don't resend prelude162/149/129).** Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. ROADMAP's last line ("Phases 129–160") is several phases behind (phases 161–180 ticks not pushed; 19KB file).
- **Next up:** Phase 181 (more string or list helpers in `prelude178.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 206 done (mini/sorting +3); run 207 = add to oldest-updated collection (rotation: generators, simulations, number-theory next); run 208 = NEW collection
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 880 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-007 (holds runs 190–214, 17 entries)
