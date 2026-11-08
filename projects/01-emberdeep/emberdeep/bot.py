"""An automated player used for balance testing (``python -m emberdeep.bot``).

The bot is a simple but competent "greedy" player built only on the public :class:`Game`
API — it sees exactly what a human would (visible/explored cells, its own pack):

1. spend level-ups (alternating Might / Vitality / Guard);
2. survive: drink healing when low, gamble on unknown potions when desperate, eat, refuel;
3. wear the best gear it has found;
4. fight: zap scrolls at tough foes, otherwise melee the weakest adjacent enemy or close in;
5. loot: pick up items, walk to visible ones;
6. rest when hurt and safe;
7. explore the nearest unexplored frontier (cached BFS path), unlock doors with keys;
8. descend once the level is explored (or it has been here too long); force locked doors
   if it is shut in;
9. on depth 10, hunt down the Ember Guardian and grab the Ember Heart.

:func:`run_many` plays many seeded games (in parallel processes) and :func:`report` turns
the results into a Markdown balance report.
"""
from __future__ import annotations

import sys
import time
from collections import Counter
from dataclasses import dataclass

from . import encumbrance
from .game import Game
from .geometry import chebyshev
from .items import Item
from .pathfinding import astar

BOON_ORDER = ("m", "v", "g", "v")
LEVEL_TURN_LIMIT = 1600     # leave a level after this many turns even if not explored
MAX_ACTIONS = 30000         # hard cap per game (a stuck bot counts as a timeout)
REST_LIMIT = 60             # max consecutive turns spent resting


@dataclass
class RunResult:
    seed: int
    victory: bool
    depth: int
    level: int
    turns: int
    kills: int
    cause: str
    timeout: bool = False
    potions_used: int = 0
    scrolls_used: int = 0
    keys_used: int = 0


