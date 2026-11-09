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
| `mdtoc.py` | Table of contents for a Markdown file (GitHub-style anchors), printed or written between `<!-- toc -->` markers |
| `baseconv.py` | Lighter twin of `bases.py`: one number shown in many bases, bytes and Roman numerals (`--from N`) |
| `cronnext.py` | Lighter twin of `cronx.py`: cron expression in English + next runs (`-n`, `--from`) |
| `linediff.py` | Lighter twin of `difftool.py`: Myers diff as a coloured unified diff (`-U`, `--demo`) |
| `cipher.py` | Caesar / ROT13 / Vigenère / Atbash, plus a Caesar cracker ranked by letter frequency and common words |
| `slug.py` | Slug, snake, kebab, camel, Pascal, title and CONSTANT case (accents folded, camelCase split); `--all` |
| `ageof.py` | Calendar difference between dates (years/months/days, weeks, weekday, next anniversary; Feb 29 aware) |
| `wc2.py` | Lines / words / chars / bytes / longest line for files or stdin |
| `roman.py` | Integer ↔ Roman numeral converter (1..3999, round-trip self-tested) |
| `dedupe.py` | Remove repeated lines keeping first occurrences (`-c` counts, `-i` ignore case) |
| `uniqwords.py` | Distinct words from files/stdin in first-seen order (`-s` sort, `-i` ignore case) |
| `epoch.py` | Unix timestamp (s or ms) ↔ ISO date converter, `now` |
| `histo.py` | Text histogram of numbers with adjustable bins (`-b`) |
| `stats.py` | Count, min, quartiles, median, mean and stdev of numbers from a file or stdin |
| `rot.py` | Reverse lines (`-r`), word order (`-w`) or characters (`-c`) of stdin |
| `bar.py` | Bar chart from `label value` lines on stdin |
| `lorem.py` | Seeded lorem-ipsum paragraphs (`-p`, `-s`) |
| `b64.py` | Base64 encode/decode stdin (`-d`, `--url`) |
| `grepc.py` | Count regex matches per file (`-i`) |

(The three "twins" come from two parallel runs in hour 7 that built the same ideas independently.)

Most tools also accept `--selftest` to run their built-in checks.
