/* Global design audit.
 *
 * Written after too many defects were found one screenshot at a time. Every
 * class of bug below had already shipped at least once on at least one page:
 *
 *   WIDTH      content occupying a fraction of a wide viewport, everything
 *              else empty. Reported from a 27-inch 5K display.
 *   EMPTY      a headline figure rendering as an em-dash. A cold reader sees
 *              a caption for a number that is not there.
 *   INVISIBLE  text whose computed colour matches what is behind it. Shipped
 *              as <b style="color:#fff"> on a white card.
 *   FOLD       the primary CTA below the fold at a real usable height.
 *   OVERSIZE   a CTA taking a whole screen band because it inherited a hero
 *              treatment it was never meant to have.
 *   TAP        interactive targets under 44px (WCAG 2.5.8).
 *   OVERFLOW   horizontal scroll on a phone.
 *   NARROW     a card that is wide but whose CONTENT is not - the inner grid
 *              never followed the container when widen.py grew it.
 *   CHROME     wrong or missing global footer, duplicate nav destinations.
 *
 * Run:  node _dev/audit.mjs [port]
 * It serves nothing - point it at a local static server for this directory.
 */
import { chromium } from '../node_modules/playwright/index.mjs';
import { readdirSync } from 'fs';

const PORT = process.argv[2] || '8140';
const BASE = `http://localhost:${PORT}/`;

const SKIP = new Set(['tycoon.html', 'concepts.html', 'local.html']);
const PUBLIC_DIRS = ['', 'for', 'getting-paid', 'licensure', 'money', 'practice', 'training'];
const PAGES = PUBLIC_DIRS.flatMap(dir => {
  const base = dir || '.';
  return readdirSync(base)
    .filter(f => f.endsWith('.html') && !SKIP.has(f))
    .map(f => dir ? `${dir}/${f}` : f);
}).sort();

/* Real usable heights: browser chrome subtracted, not the raw device size. */
const VIEWS = [
  { name: '5k',      w: 2560, h: 1300 },
  { name: 'laptop',  w: 1440, h: 780  },
  { name: 'tablet',  w: 768,  h: 920  },
  { name: 'phone',   w: 390,  h: 700  },
];

const findings = [];
const add = (page, view, kind, detail) => findings.push({ page, view, kind, detail });

/* --- colour helpers: is this text readable against what is behind it? --- */
const LUM = `(c)=>{const m=c.match(/[\\d.]+/g); if(!m) return null;
  const f=x=>{x/=255; return x<=.03928? x/12.92 : Math.pow((x+.055)/1.055,2.4)};
  if(m.length>3 && parseFloat(m[3])===0) return null;
  return .2126*f(+m[0])+.7152*f(+m[1])+.0722*f(+m[2])}`;