class Bot:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.level_turns = 0
        self.depth_seen = game.depth
        self.rest_streak = 0
        self.boon_i = 0
        self.stats = Counter()
        self.ignored: set[tuple[int, int]] = set()   # item cells it gave up walking to
        self.route: list[tuple[int, int]] = []       # cached path to the exploration frontier
        self.loot_goal: tuple[int, int] | None = None  # item cell it is walking to

    # ---- helpers --------------------------------------------------------
    @property
    def p(self):
        return self.game.player

    def pack(self) -> list[Item]:
        return list(self.p.inventory.items)

    def find(self, pred) -> Item | None:
        return next((it for it in self.pack() if pred(it)), None)

    def hp_frac(self) -> float:
        f = self.p.fighter
        return f.hp / max(1, f.max_hp)

    def blocked(self, x: int, y: int) -> bool:
        g = self.game
        return g.blocking_at(x, y) is not None or g.known_trap_at(x, y) is not None

    def step_to(self, goal: tuple[int, int]) -> bool:
        """One A* step toward ``goal`` through known terrain."""
        g = self.game
        path = astar(g.gmap, self.p.pos, goal, max_nodes=3000,
                     extra_cost=lambda x, y: 200 if g.known_trap_at(x, y) else 0)
        if not path:
            return False
        nx, ny = path[0]
        return self.move(nx - self.p.x, ny - self.p.y)

    def move(self, dx: int, dy: int) -> bool:
        g = self.game
        if g.player_move(dx, dy):
            return True
        return g.player_move(dx, dy)  # confirmation (known trap / forcing a locked door)

    # ---- one decision -----------------------------------------------------
    def act(self) -> None:
        g = self.game
        if g.depth != self.depth_seen:
            self.depth_seen, self.level_turns, self.ignored, self.route = g.depth, 0, set(), []
            self.loot_goal = None
        self.level_turns += 1
        while g.pending_levels:
            g.choose_level_up(BOON_ORDER[self.boon_i % len(BOON_ORDER)])
            self.boon_i += 1
        for rule in (self.survive, self.upkeep, self.gear, self.fight, self.loot, self.rest,
                     self.unlock, self.explore, self.leave, self.force):
            turn = g.turn
            if rule() and (g.turn != turn or g.game_over):
                return
        g.player_wait()

    def survive(self) -> bool:
        g = self.game
        foes = g.visible_monsters()
        frac = self.hp_frac()
        if frac < 0.4 and (foes or frac < 0.25 or self.p.statuses.has("poisoned")):
            heal = self.find(lambda it: it.effect == "heal" and it.identified)
            if heal is not None and g.use(heal):
                self.stats["potions"] += 1
                return True
            if frac < 0.25 and foes:
                unknown = self.find(lambda it: it.kind == "potion" and not it.identified)
                if unknown is not None and g.use(unknown):
                    self.stats["potions"] += 1
                    return True
                tele = self.find(lambda it: it.effect == "teleport" and it.identified)
                if tele is not None and g.use(tele):
                    self.stats["scrolls"] += 1
                    return True
        return False

    def upkeep(self) -> bool:
        g, res = self.game, self.game.resources
        if res.food < 350:
            food = self.find(lambda it: it.effect == "eat")
            if food is not None and g.use(food):
                return True
        if res.torch < 250:
            torch = self.find(lambda it: it.effect == "refuel")
            if torch is not None and g.use(torch):
                return True
        if encumbrance.state(self.p) != encumbrance.UNBURDENED and not g.visible_monsters():
            junk = encumbrance.heaviest_spare(self.p)
            if junk is not None and g.drop(junk):
                self.ignored.add(self.p.pos)  # don't pick it straight back up
                self.stats["dropped"] += 1
                return True
        if not g.visible_monsters():
            # read unknown scrolls when it's safe-ish, to learn what they are
            scroll = self.find(lambda it: it.kind == "scroll" and not it.identified)
            if scroll is not None and self.hp_frac() > 0.7 and g.use(scroll):
                self.stats["scrolls"] += 1
                return True
        return False

    def gear(self) -> bool:
        eq = self.p.equipment
        for it in self.pack():
            if not it.is_equipment or eq.is_equipped(it):
                continue
            cur = eq.slots.get(it.slot)

            def score(x: Item | None) -> float:
                if x is None:
                    return -1
                return x.power_bonus * 1.2 + x.defense_bonus * 1.5 + x.hp_bonus * 0.3 + x.knockback * 2

            if score(it) > score(cur):
                return self.game.toggle_equip(it)
        return False

    def fight(self) -> bool:
        g = self.game
        foes = [m for m in g.visible_monsters() if not m.asleep or chebyshev(m.pos, self.p.pos) <= 3]
        if not foes:
            return False
        near = foes[0]
        dist = chebyshev(near.pos, self.p.pos)
        tough = near.fighter.hp >= 12 or "boss" in near.tags or near.ai == "caster"
        if tough and dist <= 7:
            for eff in ("lightning", "fireball", "confuse"):
                scroll = self.find(lambda it, e=eff: it.effect == e and it.identified)
                if scroll is None or (eff == "fireball" and dist < 3) or (eff == "confuse" and near.confused):
                    continue
                if g.use(scroll, near.pos if eff != "lightning" else None):
                    self.stats["scrolls"] += 1
                    return True
            bomb = self.find(lambda it: it.effect in ("firebomb", "venom") and it.identified)
            if bomb is not None and dist >= 2 and g.throw(bomb, near.pos):
                self.stats["potions"] += 1
                return True
        adjacent = [m for m in foes if chebyshev(m.pos, self.p.pos) <= 1]
        if adjacent:
            weakest = min(adjacent, key=lambda m: m.fighter.hp)
            return self.move(weakest.x - self.p.x, weakest.y - self.p.y)
        if near.ai == "caster" or dist <= 6:
            return self.step_to(near.pos)
        return False

    def loot(self) -> bool:
        g = self.game
        here = g.items_at(*self.p.pos)
        if here and any(e.item.kind == "artifact" for e in here):
            return g.pickup()
        if here and self.p.pos not in self.ignored and self.p.inventory.can_add(here[0].item) \
                and encumbrance.can_lift(self.p, here[0].item):
            return g.pickup()
        inv = self.p.inventory
        goal = self.loot_goal
        if goal is not None and (goal == self.p.pos or goal in self.ignored or (
                g.gmap.visible[goal[1]][goal[0]] and not any(inv.can_add(e.item) for e in g.items_at(*goal)))):
            goal = self.loot_goal = None
        if goal is None:
            items = [e for e in g.visible_items() if e.pos not in self.ignored and e.pos != self.p.pos
                     and g.gmap.walkable(*e.pos) and inv.can_add(e.item)]
            if not items:
                return False
            goal = self.loot_goal = min(items, key=lambda e: chebyshev(e.pos, self.p.pos)).pos
        if self.step_to(goal):
            return True
        self.ignored.add(goal)
        self.loot_goal = None
        return False

    def rest(self) -> bool:
        g = self.game
        if self.hp_frac() >= 0.7 or not g.resources.can_regenerate or self.rest_streak >= REST_LIMIT:
            self.rest_streak = 0 if self.hp_frac() >= 0.7 else self.rest_streak
            return False
        self.rest_streak += 1
        g.player_wait()
        return True

    def unlock(self, force: bool = False) -> bool:
        """Walk to the nearest known locked door and open it (with a key, or by force)."""
        g = self.game
        if not force and self.find(lambda it: it.key == "iron key") is None:
            return False
        gm = g.gmap
        doors = [(x, y) for y in range(gm.height) for x in range(gm.width)
                 if gm.explored[y][x] and gm.tiles[y][x].name == "locked door"]
        if not doors:
            return False
        door = min(doors, key=lambda d: chebyshev(d, self.p.pos))
        if chebyshev(door, self.p.pos) == 1:
            self.stats["forced" if force else "keys"] += 1
            return self.move(door[0] - self.p.x, door[1] - self.p.y)
        return self.step_to(door)

    def force(self) -> bool:
        """Nothing left to explore and no way down in sight: break a locked door."""
        return self.unlock(force=True)

    def is_frontier(self, x: int, y: int) -> bool:
        """An explored, passable cell next to unexplored space."""
        gm = self.game.gmap
        if not gm.explored[y][x] or not gm.passable(x, y):
            return False
        for dy in (-1, 0, 1):
            row = gm.explored[y + dy] if 0 <= y + dy < gm.height else None
            for dx in (-1, 0, 1):
                if row is not None and 0 <= x + dx < gm.width and not row[x + dx]:
                    return True
        return False

    def frontier(self) -> list[tuple[int, int]]:
        gm = self.game.gmap
        return [(x, y) for y in range(1, gm.height - 1) for x in range(1, gm.width - 1)
                if self.is_frontier(x, y)]

    def path_to_frontier(self) -> list[tuple[int, int]]:
        """Breadth-first search from the player to the nearest frontier cell (path, start excluded)."""
        from collections import deque

        gm = self.game.gmap
        start = self.p.pos
        prev: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        q = deque([start])
        while q:
            cur = q.popleft()
            if cur != start and self.is_frontier(*cur):
                path = []
                while cur != start:
                    path.append(cur)
                    cur = prev[cur]
                return path[::-1]
            x, y = cur
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)):
                n = (x + dx, y + dy)
                if n in prev or not gm.in_bounds(*n) or not gm.explored[n[1]][n[0]]:
                    continue
                if not gm.passable(*n) or self.game.known_trap_at(*n):
                    continue
                prev[n] = cur
                q.append(n)
        return []

    def explore(self) -> bool:
        g = self.game
        st = g.gmap.stairs
        if self.level_turns > LEVEL_TURN_LIMIT and st is not None and g.gmap.explored[st[1]][st[0]]:
            return False
        path = self.route
        if not path or not self.is_frontier(*path[-1]) or chebyshev(path[0], self.p.pos) != 1 \
                or self.blocked(*path[0]):
            path = self.route = self.path_to_frontier()
        if not path:
            return False
        nxt = path[0]
        if self.blocked(*nxt):
            self.route = []
            return False
        before = self.p.pos
        ok = self.move(nxt[0] - self.p.x, nxt[1] - self.p.y)
        if self.p.pos != before and self.route and self.p.pos == self.route[0]:
            self.route.pop(0)
        elif self.p.pos != before:
            self.route = []
        return ok

    def leave(self) -> bool:
        g = self.game
        stairs = g.gmap.stairs
        if stairs is None:  # the boss level: go and find the Guardian (or the Heart)
            heart = next((e for e in g.entities if e.item is not None and e.item.key == "ember heart"), None)
            if heart is not None:
                if heart.pos == self.p.pos:
                    return g.pickup()
                return self.step_to(heart.pos)
            boss = next((m for m in g.monsters if "boss" in m.tags), None)
            return boss is not None and self.step_to(boss.pos)
        if not g.gmap.explored[stairs[1]][stairs[0]]:
            return False
        if self.p.pos == stairs:
            return g.descend()
        return self.step_to(stairs)


