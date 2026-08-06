/* _dev/deviceaudit.mjs — the whole site, at the sizes people actually use.
 *
 * Viewports are real device CSS sizes, not round numbers:
 *   2560x1440  27" 5K iMac / Studio Display (5120x2880 at 2x)
 *   1512x982   MacBook Pro 14"
 *   1440x900   MacBook Air 13"
 *   1024x1366  iPad Pro 12.9" portrait
 *    820x1180  iPad Air portrait
 *   1180x820   iPad Air landscape
 *    430x932   iPhone 15 Pro Max
 *    390x844   iPhone 15 / 14 / 13
 *    375x667   iPhone SE - the smallest still in real use
 */
import { chromium } from '/home/claude/.npm-global/lib/node_modules/playwright/index.mjs';
import { readdirSync, readFileSync, existsSync } from 'fs';
import { createServer } from 'http';
import { extname, join } from 'path';

/* Serve the directory and NAVIGATE, rather than page.setContent().
   setContent leaves the document on about:blank, so any page calling
   history.replaceState throws a SecurityError that has nothing to do with the
   page - working-remotely reported one at all nine viewports and it vanished
   the moment it was served over http. An audit whose own method invents nine
   HIGH findings is worse than no audit. */
const MIME = { '.html':'text/html', '.css':'text/css', '.js':'text/javascript',
               '.png':'image/png', '.svg':'image/svg+xml', '.xml':'application/xml' };