const PROBE = `(()=>{
  const lum = ${LUM};
  const out = {w:innerWidth, h:innerHeight, scrollW:document.documentElement.scrollWidth};

  /* WIDTH: the widest run of laid-out content, as a share of the viewport.
     Measured from leaf elements that actually carry text or a control, so an
     invisible full-width wrapper cannot mask a narrow column. */
  let minL=Infinity, maxR=-Infinity, n=0;
  document.querySelectorAll('main *, body > section *, article *').forEach(el=>{
    if (el.children.length) return;
    const t=(el.textContent||'').trim();
    const tag=el.tagName;
    if (!t && !['INPUT','SELECT','BUTTON','IMG','SVG'].includes(tag)) return;
    const r=el.getBoundingClientRect();
    if (r.width<8 || r.height<6) return;
    if (r.top>4000) return;                     /* first few screens only */
    const cs=getComputedStyle(el);
    if (cs.visibility==='hidden'||cs.display==='none') return;
    minL=Math.min(minL,r.left); maxR=Math.max(maxR,r.right); n++;
  });
  out.contentSpan = n ? Math.round(maxR-minL) : 0;
  out.contentPct  = n ? Math.round((maxR-minL)/innerWidth*100) : 0;

  /* EMPTY: a big display figure whose whole text is a dash. */
  out.empties=[];
  document.querySelectorAll('b,strong,span,div,p').forEach(el=>{
    if (el.children.length) return;
    const t=(el.textContent||'').trim();
    if (!/^[\\u2014\\u2013-]$/.test(t)) return;
    const r=el.getBoundingClientRect();
    if (r.top>1600 || r.width<6) return;
    const fs=parseFloat(getComputedStyle(el).fontSize);
    /* 24px, not 18px. At 18 this also caught form-summary rows that legitimately
       read "-" while the reader is still filling the form in - those are mid-page
       and small, and a dash there is honest. What is not acceptable is a HEADLINE
       figure with a caption under it and nothing above the caption. */
    if (fs<24) return;
    out.empties.push({fs:Math.round(fs), top:Math.round(r.top),
      near:(el.parentElement&&el.parentElement.textContent||'').trim().slice(0,52)});
  });

  /* INVISIBLE: computed colour indistinguishable from the nearest painted
     background behind it. */
  out.invisible=[];
  /* Walk up for the nearest PAINTED background. Critically, an ancestor with a
     background-IMAGE (every hero here is a linear-gradient over a transparent
     background-color) stops the walk and returns null: we cannot sample a
     gradient from computed style, and pretending it is not there produced 40+
     false "white text on paper" findings on the first run. */
  const bgOf=el=>{let p=el; while(p){const cs=getComputedStyle(p);
    if (cs.backgroundImage && cs.backgroundImage!=='none') return null;
    const l=lum(cs.backgroundColor); if(l!==null) return {c:cs.backgroundColor,l};
    p=p.parentElement;} return null;};
  [...document.querySelectorAll('b,strong,em,span,a,p,h1,h2,h3,li,td')].slice(0,1200).forEach(el=>{
    if (el.children.length) return;
    const t=(el.textContent||'').trim(); if (t.length<2) return;
    const r=el.getBoundingClientRect(); if (r.width<4||r.height<4||r.top>6000) return;
    const cs=getComputedStyle(el);
    if (cs.visibility==='hidden'||cs.opacity==='0') return;
    const fl=lum(cs.color); const bg=bgOf(el); if (fl===null||!bg) return;
    const ratio=(Math.max(fl,bg.l)+.05)/(Math.min(fl,bg.l)+.05);
    if (ratio < 1.6) out.invisible.push({ratio:Math.round(ratio*100)/100,
      color:cs.color, bg:bg.c, text:t.slice(0,46), top:Math.round(r.top)});
  });

  /* OVERSIZE: a link or button whose own type is heading-scale. A CTA is a
     control, not a headline; past ~30px it is wearing a hero's clothes. */
  out.oversize=[];
  [...document.querySelectorAll('a,button')].slice(0,400).forEach(el=>{
    const r=el.getBoundingClientRect(); if (r.width<40||r.top>8000) return;
    /* Only things that READ as buttons. A link-wrapped card legitimately has a
       21px heading in it; that is a card, not an oversized CTA. A button is a
       control with a painted fill of its own. */
    const bgc=getComputedStyle(el).backgroundColor;
    const painted = lum(bgc)!==null && !/rgba\(0, 0, 0, 0\)/.test(bgc);
    if (!painted) return;
    let big=0;
    el.querySelectorAll('*').forEach(k=>{const f=parseFloat(getComputedStyle(k).fontSize);
      if(f>big) big=f;});
    const own=parseFloat(getComputedStyle(el).fontSize);
    big=Math.max(big,own);
    if (big>=30 || r.height>=150) out.oversize.push({fs:Math.round(big),
      h:Math.round(r.height), wpct:Math.round(r.width/innerWidth*100),
      text:(el.textContent||'').trim().slice(0,42), top:Math.round(r.top)});
  });

  /* FOLD: the first primary-looking CTA in the first screen's worth of page. */
  const cta=[...document.querySelectorAll('a,button')].find(el=>{
    const r=el.getBoundingClientRect();
    if (r.top<0||r.top>1200||r.height<36) return false;
    const cs=getComputedStyle(el);
    const l=lum(cs.backgroundColor);
    return l!==null;                            /* has a painted background */
  });
  out.cta = cta ? {bottom:Math.round(cta.getBoundingClientRect().bottom),
                   text:(cta.textContent||'').trim().slice(0,40)} : null;

  /* TAP: interactive boxes under 44px. Inline prose links are exempt
     (WCAG 2.5.8), so anything inside a paragraph is skipped. */
  out.tap=[];
  document.querySelectorAll('a,button,select,input').forEach(el=>{
    if (el.closest('p,li,td,.pay-note,.jobfoot,.cite,.disc,footer')) return;
    const r=el.getBoundingClientRect();
    if (r.width<2||r.height<2||r.top>8000) return;
    if (r.height<44) out.tap.push({h:Math.round(r.height),
      text:(el.textContent||el.getAttribute('aria-label')||'').trim().slice(0,34)});
  });

  /* NARROW: a card whose own children use far less than its width. This is a
     DIFFERENT bug from WIDTH above: the container is wide, the content inside
     it is not, so the card reads as half empty. It appeared the moment
     widen.py grew the containers without the inner grids following - 17
     instances across the site, worst at 32%. */
  out.narrow=[];
  [...document.querySelectorAll('section,.slab,.job,.card,article,.band,.sec,.lgsec')]
    .slice(0,60).forEach(el=>{
      const r=el.getBoundingClientRect();
      if (r.width<700||r.height<120) return;
      let L=Infinity,R=-Infinity,n=0;
      el.querySelectorAll('*').forEach(k=>{
        if (k.children.length) return;
        const t=(k.textContent||'').trim();
        if (!t && !['INPUT','SELECT','BUTTON','IMG','SVG'].includes(k.tagName)) return;
        const q=k.getBoundingClientRect();
        if (q.width<6||q.height<6) return;
        const cs=getComputedStyle(k);
        if (cs.display==='none'||cs.visibility==='hidden') return;
        L=Math.min(L,q.left); R=Math.max(R,q.right); n++;});
      if (!n) return;
      const use=Math.round((R-L)/r.width*100);
      if (use<62) out.narrow.push({cls:(el.className||el.tagName).toString().slice(0,24),
        w:Math.round(r.width), used:Math.round(R-L), pct:use});
    });

  /* CHROME */
  out.footers = document.querySelectorAll('footer').length;
  out.prototypeFooter = /Prototype, not the live site/.test(document.body.innerText);
  const dests={};
  document.querySelectorAll('nav a[href], header a[href]').forEach(a=>{
    const h=(a.getAttribute('href')||'').split('#')[0];
    if(!h||h.startsWith('http')||h.startsWith('mailto')) return;
    (dests[h]=dests[h]||[]).push((a.textContent||'').trim().split('\\n')[0].slice(0,34));
  });
  out.dupNav = Object.entries(dests)
    .filter(([h,ls])=>new Set(ls).size>1)
    .map(([h,ls])=>({href:h, labels:[...new Set(ls)]}));
  return out;
})()`;

