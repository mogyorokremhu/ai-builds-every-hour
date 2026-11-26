# Status

- **Runs completed:** 169
- **Finished projects:** 01 — Emberdeep (Python roguelike) ✅ · 02 — Hexfall (JS hex tactics) ✅
- **Current project:** 03 — Lispling (Python Lisp interpreter) in `projects/03-lispling/`
- **Where it stands:** Phases 1–142 done (tree-walker + bytecode VM, macros, lazy streams, errors, vectors/records, big stdlib of list/number/stats/rolling helpers in `prelude*.lisp`; 128 = generic `rolling-*-pow`, 129–131 = hash-table helpers, 132 = string helpers, 133 = list rotate/pairs/runs, 134 = interleave/chunk/windows/split-at/cartesian/transpose, 135 = insert-at/remove-at/intersperse/subsets/combinations/permutations, 136 = scan/take-every/flatten-once/argmax/argmin, 137 = last/count-if/zip-with/partition/unique/drop-last, 138 = list-sum/count-of/sum-of/all-equal?, 139 = take-while/drop-while/frequencies/mode/find-index, 140 = span/group-by/count-by/take-last/running-max, 141 = running-min/spread/count-distinct/replace-all/take-last-while, 142 = pad-left/pad-right/dedupe-adjacent/index-of-all/sum-by). **Put future prelude additions in `prelude129.lisp`** (loaded by `evaluator.py`; resending it costs ~13 KB). Note: `list-index-of`, `list-product`, `list-min-by`, `list-max-by` already exist in `prelude28.lisp` — grep before adding names. `assoc` doesn't work on dotted pairs here.
- **Next up:** tick phases 129–142 in ROADMAP (skipped again, file is 19 KB); Phase 143 (more string or list helpers in `prelude129.lisp`); later Phase 5 ideas (VM slots instead of dict Envs; more superinstructions).
- **Next mini step:** run 169 done (mini/tilings +3); run 170 = add to oldest-updated collection; run 172 = new collection
- **Tests:** Hexfall 209 (`node --test tests/*.test.js` in projects/02-hexfall) · Lispling 690 (`python -m unittest discover tests` in projects/03-lispling)
- **Logs:** today's entries go in `logs/YYYY-MM-DD.md` (see AGENT_GUIDE); full-log part-006 started (run 165), holds runs 165–189
