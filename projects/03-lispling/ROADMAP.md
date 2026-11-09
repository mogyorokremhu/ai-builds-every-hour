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
- [x] Strings library (chars are 1-char strings), `assoc`, hash tables
- [x] Tail-call-safe `cond`/`and`/`or` audit (and/or last operand now a tail call)

## Phase 4 — Tooling
- [x] Example programs (fib, primes, queens, wordcount)
- [ ] Bytecode compiler + VM experiment
- [ ] Benchmarks vs the tree-walker
