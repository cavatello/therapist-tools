import pkg from '/home/claude/.npm-global/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
import { readFileSync, writeFileSync } from 'fs';

const BASE = 'http://127.0.0.1:8077';
const pages = readFileSync('/tmp/allpages.txt', 'utf8').trim().split('\n');

function lum(c){const s=c.map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*s[0]+0.7152*s[1]+0.0722*s[2]}
function ratio(a,b){const l1=lum(a),l2=lum(b);return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05)}
function parse(c){const m=String(c).match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(',').map(Number);if(p.length>3&&p[3]<0.9)return null;return [p[0],p[1],p[2]]}

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
for (const pat of ['**googletagmanager**','**fonts.googleapis**','**fonts.gstatic**','**clarity.ms**','**ahrefs.com**'])
  await page.route(pat, r => r.abort());

const findings = [];
// Pairs this sweep cannot reduce to two colours. Reported, never ignored.
const unmeasured = [];
let n = 0;
for (const p of pages) {
  n++;
  try {
    await page.goto(BASE + p, { waitUntil: 'domcontentloaded', timeout: 15000 });
    // OPEN EVERYTHING BEFORE MEASURING.
    //
    // The third hole, and the one that hid the worst defect: a closed nav
    // panel has zero width and height, so every rule below skipped it - and
    // the panel is on all 243 pages. "The hub" chip and the "Tools &
    // resources" button shipped at 2.06:1 while this sweep reported zero
    // findings, because a reader has to click to see them and this script
    // never did. Anything a reader can open, the audit has to open.
    await page.evaluate(() => {
      document.querySelectorAll('details').forEach(d => d.open = true);
      document.querySelectorAll('[aria-expanded]').forEach(b => b.setAttribute('aria-expanded', 'true'));
      // The nav panel is toggled by a class on the shell, not by [open].
      document.querySelectorAll('.navpanel, .sitenav-in, .sitenav').forEach(n => n.classList.add('open'));
      document.querySelectorAll('.navpanel').forEach(n => {
        n.style.setProperty('display', 'block', 'important');
        n.style.setProperty('visibility', 'visible', 'important');
        n.style.setProperty('opacity', '1', 'important');
        n.style.setProperty('height', 'auto', 'important');
        n.style.setProperty('max-height', 'none', 'important');
        n.style.setProperty('position', 'static', 'important');
      });
    });
    await page.waitForTimeout(60);
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
        // WAS `txt.length < 8`, and that floor hid the worst defect on the
        // site for weeks: "The hub" is seven characters, and the chip it
        // labels shipped at 2.06:1 on 149 pages while this sweep reported
        // zero findings. A number is text. "03" was 1.37:1.
        // Only genuinely empty or punctuation-only nodes are skipped now.
        if (txt.length < 1 || !/[A-Za-z0-9]/.test(txt)) return;
        const r = el.getBoundingClientRect();
        if (r.width < 2 || r.height < 2) return;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.opacity === '0') return;
        // A TRANSLUCENT BACKGROUND IS NOT A MISSING ONE.
        //
        // This used to stop at the first background that was not fully
        // transparent and hand it back as `bg`, and `parse()` then returned
        // null for anything with alpha under 0.9 - so the pair was dropped.
        // Dropped is not passed. `flat_bands.py` deliberately keeps 43
        // translucent fades, so a whole family of pairs was never measured
        // and the sweep reported them as clean by saying nothing.
        //
        // Now every layer is composited over the one behind it, which is
        // what the eye actually receives. A real gradient still cannot be
        // reduced to one colour, so it is reported as UNMEASURED rather than
        // skipped in silence.
        const px = c => { const m = String(c).match(/rgba?\(([^)]+)\)/); if (!m) return null;
          const a = m[1].split(',').map(Number); return [a[0], a[1], a[2], a.length > 3 ? a[3] : 1]; };
        const over = (f, b) => { const a = f[3];
          return [f[0]*a + b[0]*(1-a), f[1]*a + b[1]*(1-a), f[2]*a + b[2]*(1-a), 1]; };
        let e = el, grad = false; const layers = [];
        while (e) {
          const b = getComputedStyle(e);
          if (b.backgroundImage && b.backgroundImage !== 'none'
              && b.backgroundImage.includes('gradient')) { grad = true; break; }
          const c = px(b.backgroundColor);
          if (c && c[3] > 0) { layers.push(c); if (c[3] >= 0.999) break; }
          e = e.parentElement;
        }
        if (grad) { out.push({ unmeasured: 'gradient', cls: (el.className||'').toString().slice(0,40),
          tag: el.tagName.toLowerCase(), t: txt.slice(0, 40) }); return; }
        if (!layers.length || layers[layers.length-1][3] < 0.999) layers.push([255,255,255,1]);
        let bgc = layers[layers.length-1];
        for (let i = layers.length-2; i >= 0; i--) bgc = over(layers[i], bgc);
        let fgc = px(cs.color); if (!fgc) return;
        if (fgc[3] < 1) fgc = over(fgc, bgc);
        const bg = 'rgb(' + bgc.slice(0,3).map(Math.round).join(', ') + ')';
        const fg = 'rgb(' + fgc.slice(0,3).map(Math.round).join(', ') + ')';
        out.push({ fg, bg, composited: layers.some(l => l[3] < 0.999),
          size: parseFloat(cs.fontSize), weight: cs.fontWeight,
          cls: (el.className||'').toString().slice(0,40), tag: el.tagName.toLowerCase(),
          t: txt.slice(0, 40),
          anc: (e && e.className || '').toString().slice(0,30) });
      });
      return out;
    });
    for (const b of nodes) {
      if (b.unmeasured) { unmeasured.push({ page: p, ...b }); continue; }
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

// A pair on a real gradient cannot be reduced to two colours, so it is not
// scored - but it is NOT silence either. Silence is what let 149 pages ship
// a 2.06:1 chip. Anything here has to be read by a human.
writeFileSync('/tmp/contrast-unmeasured.json', JSON.stringify(unmeasured, null, 1));
if (unmeasured.length) {
  const u = {};
  for (const x of unmeasured) { const k = `${x.tag}.${x.cls}`;
    (u[k] = u[k] || { pages: new Set(), ex: x.t }).pages.add(x.page); }
  console.log(`\nUNMEASURED - text over a gradient, ${unmeasured.length} node(s) `
    + `on ${new Set(unmeasured.map(x=>x.page)).size} page(s). Not a pass; check by eye:`);
  for (const [k, v] of Object.entries(u).sort((a,b)=>b[1].pages.size-a[1].pages.size).slice(0,12))
    console.log(`${String(v.pages.size).padStart(4)} pages | ${k}  e.g. "${v.ex}"`);
} else {
  console.log('\nUNMEASURED: none - every text node resolved to two colours.');
}
await browser.close();
