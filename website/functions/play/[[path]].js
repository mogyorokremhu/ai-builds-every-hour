import { getUser, ghRaw, safePath } from '../_lib.js';

const TYPES = {
  html: 'text/html; charset=utf-8', css: 'text/css; charset=utf-8', js: 'text/javascript; charset=utf-8',
  mjs: 'text/javascript; charset=utf-8', json: 'application/json; charset=utf-8', svg: 'image/svg+xml',
  png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', gif: 'image/gif', webp: 'image/webp', ico: 'image/x-icon',
  wav: 'audio/wav', mp3: 'audio/mpeg', ogg: 'audio/ogg', txt: 'text/plain; charset=utf-8', woff2: 'font/woff2',
};

// Serves a project's static files from GitHub (with correct MIME types) to logged-in users,
// so browser games like Hexfall run straight from the repo at /play/<repo path>.
export async function onRequest({ request, env, params }) {
  if (request.method !== 'GET' && request.method !== 'HEAD') return new Response('Method not allowed', { status: 405 });
  if (!(await getUser(request, env)))
    return new Response('Please log in to play.', { status: 401, headers: { 'content-type': 'text/plain' } });
  const path = [].concat(params.path || []).join('/');
  if (!safePath(path)) return new Response('Not found', { status: 404 });
  const r = await ghRaw(env, path);
  if (!r.ok) return new Response('Not found', { status: r.status === 404 ? 404 : 502 });
  const ext = path.split('.').pop().toLowerCase();
  return new Response(r.body, {
    headers: {
      'content-type': TYPES[ext] || 'application/octet-stream',
      'x-content-type-options': 'nosniff',
      'cache-control': 'private, max-age=60',
      'cross-origin-embedder-policy': 'require-corp',
      'cross-origin-resource-policy': 'same-origin',
    },
  });
}
