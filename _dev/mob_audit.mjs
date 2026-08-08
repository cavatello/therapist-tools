// What a 390px phone sees, checked the way the desktop sweep could not.
//
// The contrast sweep runs at 1440 and is blind to everything that only exists
// at phone widths: a row that fits on a laptop and slices in half on a phone, a
// table that widens the document so the whole page slides sideways, a tap
// target the size of a full stop. "Seems broke iPhone" was reported once and
// fixed once, for the masthead. Nothing has ever checked the other 130 pages.
//
// Five things, in one pass, at 390x844 with touch and deviceScaleFactor 2:
//
//  1. DOCUMENT OVERFLOW - scrollWidth beyond clientWidth. The page slides.
//  2. THE CULPRIT - which element is actually wider than the viewport, walked
//     down from <body> so the report names the offender rather than the symptom.
//     Deliberate horizontal scrollers (overflow-x:auto/scroll) are NOT overflow;
//     an earlier audit reported six of those as failures and was wrong.
//  3. TAP TARGETS under 24x24 CSS px - the WCAG 2.2 AA minimum (2.5.8). Only
//     for things you are meant to hit: links, buttons, inputs, summaries. Inline
//     links inside a paragraph are exempt, because the spec exempts them and
//     because "make body copy links 24px tall" is not advice anyone should take.
//  4. TEXT UNDER 12px that is not a label. On a phone this is the difference
//     between small and unreadable.
//  5. FIXED/STICKY furniture taller than a third of the viewport - the failure
//     where a sticky masthead eats the screen and the content reads through a
//     letterbox.
//
// No contrast here: px_audit.mjs already does that properly, and running two
// screenshot-per-element passes over 131 pages twice is an hour of nothing new.
import pw from '/opt/node-tools/node_modules/playwright/index.js';

const BASE = process.env.BASE || 'http://127.0.0.1:8950/';
const urls = (process.env.URLS || '').split(',').filter(Boolean);
const W = 390, H = 844;

const b = await pw.chromium.launch();
const ctx = await b.newContext({
  viewport: { width: W, height: H }, deviceScaleFactor: 2,
  isMobile: true, hasTouch: true,
});
const out = [];

for (const u of urls) {
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(String(e).slice(0, 90)));
  try {
    await p.goto(BASE + u, { waitUntil: 'load', timeout: 25000 });
  } catch (e) { out.push({ u, err: String(e).slice(0, 60) }); await p.close(); continue; }
  await p.waitForTimeout(450);

  let r;
  try {
    r = await p.evaluate(({ W, H }) => {
      const de = document.documentElement;
      const vw = de.clientWidth;
      const res = { over: de.scrollWidth - vw, wide: [], tap: [], tiny: [], furniture: [] };

      // 2. Walk down for the actual offender. A node whose own box exceeds the
      //    viewport, whose parent does not scroll horizontally on purpose.
      const scrolls = e => {
        const c = getComputedStyle(e);
        return /auto|scroll/.test(c.overflowX);
      };
      if (res.over > 1) {
        const seen = new Set();
        const walk = n => {
          for (const e of n.children) {
            const cs = getComputedStyle(e);
            if (cs.display === 'none' || cs.visibility === 'hidden') continue;
            const rc = e.getBoundingClientRect();
            const right = rc.left + rc.width;
            if (right > vw + 1 || rc.left < -1) {
              // If an ancestor is a deliberate scroller, this is fine.
              let a = e.parentElement, inScroller = false;
              while (a && a !== de) { if (scrolls(a)) { inScroller = true; break; } a = a.parentElement; }
              if (!inScroller && !scrolls(e)) {
                const k = (e.tagName + '.' + String(e.className).split(' ')[0]).slice(0, 34);
                if (!seen.has(k) && res.wide.length < 6) {
                  seen.add(k);
                  res.wide.push(k + ' @' + Math.round(right) + 'px w' + Math.round(rc.width));
                }
                walk(e);            // go deeper: the child is usually the cause
                continue;
              }
            }
            if (e.children.length) walk(e);
          }
        };
        walk(document.body);
      }

      // 3. Tap targets. Inline links inside running text are exempt (WCAG 2.5.8).
      // WCAG 2.5.8's exception is not "is it inside a <p>". It is: the target
      // sits in a sentence, so its size is set by the line-height of the text
      // around it. A first version tested `closest('p,li,td,...')`, which let
      // a link inside a <b> full of prose through as a failure and would have
      // exempted a link that is the sole content of a <li>. The honest test is
      // whether there is more text around it than in it.
      const inlineInProse = e => {
        if (e.tagName !== 'A') return false;
        if (!getComputedStyle(e).display.startsWith('inline')) return false;
        const mine = e.textContent.trim().length;
        const par = e.parentElement;
        if (!par) return false;
        return par.textContent.trim().length >= mine * 1.5 + 10;
      };
      const seenTap = new Set();
      for (const e of document.querySelectorAll('a[href],button,summary,input,select,label[for]')) {
        const cs = getComputedStyle(e);
        if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
        const rc = e.getBoundingClientRect();
        if (rc.width < 2 || rc.height < 2) continue;      // hidden or offscreen
        if (inlineInProse(e)) continue;
        if (rc.height >= 24 && rc.width >= 24) continue;
        const k = (e.tagName + '.' + String(e.className).split(' ')[0]).slice(0, 26)
          + ':' + Math.round(rc.width) + 'x' + Math.round(rc.height);
        if (seenTap.has(k)) continue;
        seenTap.add(k);
        if (res.tap.length < 6) res.tap.push(k + ' "' + e.textContent.trim().slice(0, 18) + '"');
      }

      // 4. Text under 12px that carries a sentence rather than a label.
      const seenTiny = new Set();
      for (const e of document.querySelectorAll('p,li,dd,span,i,em,td,figcaption')) {
        const t = e.textContent.trim();
        if (!t || e.children.length || t.length < 25) continue;   // labels are short
        const cs = getComputedStyle(e);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        const rc = e.getBoundingClientRect();
        if (rc.width < 3 || rc.height < 3) continue;
        const fs = parseFloat(cs.fontSize);
        if (fs >= 12) continue;
        const k = (String(e.className) || e.tagName).split(' ')[0].slice(0, 22) + ':' + fs.toFixed(1);
        if (seenTiny.has(k)) continue;
        seenTiny.add(k);
        if (res.tiny.length < 5) res.tiny.push(k + ' "' + t.slice(0, 26) + '"');
      }

      // 5. Sticky/fixed chrome eating the screen.
      for (const e of document.querySelectorAll('header,nav,div,aside,section')) {
        const cs = getComputedStyle(e);
        if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
        const rc = e.getBoundingClientRect();
        if (rc.height > H / 3 && rc.width > vw * 0.6) {
          const k = (e.tagName + '.' + String(e.className).split(' ')[0]).slice(0, 30);
          if (res.furniture.length < 3) res.furniture.push(k + ' h' + Math.round(rc.height));
        }
      }
      return res;
    }, { W, H });
  } catch (e) { r = { evalErr: String(e).slice(0, 60) }; }

  if (errs.length) r.js = errs[0];
  const bad = (r.over > 1) || (r.wide && r.wide.length) || (r.tap && r.tap.length)
    || (r.tiny && r.tiny.length) || (r.furniture && r.furniture.length) || r.js || r.evalErr;
  if (bad) out.push({ u, ...r });
  await p.close();
}
await b.close();
console.log(JSON.stringify(out, null, 1));
