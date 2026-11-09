import {
  json, getUser, createSession, destroySession, clearCookie, hashPassword, verifyPassword, newSalt,
  tooMany, noteAttempt, ghTree, ghRaw, safePath, publicPath,
} from '../_lib.js';

async function body(request) {
  try { return await request.json(); } catch { return {}; }
}

export async function onRequest({ request, env, params }) {
  const route = [].concat(params.path || []).join('/');
  const method = request.method;
  const ip = request.headers.get('cf-connecting-ip') || 'local';
  try {
    if (method === 'POST') {
      const origin = request.headers.get('origin');
      if (origin && origin !== new URL(request.url).origin) return json({ error: 'Bad origin' }, 403);
    }

    if (route === 'me' && method === 'GET') {
      return json({ user: await getUser(request, env) });
    }

    if (route === 'register' && method === 'POST') {
      const { username, password } = await body(request);
      if (typeof username !== 'string' || !/^[A-Za-z0-9_]{3,20}$/.test(username))
        return json({ error: 'Username must be 3–20 letters, numbers or underscores.' }, 400);
      if (typeof password !== 'string' || password.length < 8 || password.length > 200)
        return json({ error: 'Password must be at least 8 characters.' }, 400);
      if (await tooMany(env, 'reg:' + ip, 5, 3600 * 1000)) return json({ error: 'Too many sign-ups, try later.' }, 429);
      await noteAttempt(env, 'reg:' + ip);
      const salt = newSalt();
      const hash = await hashPassword(password, Uint8Array.from(salt.match(/../g).map((h) => parseInt(h, 16))));
      let id;
      try {
        const r = await env.DB.prepare('INSERT INTO users (username, salt, hash, created_at) VALUES (?1, ?2, ?3, ?4)')
          .bind(username, salt, hash, Date.now()).run();
        id = r.meta.last_row_id;
      } catch {
        return json({ error: 'That username is taken.' }, 409);
      }
      return json({ user: { id, username } }, 200, { 'set-cookie': await createSession(env, id) });
    }

    if (route === 'login' && method === 'POST') {
      const { username, password } = await body(request);
      if (typeof username !== 'string' || typeof password !== 'string') return json({ error: 'Missing fields.' }, 400);
      const key = `login:${ip}:${username.toLowerCase()}`;
      if (await tooMany(env, key, 8, 15 * 60 * 1000)) return json({ error: 'Too many attempts, wait 15 minutes.' }, 429);
      const row = await env.DB.prepare('SELECT id, username, salt, hash FROM users WHERE username = ?1 COLLATE NOCASE')
        .bind(username).first();
      // Always hash, so unknown usernames cost the same time as wrong passwords.
      const ok = row
        ? await verifyPassword(password, row.salt, row.hash)
        : (await hashPassword(password, new Uint8Array(16)), false);
      if (!ok) { await noteAttempt(env, key); return json({ error: 'Wrong username or password.' }, 401); }
      return json({ user: { id: row.id, username: row.username } }, 200, { 'set-cookie': await createSession(env, row.id) });
    }

    if (route === 'logout' && method === 'POST') {
      await destroySession(request, env);
      return json({ ok: true }, 200, { 'set-cookie': clearCookie });
    }

    if (route === 'tree' && method === 'GET') {
      return json({ entries: await ghTree(env) }, 200, { 'cache-control': 'public, max-age=60' });
    }

    if (route === 'file' && method === 'GET') {
      const path = new URL(request.url).searchParams.get('path');
      if (!safePath(path)) return json({ error: 'Bad path' }, 400);
      if (!publicPath(path) && !(await getUser(request, env))) return json({ error: 'Log in to view this file.' }, 401);
      const r = await ghRaw(env, path);
      if (!r.ok) return json({ error: 'Not found' }, 404);
      const buf = await r.arrayBuffer();
      if (buf.byteLength > 1_500_000) return json({ error: 'File too large to display.' }, 413);
      return new Response(buf, { headers: { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'private, max-age=30' } });
    }

    return json({ error: 'Not found' }, 404);
  } catch (e) {
    console.error('api error', route, e && e.stack || e);
    return json({ error: 'Server error' }, 500);
  }
}
