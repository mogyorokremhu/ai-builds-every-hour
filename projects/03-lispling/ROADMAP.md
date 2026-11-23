# Lispling roadmap

## Phase 1 — Core
- [x] Tokenizer and parser (comments, strings, quote sugar)
- [x] Evaluator: quote, if, define, set!, lambda, begin, let, cond, and, or
- [x] Tail-call optimisation
- [x] Arithmetic, comparison and list builtins
- [x] REPL with multi-line input
- [x] Unit tests

## Phase 2 — Language growth
- [x] `let*`, `letrec`, named `let`, `do` loops
- [x] Quasiquote / unquote
- [x] `map`, `filter`, `reduce`, `apply`, `for-each`
- [x] Dotted pairs (`pairs.py`: `Pair` only when cdr is not a list; reader, printer, car/cdr/cons, `pair?`)
- [x] Better error messages with source positions (`diagnostics.py`)

## Phase 3 — Macros & library
- [x] `define-macro` (non-hygienic)
- [x] Standard library written in Lispling (prelude.lisp)
- [x] Strings library (chars are 1-char strings), `assoc`, hash tables
- [x] Tail-call-safe `cond`/`and`/`or` audit (and/or last operand now a tail call)

## Phase 4 — Tooling
- [x] Example programs (fib, primes, queens, wordcount)
- [x] Bytecode compiler + VM experiment (`vm.py`: core forms, explicit frame stack, tail calls, disassembler)
- [x] Benchmarks vs the tree-walker (`benchmarks/bench.py` compares both; VM only ~1.0-1.2x faster so far)

