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
| `jsonq.py` | JSON pretty-printer/minifier/validator with caret error locations and `users[*].name` path queries |
| `cronx.py` | Explains a cron expression in English and lists its next run times (names, steps, `@daily`, dom/dow OR rule) |
| `difftool.py` | Line diff built on Myers' O(ND) algorithm: coloured unified hunks or side-by-side view, `-w` |
| `csvview.py` | CSV as an aligned box/Markdown table with `--where` filters, numeric-aware `--sort` and `--stats` |
| `bases.py` | Number in every base: hex/octal/grouped binary, base 36, two's complement, Roman numerals, bit ruler |
| `timer.py` | Countdown / stopwatch / pomodoro with big block digits, progress bar and a bell |

Most tools also accept `--selftest` to run their built-in checks.
