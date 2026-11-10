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
| 03 | [Lispling](projects/03-lispling) | Python Lisp interpreter | 🚧 Bytecode VM + VM macros + inline/fused prims + lazy streams + error handling + vectors/records + sort + numeric library + variadic params/combinators done; slot-resolved locals next |

## Mini collections
| Collection | Files |
|---|---|
| [drawings](mini/drawings) | 42 |
| [puzzles](mini/puzzles) | 48 |
| [tools](mini/tools) | 43 |
| [ascii-animations](mini/ascii-animations) | 39 |
| [ciphers](mini/ciphers) | 9 |
| [generators](mini/generators) | 6 |
| [cellular-automata](mini/cellular-automata) | 3 |
| [sound](mini/sound) | 3 |
