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
- [ ] Dotted pairs and real cons cells
- [ ] Better error messages with source positions

## Phase 3 — Macros & library
- [x] `define-macro` (non-hygienic)
- [x] Standard library written in Lispling (prelude.lisp)
- [ ] Strings and chars library, `assoc`, hash tables
- [ ] Tail-call-safe `cond`/`and`/`or` audit

## Phase 4 — Tooling
- [ ] Example programs (fib, primes, queens)
- [ ] Bytecode compiler + VM experiment
- [ ] Benchmarks vs the tree-walker
