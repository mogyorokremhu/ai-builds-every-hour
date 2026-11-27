# Status

- **Runs completed:** 209
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–184 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–183 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers; 184 = forty-second, sum-29th-powers, multiples-of-27, product-multiples-of-26; 183 = forty-first, sum-28th-powers, multiples-of-26, product-multiples-of-25). **Put future prelude additions in `lispling/prelude178.lisp` (loaded last by `evaluator.py`; append there, don't resend prelude162/149/129).** Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. ROADMAP's last line ("Phases 129–160") is several phases behind (phases 161–184 ticks not pushed; 19KB file).
- **Next up:** Phase 185 (more string or list helpers in `prelude178.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 209 done (simulations +3); then rotation: number-theory, os-sims, parsers
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 900 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-007 (holds runs 190–214, 20 entries)
