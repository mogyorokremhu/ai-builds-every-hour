// Static "is every module imported by some test?" analysis (pure; no fs access).
// modules: { "hex.js": "<source>" }, tests: { "hex.test.js": "<source>" }

export function importsOf(source) {
  const out = new Set();
  const re = /from\s+["']\.\.\/src\/([\w\-./]+?)["']|import\s*\(\s*["']\.\.\/src\/([\w\-./]+?)["']\s*\)/g;
  let m;
  while ((m = re.exec(source))) out.add(m[1] || m[2]);
  return out;
}

export function exportsOf(source) {
  const names = [];
  const re = /export\s+(?:async\s+)?(?:function\*?|const|let|class)\s+([A-Za-z_$][\w$]*)/g;
  let m;
  while ((m = re.exec(source))) names.push(m[1]);
  return names;
}

// Which modules are untested, and which exports of tested modules no test mentions.
export function coverageReport(modules, tests, { ignore = [] } = {}) {
  const testedBy = {};
  for (const [tname, tsrc] of Object.entries(tests)) {
    for (const imp of importsOf(tsrc)) (testedBy[imp] ||= []).push(tname);
  }
  const allTests = Object.values(tests).join("\n");
  const rows = [];
  for (const [name, src] of Object.entries(modules).sort()) {
    if (ignore.includes(name)) continue;
    const exps = exportsOf(src);
    const unused = exps.filter((e) => !new RegExp(`\\b${e.replace(/\$/g, "\\$")}\\b`).test(allTests));
    rows.push({ module: name, tests: testedBy[name] || [], exports: exps.length, untestedExports: unused });
  }
  return {
    rows,
    untested: rows.filter((r) => r.tests.length === 0).map((r) => r.module),
    partial: rows.filter((r) => r.tests.length && r.untestedExports.length).map((r) => r.module),
  };
}

export function coverageMarkdown(report) {
  const lines = ["| module | tests | exports | not mentioned in any test |", "|---|---|---|---|"];
  for (const r of report.rows) {
    lines.push(`| ${r.module} | ${r.tests.length} | ${r.exports} | ${r.untestedExports.join(", ") || "—"} |`);
  }
  lines.push("", `Untested modules: ${report.untested.join(", ") || "none"}`);
  return lines.join("\n");
}