## Phase 5 — Ideas
- [x] VM: named let, let*, letrec, do, quasiquote (via shared expanders)
- [ ] VM: resolve locals to slots instead of dict Envs (the real speedup)
- [x] Constant folding of integer + - * (compile time)
- [x] VM: compile-time macro expansion + `define-macro` (`_CENV`, test_phase10.py)
- [x] Inline binary primitive ops (`PRIM2`: + - * < > <= >= =, runtime guard if redefined/shadowed; test_phase11.py; ~1.1-1.2x)
- [x] Inline unary primitives (`PRIM1`: car cdr null? not zero? pair?, same runtime guard; test_phase12.py)
- [x] Inline env-chain lookup in LOAD/PRIM guards (`_lookup`, test_phase13.py; no measurable speedup — slots still needed)
- [x] Fused superinstruction `PRIM2LC` (LOAD var, CONST, PRIM2 in one op; `Code.targets` guards jump targets; test_phase14.py)
- [x] `case` special form (expander; tree-walker + VM; test_phase15.py)
- [x] Lazy evaluation: `delay`/`force`/`cons-stream` + stream library in the prelude (test_phase16.py, examples/streams.lisp)
- [x] Error handling: `error`, `try`, `assert`, `when`/`unless` (test_phase17.py, examples/errors.lisp)
- [x] Vectors + `define-record-type` (test_phase18.py, examples/records.lisp)
- [x] Sorting + list utilities in the prelude (`sort`, `list-ref`, `partition`, ... ; test_phase19.py, examples/sorting.lisp)
- [x] Folds + list utilities (`fold-left/right`, `append-map`, `iota`, `any`, `every`, `count`, `zip`, `remove-duplicates`; test_phase20.py, examples/folds.lisp)
- [x] take-while/drop-while, filter-map, alist-set/ref, hash-update!, group-by, string-pad-left/right, string-prefix?/suffix? (test_phase21.py, examples/utils.lisp)
- [x] Numeric library: gcd/lcm/quotient/remainder/modulo/expt/floor/ceiling/round/truncate/number->string-radix + square/digits/memq/list-copy (test_phase22.py, examples/numbers.lisp)
- [x] Functional helpers: butlast/curry/flip/max-by/min-by/interleave/transpose/chunk/frequencies (test_phase23.py, examples/functional.lisp)
- [x] Variadic parameters (`(define (f . rest))`, `(lambda args ...)`) in evaluator + VM (test_phase24.py, examples/variadic.lisp)
- [x] Variadic `curry`/`partial`, `constantly`, `complement`, `juxt`, `compose*` (test_phase25.py, examples/combinators.lisp)
- [x] Strings & chars: char predicates, string comparisons/trim/titlecase/count, string-map/filter/take/drop, palindrome?, caesar-shift (test_phase26.py, examples/strings2.lisp)
- [x] Set ops, combinatorics (`combinations`/`permutations`/`power-set`), vector utilities incl. binary search (test_phase27.py, examples/sets_combinatorics.lisp)
- [x] Phase 28 (`prelude28.lisp`): make-list/list-tabulate/product/split-at/span/break/insert-at/delete-at, tree-map/leaves/depth, alist helpers (test_phase28.py, examples/phase28.lisp)
- [x] Phase 29: find/find-tail, list-max/min, average/median/mode, flatmap, vector-swap!/reverse! (test_phase29.py, examples/phase29.lisp)
- [x] Phase 30: prime?/primes-up-to/prime-factors/fib-list, dot-product/identity-matrix/mat-mul/mat-pow (test_phase30.py, examples/phase30.lisp)
- [x] Phase 31: factorial/binomial/divisors/perfect?/totient/mod-expt/digits->number/collatz-length (test_phase31.py, examples/phase31.lisp)
- [x] Phase 32: gcd-list/lcm-list/digit-sum/reverse-number/palindrome-number?/triangular/isqrt/perfect-square?/pascal-row/happy? (test_phase32.py, examples/phase32.lisp)
- [x] Phase 33: sliding-window/take-every/rle/rle-decode/dedupe-adjacent/scan-left/prefix-sums/unfold (test_phase33.py, examples/phase33.lisp)
- [x] Phase 34: rotate-left/right, index-of, last-index-of, zip-with, range-step, flatten-depth (test_phase34.py, examples/phase34.lisp)
- [x] Phase 35: adjacent-pairs/last-n/drop-last/argmax/running-max/interpose (test_phase35.py, examples/phase35.lisp)
- [x] Phase 36: map-indexed/replicate/remove-nth/all-equal?/chunk-by/cumulative-sum (test_phase36.py, examples/phase36.lisp)
- [x] Phase 37: differences/take-last/split-on/min-max-list/flatten-once/zip3 (test_phase37.py, examples/phase37.lisp)
- [x] Phase 38: count-if/list-index-if/remove-if/sum-list/cartesian/map-pairs (test_phase38.py, examples/phase38.lisp)
- [x] Phase 39: member-if/subsequence?/all-pairs/sum-of-squares/dedupe-by (test_phase39.py, examples/phase39.lisp)
- [x] Phase 40: list-max-by/count-occurrences/take-nth/pairwise-map/mean-of-squares (test_phase40.py, examples/phase40.lisp)
- [x] Phase 41: list-min-by/range-sum/list-product/second/third/swap-pairs (test_phase41.py, examples/phase41.lisp)
- [x] Phase 42: last-element/init/take-until/count-while/sum-by/clamp/lerp (test_phase42.py, examples/phase42.lisp)
- [x] Phase 43: product-by/none?/second-last/sign/between?/nth-or/abs-diff (test_phase43.py, examples/phase43.lisp)
- [x] Phase 44: count-true/first-n-squares/average-by/ends/wrap-index/mid-range/inc-all (test_phase44.py, examples/phase44.lisp)
- [x] Phase 45: count-evens/count-odds/repeat-list/sum-evens/cube/negate-all/alternate (test_phase45.py, examples/phase45.lisp)
- [x] Phase 46: sum-odds/square-all/count-negatives/double-all/list-range-inclusive/take-while-positive/sum-abs (test_phase46.py, examples/phase46.lisp)
- [x] Phase 47: sum-squares/count-positives/drop-while-positive/list-range-exclusive/product-evens/triple-all/positives (test_phase47.py, examples/phase47.lisp)
- [x] Phase 48: sum-of-cubes/count-zeros/negatives/take-while-negative/quadruple-all/sum-positives/list-range-step-down (test_phase48.py, examples/phase48.lisp)
- [x] Phase 49: sum-negatives/product-positives/drop-while-negative/count-nonzero/quintuple-all/nonzeros/list-range-step-up (test_phase49.py, examples/phase49.lisp)
- [x] Phase 50: sum-odd-squares/count-multiples-of/multiples-of/sextuple-all/list-range-by/product-negatives/take-while-nonzero (test_phase50.py, examples/phase50.lisp)
- [x] Phase 51: sum-even-squares/evens-squared/septuple-all/product-odds/take-while-even/count-between/drop-while-nonzero (test_phase51.py, examples/phase51.lisp)
- [x] Phase 52: sum-multiples-of/octuple-all/count-less-than/count-greater-than/take-while-odd/drop-while-odd/odds-squared (test_phase52.py, examples/phase52.lisp)
- [x] Phase 53: nonuple-all/sum-between/evens-cubed/odds-cubed/product-multiples-of/drop-while-even/take-while-multiple-of (test_phase53.py, examples/phase53.lisp)
- [x] Phase 54: decuple-all/sum-less-than/sum-greater-than/count-multiples-between/evens-doubled/odds-doubled/take-while-less-than (test_phase54.py, examples/phase54.lisp)
- [x] Phases 55-56: stats helpers in `prelude55.lisp` (test_phase55.py, test_phase56.py)
- [x] Phase 57: correlation/z-scores/min-max-normalize/moving-average (test_phase57.py, examples/phase57.lisp)
- [x] Phase 58: percentile/interquartile-range/ranks/normalize-sum (test_phase58.py, examples/phase58.lisp)
- [x] Phase 59: root-mean-square/harmonic-mean/geometric-mean/trimmed-mean (test_phase59.py, examples/phase59.lisp)
- [x] Phase 60: sum-squared-deviations/coefficient-of-variation/standard-error/midrange-of (test_phase60.py, examples/phase60.lisp)
- [x] Phase 61: sum-absolute-deviations/pearson-skewness/median-absolute-deviation/weighted-variance (test_phase61.py, examples/phase61.lisp)
- [x] Phase 62: skewness/excess-kurtosis/kurtosis/cumulative-mean (test_phase62.py, examples/phase62.lisp)
- [x] Phase 63: mean-absolute-error/mean-squared-error/root-mean-squared-error/running-min (test_phase63.py, examples/phase63.lisp)
- [x] Phase 64: linear-slope/linear-intercept/r-squared/running-max-min-range (test_phase64.py, examples/phase64.lisp)
- [x] Phase 65: predict-linear/residuals/max-error/mean-absolute-percentage-error (test_phase65.py, examples/phase65.lisp)
- [x] Phase 66: mean-bias/smape/normalized-rmse/cumulative-error (test_phase66.py, examples/phase66.lisp)
- [x] Phase 67: weighted-mean/exponential-moving-average/relative-error/median-absolute-error (test_phase67.py, examples/phase67.lisp)
- [x] Phase 68: rolling-sum/rolling-max/rolling-min/rolling-range (test_phase68.py, examples/phase68.lisp)
- [x] Phase 69: rolling-mean/rolling-median/rolling-variance/rolling-product (test_phase69.py, examples/phase69.lisp)
- [x] Phase 70: rolling-std-dev/rolling-sum-squares/rolling-geometric-mean/rolling-midrange (test_phase70.py, examples/phase70.lisp)
- [x] Phase 71: rolling-argmax/rolling-argmin/rolling-count-if/rolling-change (test_phase71.py, examples/phase71.lisp)
- [x] Phase 72: rolling-percent-change/rolling-mad/rolling-zscore-last/rolling-distinct (test_phase72.py, examples/phase72.lisp)
- [x] Phase 73: rolling-first/rolling-last/rolling-sum-abs/rolling-mean-abs (test_phase73.py, examples/phase73.lisp)
- [x] Phase 74: rolling-count-nonzero/rolling-sum-positive/rolling-sum-negative/rolling-spread (test_phase74.py, examples/phase74.lisp)
- [x] Phase 75: rolling-count-positive/rolling-count-negative/rolling-max-abs/rolling-sum-evens (test_phase75.py, examples/phase75.lisp)
- [x] Phase 76: rolling-sum-odds/rolling-min-abs/rolling-count-evens/rolling-count-odds (test_phase76.py, examples/phase76.lisp)
- [x] Phase 77: rolling-count-zero/rolling-sum-cubes/rolling-product-abs/rolling-count-above (test_phase77.py, examples/phase77.lisp)
- [x] Phase 78: rolling-count-below/rolling-sum-below/rolling-count-between/rolling-sum-above (test_phase78.py, examples/phase78.lisp)
- [x] Phase 79: rolling-sum-between/rolling-count-equal/rolling-count-outside/rolling-count-multiples (test_phase79.py, examples/phase79.lisp)
- [x] Phase 80: rolling-count-not-equal/rolling-sum-outside/rolling-count-nonmultiples/rolling-sum-multiples (test_phase80.py, examples/phase80.lisp)
