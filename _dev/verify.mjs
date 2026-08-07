// Render the new and changed pages in a real browser and check the things a
// static check cannot see.
//
// WHY THIS EXISTS. This project has twice shipped a change that parsed
// perfectly and rendered nothing - a syntactically valid edit that left a whole
// widget absent from the DOM with no console error. `node --check` passing and
// a builder's guards passing both mean "the file is well formed", never "the
// element is on the page". So every claim below is asserted against a rendered
// DOM, and the video facade is actually clicked.
//
// The overflow check deliberately excludes scrollable ancestors. Two things on
// this site legitimately extend past the viewport - the table wrappers and the
// nav chip strips - and an overflow check that does not know that reports a
// bug on every page, every time, until people stop reading it.
// Playwright lives in the image's shared tool directory, not in a local
// node_modules, and it is CommonJS - so a named ESM import of `chromium`
// fails. Take the default export and destructure it.
import pw from '/opt/node-tools/node_modules/playwright/index.js';
const { chromium } = pw;
import { readdirSync } from 'fs';

const ROOT = 'file:///home/claude/stage2/';
const VIEWS = [
  { name: 'desktop', width: 1280, height: 900 },
  { name: 'phone', width: 390, height: 844 },
];

const all = readdirSync('/home/claude/stage2').filter(f => f.endsWith('.html'));
const psy = all.filter(f => f.startsWith('psychedelic-'));
const schools = all.filter(f => f.endsWith('-mft.html'));

// A sample, not the whole site: enough to cover every template, plus every
// page whose template changed in this pass.
const PAGES = [
  ['resources.html', {
    calcs: '.lc', topics: '.tcard', changes: '.chg li', stage: '.rc',
    reflist: '.reffold', questions: '.lr',
  }],
  ['questions.html', { rows: '.lr', groups: 'section.sec' }],
  ['calculators.html', { cards: '.lc' }],
  ['changes.html', { log: '.chglog li' }],
  ['money/index.html', { cards: '.lc', intro: '.intro p', others: '.xt' }],
  ['licensure/index.html', { cards: '.lc', others: '.xt' }],
  ['simplepractice-california-therapists.html', {
    tiers: '.tier', alts: '.alt', crit: '.cr', tag: '.afl',
    whoNot: '#who-should-not', cal: '.q',
  }],
  ['affiliate-disclosure.html', { partners: '.pcard', tag: '.afl', rule: '.rule' }],
  ['solo-401k-sep-simple-california-therapist.html', {
    tables: '.arttbl, table', sources: '.artsrc li', uplink: '.uplink a.uc',
  }],
  ['hiring-first-associate-california-therapist.html', {
    sources: '.artsrc li', uplink: '.uplink a.uc',
  }],
  ['bbs-fees-california-2026.html', { uplink: '.uplink a.uc' }],
  ['become-an-mft-california.html', { uplink: '.uplink a.uc' }],
  ['insurance-panels-california-therapist.html', {
    sources: '.artsrc li', uplink: '.uplink a.uc',
  }],
  ['headway-alma-grow-therapy-compared-california.html', {
    sources: '.artsrc li', uplink: '.uplink a.uc',
  }],
  ['continuing-education-california-lmft.html', { sources: '.artsrc li' }],
  ['getting-paid/index.html', { cards: '.lc', intro: '.intro p' }],
  ['privacy.html', { uplink: '.uplink a.uc' }],
  // The cost-of-living tool, whose hero was rebuilt as a compact band. The
  // three live figures are the assertion worth checking: they are computed on
  // load, so if the script dies they render as the markup's placeholders and
  // the page still looks finished.
  ['therapist-cost-of-living-california.html', {
    band: '.clband', cta: '.clgo', figures: '.clbig b', fields: '.clf input',
    sections: '.clsec',
  }],
  ['mft-programs-california.html', {
    charts: '.ig', dots: '.ig-d', bars: '.ig-b',
    internal: 'a.go.mine', cards: 'article.pg',
    // The BBS reconciliation. Each of these is a claim the page makes only
    // because the Board's own table says so, and each rendered as nothing at
    // all before this pass: "LMFT only" was indistinguishable from "not
    // checked", and a Board warning was not on the page in any form.
    lpccNo: '.badge.lpn', boardNotice: '.warn', offList: '.offl',
    onlineFilter: '.fb[data-v="Online or out of state"]',
    lpccFilter: '.fb[data-k="lpcc"]',
    // second-generation directory UI
    tableRows: 'tr.pgr', keepButtons: '.keep', gaps: '.gapl', az: '.az a',
    ask: '#ask li', viewToggle: '#vtbl', keepPill: '#kpill', top: '#totop',
  }],
  ['sentio-university-mft.html', {
    notice: '.verd.board', noticeLink: '.verd.board a[href*="sentio_uni_nts"]',
  }],
  ['cal-poly-humboldt-mft.html', { table: '.tbl' }],
  // The Board's by-school exam figure. The caveat is asserted as a REQUIRED
  // element, not an optional one: the whole justification for publishing this
  // number is that it never appears without the note explaining what it does
  // and does not measure. If the note can go missing, the feature should not
  // ship.
  ['california-institute-of-integral-studies-mft.html', {
    exam: '#exam-results', examFigure: '.exb b', examN: '.exb span',
    examStatewide: '.exb.sw', examCaveat: '.exwarn',
  }],
  // COAMFTE outcomes, and the cohort size that has to travel with every rate.
  ['loma-linda-university-mft.html', {
    outcomes: '#outcomes', cohortRows: '.octbl tbody tr',
    cohortSizes: '.octbl tbody th span', verbatim: '.ocdef',
  }],
  ['california-institute-of-integral-studies-mft.html', {
    video: '.vplay', courses: '.crs', terms: '.trm', practicum: '#practicum',
    voices: '.vox', gaps: '#what-i-could-not-find',
  }],
  ['san-diego-state-university-mft.html', { photo: '.pfig img', courses: '.crs' }],
  ['daybreak-university-mft.html', { practicum: '#practicum', courses: '.crs' }],
  ['psychedelic-therapy-training-california.html', {
    ledger: '.ledg', law: 'details.law', cards: '.pcard', video: '.vplay',
  }],
  ['psychedelic-training-ciis-psychedelic-assisted-therapies.html', {
    ledger: '.ledg', can: '.lcol.can li', cannot: '.lcol.cant li', mods: '.mods li',
  }],
  ['psychedelic-training-innertrek.html', { ledger: '.ledg', badge: '.sb.ok' }],
];

