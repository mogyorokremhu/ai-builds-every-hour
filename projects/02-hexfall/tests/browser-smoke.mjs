// Browser smoke test (not part of `npm test`; needs Playwright and a static server):
//   python3 -m http.server 8765 &  node tests/browser-smoke.mjs [http://localhost:8765/]
// Plays a few real clicks — select, move, attack, end turn, undo, save/load — and fails on any page error.
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright"); // CommonJS lookup also honours NODE_PATH

const url = process.argv[2] ?? "http://localhost:8765/";
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 860 } });
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
await page.goto(url + "#7");
await page.waitForFunction(() => window.hexfall?.state.game);
// hot-seat for the scripted part (blue defaults to the AI)
await page.selectOption("#blueai", "human");

async function clickHex(h) {
  const p = await page.evaluate(([q, r]) => {
    const c = window.hexfall.hexCenter({ q, r }, window.hexfall.view());
    const box = document.getElementById("board").getBoundingClientRect();
    return { x: box.left + c.x, y: box.top + c.y };
  }, [h.q, h.r]);
  await page.mouse.move(p.x, p.y);
  await page.mouse.down();
  await page.mouse.up();
  await page.waitForFunction(() => !window.hexfall.state.busy);
}
const game = () => page.evaluate(() => JSON.parse(JSON.stringify(window.hexfall.state.game.toJSON())));

let g = await game();
const red = g.units.find((u) => u.side === "red" && u.type === "cavalry");
await clickHex(red);
const sel = await page.evaluate(() => window.hexfall.state.selected);
if (sel !== red.id) throw new Error(`selecting failed: ${sel}`);
const dest = await page.evaluate(() => {
  const nodes = [...window.hexfall.state.area.values()].filter((n) => n.canStop && n.cost >= 3);
  return nodes[0].hex;
});
await clickHex(dest);
g = await game();
const moved = g.units.find((u) => u.id === red.id);
if (moved.q !== dest.q || moved.r !== dest.r) throw new Error("move failed");
await page.click("#undo");
g = await game();
if (g.units.find((u) => u.id === red.id).q !== red.q) throw new Error("undo failed");

// march the armies at each other for a few turns, attacking whenever possible
for (let turn = 0; turn < 14 && !(await game()).winner; turn++) {
  const ids = await page.evaluate(() => window.hexfall.state.game.unitsOf(window.hexfall.state.game.side).map((u) => u.id));
  for (const id of ids) {
    const act = await page.evaluate((id) => {
      const g = window.hexfall.state.game;
      const u = g.unitById(id);
      if (!u) return null;
      const foes = g.units.filter((t) => t.side !== u.side);
      const target = foes.find((t) => g.attackPlan(u, t));
      if (target) return { unit: { q: u.q, r: u.r }, target: { q: target.q, r: target.r } };
      const nearest = foes.sort((a, b) => Math.hypot(a.q - u.q, a.r - u.r) - Math.hypot(b.q - u.q, b.r - u.r))[0];
      const nodes = [...g.area(u).values()].filter((n) => n.canStop);
      const d = (h) => (Math.abs(h.q - nearest.q) + Math.abs(h.r - nearest.r) + Math.abs(h.q + h.r - nearest.q - nearest.r)) / 2;
      nodes.sort((a, b) => d(a.hex) - d(b.hex));
      return { unit: { q: u.q, r: u.r }, move: nodes[0].hex };
    }, id);
    if (!act) continue;
    await clickHex(act.unit);
    if (act.target) {
      await clickHex(act.target);
    } else if (act.move.q !== act.unit.q || act.move.r !== act.unit.r) {
      await clickHex(act.move);
    } else {
      await page.keyboard.press("Escape");
    }
  }
  await page.keyboard.press("e");
}
// recruiting: whoever is to move recruits the cheapest affordable unit via the panel
const before = (await game()).units.length;
const enabled = await page.$$("#recruit button:not([disabled])");
if (enabled.length) {
  await enabled[0].click();
  if ((await game()).units.length !== before + 1) throw new Error("recruit button did not add a unit");
}
// hand blue to the AI and let it play a turn by itself
await page.selectOption("#blueai", "normal");
if ((await game()).active === 0 && !(await game()).winner) await page.keyboard.press("e");
await page.waitForFunction(() => !window.hexfall.state.aiRunning && (window.hexfall.state.game.side === "red" || window.hexfall.state.game.winner), null, { timeout: 30000 });
const aiTurn = (await game()).log.slice(-60).some((l) => l.side === "blue");
if (!aiTurn) throw new Error("the AI did not play blue's turn");
g = await game();
const attacks = g.log.filter((l) => /hits|shoots|blasts/.test(l.text)).length;
await page.click("#save");
await page.click("#load");
const text = await page.textContent("#info");

// fog of war + abilities: a fresh hot-seat battle with fog, then a shield wall via key "1"
await page.selectOption("#blueai", "human");
await page.check("#fog");
await page.waitForFunction(() => window.hexfall.state.game.rules.fog && window.hexfall.state.game.turn === 1);
const fogInfo = await page.evaluate(() => {
  const g = window.hexfall.state.game;
  return { hidden: g.hiddenIds("red").size, roster: document.getElementById("roster").textContent };
});
if (!fogInfo.hidden) throw new Error("fog of war hides nothing at the start");
if (!/seen/.test(fogInfo.roster)) throw new Error("the roster does not hide unseen enemies");
const spear = (await game()).units.find((u) => u.side === "red" && u.type === "spearman");
await clickHex(spear);
const buttons = await page.$$("#abilities button:not([disabled])");
if (!buttons.length) throw new Error("no ability button for the spearman");
await page.keyboard.press("1");
await page.waitForFunction(() => !window.hexfall.state.busy);
if (!(await game()).log.some((l) => /shield wall/.test(l.text))) throw new Error("shield wall was not used");
const braced = (await game()).units.find((u) => u.id === spear.id).status.braced;
if (!braced) throw new Error("the spearman is not braced");
await page.screenshot({ path: process.env.SHOT ?? "/tmp/hexfall-smoke.png" });
await browser.close();
if (errors.length) throw new Error("page errors:\n" + errors.join("\n"));
if (!attacks) throw new Error("no attacks happened");
console.log(`ok: turn ${g.turn}, ${g.units.length} units left, ${attacks} attacks, winner ${g.winner ?? "none"}; ${text}; fog hid ${fogInfo.hidden} enemies; shield wall used`);
