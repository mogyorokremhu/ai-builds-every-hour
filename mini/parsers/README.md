# parsers

Small hand-written parsers, each with a built-in self-check.

- `shunting_yard.py` — infix to RPN with precedence/associativity, then evaluation.
- `json_parser.py` — recursive-descent JSON parser verified against `json.loads`.
- `csv_parser.py` — CSV state machine with quotes and embedded newlines.
- `ini_parser.py` — INI sections/keys/comments with bool, int and float coercion.
- `arg_parser.py` — getopt-style parser for `--long`, `--k=v`, `-abc`, `-o value` and `--`.
- `s_expr_parser.py` — s-expression tokenizer/reader to nested lists, plus a printer.
- `url_parser.py` — regex-free URL splitter (scheme, userinfo, host, port, path, query, fragment) checked against urllib.
- `toml_lite_parser.py` — TOML subset (tables, nested tables, scalars, arrays) checked against tomllib.
- `markdown_inline.py` — recursive Markdown inline parser (bold, italic, code, links) to escaped HTML.