const fails = [];
const note = (p, m) => fails.push(`${p}: ${m}`);

const PHASE = process.argv[2] || 'all';

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--disable-dev-shm-usage', '--no-sandbox'],
});

for (const view of (PHASE === 'bulk' ? [] : VIEWS)) {
  const ctx = await browser.newContext({ viewport: view });
  await ctx.route('**/*', r =>
    r.request().url().startsWith('file://') ? r.continue() : r.abort());
  for (const [file, sel] of PAGES) {
    const page = await ctx.newPage();
    const errs = [];
    // Ignore network failures. This sandbox has no route to fonts.googleapis
    // or i.ytimg, so every page reports ERR_CONNECTION_RESET for its webfont
    // and its video poster - which drowns out the script errors this check
    // exists to catch. Failures to FETCH are not failures of the page.
    const NET = /Failed to load resource|ERR_(CONNECTION|NAME|INTERNET|BLOCKED)/;
    page.on('console', m => {
      if (m.type() === 'error' && !NET.test(m.text())) errs.push(m.text());
    });
    page.on('pageerror', e => errs.push(String(e)));
    // Third-party requests must not fire on load. The whole point of the
    // click-to-load facade is that nothing reaches YouTube until asked.
    const third = [];
    page.on('request', r => {
      const u = r.url();
      if (/youtube|googlevideo|doubleclick/.test(u)) third.push(u);
    });
    await page.goto(ROOT + file, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(220);

    for (const [label, css] of Object.entries(sel)) {
      const n = await page.locator(css).count();
      if (!n) note(`${file} [${view.name}]`, `no ${label} (${css})`);
    }
    if (errs.length) note(`${file} [${view.name}]`, `console: ${errs[0].slice(0, 130)}`);
    if (third.length) note(`${file} [${view.name}]`, `loaded ${third[0].slice(0, 70)} before any click`);

    if (await page.locator('h1').count() !== 1)
      note(`${file} [${view.name}]`, 'not exactly one h1');

    // Horizontal overflow, ignoring elements inside a scrollable ancestor.
    const over = await page.evaluate(w => {
      const bad = [];
      const scrollable = el => {
        for (let p = el.parentElement; p; p = p.parentElement) {
          const o = getComputedStyle(p).overflowX;
          if (o === 'auto' || o === 'scroll') return true;
        }
        return false;
      };
      for (const el of document.querySelectorAll('body *')) {
        const r = el.getBoundingClientRect();
        if (r.width && r.right > w + 1.5 && !scrollable(el)) {
          bad.push(`${el.tagName}.${el.className}`.slice(0, 60) + ` @${Math.round(r.right)}`);
          if (bad.length > 2) break;
        }
      }
      return bad;
    }, view.width);
    if (over.length) note(`${file} [${view.name}]`, `overflows: ${over.join(' | ')}`);

    // The header has shipped dead on this site before. Click it, every page.
    const trig = page.locator('header [aria-controls="navpanel"], header .navbtn').first();
    if (await trig.count()) {
      await trig.click();
      await page.waitForTimeout(160);
      if (!(await page.locator('#navpanel').isVisible()))
        note(`${file} [${view.name}]`, 'nav panel did not open');
      // Match on the tail of the href: a page one level down links to
      // ../psychedelic-… and an exact-match selector reads that as missing.
      else if (!(await page.locator('#navpanel a[href$="psychedelic-therapy-training-california.html"]').count()))
        note(`${file} [${view.name}]`, 'psychedelic training missing from the panel');
      await page.keyboard.press('Escape');
    } else {
      note(`${file} [${view.name}]`, 'no nav trigger in the header');
    }

    // The region filter has to partition the cards, not sample them. Static
    // markup cannot show this: every card carries SOME data-region, so a
    // card in a bucket no button selects looks identical in the HTML to one
    // in a bucket that is selectable. Press each region button in turn and
    // check the three counts add up to the whole grid. Four schools were
    // unreachable this way for months.
    if (file === 'mft-programs-california.html' && view.name === 'desktop') {
      const total = await page.locator('article.pg').count();
      let sum = 0;
      for (const btn of await page.locator('.fb[data-k="region"]').all()) {
        await btn.click();
        await page.waitForTimeout(90);
        sum += await page.locator('article.pg:not(.hide)').count();
        await btn.click();
        await page.waitForTimeout(60);
      }
      if (sum !== total)
        note(file, `region filters reach ${sum} of ${total} cards`);
      const lp = page.locator('.fb[data-k="lpcc"]');
      await lp.click();
      await page.waitForTimeout(90);
      const yes = await page.locator('article.pg:not(.hide)').count();
      if (!yes || yes >= total)
        note(file, `the LPCC filter shows ${yes} of ${total} - it filters nothing`);
      await lp.click();
    }

    // The second-generation directory controls, exercised rather than counted.
    // Every one of these renders identically in the markup whether it works or
    // not, which is the failure mode this whole file exists for.
    if (file === 'mft-programs-california.html' && view.name === 'desktop') {
      const cards = await page.locator('article.pg').count();
      const rows = await page.locator('tr.pgr').count();
      if (cards !== rows) note(file, `${cards} cards but ${rows} table rows`);

      // table view swaps, and the same filter reaches both renderings
      await page.locator('#vtbl').click();
      await page.waitForTimeout(140);
      if (!(await page.locator('#tbl').isVisible()))
        note(file, 'table view button did not show the table');
      if (await page.locator('.grid').isVisible())
        note(file, 'cards still visible in table view');
      await page.locator('.fb[data-k="coamfte"]').click();
      await page.waitForTimeout(140);
      const vr = await page.locator('tr.pgr:not(.hide)').count();
      const vc = await page.locator('article.pg:not(.hide)').count();
      if (vr !== vc) note(file, `filter left ${vc} cards and ${vr} rows visible`);
      if (!/#.*coamfte=yes/.test(page.url())) note(file, 'filter state not written to the URL');
      if (!(await page.locator('.chip').count())) note(file, 'no chip for the active filter');
      await page.locator('#clr').click();
      await page.waitForTimeout(140);
      if (await page.locator('article.pg.hide').count())
        note(file, 'clear all did not restore every card');
      await page.locator('#vcard').click();
      await page.waitForTimeout(120);

      // the shortlist: keep one, and it must persist a reload
      const first = page.locator('article.pg .keep').first();
      const id = await page.locator('article.pg').first().getAttribute('id');
      await first.click();
      await page.waitForTimeout(120);
      if (!/Kept 1/.test(await page.locator('#kpill').textContent() || ''))
        note(file, 'keeping a school did not update the count');
      await page.reload({ waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(220);
      if (!/Kept 1/.test(await page.locator('#kpill').textContent() || ''))
        note(file, 'the shortlist did not survive a reload');
      await page.locator('#kpill').click();
      await page.waitForTimeout(140);
      const only = await page.locator('article.pg:not(.hide)').count();
      if (only !== 1) note(file, `kept-only view shows ${only} cards, expected 1`);
      await page.locator(`#${id} .keep`).click();      // leave storage clean
      await page.waitForTimeout(100);
    }

    // Two assertions that are about editorial policy rather than layout, and
    // both would fail silently. There must be NO pass-rate figure anywhere in
    // the directory, and no school page may print an exam rate without its
    // caveat - those are the two promises the exam section makes about itself.
    if (file === 'mft-programs-california.html' && view.name === 'desktop') {
      const body = await page.evaluate(() => document.body.innerText);
      if (/passed first time|pass rate/i.test(body))
        note(file, 'a pass-rate figure has appeared in the directory');
      if (await page.locator('.exb').count())
        note(file, 'an exam figure block is on the directory page');
    }
    if (/-mft\.html$/.test(file) && await page.locator('.exb b').count()
        && !(await page.locator('.exwarn').count()))
      note(file, 'an exam rate with no caveat beside it');

    // The facade has to actually become a player.
    if (view.name === 'desktop' && await page.locator('.vplay').count()) {
      await page.locator('.vplay').first().click();
      await page.waitForTimeout(260);
      const src = await page.locator('.vframe iframe').first().getAttribute('src')
        .catch(() => null);
      if (!src) note(file, 'clicking the video did not create a player');
      else if (!src.startsWith('https://www.youtube-nocookie.com/embed/'))
        note(file, `player points at ${src.slice(0, 50)}`);
    }
    await page.close();
  }
  await ctx.close();
}

// Every built page must at least load without a script error and carry a title.
const ctx = await browser.newContext({ viewport: VIEWS[0] });
// Block off-origin here too. The template pass has always done this; this one
// did not, and it only ever passed because the pages it loads happened to
// resolve their webfont failures fast. The moment one did not, the whole run
// died on a 30s navigation timeout with no findings at all - which reads as a
// broken check rather than as a missing route, and cost an afternoon.
await ctx.route('**/*', r =>
  r.request().url().startsWith('file://') ? r.continue() : r.abort());
for (const f of (PHASE === 'templates' ? [] : [...psy, ...schools])) {
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  await page.goto(ROOT + f, { waitUntil: 'domcontentloaded' });
  // One round-trip, not four. Playwright's `locator().count()` re-queries and
  // re-serialises across the protocol boundary each time, which on a 135 KB
  // page with several thousand nodes costs seconds - times four checks times
  // fifty-four pages, the pass stops finishing at all.
  const r = await page.evaluate(() => ({
    title: document.title,
    h1: document.querySelectorAll('h1').length,
    dead: document.querySelectorAll('a[href=""], a:not([href])').length,
    nav: !!document.querySelector('#navpanel'),
    yt: document.querySelectorAll('iframe[src*="youtube"]').length,
  }));
  if (errs.length) note(f, `pageerror: ${errs[0].slice(0, 110)}`);
  if (!r.title || r.title.length < 25) note(f, `thin title: ${r.title}`);
  if (r.h1 !== 1) note(f, `${r.h1} h1 elements`);
  if (r.dead) note(f, `${r.dead} link(s) with no destination`);
  if (!r.nav) note(f, 'no nav panel in the markup');
  if (r.yt) note(f, 'a YouTube iframe is in the initial markup');
  await page.close();
}
await ctx.close();
await browser.close();

console.log(`checked ${PAGES.length} templates x ${VIEWS.length} viewports, ` +
            `plus ${psy.length + schools.length} pages for load errors`);
if (fails.length) {
  console.log(`\n${fails.length} PROBLEM(S):`);
  fails.slice(0, 30).forEach(f => console.log('  - ' + f));
  process.exit(1);
}
console.log('clean');