const DIR = process.argv[2] || 'finallive';
const ONLY = process.argv[3] || null;
const SKIP = new Set(['tycoon.html', 'concepts.html']);
const isRedirect = f => /<meta[^>]+http-equiv=["']?refresh/i
  .test(readFileSync(`${DIR}/${f}`, 'utf8').slice(0, 4000));

const VIEWS = [
  ['27" 5K iMac',     2560, 1440, false],
  ['MacBook Pro 14',  1512,  982, false],
  ['MacBook Air 13',  1440,  900, false],
  ['iPad Pro port',   1024, 1366, true],
  ['iPad Air port',    820, 1180, true],
  ['iPad Air land',   1180,  820, true],
  ['iPhone Pro Max',   430,  932, true],
  ['iPhone 15',        390,  844, true],
  ['iPhone SE',        375,  667, true],
];

const files = readdirSync(DIR)
  .filter(f => f.endsWith('.html') && !SKIP.has(f) && !isRedirect(f))
  .filter(f => !ONLY || f === ONLY);

const server = createServer((req, res) => {
  const f = decodeURIComponent(req.url.split('?')[0]).replace(/^\//, '') || 'index.html';
  const path = join(DIR, f);
  if (!existsSync(path)) { res.writeHead(404); return res.end('nope'); }
  res.writeHead(200, { 'Content-Type': MIME[extname(path)] || 'text/plain' });
  res.end(readFileSync(path));
});
await new Promise(r => server.listen(0, r));
const ORIGIN = 'http://127.0.0.1:' + server.address().port;

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

const findings = [];
const add = (sev, kind, page, view, detail) =>
  findings.push({ sev, kind, page, view, detail });

for (const f of files) {
  const html = readFileSync(`${DIR}/${f}`, 'utf8');

  for (const [vname, w, h, touch] of VIEWS) {
    const ctx = await browser.newContext({
      viewport: { width: w, height: h }, hasTouch: touch,
      isMobile: touch && w < 500 });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push(String(e).slice(0, 120)));
    await p.route('**/*', r => {
      const u = r.request().url();
      return (u.startsWith(ORIGIN) || u.startsWith('data:') || u.startsWith('about:'))
        ? r.continue() : r.abort();
    });
    await p.goto(`${ORIGIN}/${f}`, { waitUntil: 'domcontentloaded' });
    await p.waitForTimeout(touch ? 260 : 200);

    const r = await p.evaluate(([vw, isTouch]) => {
      const out = { over: [], tiny: [], smallTap: [], overlap: [], width: null,
                    dupIds: [], noAlt: 0, scroll: 0 };

      /* horizontal overflow, ignoring real scroll containers */
      document.querySelectorAll('*').forEach(el => {
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') return;
        const q = el.getBoundingClientRect();
        if (!(q.width > 0)) return;
        if (q.right > vw + 1 && q.left < vw) {
          let scrolls = false;
          for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
            const ox = getComputedStyle(a).overflowX;
            if (ox === 'auto' || ox === 'scroll') { scrolls = true; break; }
          }
          if (!scrolls) out.over.push((el.className || el.tagName).toString().slice(0, 40)
            + ' right=' + Math.round(q.right));
        }
      });
      out.over = [...new Set(out.over)].slice(0, 4);
      out.scroll = Math.max(0, document.documentElement.scrollWidth - vw);

      /* how much of the window the content actually uses */
      const main = document.querySelector('main,.pw,.in,.wrap,.clwrap') || document.body;
      const mw = main.getBoundingClientRect().width;
      out.width = Math.round(mw / vw * 100);

      /* text too small to read */
      document.querySelectorAll('p,li,td,th,span,i,em,b,a,label,div').forEach(el => {
        if (el.children.length) return;
        const t = (el.textContent || '').trim();
        if (t.length < 12) return;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') return;
        /* 10px is the floor, not 11.5. The site uses 10-11px deliberately for
           secondary description under a bold label and for tracked uppercase
           micro-labels, and both read fine at every size tested. Flagging them
           produced 135 findings that all resolved to "yes, on purpose", which
           is how an audit stops being read. Below 10px is a different claim. */
        const px = parseFloat(cs.fontSize);
        if (px && px < 10) out.tiny.push(Math.round(px * 10) / 10 + 'px "'
          + t.slice(0, 34) + '"');
      });
      out.tiny = [...new Set(out.tiny)].slice(0, 4);

      /* tap targets, on touch viewports only */
      if (isTouch) {
        document.querySelectorAll('a,button,input,select,textarea,[role=button]').forEach(el => {
          const cs = getComputedStyle(el);
          if (cs.display === 'none' || cs.visibility === 'hidden') return;
          const q = el.getBoundingClientRect();
          if (!(q.width > 0 && q.height > 0)) return;
          if (q.top > 6000) return;                 /* far below the fold, cheap to skip */

          /* A LINK INSIDE A SENTENCE IS NOT A BUTTON. Citation links, "see the
             Terms of Use", "Read Field Notes ->" - these sit inline in prose and
             cannot be given height without wrecking the line box they live in.
             Every typographic convention allows this and every real page does
             it. Flagging them buried the two findings that mattered. */
          const par = el.parentElement;
          const inProse = par && /^(P|LI|TD|SPAN|I|EM|SMALL|BLOCKQUOTE)$/.test(par.tagName)
            && cs.display.startsWith('inline');
          if (inProse) return;

          /* Nor is a control whose LABEL is the real target. The consent
             checkbox is 22x22 inside a 354x37 <label>, so the tappable thing is
             the row, not the box. Measure what the finger actually hits. */
          const lab = el.closest('label');
          if (lab && lab !== el) {
            const lq = lab.getBoundingClientRect();
            if (lq.height >= 30 && lq.width >= 30) return;
          }

          /* A WIDE, SHORT target is not a small target. The masthead logo is
             226x26 - trivially hittable, and making it taller would mean
             padding the site header on every page to fix a number. Require one
             dimension to be genuinely small before calling it a problem. */
          const bigEnough = (q.width >= 120 && q.height >= 24)
                         || (q.height >= 120 && q.width >= 24);
          if (bigEnough) return;

          if (q.height < 30 || q.width < 30) {
            const lbl = (el.textContent || el.getAttribute('aria-label') || el.tagName)
              .trim().slice(0, 30);
            out.smallTap.push(Math.round(q.width) + 'x' + Math.round(q.height) + ' "' + lbl + '"');
          }
        });
        out.smallTap = [...new Set(out.smallTap)].slice(0, 5);
      }

      /* duplicate ids break anchors and labels */
      const seen = {}, dup = new Set();
      document.querySelectorAll('[id]').forEach(el => {
        if (seen[el.id]) dup.add(el.id); seen[el.id] = 1; });
      out.dupIds = [...dup].slice(0, 5);

      out.noAlt = [...document.querySelectorAll('img')]
        .filter(i => i.getAttribute('alt') === null).length;
      return out;
    }, [w, touch]);

    const V = `${vname} ${w}x${h}`;
    if (r.over.length) add('HIGH', 'overflow', f, V, r.over.join(' · '));
    if (r.scroll > 1) add('HIGH', 'h-scroll', f, V, r.scroll + 'px of sideways scroll');
    if (r.tiny.length) add('MED', 'tiny-text', f, V, r.tiny.join(' · '));
    if (r.smallTap.length) add('MED', 'tap-target', f, V, r.smallTap.join(' · '));
    if (r.dupIds.length) add('MED', 'duplicate-id', f, V, r.dupIds.join(', '));
    if (r.noAlt) add('LOW', 'img-no-alt', f, V, r.noAlt + ' images');
    if (errs.length) add('HIGH', 'js-error', f, V, errs[0]);
    if (w >= 1440 && r.width !== null && r.width < 55)
      add('LOW', 'narrow-content', f, V, r.width + '% of window used');

    await ctx.close();
  }
}

