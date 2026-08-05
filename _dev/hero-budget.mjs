/* _dev/hero-budget.mjs — keep heroes honest.
 *
 * Written after the working-remotely hero measured 716px (80% of a 900px
 * viewport) with the first input at y=1748 — more than twice as far down as any
 * other page on a site whose entire value is "put your numbers in". The fix was
 * per-page; this is what stops it coming back.
 *
 * The rule that matters is NOT height. The practice simulator has a tall banner
 * and is the best page on the site, because its first control sits at y=469.
 * Height is a proxy; DISTANCE TO THE FIRST LEVER is the thing. Both are checked,
 * and the distance one is the one that fails loudest.
 *
 * See claude/hero-design-rules.md.
 *
 * Usage: node _dev/hero-budget.mjs [dir]
 */
import { chromium } from '/home/claude/.npm-global/lib/node_modules/playwright/index.mjs';
import { readdirSync, readFileSync } from 'fs';

const DIR = process.argv[2] || '.';
const SKIP = new Set(['tycoon.html', 'concepts.html']);
/* Reference pages have no lever to reach, so the distance rule cannot apply.
   They are still held to the block count — two stacked orientation strips is a
   mess whether or not there is a form underneath. */
const NO_TOOL = new Set(['about.html', 'contact.html', 'newsletter.html',
                         'privacy.html', 'terms.html', 'tools.html', 'rates.html']);

const BUDGET = {
  1440: { vh: 900, heroPct: 45, firstControl: 900 },
  390:  { vh: 844, heroPct: 60, firstControl: 1200 },
};
const MAX_BLOCKS = 4;   // orientation, h1, one deck sentence, one action

const files = readdirSync(DIR).filter(f => f.endsWith('.html') && !SKIP.has(f));
const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

let fails = 0;
for (const f of files) {
  const lines = [];
  for (const [w, b] of Object.entries(BUDGET)) {
    const ctx = await browser.newContext({ viewport: { width: +w, height: b.vh } });
    const p = await ctx.newPage();
    await p.route('**/*', r => {
      const u = r.request().url();
      return (u.startsWith('data:') || u.startsWith('about:')) ? r.continue() : r.abort();
    });
    await p.setContent(readFileSync(`${DIR}/${f}`, 'utf8'), { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(70);

    const m = await p.evaluate(() => {
      const h1 = document.querySelector('h1');
      if (!h1) return null;
      const hero = h1.closest('section') || document.body;
      const hr = hero.getBoundingClientRect();
      /* Is this actually a hero, or is it the whole document? On terms.html and
         tools.html the h1 lives in the one section that holds the entire page,
         so "hero height" measured 899% of the viewport — a true number about
         the wrong box. A hero introduces the page; it does not contain its
         sections. More than one h2 inside means this is content, so the height
         rule is skipped and only the block count applies. */
      const isHero = hero.querySelectorAll('h2').length <= 1;
      /* first thing the reader can operate, excluding site chrome */
      const first = [...document.querySelectorAll('input,select,textarea,[role=slider]')]
        .filter(e => !e.closest('header,nav,.sitenav,footer'))
        .map(e => Math.round(e.getBoundingClientRect().top + scrollY))
        .filter(y => y > 0).sort((a, c) => a - c)[0] ?? null;
      /* blocks before the hero's action: every non-empty text child of the hero
         that sits above the first link-that-looks-like-a-button */
      const cta = hero.querySelector('a[class*=cta],a[class*=go],a[class*=Go]');
      const cy = cta ? cta.getBoundingClientRect().top : Infinity;
      const blocks = [...hero.querySelectorAll('p,h1,blockquote,ol[class*=bcr],div[class*=quote]')]
        .filter(e => {
          const t = (e.textContent || '').trim();
          if (!t) return false;
          if (e.parentElement && e.parentElement.closest('a[class*=cta],a[class*=go]')) return false;
          return e.getBoundingClientRect().top <= cy;
        }).length;
      return { heroH: Math.round(hr.height), first, blocks, isHero };
    });
    await ctx.close();
    if (!m) continue;

    const pct = Math.round(m.heroH / b.vh * 100);
    const bad = [];
    if (m.isHero && pct > b.heroPct) bad.push(`hero ${pct}% > ${b.heroPct}%`);
    if (m.blocks > MAX_BLOCKS) bad.push(`${m.blocks} blocks > ${MAX_BLOCKS}`);
    if (!NO_TOOL.has(f)) {
      if (m.first === null) bad.push('no control found');
      else if (m.first > b.firstControl)
        bad.push(`FIRST LEVER at y=${m.first} > ${b.firstControl}`);
    }
    if (bad.length) lines.push(`  ${String(w).padStart(4)}px  ` + bad.join('  ·  '));
  }
  if (lines.length) { fails++; console.log(`\n${f}`); lines.forEach(l => console.log(l)); }
}
await browser.close();
console.log(`\n================================================`);
console.log(`${files.length} pages checked · ${fails} over budget`);
process.exit(fails ? 1 : 0);
