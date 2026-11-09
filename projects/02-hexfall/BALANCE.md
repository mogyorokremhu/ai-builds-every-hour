# Hexfall balance notes

Generated with `node tools/balance.mjs --games 20` (seeds 1–20, symmetric maps, 30-turn limit).
Analysis lives in `src/balance.js` (tested in `tests/balance.test.js`). "Kills/100g" is kills
credited per 100 gold of recruit cost; the Healer's kills are mostly incidental.

## Findings (run 25)

- **Side bias:** none significant (|z| < 1.96 in both series). Symmetric maps are fair.
- **Mage** is the clear outlier: ~3x the median kills per gold in both series, but the AI only
  recruits it ~10 times in 20 games, so it is under-used rather than too weak or strong. Candidate
  change: nothing yet — first teach the AI to recruit more mages, then re-measure.
- **Rogue** underperforms (1–2.6 kills/100g) while being recruited ~50 times: the AI recruits it as
  a cheap filler and its backstab/envenom rarely finish kills. Candidate: lower envenom cost or let
  the AI score flanking positions higher.
- **Healer** is almost never recruited by the AI (0–1 per 20 games). Candidate: a recruit bonus when
  the army has 4+ melee units.
- **Cavalry** is mildly strong (1.2–1.5 kills/recruit), consistent with its 20 gold price.
- Spearman, Swordsman and Archer sit within ±15% of each other: healthy.
- Games are decided by village holds (17–19 of 20), not by routs.

## Run 26 — AI recruiting tweak

`RECRUIT_MIX` changed: mage 1.4 → 1.7, healer 1 → 1.1 (plus x2.5 when the army has 4+ melee units
and no healer), rogue 1.4 → 1.15. First attempt (mage 2.4, rogue 0.9) overshot: mages 56–73 recruits,
rogues ~1, red share 75% in one series. Final numbers over 20 games per series: healers recruited
18–23 (was 0–1), mages 11–16 (was 9), rogues 22–27 (was ~49). Mage stays efficient (10–11 kills/100g),
healers still score few kills by design. No side bias (z 0.45–0.89).

## Raw reports (run 25, before the tweak)

### normal (red) vs normal (blue)

20 games, avg 14.9 turns. Red 11 – blue 9 (red share 55%, z=0.45). End reasons: hold 19, turns 1.

| Unit | Cost | Recruited | Kills | Kills/recruit | Kills/100g |
|---|---|---|---|---|---|
| Spearman | 14 | 71 | 46 | 0.65 | 4.6 |
| Swordsman | 17 | 61 | 53 | 0.87 | 5.1 |
| Archer | 15 | 41 | 28 | 0.68 | 4.6 |
| Cavalry | 20 | 51 | 77 | 1.51 | 7.5 |
| Mage | 20 | 9 | 26 | 2.89 | 14.4 |
| Healer | 16 | 0 | 4 | 0.00 | 0.0 |
| Rogue | 15 | 49 | 8 | 0.16 | 1.1 |

Ability uses: shieldwall 222, heal 187, volley 98, charge 98, rally 92, envenom 62, fireball 35.

Flags:
- Mage overperforms (14.4 kills/100g vs median 5.1)
- Rogue underperforms (1.1 kills/100g vs median 5.1)
- Healer was never recruited

### hard (red) vs easy (blue)

20 games, avg 15.4 turns. Red 13 – blue 7 (red share 65%, z=1.34). End reasons: hold 17, rout 2, turns 1.

| Unit | Cost | Recruited | Kills | Kills/recruit | Kills/100g |
|---|---|---|---|---|---|
| Spearman | 14 | 68 | 48 | 0.71 | 5.0 |
| Swordsman | 17 | 62 | 57 | 0.92 | 5.4 |
| Archer | 15 | 40 | 31 | 0.78 | 5.2 |
| Cavalry | 20 | 55 | 66 | 1.20 | 6.0 |
| Mage | 20 | 10 | 32 | 3.20 | 16.0 |
| Healer | 16 | 1 | 3 | 3.00 | 18.8 |
| Rogue | 15 | 52 | 20 | 0.38 | 2.6 |

Ability uses: heal 193, shieldwall 187, volley 104, charge 98, rally 88, envenom 79, fireball 32.

Flags:
- Mage overperforms (16.0 kills/100g vs median 5.4)
- Healer overperforms (18.8 kills/100g vs median 5.4)
- Rogue underperforms (2.6 kills/100g vs median 5.4)
