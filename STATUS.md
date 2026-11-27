# Status

- **Runs completed:** 215
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–190 done (190 = forty-eighth, sum-35th-powers, multiples-of-33, product-multiples-of-32; 189 = forty-seventh, sum-34th-powers, multiples-of-32, product-multiples-of-31; 188 = forty-sixth, sum-33rd-powers, multiples-of-31, product-multiples-of-30) (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; phases 128–183 = rolling-pow, hash-table, string and many list/counting/summing/nth-element helpers). **Put future prelude additions in `lispling/prelude178.lisp` (loaded last by `evaluator.py`; append there, don't resend prelude162/149/129).** Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here. Odd powers of negatives are negative (test accordingly). ROADMAP's last line ("Phases 129–160") is several phases behind (phases 161–190 ticks not pushed; 19KB file).
- **Next up:** Phase 191 (more string or list helpers in `prelude178.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 215 done (probability +3); run 216 is divisible by 4 → start a NEW collection; then rotation: ascii-animations, compression, games, geometry, graphs, interpreters, math-art, quizzes, sound
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 930 (`python -m unittest discover tests` in projects/03-lispling; full suite is slow, run only the phase file)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-008 (runs 215–239 — holds 1 entry so far)
