import pkg from '/home/claude/.npm-global/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
import { readFileSync } from 'fs';

const BASE = 'http://127.0.0.1:8077';
const findings = JSON.parse(readFileSync('/tmp/contrast.json', 'utf8'));
const pages = [...new Set(findings.filter(f => !f.err).map(f => f.page))];

function lum(c){const s=c.map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*s[0]+0.7152*s[1]+0.0722*s[2]}
function ratio(a,b){const l1=lum(a),l2=lum(b);return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05)}
function parse(c){const m=String(c).match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(',').map(Number);if(p.length>3&&p[3]<0.9)return null;return [p[0],p[1],p[2]]}

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
for (const pat of ['**googletagmanager**','**fonts.googleapis**','**fonts.gstatic**','**clarity.ms**','**ahrefs.com**'])
  await page.route(pat, r => r.abort());

const seen = new Map();
for (const p of pages) {
  await page.goto(BASE + p, { waitUntil: 'domcontentloaded', timeout: 15000 });
  const rows = await page.evaluate(() => {
    const out = [];
    const path = el => {
      const bits = [];
      let e = el, n = 0;
      while (e && e !== document.body && n < 4) {
        let s = e.tagName.toLowerCase();
        const c = (e.className || '').toString().trim().split(/\s+/).filter(Boolean);
        if (c.length) s += '.' + c.join('.');
        bits.unshift(s); e = e.parentElement; n++;
      }
      return bits.join(' > ');
    };
    document.querySelectorAll('body *').forEach(el => {
      if (el.closest('header,footer,nav,script,style')) return;
      let txt = ''; el.childNodes.forEach(nd => { if (nd.nodeType === 3) txt += nd.textContent; });
      if (txt.trim().length < 8) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.opacity === '0') return;
      let e = el, bg = null, grad = false;
      while (e) { const b = getComputedStyle(e);
        if (b.backgroundImage && b.backgroundImage !== 'none') { grad = true; break; }
        const bc = b.backgroundColor;
        if (bc && !/rgba\(0, 0, 0, 0\)/.test(bc)) { bg = bc; break; } e = e.parentElement; }
      if (grad || !bg) return;
      out.push({ path: path(el), fg: cs.color, bg, size: parseFloat(cs.fontSize), weight: cs.fontWeight, t: txt.trim().slice(0,34) });
    });
    return out;
  });
  for (const b of rows) {
    const f = parse(b.fg), g = parse(b.bg);
    if (!f || !g) continue;
    const rr = ratio(f, g);
    const large = b.size >= 24 || (b.size >= 18.66 && parseInt(b.weight) >= 700);
    if (rr >= (large ? 3 : 4.5)) continue;
    const k = b.path + '|' + b.fg + '|' + b.bg;
    if (!seen.has(k)) seen.set(k, { ...b, ratio: +rr.toFixed(2), pages: new Set() });
    seen.get(k).pages.add(p);
  }
}
const rows = [...seen.values()].sort((a,b) => b.pages.size - a.pages.size);
for (const r of rows) console.log(`${String(r.pages.size).padStart(2)}p ${String(r.ratio).padStart(5)}  ${r.fg} on ${r.bg}\n      ${r.path}\n      "${r.t}"  [${[...r.pages][0]}]`);
console.log('\ndistinct signatures:', rows.length);
await browser.close();
