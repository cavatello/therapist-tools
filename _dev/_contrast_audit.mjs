import pkg from '/home/claude/.npm-global/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
import { readFileSync, writeFileSync } from 'fs';

const BASE = 'http://127.0.0.1:8077';
const pages = readFileSync('/tmp/allpages.txt', 'utf8').trim().split('\n');

// The width to measure at. This audit ran at 1440 and ONLY at 1440 for its
// whole life, and reported "0 findings across 242 pages" while eight pairs
// were failing at 390 - including text at 1.29:1. A contrast failure is a
// property of a rendered layout, and this site has a different layout below
// 900px. Pass a width, or get both:
//
//     node _dev/_contrast_audit.mjs            1440, as before
//     node _dev/_contrast_audit.mjs 390        the phone layout
//
// See _dev/_tool_audit.mjs for the other half of what this misses: the seven
// calculator pages write most of their content with JavaScript, and none of
// it exists at the moment this audit measures.
const WIDTH = Number(process.argv[2]) || 1440;

function lum(c){const s=c.map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*s[0]+0.7152*s[1]+0.0722*s[2]}
function ratio(a,b){const l1=lum(a),l2=lum(b);return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05)}
function parse(c){const m=String(c).match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(',').map(Number);if(p.length>3&&p[3]<0.9)return null;return [p[0],p[1],p[2]]}

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: WIDTH, height: 900 } });
const page = await ctx.newPage();
for (const pat of ['**googletagmanager**','**fonts.googleapis**','**fonts.gstatic**','**clarity.ms**','**ahrefs.com**'])
  await page.route(pat, r => r.abort());

const findings = [];
let n = 0;
for (const p of pages) {
  n++;
  try {
    await page.goto(BASE + p, { waitUntil: 'domcontentloaded', timeout: 15000 });
    const nodes = await page.evaluate(() => {
      const out = [];
      document.querySelectorAll('body *').forEach(el => {
        // NOT header/footer/nav. That exclusion was made when this sweep
        // was about article text, and it hid the worst finding on the site:
        // the masthead CTA label at 2.28:1 on 238 pages. Chrome is where a
        // reader looks first. Only non-rendering elements are skipped.
        if (el.closest('script,style,template')) return;
        let txt = ''; el.childNodes.forEach(nd => { if (nd.nodeType === 3) txt += nd.textContent; });
        txt = txt.trim();
        if (txt.length < 8) return;
        const r = el.getBoundingClientRect();
        if (r.width < 2 || r.height < 2) return;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.opacity === '0') return;
        let e = el, bg = null, grad = false;
        while (e) {
          const b = getComputedStyle(e);
          if (b.backgroundImage && b.backgroundImage !== 'none') { grad = true; break; }
          const bc = b.backgroundColor;
          if (bc && !/rgba\(0, 0, 0, 0\)/.test(bc)) { bg = bc; break; }
          e = e.parentElement;
        }
        if (grad || !bg) return;
        out.push({ fg: cs.color, bg, size: parseFloat(cs.fontSize), weight: cs.fontWeight,
          cls: (el.className||'').toString().slice(0,40), tag: el.tagName.toLowerCase(),
          t: txt.slice(0, 40),
          anc: (e.className||'').toString().slice(0,30) });
      });
      return out;
    });
    for (const b of nodes) {
      const f = parse(b.fg), g = parse(b.bg);
      if (!f || !g) continue;
      const rr = ratio(f, g);
      const large = b.size >= 24 || (b.size >= 18.66 && parseInt(b.weight) >= 700);
      const min = large ? 3 : 4.5;
      if (rr < min) findings.push({ page: p, ratio: +rr.toFixed(2), min, ...b });
    }
  } catch (e) { findings.push({ page: p, err: e.message.slice(0, 50) }); }
  if (n % 40 === 0) console.log(`... ${n}/${pages.length}, ${findings.length} findings`);
}
writeFileSync('/tmp/contrast.json', JSON.stringify(findings, null, 1));

// summarize by the css signature, which is what a fix targets
const bySig = {};
for (const f of findings) {
  if (f.err) continue;
  const k = `${f.tag}.${f.cls} in .${f.anc} | ${f.fg} on ${f.bg} | ${f.ratio}`;
  (bySig[k] = bySig[k] || { n: 0, pages: new Set(), ex: f.t }).n++;
  bySig[k].pages.add(f.page);
}
const rows = Object.entries(bySig).sort((a,b) => b[1].pages.size - a[1].pages.size);
console.log(`\nTOTAL findings ${findings.length} across ${new Set(findings.map(f=>f.page)).size} pages\n`);
for (const [k, v] of rows.slice(0, 30))
  console.log(`${String(v.pages.size).padStart(4)} pages | ${k}\n            e.g. "${v.ex}"`);
await browser.close();
