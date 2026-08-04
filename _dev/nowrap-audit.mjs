/* _dev/nowrap-audit.mjs — catch the cost-of-living hero bug everywhere else.
 *
 * The bug (queue items 5 and 6, claude/cola-hero-overflow.md): a stat block
 * styled its figures with a BARE DESCENDANT selector — `.clbig b` — which also
 * matched a <b> inside a prose paragraph in the same block. That sentence
 * inherited `white-space:nowrap` at 22px and rendered 406px wide inside a 390px
 * viewport. Nothing errored. No test caught it. It is a naming accident, and
 * the same shape exists wherever a figure block also contains prose.
 *
 * Rather than grep for selector names, detect the CONDITION at runtime:
 *   an element with white-space:nowrap, holding more than a few words,
 *   whose box is wider than the space it has to live in.
 * That catches it whatever the class is called, including in pages nobody has
 * thought about yet.
 *
 * Usage:  node _dev/nowrap-audit.mjs [width]      (default 390)
 */
import { chromium } from '/home/claude/.npm-global/lib/node_modules/playwright/index.mjs';
import { readdirSync, readFileSync } from 'fs';

const DIR = process.argv[3] || '/mnt/user-data/uploads/therapy-practice-site';
const W = +(process.argv[2] || 390);
const SKIP = new Set(['tycoon.html', 'concepts.html']);   // not ours / not published nav

const files = readdirSync(DIR).filter(f => f.endsWith('.html') && !SKIP.has(f));
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

let totalFind = 0, totalOver = 0;
for (const f of files) {
  const ctx = await b.newContext({ viewport: { width: W, height: 900 } });
  const p = await ctx.newPage();
  await p.route('**/*', r => {
    const u = r.request().url();
    return (u.startsWith('data:') || u.startsWith('about:')) ? r.continue() : r.abort();
  });
  await p.setContent(readFileSync(`${DIR}/${f}`, 'utf8'), { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(120);

  const r = await p.evaluate(vw => {
    const out = { nowrap: [], over: [] };
    document.querySelectorAll('*').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      const q = el.getBoundingClientRect();
      if (!(q.width > 0)) return;

      /* the bug shape: nowrap on something that is a SENTENCE, not a figure */
      if (cs.whiteSpace === 'nowrap' || cs.whiteSpace === 'pre') {
        const t = (el.textContent || '').trim();
        const words = t.split(/\s+/).length;
        /* Only a problem when it does not FIT: a nowrap CTA or an SVG label is
           deliberate and harmless, and an audit that reports healthy pages gets
           muted, and a muted audit catches nothing.
           Compare against the VIEWPORT, not the parent. A nowrap sentence
           stretches its own parent, so the parent always "fits" it — measuring
           against the parent made this check silently toothless on the very bug
           it was written for. The viewport is the thing that cannot stretch. */
        if (words >= 5 && el.children.length === 0) {
          const avail = vw;
          if (q.width > avail + 0.5)
            out.nowrap.push({ tag: el.tagName, cls: el.className || '',
                              words, chars: t.length, w: Math.round(q.width),
                              avail: Math.round(avail), text: t.slice(0, 58) });
        }
      }
      /* and anything actually past the viewport — EXCEPT where an ancestor is
         a real horizontal scroll container. A wide table inside overflow-x:auto
         is a design decision, not a bug, and an audit that cannot tell the
         difference cries wolf on every data table and stops being read. The
         handoff already flags this: skip elements whose ancestors legitimately
         scroll. Checked on COMPUTED style, not class name — rates.html uses
         .ledger-wrap and the tax page uses .tw, and one of those rules is
         scoped so it does not always apply. */
      if (q.right > vw + 0.5 && q.left < vw) {
        let scrolls = false;
        for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
          const ox = getComputedStyle(a).overflowX;
          if (ox === 'auto' || ox === 'scroll') { scrolls = true; break; }
        }
        if (!scrolls)
          out.over.push({ tag: el.tagName, cls: el.className || '',
                          x: Math.round(q.left), w: Math.round(q.width),
                          right: Math.round(q.right) });
      }
    });
    /* keep only the outermost overflowing element of each chain */
    out.over = out.over.filter((o, i, a) =>
      !a.some((p2, j) => j !== i && p2.right >= o.right && p2.w > o.w));
    return out;
  }, W);

  const nf = r.nowrap.length, no = r.over.length;
  totalFind += nf; totalOver += no;
  if (nf || no) {
    console.log(`\n${f}`);
    r.nowrap.slice(0, 5).forEach(x => console.log(
      `  NOWRAP SENTENCE  <${x.tag.toLowerCase()} class="${x.cls}">  ${x.words} words, ${x.w}px vs ${x.avail}px viewport  “${x.text}…”`));
    r.over.slice(0, 5).forEach(x => console.log(
      `  OVERFLOWS ${W}px   <${x.tag.toLowerCase()} class="${x.cls}">  x=${x.x} w=${x.w} right=${x.right}`));
  }
  await ctx.close();
}
await b.close();
console.log(`\n================================================`);
console.log(`${files.length} pages at ${W}px`);
console.log(`  nowrap sentences (the cola bug shape): ${totalFind}`);
console.log(`  elements past the viewport:            ${totalOver}`);
process.exit(totalFind || totalOver ? 1 : 0);
