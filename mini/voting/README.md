# voting

Voting-system demos on random ranked ballots, standard library only. Run from this folder.

- `ballots.py` — shared random ranked-ballot generator (seeded).
- `irv.py` — plurality vs instant-runoff (ranked-choice) with round-by-round tallies.
- `condorcet.py` — pairwise matrix, Condorcet winner, Copeland and Borda scores.
- `plurality.py` — first-past-the-post with majority check and top-two runoff.
- `approval.py` — approval voting where each voter approves their top k.
- `score_voting.py` — range voting with ranks mapped linearly to 0–10 scores.
