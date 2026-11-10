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