def play(seed: int, max_actions: int = MAX_ACTIONS) -> RunResult:
    """Let the bot play one full game with ``seed``."""
    g = Game(seed)
    bot = Bot(g)
    actions = 0
    while not g.game_over and actions < max_actions:
        bot.act()
        actions += 1
    timeout = not g.game_over
    cause = "victory" if g.victory else ("timeout" if timeout else (g.death_cause or "unknown"))
    return RunResult(seed, g.victory, g.max_depth, g.level, g.turn, g.kills, cause, timeout,
                     bot.stats["potions"], bot.stats["scrolls"], bot.stats["keys"])


def run_many(n: int, start_seed: int = 1, processes: int | None = None) -> list[RunResult]:
    """Play ``n`` games with consecutive seeds, using several processes when available."""
    seeds = list(range(start_seed, start_seed + n))
    if processes == 1 or n < 8:
        return [play(s) for s in seeds]
    import multiprocessing as mp

    with mp.Pool(processes) as pool:
        return pool.map(play, seeds, chunksize=4)


def _cause_group(cause: str) -> str:
    if cause.startswith("killed by"):
        rest = cause[len("killed by "):]
        rest = rest.split("'s ")[0]
        for art in ("an ", "a ", "the "):
            if rest.startswith(art):
                rest = rest[len(art):]
        return f"killed by {rest}"
    return cause


