# Emberdeep balance report

Automated bot runs: **1000** (seeds 1–1000), 3025s wall time

| Metric | Value |
|---|---|
| Victories | 270 (27.0%) |
| Timeouts (bot got stuck) | 0 |
| Mean deepest depth | 8.45 |
| Mean character level | 11.70 |
| Mean turns | 3928 |
| Mean kills | 240.8 |
| Mean potions / scrolls used | 17.4 / 20.8 |
| Runs that used an iron key | 767 |

## Deepest depth reached

| Depth | Runs | Share | |
|---|---|---|---|
| 2 | 7 | 0.7% | █ |
| 3 | 21 | 2.1% | █ |
| 4 | 79 | 7.9% | ███ |
| 5 | 41 | 4.1% | ██ |
| 6 | 42 | 4.2% | ██ |
| 7 | 115 | 11.5% | █████ |
| 8 | 62 | 6.2% | ██ |
| 9 | 36 | 3.6% | █ |
| 10 | 597 | 59.7% | ████████████████████████ |

## How runs ended

| Cause | Runs |
|---|---|
| victory | 270 |
| killed by Ember Guardian | 168 |
| burned to death | 164 |
| killed by magma hound | 102 |
| succumbed to poison | 67 |
| killed by ember imp | 53 |
| killed by cave troll | 43 |
| starved to death | 37 |
| incinerated by the Ember Guardian | 32 |
| drank liquid fire | 14 |
| killed by kobold | 12 |
| killed by jackal | 11 |
| killed by fire beetle | 10 |
| killed by cave spider | 9 |
| killed by myconid | 3 |
| burned by a fire trap | 2 |

## Hour 7: the 1000-run sweep

Run after encumbrance, scavenging kobolds, explore mode and the run timeline landed. The
bot now has to manage its load (it drops the heaviest spare item when burdened), which costs
it speed in the late game. **27.0% wins over 1000 seeds** — inside the 25–40% target band,
so no numbers were changed. Observations for future tuning:

* 60% of runs reach depth 10; the Ember Guardian (melee + incineration) ends a third of those.
  That is the intended final exam, but if humans find it too hard, `ENRAGE_POWER` is the
  first knob to turn.
* Fire is the biggest killer overall (burned to death + magma hounds + imps ≈ 32% of runs).
  Fire resistance gear would be a natural future addition.
* Starvation is rare (3.7%), so the food clock is about right for a thorough player.

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
Guardian and the healing supply were tightened again, giving 53% wins over 200 seeds. The bot is
thorough (it clears every level), so a human usually sees fewer fights but also less XP.
Target band: a bot win rate around 25–40%, with deaths spread across all three themes.

Regenerate with:

```bash
python -m emberdeep.bot 1000 report.md   # ~50 min on 2 cores; compare with the numbers above
```
