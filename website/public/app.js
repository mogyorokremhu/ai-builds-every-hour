// Single-page browser for the repo: home, folders, files, accounts and the Play overlay.
const $ = (s, el = document) => el.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const REPO_URL = 'https://github.com/mogyorokremhu/ai-builds-every-hour';

let user = null;
let entries = [];
let sizes = new Map();
let index = new Map(); // dir -> { dirs:Set, files:[] }

// ---------- API ----------
async function api(path, opts) {
  const r = await fetch('/api/' + path, { credentials: 'same-origin', ...opts });
  let data = null;
  try { data = await r.json(); } catch {}
  return { ok: r.ok, status: r.status, data };
}
async function getText(path) {
  const r = await fetch('/api/file?path=' + encodeURIComponent(path), { credentials: 'same-origin' });
  if (!r.ok) {
    let msg = 'Could not load file';
    try { msg = (await r.json()).error || msg; } catch {}
    throw Object.assign(new Error(msg), { status: r.status });
  }
  return r.text();
}

// ---------- repo index ----------
function buildIndex() {
  index = new Map([['', { dirs: new Set(), files: [] }]]);
  sizes = new Map(entries.map((e) => [e.p, e.s]));
  for (const { p } of entries) {
    const parts = p.split('/');
    let dir = '';
    for (let i = 0; i < parts.length - 1; i++) {
      const next = dir ? dir + '/' + parts[i] : parts[i];
      index.get(dir).dirs.add(parts[i]);
      if (!index.has(next)) index.set(next, { dirs: new Set(), files: [] });
      dir = next;
    }
    index.get(dir).files.push(parts[parts.length - 1]);
  }
}
const countFiles = (dir) => entries.reduce((n, e) => n + (e.p.startsWith(dir + '/') ? 1 : 0), 0);
const pretty = (n) => n.replace(/^\d+-/, '').replace(/[-_]/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
const href = (kind, p) => '#/' + kind + (p ? '/' + p.split('/').map(encodeURIComponent).join('/') : '');
const fmtSize = (n) => (n < 1024 ? n + ' B' : n < 1048576 ? (n / 1024).toFixed(1) + ' KB' : (n / 1048576).toFixed(1) + ' MB');

// Which folders can be played, and how.
function playInfo(dir) {
  const d = index.get(dir);
  if (!d) return null;
  if (d.files.includes('index.html')) return { entry: `/play/${dir}/index.html` };
  for (const sub of [...d.dirs].sort()) {
    const sd = index.get(dir + '/' + sub);
    if (sd && sd.files.includes('__main__.py')) return { q: { type: 'module', root: dir, module: sub } };
  }
  for (const f of ['repl.py', 'main.py', 'app.py', 'play.py'])
    if (d.files.includes(f)) return { q: { type: 'script', root: dir, file: `${dir}/${f}` } };
  return null;
}
const isProjectDir = (p) => /^projects\/[^/]+$/.test(p);

// ---------- Markdown (small, escapes everything first) ----------
function resolveLink(base, h) {
  if (/^https?:\/\//i.test(h)) return h;
  if (/^[a-z]+:/i.test(h) || h.startsWith('#')) return '#';
  const parts = (h.startsWith('/') ? '' : base).split('/').filter(Boolean);
  for (const seg of h.split('#')[0].split('/')) {
    if (seg === '..') parts.pop(); else if (seg && seg !== '.') parts.push(seg);
  }
  const p = parts.join('/');
  return index.has(p) ? href('tree', p) : href('file', p);
}
function md(src, base) {
  const inline = (t) => {
    const codes = [];
    let s = esc(t).replace(/`([^`]+)`/g, (_, c) => { codes.push(c); return `\u0000${codes.length - 1}\u0000`; });
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g, '$1<em>$2</em>');
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, txt, h) => {
      const url = resolveLink(base, h.replace(/&amp;/g, '&'));
      return `<a href="${esc(url)}"${/^https?:/i.test(url) ? ' target="_blank" rel="noopener"' : ''}>${txt}</a>`;
    });
    return s.replace(/\u0000(\d+)\u0000/g, (_, n) => `<code>${codes[n]}</code>`);
  };
  const cells = (l) => l.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
  const lines = src.replace(/\r/g, '').split('\n');
  const out = [];
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (/^```/.test(l)) {
      const buf = [];
      for (i++; i < lines.length && !/^```/.test(lines[i]); i++) buf.push(lines[i]);
      out.push(`<pre><code>${esc(buf.join('\n'))}</code></pre>`);
    } else if (/^#{1,6}\s/.test(l)) {
      const n = l.match(/^#+/)[0].length;
      out.push(`<h${n}>${inline(l.replace(/^#+\s*/, ''))}</h${n}>`);
    } else if (/^(-{3,}|\*{3,})\s*$/.test(l)) {
      out.push('<hr>');
    } else if (l.includes('|') && i + 1 < lines.length && /^\s*\|?\s*:?-{2,}[\s:|-]*$/.test(lines[i + 1])) {
      const head = cells(l);
      const rows = [];
      for (i += 2; i < lines.length && lines[i].includes('|') && lines[i].trim(); i++) rows.push(cells(lines[i]));
      i--;
      out.push(`<table><thead><tr>${head.map((c) => `<th>${inline(c)}</th>`).join('')}</tr></thead><tbody>${rows
        .map((r) => `<tr>${r.map((c) => `<td>${inline(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>`);
    } else if (/^>/.test(l)) {
      const buf = [];
      for (; i < lines.length && /^>/.test(lines[i]); i++) buf.push(lines[i].replace(/^>\s?/, ''));
      i--;
      out.push(`<blockquote>${inline(buf.join(' '))}</blockquote>`);
    } else if (/^\s*([-*]|\d+\.)\s+/.test(l)) {
      const ordered = /^\s*\d+\./.test(l);
      const items = [];
      for (; i < lines.length && /^\s*([-*]|\d+\.)\s+/.test(lines[i]); i++) {
        const m = lines[i].match(/^(\s*)(?:[-*]|\d+\.)\s+(.*)$/);
        items.push(`<li${m[1].length >= 2 ? ' class="l2"' : ''}>${inline(m[2])}</li>`);
      }
      i--;
      out.push(`<${ordered ? 'ol' : 'ul'}>${items.join('')}</${ordered ? 'ol' : 'ul'}>`);
    } else if (l.trim()) {
      const buf = [];
      for (; i < lines.length && lines[i].trim() && !/^(```|#|>|\s*([-*]|\d+\.)\s)/.test(lines[i]); i++) buf.push(lines[i]);
      i--;
      out.push(`<p>${inline(buf.join(' '))}</p>`);
    }
  }
  return out.join('\n');
}
const firstParagraph = (src) => {
  for (const block of src.replace(/\r/g, '').split(/\n\s*\n/)) {
    const t = block.trim();
    if (!t || /^(#|```|\||[-*]\s|>|<)/.test(t)) continue;
    return t.replace(/\s+/g, ' ').replace(/\*\*|`/g, '').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').slice(0, 170);
  }
  return '';
};

// ---------- auth UI ----------
function renderAuth() {
  const el = $('#auth');
  if (user) {
    el.innerHTML = `<span class="muted">👤 ${esc(user.username)}</span> <button class="btn" id="b-out">Log out</button>`;
    $('#b-out').onclick = async () => { await api('logout', { method: 'POST' }); user = null; renderAuth(); route(); };
  } else {
    el.innerHTML = '<button class="btn" id="b-in">Log in</button> <button class="btn primary" id="b-reg">Register</button>';
    $('#b-in').onclick = () => showAuth('login');
    $('#b-reg').onclick = () => showAuth('register');
  }
}
function showAuth(mode, note = '') {
  const m = $('#modal');
  const isLogin = mode === 'login';
  m.hidden = false;
  m.innerHTML = `<div class="dlg"><button class="btn x" type="button" id="a-x">✕</button>
    <h2>${isLogin ? 'Log in' : 'Create your account'}</h2>${note ? `<p class="note">${esc(note)}</p>` : ''}
    <form id="a-form"><label>Username<input name="u" autocomplete="username" required minlength="3" maxlength="20" autocapitalize="off"></label>
    <label>Password<input name="p" type="password" autocomplete="${isLogin ? 'current-password' : 'new-password'}" required minlength="${isLogin ? 1 : 8}"></label>
    <p class="err" id="a-err" hidden></p><button class="btn primary">${isLogin ? 'Log in' : 'Register'}</button></form>
    <p class="sw">${isLogin ? 'No account yet? <a href="#" id="a-sw">Register</a>' : 'Already registered? <a href="#" id="a-sw">Log in</a>'}</p></div>`;
  $('#a-x').onclick = () => (m.hidden = true);
  $('#a-sw').onclick = (e) => { e.preventDefault(); showAuth(isLogin ? 'register' : 'login', note); };
  $('input', m).focus();
  $('#a-form').onsubmit = async (e) => {
    e.preventDefault();
    const f = e.target;
    const r = await api(mode, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ username: f.u.value.trim(), password: f.p.value }) });
    if (r.ok) { user = r.data.user; m.hidden = true; renderAuth(); route(); }
    else { const er = $('#a-err'); er.hidden = false; er.textContent = (r.data && r.data.error) || 'Something went wrong.'; }
  };
}

// ---------- Play overlay ----------
function openPlay(title, url) {
  if (!user) return showAuth('register', 'Create a free account to play.');
  $('#ov-title').textContent = title;
  $('#ov-frame').src = url;
  $('#overlay').hidden = false;
  document.body.classList.add('noscroll');
}
$('#ov-close').onclick = () => {
  $('#ov-frame').src = 'about:blank';
  $('#overlay').hidden = true;
  document.body.classList.remove('noscroll');
};
const playUrl = (info) => info.entry || '/player.html?' + new URLSearchParams(info.q);

// ---------- views ----------
const view = $('#view');
const crumbs = (path, last) => {
  const parts = path ? path.split('/') : [];
  let acc = '';
  const links = parts.slice(0, last ? parts.length - 1 : parts.length).map((p) => { acc = acc ? acc + '/' + p : p; return `<a href="${href('tree', acc)}">${esc(p)}</a>`; });
  return `<div class="crumbs"><a href="#/">Home</a>${links.length ? ' / ' + links.join(' / ') : ''}${last ? ' / ' + esc(parts[parts.length - 1]) : ''}</div>`;
};
const lockedBox = (what) => `<div class="locked"><h3>🔒 ${esc(what)}</h3><p>Create a free account to read the source code and play the games in your browser.</p>
  <button class="btn primary" id="l-reg">Register</button> <button class="btn" id="l-in">Log in</button></div>`;
const wireLocked = () => { const r = $('#l-reg'); if (r) { r.onclick = () => showAuth('register'); $('#l-in').onclick = () => showAuth('login'); } };

function card(dir) {
  const play = isProjectDir(dir) && playInfo(dir);
  return `<a class="card" href="${href('tree', dir)}"><h3>${esc(pretty(dir.split('/').pop()))}</h3>
    <p data-readme="${esc(dir)}">&nbsp;</p><div class="meta"><span class="badge">${countFiles(dir)} files</span>${play ? '<span class="badge play">▶ playable</span>' : ''}</div></a>`;
}
async function fillDescriptions() {
  for (const p of view.querySelectorAll('[data-readme]')) {
    try {
      const d = p.dataset.readme;
      if (index.get(d)?.files.includes('README.md')) p.textContent = firstParagraph(await getText(d + '/README.md'));
    } catch {}
  }
}
function viewHome() {
  const projects = [...(index.get('projects')?.dirs || [])].sort().map((d) => 'projects/' + d);
  const minis = [...(index.get('mini')?.dirs || [])].sort().map((d) => 'mini/' + d);
  view.innerHTML = `<section class="hero"><h1>An AI builds something new every hour</h1>
    <p>Big multi-day projects and tiny creative experiments, written by Claude on a schedule. Browse everything below — register for free to read the code and play the games right here in your browser.</p>
    ${user ? '' : '<button class="btn primary big" id="h-reg">Register to play</button>'}</section>
    <h2 class="sec">Projects</h2><div class="grid">${projects.map(card).join('') || '<p class="muted">No projects yet.</p>'}</div>
    <h2 class="sec">Mini collections</h2><div class="grid">${minis.map(card).join('') || '<p class="muted">None yet.</p>'}</div>`;
  const b = $('#h-reg'); if (b) b.onclick = () => showAuth('register');
  fillDescriptions();
}

async function viewDir(dir) {
  const d = index.get(dir);
  if (!d) return notFound();
  const info = isProjectDir(dir) && playInfo(dir);
  const desc = dir === 'logs' ? [...d.files].sort().reverse() : [...d.files].sort();
  const rows = [...d.dirs].sort().map((n) => `<a class="row" href="${href('tree', dir + '/' + n)}"><span>📁</span><span class="n">${esc(n)}</span><span class="s">${countFiles(dir + '/' + n)} files</span></a>`)
    .concat(desc.map((n) => {
      const full = dir + '/' + n;
      const lock = !user && !/\.md$/i.test(n) ? '🔒' : '📄';
      return `<a class="row" href="${href('file', full)}"><span>${lock}</span><span class="n">${esc(n)}</span><span class="s">${fmtSize(sizes.get(full) || 0)}</span></a>`;
    }));
  view.innerHTML = `${crumbs(dir)}<div class="head"><h1>${esc(pretty(dir.split('/').pop() || 'Repository'))}</h1>
    ${info ? '<button class="btn primary big" id="d-play">▶ Play</button>' : ''}</div>
    <div class="list">${rows.join('') || '<p class="muted" style="padding:14px">Empty.</p>'}</div><div class="md" id="readme"></div>`;
  if (info) $('#d-play').onclick = () => openPlay(pretty(dir.split('/').pop()), playUrl(info));
  if (d.files.includes('README.md')) {
    try { $('#readme').innerHTML = md(await getText(dir + '/README.md'), dir); } catch {}
  }
}

const UNSUPPORTED = /^\s*(?:import|from)\s+(turtle|tkinter|curses|pygame)\b/m;
async function viewFile(path) {
  if (!sizes.has(path)) return notFound();
  const name = path.split('/').pop();
  const isMd = /\.md$/i.test(name);
  const dir = path.split('/').slice(0, -1).join('/');
  const canRun = /^mini\/.+\.py$/.test(path);
  view.innerHTML = `${crumbs(path, true)}<div class="head"><h1>${esc(name)}</h1><span id="f-act"></span>
    <a class="btn" target="_blank" rel="noopener" href="${REPO_URL}/blob/main/${path.split('/').map(encodeURIComponent).join('/')}">GitHub ↗</a></div><div id="f-body"></div>`;
  const body = $('#f-body');
  if (!isMd && !user) { body.innerHTML = lockedBox('Source code is for registered users'); return wireLocked(); }
  body.innerHTML = '<p class="muted">Loading…</p>';
  try {
    const text = await getText(path);
    if (isMd) { body.innerHTML = `<div class="md">${md(text, dir)}</div>`; return; }
    body.innerHTML = `<pre class="code"><code>${esc(text)}</code></pre>`;
    if (canRun) {
      if (UNSUPPORTED.test(text)) $('#f-act').innerHTML = '<span class="muted">Needs a window or terminal UI — can’t run in the browser.</span>';
      else {
        $('#f-act').innerHTML = '<button class="btn primary" id="f-run">▶ Run</button>';
        $('#f-run').onclick = () => openPlay(name, playUrl({ q: { type: 'script', single: '1', root: dir, file: path } }));
      }
    }
  } catch (e) {
    body.innerHTML = e.status === 401 ? lockedBox('Please log in to view this file') : `<p class="err">${esc(e.message)}</p>`;
    wireLocked();
  }
}

const notFound = () => { view.innerHTML = '<p>Not found. <a href="#/">Back home</a></p>'; };

async function route() {
  const parts = (location.hash.slice(1) || '/').split('/').filter(Boolean);
  const kind = parts.shift();
  const path = parts.map(decodeURIComponent).join('/');
  window.scrollTo(0, 0);
  try {
    if (!kind) viewHome();
    else if (kind === 'tree') await viewDir(path);
    else if (kind === 'file') await viewFile(path);
    else notFound();
  } catch (e) { view.innerHTML = `<p class="err">${esc(e.message)}</p>`; }
}

async function init() {
  $('#gh').href = REPO_URL;
  try {
    const [me, tree] = await Promise.all([api('me'), api('tree')]);
    user = me.data && me.data.user;
    if (!tree.ok) throw new Error('Could not load the repository list.');
    entries = tree.data.entries;
    buildIndex();
  } catch (e) {
    view.innerHTML = `<p class="err">${esc(e.message)} <button class="btn" onclick="location.reload()">Retry</button></p>`;
    return;
  }
  renderAuth();
  window.addEventListener('hashchange', route);
  route();
}
init();