def report(results: list[RunResult], seconds: float | None = None) -> str:
    """A Markdown balance report for a batch of bot runs."""
    n = len(results)
    wins = sum(r.victory for r in results)
    depth_hist = Counter(r.depth for r in results)
    causes = Counter(_cause_group(r.cause) for r in results if not r.victory)
    lines = [
        "# Emberdeep balance report",
        "",
        f"Automated bot runs: **{n}** (seeds {results[0].seed}–{results[-1].seed})"
        + (f", {seconds:.0f}s wall time" if seconds is not None else ""),
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Victories | {wins} ({100 * wins / n:.1f}%) |",
        f"| Timeouts (bot got stuck) | {sum(r.timeout for r in results)} |",
        f"| Mean deepest depth | {sum(r.depth for r in results) / n:.2f} |",
        f"| Mean character level | {sum(r.level for r in results) / n:.2f} |",
        f"| Mean turns | {sum(r.turns for r in results) / n:.0f} |",
        f"| Mean kills | {sum(r.kills for r in results) / n:.1f} |",
        f"| Mean potions / scrolls used | {sum(r.potions_used for r in results) / n:.1f} / "
        f"{sum(r.scrolls_used for r in results) / n:.1f} |",
        f"| Runs that used an iron key | {sum(1 for r in results if r.keys_used)} |",
        "",
        "## Deepest depth reached",
        "",
        "| Depth | Runs | Share | |",
        "|---|---|---|---|",
    ]
    for d in sorted(depth_hist):
        share = depth_hist[d] / n
        lines.append(f"| {d} | {depth_hist[d]} | {100 * share:.1f}% | {'█' * max(1, round(share * 40))} |")
    lines += ["", "## How runs ended", "", "| Cause | Runs |", "|---|---|"]
    if wins:
        lines.append(f"| victory | {wins} |")
    for cause, k in causes.most_common(15):
        lines.append(f"| {cause} | {k} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> None:  # pragma: no cover - CLI
    args = list(sys.argv[1:] if argv is None else argv)
    n = int(args[0]) if args else 100
    out = args[1] if len(args) > 1 else None
    t0 = time.time()
    results = run_many(n)
    text = report(results, time.time() - t0)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {out}")
    print(text)


if __name__ == "__main__":  # pragma: no cover
    main()
