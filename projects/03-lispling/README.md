# 03 — Lispling

A small Scheme-flavoured Lisp interpreter in pure Python (no dependencies).

```
python repl.py            # interactive
python repl.py prog.lisp  # run a file
python -m unittest discover tests
```

Layout: `lispling/reader.py` (tokenizer + parser), `types.py` (Symbol, Env, Lambda),
`builtins.py` (primitives), `stdlib.py` (strings, assoc, hash tables), `forms.py`/`higher.py`/`prelude.lisp`, `evaluator.py` (special forms, tail-call optimised).
Experimental bytecode compiler + stack VM: `lispling/vm.py` (`run_vm`), compare with `python benchmarks/bench.py`.
See [ROADMAP.md](ROADMAP.md).
