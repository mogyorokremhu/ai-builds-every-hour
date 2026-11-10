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
