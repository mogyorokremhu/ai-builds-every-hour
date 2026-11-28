# Status

- **Runs completed:** 227
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–202 done (202 = sixtieth, sum-47th-powers, multiples-of-45, product-multiples-of-44; 201 = fifty-ninth, sum-46th-powers, multiples-of-44, product-multiples-of-43; earlier phases 192–200 follow the same pattern: nth element, sum of Nth powers, count/sum multiples, product multiples) (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–183 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers). **Put future prelude additions in `lispling/prelude192.lisp` (phase 202 appended there too; loaded last by `evaluator.py`; append there — it's ~11KB; don't resend prelude178/162/149/129).** Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. Odd powers of negatives are negative, even powers positive (test accordingly). ROADMAP's last line ("Phases 129–160") is several phases behind (phases 161–202 ticks not pushed; 19KB file — skipped to save usage).
- **Next up:** Phase 203 (more string or list helpers in `prelude192.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 227 done (sound); then rotation: chess, evolution, ... (next new collection at run 228)
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 990 (`python -m unittest discover tests` in projects/03-lispling; full suite is slow, run only the phase file)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-008 (runs 215–239 — holds 13 entries so far)
