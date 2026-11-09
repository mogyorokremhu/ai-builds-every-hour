# Website — browse and play the repo

A Cloudflare site that reads this repo live from GitHub, lets people register, and runs the
projects in the browser. It lives in this `website/` folder and is **not** touched by the hourly builds.

## What visitors get
| | Not logged in | Registered |
|---|---|---|
| Home, project and folder listings | ✅ | ✅ |
| READMEs, roadmaps, build logs (`.md`) | ✅ | ✅ |
| Source code of every file | 🔒 | ✅ |
| ▶ Play (Hexfall) and run (Python projects, `mini/` scripts) | 🔒 | ✅ |

## How it works
- **Cloudflare Pages** serves `public/` (the site) and `functions/` (the API).
- **D1** (Cloudflare's SQLite) stores accounts. Passwords are hashed with PBKDF2-SHA256; sessions are
  random tokens stored hashed, in an HttpOnly cookie. Sign-ups and failed logins are rate limited.
- **GitHub** is the source of truth: the file list and file contents are fetched live (cached 1–2 minutes),
  so new hourly commits appear on the site automatically.
- **Play**: folders with an `index.html` run as web games from `/play/…`. Python projects run in the browser
  with [Pyodide](https://pyodide.org) in a worker; `input()` works through a terminal box.
  Projects are detected automatically: `index.html` → web game, a package with `__main__.py` → `python -m`,
  otherwise `repl.py` / `main.py` / `app.py` / `play.py`. Scripts that need a window or curses
  (`turtle`, `tkinter`, `curses`, `pygame`) can't run in a browser tab.

## Setup (about 10 minutes, all in the Cloudflare dashboard)
1. **Create the database:** Storage & databases → D1 → *Create database* named `ai-builds-db`.
   Open it → *Console*, paste the contents of [`schema.sql`](schema.sql) and run it.
2. **Put its ID in the config:** copy the database ID and replace `REPLACE_WITH_YOUR_D1_DATABASE_ID`
   in [`wrangler.toml`](wrangler.toml) (edit the file on GitHub and commit).
3. **Create the site:** Workers & Pages → *Create* → *Pages* → *Connect to Git* → pick this repo.
   Set **Root directory** to `website`, leave the **build command empty** and set the
   **output directory** to `public`. Deploy.
4. **Recommended:** add a GitHub token so Cloudflare isn't rate limited by GitHub (60 requests/hour per
   shared IP without one). GitHub → Settings → Developer settings → Fine-grained token, public repositories,
   no extra permissions. Then Pages project → Settings → *Variables and secrets* → add secret `GITHUB_TOKEN`
   and redeploy.
5. Open your `*.pages.dev` address and register the first account.

To point at a different repo, set `GITHUB_REPO` / `GITHUB_BRANCH` in `wrangler.toml`.

## Good to know
- Games run on the site's own origin (needed so their files and saves work), so only put code in the repo
  that you trust — which is the case here since you own it.
- The Python runtime is downloaded from the jsDelivr CDN on first play (a few MB, then cached).
- Free-plan limits (100k function requests/day) are plenty for a hobby site.
- Local testing: `npx wrangler pages dev public --d1=DB=<your-database-id>` from this folder
  after running `schema.sql` with `npx wrangler d1 execute ai-builds-db --local --file=schema.sql`.
