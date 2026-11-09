// Shared helpers for the Pages Functions: JSON, passwords, sessions, GitHub access.
const enc = new TextEncoder();
const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
const fromHex = (s) => new Uint8Array(s.match(/../g).map((h) => parseInt(h, 16)));

export const json = (data, status = 200, headers = {}) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...headers },
  });

export async function sha256Hex(s) {
  return hex(await crypto.subtle.digest('SHA-256', enc.encode(s)));
}

// PBKDF2-SHA256, 100k iterations (the maximum Workers allows).
export async function hashPassword(password, salt) {
  const key = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveBits']);
  return hex(await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt, iterations: 100000 }, key, 256));
}

export const newSalt = () => hex(crypto.getRandomValues(new Uint8Array(16)));

export async function verifyPassword(password, saltHex, expectedHex) {
  const got = await hashPassword(password, fromHex(saltHex));
  let diff = got.length ^ expectedHex.length;
  for (let i = 0; i < got.length; i++) diff |= got.charCodeAt(i) ^ (expectedHex.charCodeAt(i) || 0);
  return diff === 0;
}

const SESSION_MS = 30 * 24 * 3600 * 1000;

export async function createSession(env, userId) {
  const token = hex(crypto.getRandomValues(new Uint8Array(32)));
  await env.DB.prepare('DELETE FROM sessions WHERE expires < ?1').bind(Date.now()).run();
  await env.DB.prepare('INSERT INTO sessions (token_hash, user_id, expires) VALUES (?1, ?2, ?3)')
    .bind(await sha256Hex(token), userId, Date.now() + SESSION_MS).run();
  return `sid=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_MS / 1000}`;
}

export const clearCookie = 'sid=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0';

function sidOf(request) {
  const m = /(?:^|;\s*)sid=([a-f0-9]{64})/.exec(request.headers.get('cookie') || '');
  return m && m[1];
}

export async function getUser(request, env) {
  const sid = sidOf(request);
  if (!sid) return null;
  return env.DB.prepare(
    'SELECT u.id, u.username FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token_hash = ?1 AND s.expires > ?2',
  ).bind(await sha256Hex(sid), Date.now()).first();
}

export async function destroySession(request, env) {
  const sid = sidOf(request);
  if (sid) await env.DB.prepare('DELETE FROM sessions WHERE token_hash = ?1').bind(await sha256Hex(sid)).run();
}

// ---- simple rate limiting backed by D1 ----
export async function tooMany(env, key, max, windowMs) {
  const r = await env.DB.prepare('SELECT COUNT(*) AS c FROM attempts WHERE key = ?1 AND ts > ?2')
    .bind(key, Date.now() - windowMs).first();
  return r.c >= max;
}
export async function noteAttempt(env, key) {
  await env.DB.prepare('DELETE FROM attempts WHERE ts < ?1').bind(Date.now() - 24 * 3600 * 1000).run();
  await env.DB.prepare('INSERT INTO attempts (key, ts) VALUES (?1, ?2)').bind(key, Date.now()).run();
}

// ---- GitHub access (public repo; optional GITHUB_TOKEN raises rate limits) ----
export function repoCfg(env) {
  return { repo: env.GITHUB_REPO || 'mogyorokremhu/ai-builds-every-hour', branch: env.GITHUB_BRANCH || 'main' };
}
function ghHeaders(env, extra = {}) {
  const h = { 'user-agent': 'ai-builds-site', ...extra };
  if (env.GITHUB_TOKEN) h.authorization = `Bearer ${env.GITHUB_TOKEN}`;
  return h;
}

export async function ghTree(env) {
  const { repo, branch } = repoCfg(env);
  const r = await fetch(`https://api.github.com/repos/${repo}/git/trees/${encodeURIComponent(branch)}?recursive=1`, {
    headers: ghHeaders(env, { accept: 'application/vnd.github+json' }),
    cf: { cacheTtl: 120, cacheEverything: true },
  });
  if (!r.ok) throw new Error('GitHub tree ' + r.status);
  const j = await r.json();
  return j.tree.filter((e) => e.type === 'blob').map((e) => ({ p: e.path, s: e.size }));
}

export function ghRaw(env, path) {
  const { repo, branch } = repoCfg(env);
  const url = `https://raw.githubusercontent.com/${repo}/${branch}/${path.split('/').map(encodeURIComponent).join('/')}`;
  return fetch(url, { headers: ghHeaders(env), cf: { cacheTtl: 60, cacheEverything: true } });
}

// Only plain repo-relative paths; no traversal and no dotfiles.
export function safePath(p) {
  return typeof p === 'string' && p.length > 0 && p.length < 300 && !p.startsWith('/') &&
    /^[\w .\-\/@+()]+$/.test(p) && !p.split('/').some((s) => s === '' || s.startsWith('.'));
}

// Visitors may read Markdown (READMEs, roadmaps, logs); everything else needs an account.
export const publicPath = (p) => /\.md$/i.test(p);
