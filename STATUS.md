# Status

- **Runs completed:** 210
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–185 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–183 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers; 185 = forty-third, sum-30th-powers, multiples-of-28, product-multiples-of-27; 184 = forty-second, sum-29th-powers, multiples-of-27, product-multiples-of-26; 183 = forty-first, sum-28th-powers, multiples-of-26, product-multiples-of-25). **Put future prelude additions in `lispling/prelude178.lisp` (loaded last by `evaluator.py`; append there, don't resend prelude162/149/129).** Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. ROADMAP's last line ("Phases 129–160") is several phases behind (phases 161–185 ticks not pushed; 19KB file).
- **Next up:** Phase 186 (more string or list helpers in `prelude178.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 210 done (number-theory +3); then rotation: os-sims, parsers, then next-oldest
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 905 (`python -m unittest discover tests` in projects/03-lispling; full suite is slow, run only the phase file)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-007 (holds runs 190–210, 21 entries)
