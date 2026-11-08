# Emberdeep balance report

Automated bot runs: **200** (seeds 1–200), 455s wall time

| Metric | Value |
|---|---|
| Victories | 106 (53.0%) |
| Timeouts (bot got stuck) | 0 |
| Mean deepest depth | 8.51 |
| Mean character level | 11.98 |
| Mean turns | 4329 |
| Mean kills | 250.1 |
| Mean potions / scrolls used | 22.3 / 19.8 |
| Runs that used an iron key | 143 |

## Deepest depth reached

| Depth | Runs | Share | |
|---|---|---|---|
| 2 | 3 | 1.5% | █ |
| 3 | 7 | 3.5% | █ |
| 4 | 16 | 8.0% | ███ |
| 5 | 8 | 4.0% | ██ |
| 6 | 6 | 3.0% | █ |
| 7 | 15 | 7.5% | ███ |
| 8 | 8 | 4.0% | ██ |
| 9 | 5 | 2.5% | █ |
| 10 | 132 | 66.0% | ██████████████████████████ |

## How runs ended

| Cause | Runs |
|---|---|
| victory | 106 |
| burned to death | 17 |
| killed by magma hound | 15 |
| starved to death | 13 |
| killed by ember imp | 10 |
| killed by Ember Guardian | 9 |
| killed by cave troll | 7 |
| incinerated by the Ember Guardian | 5 |
| killed by jackal | 3 |
| killed by kobold | 3 |
| succumbed to poison | 3 |
| killed by myconid | 2 |
| killed by fire beetle | 2 |
| drank liquid fire | 2 |
| killed by poison dart | 1 |
| burned by a fire trap | 1 |

## Tuning history (hour 6)

The first bot runs on the untuned game (40 seeds) won only **5%** and over half of all deaths
were caused by ember imps: they kited perfectly (always stepping back when approached) and their
bolts set the player alight half the time. Changes made from the bot's numbers:

| Change | Before → after |
|---|---|
| Caster kiting (backs off when you close in) | always → 60% of the time |
| Ember bolt cooldown / burn chance | 3 turns, 50% → 4 turns, 35% |
| Ember imp spawn weight | 20 → 14 |
| Monster groups per area | `randint(0, 2 + depth//2)` → `randint(0, 2 + depth//3)` |
| XP curve | `40 + 35(l-1)` → `40 + 35(l-1) + 4(l-1)²` (the cap was reached too early) |
| Ember Guardian HP / power | 110 / 8 → 150 / 9 |
| Healing potion loot weight | 35 → 28 |

After the caster, spawn and XP changes the bot jumped to ~62% wins (60 seeds), so the
Guardian and the healing supply were tightened again; the report above is the result. The bot is thorough (it clears
every level), so a human usually sees fewer fights but also less XP. Target for the next
pass: a bot win rate around 25–40%, with deaths spread across all three themes.

Regenerate with:

```bash
python -m emberdeep.bot 200 report.md   # then compare with the numbers above
```
