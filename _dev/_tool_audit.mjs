// The audit for the half of this site that is an application, not a document.
//
// WHY THIS EXISTS
//
// `_dev/_contrast_audit.mjs` walks the DOM as delivered. Seven pages here are
// calculators: they render most of what a reader sees only after an input
// changes. In the delivered HTML that content is a hidden template with zero
// height, so the audit measures nothing, moves on, and reports clean.
//
// It reported "0 findings across 242 pages" while the tax page was showing
// six ledger rows at 2.18:1 and a verdict card at 1.29:1 on a phone. Nobody
// found that with a tool. It was reported from a phone, by eye.
//
// So this one fills every input in, waits for the tool to recompute, and then
// measures - at whatever widths you give it. Colours are blended against the
// nearest painted ancestor, so a translucent overlay is scored as it actually
// looks rather than as it is declared.
//
//     node _dev/_tool_audit.mjs               390 and 1440
//     node _dev/_tool_audit.mjs 390 768 1440  whichever widths you want
//
// Exits non-zero on any failure, so it can be a gate rather than a report.
import pkg from '/home/claude/.npm-global/lib/node_modules/playwright/index.js';
const { chromium } = pkg;

const BASE = 'http://127.0.0.1:8077';
// The seven pages whose output is computed rather than written.
const PAGES = [
  'amft-3000-hours-california.html',
  'associate-mft-job-advisor.html',
  'grow-your-therapy-practice.html',
  'practice-simulator.html',
  'therapist-cost-of-living-california.html',
  'therapist-tax-strategy-california.html',
  'therapist-working-remotely-california.html',
];
const WIDTHS = process.argv.slice(2).map(Number).filter(Boolean);
const widths = WIDTHS.length ? WIDTHS : [390, 1440];

const MEASURE = () => {
  const lum = c => { const m = String(c).match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const q = m[1].split(',').map(Number);
    const s = q.slice(0, 3).map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2]; };
  // A translucent colour is judged as it lands, not as it is written.
  const blend = (fg, bg) => { const f = String(fg).match(/[\d.]+/g).map(Number);
    const k = String(bg).match(/[\d.]+/g).map(Number);
    const a = f.length > 3 ? f[3] : 1;
    return `rgb(${[0,1,2].map(i => Math.round(f[i] * a + k[i] * (1 - a))).join(', ')})`; };
  const ratio = (a, bg) => { const l1 = lum(a), l2 = lum(bg);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); };
  const bgOf = el => { let n = el;
    while (n) { const c = getComputedStyle(n).backgroundColor;
      const m = String(c).match(/rgba?\(([^)]+)\)/);
      if (m) { const q = m[1].split(',').map(Number); if (!(q.length > 3 && q[3] < 0.5)) return c; }
      n = n.parentElement; }
    return 'rgb(255, 255, 255)'; };
  const rows = [];
  for (const el of document.querySelectorAll('body *')) {
    const own = [...el.childNodes].filter(n => n.nodeType === 3)
      .map(n => n.textContent.trim()).join(' ').trim();
    if (own.length < 4) continue;
    const cs = getComputedStyle(el), bx = el.getBoundingClientRect();
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.05 || !bx.height) continue;
    const bg = bgOf(el), eff = blend(cs.color, bg);
    const r = ratio(eff, bg);
    const size = parseFloat(cs.fontSize), weight = +cs.fontWeight || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3.0 : 4.5;
    if (r < need) rows.push({ r: +r.toFixed(2), need, size, eff, bg, txt: own.slice(0, 60) });
  }
  return rows;
};

// Fill everything in. The values only have to be plausible - the point is to
// make the tool render its output, not to test any particular scenario.
const DRIVE = () => {
  const set = (el, v) => { const d = Object.getOwnPropertyDescriptor(el.__proto__, 'value');
    if (!d || !d.set) return; d.set.call(el, v);
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true })); };
  for (const el of document.querySelectorAll('input')) {
    const n = (el.id + el.name + el.className).toLowerCase();
    if (el.type === 'checkbox') continue;
    if (el.type === 'range') { set(el, el.value); continue; }
    if (/rate|price|fee/.test(n)) set(el, '200');
    else if (/sess|week|client|hour/.test(n)) set(el, '20');
    else if (/profit|income|gross|salary|pay/.test(n)) set(el, '195000');
    else if (/exp|cost/.test(n)) set(el, '3500');
    else if (/age/.test(n)) set(el, '45');
    else if (el.type === 'number') set(el, '20');
  }
};

const browser = await chromium.launch();
let total = 0;
for (const width of widths) {
  const ctx = await browser.newContext({ viewport: { width, height: 900 } });
  await ctx.route('**', r => r.request().url().startsWith(BASE) ? r.continue() : r.abort());
  const page = await ctx.newPage();
  let n = 0;
  for (const f of PAGES) {
    await page.goto(`${BASE}/${f}`, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await page.waitForTimeout(600);
    const before = await page.evaluate(MEASURE);
    await page.evaluate(DRIVE);
    await page.waitForTimeout(1100);
    const after = await page.evaluate(MEASURE);
    const all = [...before, ...after];
    n += all.length;
    if (!all.length) continue;
    console.log(`\n${width}px  ${f}`);
    const seen = new Set();
    for (const x of all) {
      const k = `${x.eff}|${x.bg}|${x.size}`;
      if (seen.has(k)) continue; seen.add(k);
      const state = before.some(y => y.txt === x.txt) ? 'on load ' : 'in use  ';
      console.log(`   ${state} ${String(x.r).padStart(5)}:1 (needs ${x.need})  ${x.size}px  ${x.eff} on ${x.bg}`);
      console.log(`             "${x.txt}"`);
    }
  }
  console.log(`\n${width}px: ${n} failure(s) across ${PAGES.length} calculator page(s)`);
  total += n;
  await ctx.close();
}
await browser.close();
console.log(total ? `\nTOTAL ${total} contrast failure(s) in tool output`
                  : `\nTOTAL 0 - every calculator is readable at ${widths.join(', ')}px, before and after use`);
process.exit(total ? 1 : 0);
