// Terminal UI for the Python player: loads project files, runs them in a Pyodide worker.
const $ = (s) => document.querySelector(s);
const esc = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

class Term {
  constructor(el) { this.el = el; this.carry = ''; this.clear(); }
  clear() { this.rows = [[]]; this.r = 0; this.c = 0; this.fg = ''; this.bg = ''; this.bold = false; this.schedule(); }
  get st() { return [this.fg, this.bg, this.bold ? 'bold' : ''].filter(Boolean).join(' '); }
  row() { while (this.rows.length <= this.r) this.rows.push([]); return this.rows[this.r]; }
  put(ch) { const row = this.row(); while (row.length < this.c) row.push({ ch: ' ', st: '' }); row[this.c++] = { ch, st: this.st }; }
  newline() { this.r++; this.c = 0; this.row(); if (this.rows.length > 3000) { this.rows.shift(); this.r--; } }
  write(s) {
    s = this.carry + s; this.carry = '';
    for (let i = 0; i < s.length; i++) {
      const ch = s[i];
      if (ch === '\x1b') {
        if (s[i + 1] === '[') {
          let j = i + 2;
          while (j < s.length && !/[@-~]/.test(s[j])) j++;
          if (j >= s.length) { this.carry = s.slice(i); break; }
          this.csi(s.slice(i + 2, j), s[j]); i = j;
        } else if (i + 1 >= s.length) { this.carry = s.slice(i); break; }
        else { if (s[i + 1] === 'c') this.clear(); i++; }
      } else if (ch === '\n') this.newline();
      else if (ch === '\r') this.c = 0;
      else if (ch === '\b') this.c = Math.max(0, this.c - 1);
      else if (ch === '\t') { do this.put(' '); while (this.c % 8); }
      else if (ch >= ' ') this.put(ch);
    }
    this.schedule();
  }
  csi(args, cmd) {
    const p = args.replace(/^\?/, '').split(';').map((n) => parseInt(n, 10));
    const n = Number.isNaN(p[0]) ? 0 : p[0];
    const one = n || 1;
    if (args.startsWith('?')) return;
    switch (cmd) {
      case 'm': {
        const list = args === '' ? [0] : p.map((x) => (Number.isNaN(x) ? 0 : x));
        for (let k = 0; k < list.length; k++) {
          const v = list[k];
          if (v === 0) { this.fg = ''; this.bg = ''; this.bold = false; }
          else if (v === 1) this.bold = true;
          else if (v === 22) this.bold = false;
          else if (v >= 30 && v <= 37) this.fg = 'c' + (v - 30);
          else if (v >= 90 && v <= 97) this.fg = 'g' + (v - 90);
          else if (v >= 40 && v <= 47) this.bg = 'b' + (v - 40);
          else if (v === 39) this.fg = '';
          else if (v === 49) this.bg = '';
          else if (v === 38 || v === 48) k += list[k + 1] === 5 ? 2 : 4;
        }
        break;
      }
      case 'H': case 'f': this.r = Math.max(0, (Number.isNaN(p[0]) ? 1 : p[0]) - 1); this.c = Math.max(0, (Number.isNaN(p[1]) ? 1 : p[1]) - 1); this.row(); break;
      case 'A': this.r = Math.max(0, this.r - one); break;
      case 'B': this.r += one; this.row(); break;
      case 'C': this.c += one; break;
      case 'D': this.c = Math.max(0, this.c - one); break;
      case 'G': this.c = Math.max(0, one - 1); break;
      case 'J':
        if (n === 2 || n === 3) { this.rows = [[]]; if (n === 3) { this.r = 0; this.c = 0; } this.row(); }
        else if (n === 0) { this.row().length = Math.min(this.row().length, this.c); this.rows.length = this.r + 1; }
        break;
      case 'K': {
        const row = this.row();
        if (n === 0) row.length = Math.min(row.length, this.c);
        else if (n === 1) for (let k = 0; k < this.c && k < row.length; k++) row[k] = { ch: ' ', st: '' };
        else row.length = 0;
        break;
      }
    }
  }
  schedule() { if (!this.pending) { this.pending = true; requestAnimationFrame(() => { this.pending = false; this.paint(); }); } }
  paint() {
    const el = this.el;
    const stick = el.scrollHeight - el.scrollTop - el.clientHeight < 40;
    el.innerHTML = this.rows.map((row) => {
      let html = '', cur = null, buf = '';
      const flush = () => { if (buf) html += cur ? `<span class="${cur}">${esc(buf)}</span>` : esc(buf); buf = ''; };
      for (const cell of row) { if (cell.st !== cur) { flush(); cur = cell.st; } buf += cell.ch; }
      flush();
      return html;
    }).join('\n');
    if (stick) el.scrollTop = el.scrollHeight;
  }
}