/* One viewport per invocation, and a fresh browser every few pages. Running all
   three viewports across seventeen JS-heavy pages in a single browser exhausted
   it mid-run: newPage() started failing with "browser has been closed". */
const ONLY = process.argv[3];
const RUN = ONLY ? VIEWS.filter(v => v.name === ONLY) : VIEWS;
let b = await chromium.launch();
let since = 0;
for (const page of PAGES) {
  if (since >= 4) { await b.close(); b = await chromium.launch(); since = 0; }
  since++;
  for (const v of RUN) {
    const p = await b.newPage({ viewport: { width: v.w, height: v.h } });
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    try {
      await p.goto(BASE + page, { waitUntil: 'load', timeout: 20000 });
    } catch (e) { add(page, v.name, 'LOAD', e.message.slice(0, 60)); await p.close(); continue; }
    await p.waitForTimeout(300);
    /* One page with a few thousand nodes made the contrast walk take minutes and
       the whole run looked like a hang. Budget it, and report the timeout as a
       finding rather than silently dropping the page. */
    let r;
    try {
      r = await Promise.race([
        p.evaluate(PROBE),
        new Promise((_, rej) => setTimeout(() => rej(new Error('probe exceeded 15s')), 15000)),
      ]);
    } catch (e) { add(page, v.name, 'SLOW', e.message); await p.close(); continue; }

    if (v.name !== 'phone' && r.contentPct && r.contentPct < 62)
      add(page, v.name, 'WIDTH', `content spans ${r.contentSpan}px of ${r.w}px (${r.contentPct}%)`);
    r.empties.forEach(e =>
      add(page, v.name, 'EMPTY', `${e.fs}px figure is just a dash, near "${e.near}"`));
    /* one line per distinct colour pair, not one per word */
    const seen = new Set();
    r.invisible.forEach(i => {
      const k = i.color + '|' + i.bg;
      if (seen.has(k)) return; seen.add(k);
      add(page, v.name, 'INVISIBLE', `contrast ${i.ratio}:1 — ${i.color} on ${i.bg} — "${i.text}"`);
    });
    r.oversize.forEach(o =>
      add(page, v.name, 'OVERSIZE', `CTA ${o.fs}px type, ${o.h}px tall, ${o.wpct}% wide — "${o.text}"`));
    if (r.cta && r.cta.bottom > v.h)
      add(page, v.name, 'FOLD', `primary CTA ${r.cta.bottom - v.h}px below the fold — "${r.cta.text}"`);
    /* only on the wide viewports - at phone width a single column IS correct */
    if (v.name !== 'phone')
      [...new Map(r.narrow.map(x => [x.cls, x])).values()].slice(0, 3).forEach(x =>
        add(page, v.name, 'NARROW',
            `${x.cls} is ${x.w}px wide, content uses ${x.used}px (${x.pct}%)`));
    if (r.scrollW > r.w + 1)
      add(page, v.name, 'OVERFLOW', `${r.scrollW - r.w}px of horizontal scroll`);
    if (v.name === 'phone')
      [...new Map(r.tap.map(t => [t.text, t])).values()].slice(0, 4).forEach(t =>
        add(page, v.name, 'TAP', `${t.h}px target — "${t.text}"`));
    if (v.name === 'laptop') {
      if (r.footers !== 1) add(page, v.name, 'CHROME', `${r.footers} <footer> elements`);
      if (r.prototypeFooter) add(page, v.name, 'CHROME', 'carries the PROTOTYPE footer');
      r.dupNav.forEach(d =>
        add(page, v.name, 'CHROME', `nav points at ${d.href} twice: ${d.labels.join(' / ')}`));
    }
    errs.forEach(e => add(page, v.name, 'JSERROR', e.slice(0, 70)));
    await p.close();
  }
}
await b.close();

const ORDER = ['LOAD', 'JSERROR', 'INVISIBLE', 'EMPTY', 'CHROME', 'FOLD', 'OVERFLOW',
               'OVERSIZE', 'WIDTH', 'NARROW', 'TAP'];
findings.sort((a, c) => ORDER.indexOf(a.kind) - ORDER.indexOf(c.kind) ||
                        a.page.localeCompare(c.page));
let last = '';
for (const f of findings) {
  if (f.kind !== last) { console.log(`\n=== ${f.kind} ===`); last = f.kind; }
  console.log(`  ${f.page.padEnd(44)} ${f.view.padEnd(7)} ${f.detail}`);
}
console.log(`\n${findings.length} findings across ${PAGES.length} pages × ${RUN.length} viewport(s)`);
