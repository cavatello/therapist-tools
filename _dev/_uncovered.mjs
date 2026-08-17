import pkg from '/home/claude/.npm-global/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
const BASE = 'http://127.0.0.1:8077';
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
for (const pat of ['**googletagmanager**','**fonts.googleapis**','**fonts.gstatic**','**clarity.ms**','**ahrefs.com**'])
  await page.route(pat, r => r.abort());

for (const p of process.argv.slice(2)) {
  await page.goto(BASE + p, { waitUntil: 'domcontentloaded', timeout: 15000 });
  const r = await page.evaluate(() => {
    // every class used in the body
    const used = new Set();
    document.querySelectorAll('body *').forEach(el =>
      (el.className || '').toString().trim().split(/\s+/).filter(Boolean).forEach(c => used.add(c)));
    // every class mentioned by any loaded rule
    const styled = new Set();
    for (const sh of document.styleSheets) {
      let rs; try { rs = sh.cssRules; } catch (e) { continue; }
      const walk = list => { for (const r of list) {
        if (r.cssRules) { walk(r.cssRules); if (!r.selectorText) continue; }
        if (!r.selectorText) continue;
        for (const m of r.selectorText.matchAll(/\.([A-Za-z0-9_-]+)/g)) styled.add(m[1]);
      } };
      walk(rs);
    }
    const uncovered = [...used].filter(c => !styled.has(c)).sort();
    // of those, which actually render visible text?
    const withText = uncovered.filter(c => {
      const el = document.querySelector('.' + CSS.escape(c));
      return el && (el.innerText || '').trim().length > 3;
    });
    return { sheets: document.styleSheets.length, used: used.size, uncovered, withText };
  });
  console.log(`\n=== ${p}  (${r.sheets} sheets, ${r.used} classes used)`);
  console.log(`uncovered (${r.uncovered.length}): ${r.uncovered.join(' ')}`);
  console.log(`   of those, carrying text (${r.withText.length}): ${r.withText.join(' ')}`);
}
await browser.close();
