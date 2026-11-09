// Capture documentation screenshots of the running game (needs Playwright + a static server):
//   python3 -m http.server 8765 &  node tools/screenshots.mjs [http://localhost:8765/] [outDir]
// Writes board.png, fog.png, contrast.png and mobile.png into outDir (default docs/img).
import { createRequire } from "node:module";
import { mkdirSync } from "node:fs";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const url = process.argv[2] ?? "http://localhost:8765/";
const out = process.argv[3] ?? "docs/img";
mkdirSync(out, { recursive: true });

const browser = await chromium.launch();
const errors = [];
async function open(opts, hash) {
  const ctx = await browser.newContext(opts);
  const page = await ctx.newPage();
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(url + hash);
  await page.waitForFunction(() => window.hexfall?.state.game);
  return page;
}

let page = await open({ viewport: { width: 1280, height: 860 } }, "#7");
await page.screenshot({ path: `${out}/board.png` });
await page.close();

page = await open({ viewport: { width: 1280, height: 860 } }, "#21");
await page.selectOption("#blueai", "human");
await page.screenshot({ path: `${out}/fog.png` });
await page.close();

page = await open({ viewport: { width: 1280, height: 860 } }, "#7");
const hasTheme = await page.$("#theme");
if (hasTheme) await page.selectOption("#theme", { index: 1 });
await page.screenshot({ path: `${out}/contrast.png` });
await page.close();

page = await open({ viewport: { width: 390, height: 780 }, hasTouch: true, isMobile: true }, "#7");
await page.screenshot({ path: `${out}/mobile.png` });
await browser.close();

if (errors.length) {
  console.error("page errors:\n" + errors.join("\n"));
  process.exit(1);
}
console.log(`wrote 4 screenshots to ${out}`);
