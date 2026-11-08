# 🛠️ Tools

Small, dependency-free command-line utilities. Each runs with `python <file>.py`
(use `--help` or read the docstring for options).

| File | What it does |
|---|---|
| `calc.py` | Safe calculator with a Pratt parser: precedence, `**`, variables, functions, REPL with `ans` |
| `hexdump.py` | Colourful `xxd`-style hexdump with adjustable width and a reverse (`-r`) mode |
| `passphrase.py` | Passphrases/passwords from `secrets` with entropy estimates and a strength checker |
| `tree.py` | Directory tree with human-readable sizes, depth limit and size sorting |
| `wordfreq.py` | Word-frequency bar chart plus text statistics (stopword filtering) |
| `units.py` | Unit converter with dimensional analysis (`km/h`, `kg*m/s^2`, `kWh`) and temperatures |
| `linediff.py` | Myers O(ND) line diff printed as a coloured unified diff with hunks (`-U n`, diff-style exit code) |
| `csvview.py` | CSV as a boxed, aligned table: delimiter sniffing, `--sort`, `--where`, `--cols`, `--stats` |
| `jsonq.py` | Tiny jq: `.a[0].b`, `[]` iteration, `[?age>30]` filters, pipes (`length`, `uniq`, `sum`…), colours |
| `baseconv.py` | Number in every base at once (hex/oct/bin/base36, roman numerals, bytes, two's complement) |
| `cronnext.py` | Explains a cron expression in English and lists its next run times (names, steps, `@daily`) |
| `mdtoc.py` | Markdown table of contents with GitHub-style anchors; `--write` updates it in place |
