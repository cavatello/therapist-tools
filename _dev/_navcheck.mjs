import pkg from '/home/claude/.npm-global/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
const BASE = 'http://127.0.0.1:8077';
const PAGES = ['/index.html', '/mft-programs-california.html', '/practice-simulator.html',
  '/about.html', '/for/licensed.html', '/hiring-first-associate-california-therapist.html',
  '/alliant-international-university-mft.html', '/resources.html'];
const WIDTHS = [360, 390, 768, 1024, 1440];
const browser = await chromium.launch();
let bad = 0;
for (const w of WIDTHS) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
  const page = await ctx.newPage();
  for (const pat of ['**googletagmanager**','**fonts.googleapis**','**fonts.gstatic**','**clarity.ms**','**ahrefs.com**'])
    await page.route(pat, r => r.abort());
  for (const p of PAGES) {
    await page.goto(BASE + p, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(250);
    const r = await page.evaluate(() => {
      const nav = document.querySelector('.sitenav');
      const links = document.querySelector('.sitenav-links');
      if (!nav || !links) return null;
      const tops = [...links.querySelectorAll('.sitenav-top')];
      const rows = new Set(tops.map(t => Math.round(t.getBoundingClientRect().top))).size;
      const cs = getComputedStyle(links);
      return { navH: Math.round(nav.getBoundingClientRect().height), rows, n: tops.length,
        bg: cs.backgroundColor, disp: cs.display,
        overflow: Math.round(links.scrollWidth - links.clientWidth),
        docW: document.documentElement.scrollWidth };
    });
    if (!r) { console.log(`  ${p} @${w}: no nav`); continue; }
    const problems = [];
    if (w >= 1024 && r.rows > 1) problems.push(`${r.rows} rows`);
    if (w >= 1024 && r.navH > 110) problems.push(`navH ${r.navH}`);
    if (!/rgba\(0, 0, 0, 0\)/.test(r.bg)) problems.push(`pill bg ${r.bg}`);
    if (r.docW > w + 2) problems.push(`page overflow ${r.docW}`);
    if (problems.length) { bad++; console.log(`FAIL ${p} @${w}: ${problems.join(', ')}  (${r.n} items, ${r.disp})`); }
  }
  await ctx.close();
}
console.log(bad ? `\n${bad} nav problem(s)` : '\nNAV CLEAN at all widths');
await browser.close();
process.exit(bad ? 1 : 0);
