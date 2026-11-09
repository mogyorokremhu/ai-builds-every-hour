// Runs Python in the browser with Pyodide. Blocking input() works through a SharedArrayBuffer.
importScripts('https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js');

let pyodide = null;
let flag = null, data = null;
const pending = [];
let lastFlush = 0;
const dec = new TextDecoder();
const inDec = new TextDecoder();

function flush() {
  if (pending.length) { postMessage({ t: 'out', s: dec.decode(new Uint8Array(pending), { stream: true }) }); pending.length = 0; }
  lastFlush = performance.now();
}
function rawOut(b) {
  pending.push(b & 255);
  if (b === 10 && performance.now() - lastFlush > 25) flush();
  else if (pending.length > 4096) flush();
}
function readLine() {
  flush();
  Atomics.store(flag, 0, 0);
  postMessage({ t: 'input' });
  Atomics.wait(flag, 0, 0);
  const n = Atomics.load(flag, 1);
  Atomics.store(flag, 0, 0);
  return inDec.decode(data.slice(0, n));
}

const BOOT = `
import json, sys, os, runpy, time, webterm
cfg = json.loads(cfg_json)
_sleep = time.sleep
def _s(t):
    webterm.flush()
    _sleep(t)
time.sleep = _s
os.chdir(cfg['cwd'])
sys.path.insert(0, cfg['cwd'])
sys.argv = [cfg['name']] + cfg['args']
code = 0
try:
    if cfg['mode'] == 'module':
        runpy.run_module(cfg['module'], run_name='__main__', alter_sys=True)
    else:
        runpy.run_path(cfg['file'], run_name='__main__')
except SystemExit as e:
    code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
code
`;

onmessage = async (e) => {
  const m = e.data;
  if (m.t !== 'run') return;
  try {
    flag = new Int32Array(m.sab, 0, 2);
    data = new Uint8Array(m.sab, 8);
    if (!pyodide) { postMessage({ t: 'status', s: 'Loading Python (first time takes a few seconds)…' }); pyodide = await loadPyodide(); }
    pyodide.setStdout({ raw: rawOut });
    pyodide.setStderr({ raw: rawOut });
    pyodide.setStdin({ stdin: readLine });
    pyodide.registerJsModule('webterm', { flush });
    postMessage({ t: 'status', s: 'Preparing files…' });
    for (const [path, text] of Object.entries(m.files)) {
      pyodide.FS.mkdirTree(path.split('/').slice(0, -1).join('/') || '/');
      pyodide.FS.writeFile(path, text);
    }
    pyodide.globals.set('cfg_json', JSON.stringify({ cwd: m.cwd, mode: m.mode, module: m.module, file: m.file, name: m.name, args: m.args }));
    postMessage({ t: 'status', s: 'Running…' });
    const code = await pyodide.runPythonAsync(BOOT);
    flush();
    postMessage({ t: 'done', code });
  } catch (err) {
    flush();
    postMessage({ t: 'err', s: String(err && err.message ? err.message : err) });
  }
};
