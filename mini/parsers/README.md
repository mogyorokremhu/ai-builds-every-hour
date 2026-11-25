# parsers

Small hand-written parsers, each with a built-in self-check.

- `shunting_yard.py` — infix to RPN with precedence/associativity, then evaluation.
- `json_parser.py` — recursive-descent JSON parser verified against `json.loads`.
- `csv_parser.py` — CSV state machine with quotes and embedded newlines.
