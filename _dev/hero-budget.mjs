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

/* heroPct at 390 is a BACKSTOP, not the rule. The rule on a phone is
   `actionY` below: the reader must be able to SEE something to press without
   scrolling. A hero can be 780px tall and still be excellent if its buttons
   sit at y=600, and it can be 500px tall and useless if it is all prose - so
   the phone budget checks where the action is and keeps a loose height limit
   only to catch runaways (newsletter.html measured 159%).

   firstControl at 390 is one and a half screens (844 x 1.5). Set from the
   pages that measure well after the mobile-hero pass - grow lands at 1238 and
   tax at 1227 - and it still fails everything this audit was written for:
   working-remotely was at 1762 before it was fixed, and grow itself was 1293. */
const BUDGET = {
  1440: { vh: 900, heroPct: 45, firstControl: 900,  actionY: 900 },
  390:  { vh: 844, heroPct: 120, firstControl: 1266, actionY: 844 },
};
const MAX_BLOCKS = 4;   // kicker, h1, one deck sentence, one action (crumb excluded)

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
      /* Blocks before the reader can act. "Act" is whichever comes FIRST: the
         hero's call-to-action link, or an actual field.

         Counting only to the CTA scored practice-simulator at 5 blocks and
         called it a failure. That page puts its rate/sessions/weeks-off inputs
         inside the hero, so the reader reaches a lever at y=434 — better than
         any page that passed — and its fifth "block" was the note sitting
         directly above those inputs, where it belongs. Measuring to the CTA
         alone punishes the best pattern on the site. */
      /* The action. NOT `a[class*=cta]` - that was the original selector and it
         never matched anything on this site, because the class lives on the
         ROW (.gherocta, .therocta, .aherocta) and the links inside it are bare
         or .ghost. Every page silently reported "no CTA", which is why the
         block count was measuring to Infinity and passing pages it should not
         have. Match the row, then take its first link. */
      const cta = hero.querySelector('[class*=erocta] a, [class*=erocta] button, '
        + 'a[class*=cta],a[class*=btn],a[class*=Go],button[class*=cta]');
      const lever = [...hero.querySelectorAll('input,select,textarea,[role=slider]')]
        .filter(e => !e.closest('header,nav,.sitenav,footer'))
        .map(e => e.getBoundingClientRect().top).sort((a, c) => a - c)[0];
      const cy = Math.min(cta ? cta.getBoundingClientRect().top : Infinity,
                          lever ?? Infinity);
      /* The breadcrumb is navigation, not content. It is deliberately styled
         as chrome (see _dev/breadcrumbs.py) and it is the same one line on
         every page; charging it against a budget meant for prose made four
         well-behaved heroes read as failures. Count what the reader has to
         READ before acting: kicker, h1, one deck sentence, one action. */
      const blocks = [...hero.querySelectorAll('p,h1,blockquote,div[class*=quote]')]
        .filter(e => {
          const t = (e.textContent || '').trim();
          if (!t) return false;
          if (e.closest('[class*=erocta],a[class*=cta],a[class*=btn]')) return false;
          return e.getBoundingClientRect().top <= cy;
        }).length;
      /* Where the reader first sees something to press or type. Document
         coordinates, so it is comparable with the viewport height. */
      const actionEl = cta || [...hero.querySelectorAll('input,select,textarea,[role=slider]')]
        .filter(e => !e.closest('header,nav,.sitenav,footer'))[0] || null;
      const actionY = actionEl
        ? Math.round(actionEl.getBoundingClientRect().top + scrollY) : null;
      return { heroH: Math.round(hr.height), first, blocks, isHero, actionY };
    });
    await ctx.close();
    if (!m) continue;

    const pct = Math.round(m.heroH / b.vh * 100);
    const bad = [];
    if (m.isHero && pct > b.heroPct) bad.push(`hero ${pct}% > ${b.heroPct}%`);
    /* Same reason the height rule is skipped for these: when the h1's section
       IS the document, "blocks above the action" counts the whole page. terms,
       privacy and rates reported 5 blocks for having five paragraphs of body
       copy, which is what a terms page is. */
    if (m.isHero && m.blocks > MAX_BLOCKS) bad.push(`${m.blocks} blocks > ${MAX_BLOCKS}`);
    if (!NO_TOOL.has(f)) {
      if (m.actionY === null) bad.push('hero offers no action');
      else if (m.actionY > b.actionY)
        bad.push(`ACTION at y=${m.actionY} > ${b.actionY} (below the fold)`);
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
