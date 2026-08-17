import pkg from '/home/claude/.npm-global/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
import { readFileSync } from 'fs';

// The P8 house style ("the fifth thing"), from claude/house-style-the-fifth-thing.md
const SPEC = {
  paper: '#F6F8F6', card: '#FFFFFF', ink: '#1B2420', dim: '#5F6A64',
  line: '#DFE4E0', pine: '#2C6350', deep: '#123C30', gold: '#FFE7A3',
};
const PATH_HUES = ['#2F6FDB', '#7A5AF8', '#0E8FA8', '#17864A', '#B0730B', '#BC3F86'];
const BODY_PX = 16.5;

const BASE = process.env.BASE || 'http://127.0.0.1:8077';
const pages = readFileSync('/tmp/allpages.txt', 'utf8').trim().split('\n');
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
for (const pat of ['**googletagmanager**','**fonts.googleapis**','**fonts.gstatic**','**clarity.ms**','**ahrefs.com**'])
  await page.route(pat, r => r.abort());

const agg = {
  tokens: {}, gradients: {}, pills: {}, bodyPx: {}, slabs: {},
  pureWhiteBg: 0, fonts: {}, radii: {},
};
const bump = (o, k) => { o[k] = (o[k] || 0) + 1; };

let n = 0;
for (const p of pages) {
  n++;
  try {
    await page.goto(BASE + p, { waitUntil: 'domcontentloaded', timeout: 15000 });
    const r = await page.evaluate((SPEC) => {
      const cs = getComputedStyle(document.body);
      const tok = {};
      for (const k of Object.keys(SPEC)) tok[k] = cs.getPropertyValue('--' + k).trim();
      tok.dim = tok.dim || cs.getPropertyValue('--muted').trim();
      // gradients on real, sizeable elements
      let grad = 0, pill = 0, radii = {};
      document.querySelectorAll('body *').forEach(el => {
        const s = getComputedStyle(el);
        const b = el.getBoundingClientRect();
        if (b.width < 24 || b.height < 12) return;
        if (s.backgroundImage && s.backgroundImage.includes('gradient')) grad++;
        const br = parseFloat(s.borderTopLeftRadius) || 0;
        const isBtn = el.tagName === 'BUTTON' || el.tagName === 'A' ||
                      /btn|cta|go\b/.test((el.className || '').toString());
        if (isBtn && br >= 100) pill++;
        if (isBtn && br > 0) radii[Math.round(br)] = (radii[Math.round(br)] || 0) + 1;
      });
      return {
        tok, grad, pill, radii,
        bodyFont: cs.fontFamily.split(',')[0].replace(/["']/g, ''),
        bodyPx: parseFloat(cs.fontSize),
        bodyBg: cs.backgroundColor,
        slabs: document.querySelectorAll('.slab').length,
      };
    }, SPEC);

    for (const [k, v] of Object.entries(r.tok)) {
      const want = SPEC[k];
      if (!v) { bump(agg.tokens, `${k}: UNSET`); continue; }
      if (v.toUpperCase() !== want.toUpperCase()) bump(agg.tokens, `${k}: ${v} (spec ${want})`);
    }
    if (r.grad) bump(agg.gradients, String(r.grad));
    if (r.pill) bump(agg.pills, String(r.pill));
    bump(agg.bodyPx, String(r.bodyPx));
    bump(agg.fonts, r.bodyFont);
    bump(agg.slabs, String(r.slabs));
    if (/rgb\(255, 255, 255\)/.test(r.bodyBg)) agg.pureWhiteBg++;
    for (const [k, c] of Object.entries(r.radii)) agg.radii[k] = (agg.radii[k] || 0) + c;
  } catch (e) { console.error("ERR " + p + ": " + e.message.slice(0,120)); }
  if (n % 60 === 0) console.error(`... ${n}/${pages.length}`);
}
const show = (title, o, limit = 8) => {
  const rows = Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, limit);
  console.log(`\n## ${title}`);
  if (!rows.length) { console.log('   (none) OK'); return; }
  for (const [k, v] of rows) console.log(`   ${String(v).padStart(4)} pages  ${k}`);
};
console.log(`AUDITED ${pages.length} pages against the P8 house style\n`);
show('TOKENS off spec', agg.tokens, 12);
show('pages with GRADIENTS (spec: none from anywhere)', agg.gradients);
show('pages with PILL buttons (spec: 6px, no pills)', agg.pills);
show('button corner radii in use (spec: 6px)', agg.radii, 10);
show(`body font-size (spec ${BODY_PX}px)`, agg.bodyPx);
show('body font family (spec: Inter)', agg.fonts);
show('slabs per page (spec: exactly one)', agg.slabs);
console.log(`\n## body background pure white (spec: never) : ${agg.pureWhiteBg} pages`);
await browser.close();