/* ---- internal links, once, statically */
const pages = new Set(readdirSync(DIR).filter(x => x.endsWith('.html')));
for (const f of files) {
  const raw = readFileSync(`${DIR}/${f}`, 'utf8');
  /* Strip scripts first. These pages BUILD markup in JS, so a naive sweep finds
     href="' + taxHref() + '" and reports a dead link that does not exist. Five
     of those were the audit's first HIGH findings, and all five were fiction. */
  const s = raw.replace(/<script[\s\S]*?<\/script>/gi, '');
  const hrefs = [...s.matchAll(/href="([^"]+)"/g)].map(m => m[1]);
  for (const hd of new Set(hrefs)) {
    if (/^(https?:|mailto:|tel:|#|data:)/.test(hd)) continue;
    const file = hd.split('#')[0];
    if (!file) continue;
    if (!pages.has(file) && !existsSync(`${DIR}/${file}`))
      add('HIGH', 'dead-link', f, 'static', hd);
  }
  /* in-page anchors */
  for (const hd of new Set(hrefs.filter(x => x.startsWith('#') && x.length > 1))) {
    const id = hd.slice(1);
    if (!raw.includes('id="' + id + '"') && !raw.includes("id='" + id + "'"))
      add('MED', 'dead-anchor', f, 'static', hd);
  }
}

await browser.close();
server.close();

const order = { HIGH: 0, MED: 1, LOW: 2 };
findings.sort((a, b) => order[a.sev] - order[b.sev] || a.kind.localeCompare(b.kind));
const byKind = {};
for (const x of findings) (byKind[x.sev + ' ' + x.kind] ??= []).push(x);

console.log(`${files.length} pages x ${VIEWS.length} viewports\n`);
for (const [k, list] of Object.entries(byKind)) {
  console.log(`${k}  (${list.length})`);
  const shown = list.slice(0, 8);
  for (const x of shown) console.log(`   ${x.page}  [${x.view}]  ${x.detail}`);
  if (list.length > shown.length) console.log(`   … and ${list.length - shown.length} more`);
  console.log();
}
console.log('================================================');
const h = findings.filter(x => x.sev === 'HIGH').length;
const m = findings.filter(x => x.sev === 'MED').length;
const l = findings.filter(x => x.sev === 'LOW').length;
console.log(`${h} HIGH · ${m} MED · ${l} LOW`);
process.exit(h ? 1 : 0);
