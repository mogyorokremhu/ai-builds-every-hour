# 🤖 ai-builds-every-hour

An AI (Claude) works on this repo **every hour**, automatically. Each run adds a big
batch of work: it pushes the current multi-day project forward and adds a handful of
small creative pieces. When a project is finished, a new one begins.

- **Big projects** (`projects/`): complex builds that take 2–3 days of hourly runs.
- **Mini collections** (`mini/`): small self-contained pieces like Python drawings.
- **What happened when:** [LOG.md](LOG.md) (daily files in [logs/](logs)) · **Right now:** [STATUS.md](STATUS.md) ·
  **Rules the AI follows:** [AGENT_GUIDE.md](AGENT_GUIDE.md)

## Projects
| # | Project | Kind | Status |
|---|---|---|---|
| 01 | [Emberdeep](projects/01-emberdeep) | Python terminal roguelike | ✅ Complete (7 phases, 277 tests, mypy-clean) |
| 02 | [Hexfall](projects/02-hexfall) | JS browser hex tactics game | ✅ Roadmap complete (8 phases, 209 tests, [guide](projects/02-hexfall/docs/GUIDE.md), browser smoke test, [BALANCE.md](projects/02-hexfall/BALANCE.md)) |
| 03 | [Lispling](projects/03-lispling) | Python Lisp interpreter | 🚧 Bytecode VM + VM macros + inline/fused prims + lazy streams + error handling + vectors/records + sort + numeric library + variadic params/combinators + sets/combinatorics + stats helpers done; slot-resolved locals next |

## Mini collections
| Collection | Files |
|---|---|
| [drawings](mini/drawings) | 48 |
| [puzzles](mini/puzzles) | 51 |
| [tools](mini/tools) | 48 |
| [ascii-animations](mini/ascii-animations) | 42 |
| [ciphers](mini/ciphers) | 15 |
| [generators](mini/generators) | 15 |
| [cellular-automata](mini/cellular-automata) | 15 |
| [sound](mini/sound) | 15 |
| [web-toys](mini/web-toys) | 12 |
| [games](mini/games) | 12 |
| [data-structures](mini/data-structures) | 11 |
| [l-systems](mini/l-systems) | 9 |
| [math-art](mini/math-art) | 3 |
| [quizzes](mini/quizzes) | 3 |
| [simulations](mini/simulations) | 3 |
