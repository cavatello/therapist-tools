import pkg from '/home/claude/.npm-global/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
const BASE = process.env.BASE || 'http://127.0.0.1:8077';
const PAGES = ['/index.html', '/resources.html', '/practice-simulator.html',
  '/mft-programs-california.html', '/about.html', '/tools.html', '/for/licensed.html',
  '/therapist-tax-strategy-california.html', '/newsletter.html'];
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
for (const pat of ['**googletagmanager**','**fonts.googleapis**','**fonts.gstatic**','**clarity.ms**','**ahrefs.com**'])
  await page.route(pat, r => r.abort());
const agg = {};
for (const u of PAGES) {
  try { await page.goto(BASE + u, { waitUntil: 'domcontentloaded', timeout: 15000 }); }
  catch (e) { continue; }
  const rows = await page.evaluate(() => {
    const o = [];
    document.querySelectorAll('a,button,span,div,h5').forEach(el => {
      const s = getComputedStyle(el);
      const br = parseFloat(s.borderTopLeftRadius) || 0;
      const r = el.getBoundingClientRect();
      if (br < 100 || r.width < 20 || r.height < 10) return;
      const cls = (el.className || '').toString().trim().split(/\s+/).filter(Boolean).join('.');
      o.push(`${el.tagName.toLowerCase()}${cls ? '.' + cls : ''}`.slice(0, 40)
        + ` | h${Math.round(r.height)} | "${(el.textContent || '').trim().slice(0, 20)}"`);
    });
    return o;
  });
  rows.forEach(x => agg[x] = (agg[x] || 0) + 1);
}
console.log(Object.entries(agg).sort((a, b) => b[1] - a[1])
  .map(([k, v]) => String(v).padStart(3) + '  ' + k).join('\n'));
await browser.close();