const q = new URLSearchParams(location.search);
const term = new Term($('#screen'));
const status = (s) => { $('#status').textContent = s; };
let worker = null, sab = null, gen = 0;

function setInput(on) {
  $('#inp').classList.toggle('off', !on);
  $('#line').disabled = !on;
  $('#line').placeholder = on ? 'Type here and press Enter' : 'Waiting…';
  if (on) $('#line').focus();
}

async function fetchAll(paths, myGen) {
  const out = {};
  let next = 0;
  async function worker1() {
    while (next < paths.length) {
      const p = paths[next++];
      const r = await fetch('/api/file?path=' + encodeURIComponent(p), { credentials: 'same-origin' });
      if (r.status === 401) throw new Error('Please log in first.');
      if (!r.ok) throw new Error(`Could not load ${p} (${r.status})`);
      out[p] = await r.text();
      if (myGen !== gen) return;
      status(`Loading files… ${Object.keys(out).length}/${paths.length}`);
    }
  }
  await Promise.all(Array.from({ length: 6 }, worker1));
  return out;
}

async function start() {
  const myGen = ++gen;
  if (worker) worker.terminate();
  term.clear(); setInput(false);
  if (!self.crossOriginIsolated || typeof SharedArrayBuffer === 'undefined') {
    status('Unsupported browser tab'); term.write('This player needs a cross-origin isolated page (SharedArrayBuffer).\nTry a recent Chrome, Edge, Firefox or Safari.\n'); return;
  }
  try {
    const type = q.get('type'), root = q.get('root'), file = q.get('file'), mod = q.get('module');
    const single = q.get('single') === '1';
    status('Reading the project…');
    let paths;
    if (single) paths = [file];
    else {
      const { entries } = await (await fetch('/api/tree')).json();
      paths = entries.filter((e) => e.p.startsWith(root + '/') && /\.(py|lisp|txt|json|csv)$/i.test(e.p) &&
        !/\/(tests|benchmarks|docs)\//.test(e.p) && e.s < 400000).map((e) => e.p).slice(0, 150);
    }
    const texts = await fetchAll(paths, myGen);
    if (myGen !== gen) return;
    const files = {};
    for (const [p, t] of Object.entries(texts)) files['/work/' + p] = t;
    const cwd = '/work/' + (single ? file.split('/').slice(0, -1).join('/') : root);
    let args = [];
    if (type === 'module' && /--text/.test(texts[`${root}/${mod}/__main__.py`] || '')) args = ['--text'];
    sab = new SharedArrayBuffer(65544);
    worker = new Worker('/pyworker.js');
    worker.onmessage = (e) => {
      if (myGen !== gen) return;
      const m = e.data;
      if (m.t === 'out') term.write(m.s);
      else if (m.t === 'status') status(m.s);
      else if (m.t === 'input') { setInput(true); status('Waiting for your input'); }
      else if (m.t === 'err') { term.write(`\n\x1b[31m${m.s}\x1b[0m\n`); status('Stopped with an error'); setInput(false); }
      else if (m.t === 'done') { term.write(`\n\x1b[90m[program finished${m.code ? ', exit code ' + m.code : ''}]\x1b[0m\n`); status('Finished'); setInput(false); }
    };
    worker.postMessage({ t: 'run', files, cwd, mode: type === 'module' ? 'module' : 'script', module: mod, file: '/work/' + file, name: type === 'module' ? mod : file.split('/').pop(), args, sab });
  } catch (e) { status('Error'); term.write('\x1b[31m' + e.message + '\x1b[0m\n'); }
}

$('#inp').onsubmit = (e) => {
  e.preventDefault();
  if ($('#line').disabled || !sab) return;
  const text = $('#line').value;
  $('#line').value = '';
  term.write(text + '\n');
  const bytes = new TextEncoder().encode(text).slice(0, 65000);
  new Uint8Array(sab, 8).set(bytes);
  const flag = new Int32Array(sab, 0, 2);
  Atomics.store(flag, 1, bytes.length);
  Atomics.store(flag, 0, 1);
  Atomics.notify(flag, 0);
  setInput(false); status('Running…');
};
$('#stop').onclick = () => { if (worker) { worker.terminate(); worker = null; } gen++; setInput(false); status('Stopped'); };
$('#restart').onclick = start;
start();
