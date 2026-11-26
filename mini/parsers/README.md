# parsers

Small hand-written parsers, each with a built-in self-check.

- `shunting_yard.py` — infix to RPN with precedence/associativity, then evaluation.
- `json_parser.py` — recursive-descent JSON parser verified against `json.loads`.
- `csv_parser.py` — CSV state machine with quotes and embedded newlines.
- `ini_parser.py` — INI sections/keys/comments with bool, int and float coercion.
- `arg_parser.py` — getopt-style parser for `--long`, `--k=v`, `-abc`, `-o value` and `--`.
- `s_expr_parser.py` — s-expression tokenizer/reader to nested lists, plus a printer.
