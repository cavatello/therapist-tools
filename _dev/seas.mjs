/* Seasonality UI — verification.
   Asserts the invariant the engine doc names as the decision that matters most
   (normalisation: changing the shape must NOT change annual arrivals), plus the
   UI contract: twelve bars at every viewport, drag writes state, state travels
   in the hash, nothing overflows a 390px phone. */
import { chromium } from '/home/claude/.npm-global/lib/node_modules/playwright/index.mjs';
import { readFileSync } from 'fs';

const FILE = '/home/claude/work/mock/growpage/grow-your-therapy-practice.html';
const html = readFileSync(FILE, 'utf8');

let pass = 0, fail = 0;
const ok = (c, m) => { c ? pass++ : (fail++, console.log('  FAIL ' + m)); };

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

async function fresh(vw = 1280, vh = 900) {
  const ctx = await browser.newContext({ viewport: { width: vw, height: vh } });
  const page = await ctx.newPage();
  const errs = [];
  /* The sandbox cannot reach the webfont/analytics hosts, so every load here
     emits ERR_CONNECTION_RESET. Those are the environment, not the page —
     filtering them is what makes a real JS error visible instead of buried. */
  const noise = /net::ERR_|Failed to load resource/;
  page.on('console', m => { if (m.type() === 'error' && !noise.test(m.text())) errs.push(m.text()); });
  page.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  /* Block every external request outright. The page links webfonts and
     analytics that this sandbox cannot reach, and waitUntil:'load' politely
     waits out each connection reset — roughly 30s per context, which is what
     made a nine-context suite look like an infinite hang rather than a slow
     one. Nothing asserted here depends on a font arriving. */
  await page.route('**/*', r => {
    const u = r.request().url();
    return (u.startsWith('data:') || u.startsWith('about:')) ? r.continue() : r.abort();
  });
  await page.setContent(html, { waitUntil: 'domcontentloaded' });
  return { ctx, page, errs };
}

const FILL = async (page) => {
  for (const [id, v] of [['i-rate','180'],['i-tenure','20'],['i-clients','30'],
                         ['i-sessions','25'],['i-churn','2'],['i-weeksOff','2'],
                         ['i-pt_views','1000'],['i-pt_enq','40'],['i-pt_got','12']]) {
    await page.fill('#' + id, v);
  }
  await page.waitForTimeout(60);
};

console.log('>> section 1');
/* ---------- 1. structure and zero state ---------- */
{
  const { ctx, page, errs } = await fresh();
  ok(await page.locator('#seasout').count() === 1, 'seasout present');
  ok(await page.locator('.shc').count() === 4, 'four shape cards');
  ok(await page.locator('.smo').count() === 12, 'twelve month bars in zero state');
  ok(await page.locator('#seasout .empty').count() === 1, 'zero state shows the empty note');
  ok(await page.locator('.ld').count() === 0, 'no caseload chart before there is data');
  ok(errs.length === 0, 'no console errors on boot: ' + errs.join(' | '));
  await ctx.close();
}

console.log('>> section 2');
/* ---------- 2. live state renders the chart ---------- */
{
  const { ctx, page, errs } = await fresh();
  await FILL(page);
  ok(await page.locator('.ld').count() === 12, 'twelve caseload columns');
  ok(await page.locator('#seasout .tiles .tl').count() === 4, 'four headline tiles');
  ok(await page.locator('.ldcap').count() === 1, 'ceiling line drawn when capacity is set');
  ok(await page.locator('#seasout .empty').count() === 0, 'empty note gone');
  ok(errs.length === 0, 'no console errors when live: ' + errs.join(' | '));
  await ctx.close();
}

console.log('>> section 3');
/* ---------- 3. THE invariant: normalisation holds annual arrivals ---------- */
{
  const { ctx, page } = await fresh();
  await FILL(page);
  const annual = async () => page.evaluate(() => {
    const r = grow().monthly.rows;
    return { arrive: r.reduce((a, x) => a + x.arrive, 0),
             mult:   r.reduce((a, x) => a + x.mult, 0) };
  });
  const a0 = await annual();
  ok(Math.abs(a0.mult - 12) < 1e-9, 'multipliers sum to 12.000 (typical), got ' + a0.mult);

  for (const k of ['flat', 'school', 'steady']) {
    await page.click(`.shc[data-shape="${k}"]`);
    await page.waitForTimeout(40);
    const a = await annual();
    ok(Math.abs(a.mult - 12) < 1e-9, `multipliers sum to 12.000 (${k}), got ${a.mult}`);
    ok(Math.abs(a.arrive - a0.arrive) < 1e-9,
       `annual arrivals unchanged switching to ${k}: ${a.arrive} vs ${a0.arrive}`);
  }
  /* and after a hand edit, which is the case most likely to break it */
  await page.evaluate(() => { S.months[6] = '20'; render(); });
  const a2 = await annual();
  ok(Math.abs(a2.mult - 12) < 1e-9, 'multipliers still sum to 12.000 after a drag');
  ok(Math.abs(a2.arrive - a0.arrive) < 1e-9, 'annual arrivals unchanged after a drag');

  /* the shapes must actually differ month to month, or the above is vacuous */
  await page.evaluate(() => { S.months = ['','','','','','','','','','','','']; S.shape = 'flat'; render(); });
  const flat = await page.evaluate(() => grow().monthly.rows.map(r => +r.load.toFixed(4)));
  await page.evaluate(() => { S.shape = 'school'; render(); });
  const school = await page.evaluate(() => grow().monthly.rows.map(r => +r.load.toFixed(4)));
  ok(JSON.stringify(flat) !== JSON.stringify(school), 'flat and school produce different curves');
  await ctx.close();
}

console.log('>> section 4');
/* ---------- 4. dragging writes state and moves the bar ---------- */
{
  const { ctx, page, errs } = await fresh();
  await FILL(page);
  /* hover({position}) rather than mouse.move(boundingBox): boundingBox() is in
     DOCUMENT coordinates and mouse.move() takes VIEWPORT coordinates, so on a
     long page the two disagree by the scroll offset and the press lands on
     nothing. hover() scrolls the element in and positions relative to it. */
  await page.locator('.smo[data-i="6"] .smot').hover({ position: { x: 6, y: 3 } });
  await page.mouse.down();
  await page.mouse.up();
  await page.waitForTimeout(60);
  const v = await page.evaluate(() => S.months[6]);
  ok(v !== '' && +v >= 180, 'press near the top of the track sets a high value, got ' + v);
  ok(await page.locator('.smo[data-i="6"].on').count() === 1, 'edited month is flagged');
  ok(await page.locator('#seasreset').count() === 1, 'reset appears once a month is edited');

  /* painting sideways: hold, drag across two neighbours, release */
  await page.locator('.smo[data-i="2"] .smot').hover({ position: { x: 6, y: 90 } });
  await page.mouse.down();
  for (const i of [3, 4]) {
    await page.locator(`.smo[data-i="${i}"] .smot`).hover({ position: { x: 6, y: 90 } });
  }
  await page.mouse.up();
  await page.waitForTimeout(60);
  const painted = await page.evaluate(() => [2, 3, 4].map(i => S.months[i]));
  ok(painted.every(x => x !== '' && +x <= 40),
     'dragging sideways paints every month crossed, got ' + JSON.stringify(painted));

  await page.click('#seasreset');
  await page.waitForTimeout(40);
  ok(await page.evaluate(() => S.months.every(x => x === '')), 'reset clears every override');
  ok(await page.locator('#seasreset').count() === 0, 'reset disappears again');
  ok(errs.length === 0, 'no console errors through a drag: ' + errs.join(' | '));
  await ctx.close();
}

console.log('>> section 4b (units)');
/* ---------- 4b. UNITS. The shape tests above are all relative — they compare
   one shape against another, so a scaling error common to every shape passes
   them silently. These pin the absolute magnitude instead. ---------- */
{
  const { ctx, page } = await fresh();
  /* arrivals exactly equal departures, flat shape => a caseload that does not
     move all year. Any stray /12 on either side breaks this immediately. */
  for (const [id, v] of [['i-rate','180'],['i-tenure','20'],['i-clients','24'],
                         ['i-sessions','25'],['i-churn','4'],['i-weeksOff','2'],
                         ['i-pt_views','1000'],['i-pt_enq','40'],['i-pt_got','4']]) {
    await page.fill('#' + id, v);
  }
  await page.evaluate(() => { S.shape = 'flat'; render(); });
  await page.waitForTimeout(40);
  const m = await page.evaluate(() => {
    const x = grow().monthly;
    return { loads: x.rows.map(r => +r.load.toFixed(6)), swing: x.swing,
             arrive: +x.rows[0].arrive.toFixed(6), leave: +x.rows[0].leave.toFixed(6) };
  });
  ok(m.arrive === 4, '4 clients a month in is read as 4, got ' + m.arrive);
  ok(m.leave === 4, '4 clients a month out is read as 4, got ' + m.leave);
  ok(m.loads.every(v => Math.abs(v - 24) < 1e-9),
     'in == out on a flat shape holds the caseload still: ' + JSON.stringify(m.loads.slice(0, 3)));
  ok(Math.abs(m.swing) < 1e-9, 'and the swing is zero, got ' + m.swing);

  /* DETRENDING. A flat shape must report zero seasonal swing at ANY growth
     rate — that is the whole point of the correction. Before it, a practice
     growing 2 clients a month reported a 24-client "swing" with no seasonality
     whatsoever, and named January the trough purely for being month one. */
  for (const got of ['2', '6', '10']) {
    await page.fill('#i-pt_got', got);
    await page.waitForTimeout(40);
    const s = await page.evaluate(() => grow().monthly);
    ok(Math.abs(s.swing) < 1e-9,
       `flat shape, net ${+got - 4}/month => zero seasonal swing, got ${s.swing}`);
    ok(Math.abs(s.trend - (+got - 4)) < 1e-9,
       `trend reported as ${+got - 4}/month, got ${s.trend}`);
  }
  /* and with a real shape the swing must be positive and NOT equal the growth */
  await page.fill('#i-pt_got', '6');
  await page.evaluate(() => { S.shape = 'school'; render(); });
  await page.waitForTimeout(40);
  const sc = await page.evaluate(() => grow().monthly);
  ok(sc.swing > 0.5, 'a real shape produces a real swing, got ' + sc.swing.toFixed(3));
  ok(sc.lowMonth !== 'Jan', 'the trough is no longer pinned to month one, got ' + sc.lowMonth);

  /* net growth of exactly +2/month must land 24 clients higher after a year */
  await page.fill('#i-pt_got', '6');
  await page.waitForTimeout(40);
  const end = await page.evaluate(() => grow().monthly.rows[11].load);
  ok(Math.abs(end - 48) < 1e-6, '+2 a month for 12 months ends at 48, got ' + end.toFixed(3));
  await ctx.close();
}

console.log('>> section 4c (tiles reconcile)');
/* ---------- 4c. The three seasonality tiles must add up AS PRINTED.
   Independent rounding of peak, trough and swing is how this project has
   shipped a visibly-wrong column three times. ---------- */
{
  const { ctx, page } = await fresh();
  await FILL(page);
  for (const shape of ['typical', 'school', 'steady']) {
    for (const got of ['3', '5', '9']) {
      await page.fill('#i-pt_got', got);
      await page.evaluate(s => { S.shape = s; render(); }, shape);
      await page.waitForTimeout(30);
      const t = await page.evaluate(() =>
        [...document.querySelectorAll('#seasout .tiles .tl')].map(el => ({
          lab: el.querySelector('em').textContent,
          val: el.querySelector('b').textContent,
          sub: (el.querySelector('u') || {}).textContent || ''
        })));
      const num = s => { const m = String(s).match(/[-−+]?\d[\d,]*/);
                         return m ? +m[0].replace(/,/g, '').replace('−', '-') : NaN; };
      const swing = num(t[0].val), hi = num(t[1].sub), lo = num(t[2].sub);
      ok(hi - lo === swing,
         `${shape}/${got}: printed peak ${hi} minus trough ${lo} equals printed swing ${swing}`);
      /* and the peak must never be printed below the trough */
      ok(hi >= lo, `${shape}/${got}: peak deviation is not below the trough`);
    }
  }
  await ctx.close();
}

console.log('>> section 5');
/* ---------- 5. keyboard ---------- */
{
  const { ctx, page } = await fresh();
  await FILL(page);
  await page.locator('.smo[data-i="0"]').focus();
  await page.keyboard.press('ArrowDown');
  await page.waitForTimeout(40);
  const after = await page.evaluate(() => S.months[0]);
  ok(after === '140', 'ArrowDown moves Jan 145 -> 140, got ' + after);
  await page.keyboard.press('ArrowUp');
  await page.waitForTimeout(40);
  ok(await page.evaluate(() => S.months[0]) === '145', 'ArrowUp returns it');
  ok(await page.evaluate(() => document.activeElement.getAttribute('data-i')) === '0',
     'focus survives the repaint');
  await ctx.close();
}

console.log('>> section 6');
/* ---------- 6. the hash carries the seasonality ---------- */
{
  const { ctx, page } = await fresh();
  await FILL(page);
  await page.click('.shc[data-shape="school"]');
  await page.evaluate(() => { S.months[6] = '25'; render(); });
  await page.waitForTimeout(40);
  const hash = await page.evaluate(() => location.hash);
  ok(/shape=school/.test(hash), 'shape written to the hash');
  ok(/mo=/.test(hash), 'month overrides written to the hash');

  /* default shape must NOT bloat an ordinary link */
  await page.evaluate(() => { S.shape = 'typical'; S.months = ['','','','','','','','','','','','']; render(); });
  ok(!/shape=|mo=/.test(await page.evaluate(() => location.hash)),
     'a default setup writes neither key');

  /* round trip */
  const { ctx: c2, page: p2 } = await fresh();
  await p2.evaluate(h => { location.hash = h; }, hash);
  await p2.evaluate(() => { readHash(); render(); });
  await p2.waitForTimeout(40);
  ok(await p2.evaluate(() => S.shape) === 'school', 'shape survives the round trip');
  ok(await p2.evaluate(() => S.months[6]) === '25', 'month override survives the round trip');
  await c2.close();
  await ctx.close();
}

console.log('>> section 7');
/* ---------- 7. phone: twelve columns, nothing over the edge ---------- */
for (const [w, h] of [[390, 844], [768, 1024]]) {
  const { ctx, page, errs } = await fresh(w, h);
  await FILL(page);
  ok(await page.locator('.smo').count() === 12, `twelve bars at ${w}px`);
  ok(await page.locator('.ld').count() === 12, `twelve caseload columns at ${w}px`);

  /* per-element right edge, per the handoff: overflow-x:clip makes "does the
     page scroll sideways" a meaningless test on this site */
  const over = await page.evaluate((vw) => {
    const bad = [];
    document.querySelectorAll('#season *').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.right > vw + 0.5) bad.push(el.className + ' right=' + Math.round(r.right));
    });
    return bad.slice(0, 6);
  }, w);
  ok(over.length === 0, `nothing overflows ${w}px: ` + over.join(' | '));

  /* the bars must stay wide enough to be a drag target */
  const bw = await page.evaluate(() => document.querySelector('.smot').getBoundingClientRect().width);
  ok(bw >= 18, `month bar is ${bw.toFixed(1)}px wide at ${w}px — still draggable`);
  ok(errs.length === 0, `no console errors at ${w}px: ` + errs.join(' | '));
  await ctx.close();
}


console.log('>> section 8 (funnel)');
{
  const { ctx, page, errs } = await fresh();
  await FILL(page);
  ok(await page.locator('.fung').count() === 3, 'three gutter rows');
  ok(await page.locator('.fun-real').count() === 1, 'the real funnel is drawn');
  ok(await page.locator('.fun-sim').count() === 0, 'no what-if outline before anything is dragged');
  ok(await page.locator('.fun-grip').count() === 2, 'two draggable necks');
  ok(await page.locator('#funreset').count() === 0, 'no reset until a lever moves');
  ok(await page.locator('.stg').count() === 0, 'the old stacked bars are gone');

  const gut = await page.locator('.fung b').allTextContents();
  ok(gut[0] === '1,000' && gut[1] === '40' && gut[2] === '12',
     'gutter prints the entered counts, got ' + JSON.stringify(gut));

  await page.locator('.fun-grip.g1').hover();
  await page.mouse.down();
  const box = await page.locator('#funsvg').boundingBox();
  await page.mouse.move(box.x + box.width * 0.80, box.y + box.height * 0.31);
  await page.mouse.up();
  await page.waitForTimeout(60);

  const sim = await page.evaluate(() => S.simEnq);
  ok(sim !== '' && +sim > 4, 'dragging the first neck outward raises the rate, got ' + sim);
  ok(await page.locator('.fun-sim').count() === 1, 'the what-if outline appears');
  ok(await page.locator('.fun-sim-out').count() === 1, 'the outcome card appears');

  /* the entered data must NOT be touched — this is the whole design */
  const raw = await page.evaluate(() => JSON.stringify(S.chan));
  ok(/"views":"1000"/.test(raw) && /"enq":"40"/.test(raw) && /"got":"12"/.test(raw),
     'a what-if never overwrites the numbers the reader typed');

  /* the card's own printed figures must be re-derivable from the engine */
  const card = await page.evaluate(() => {
    const el = document.querySelector('.fun-sim-out');
    return { head: el.querySelector('.fso-h b').textContent,
             /* the ANNUAL figure is the bolded one; the first $ in the sentence
                is the per-client worth, a different number entirely */
             body: el.querySelector('.fso-p b').textContent,
             worth: grow().worth, got: grow().got,
             simGot: funnelStages(grow()).got };
  });
  const clients = +card.head.match(/[\d,]+/)[0].replace(/,/g, '');
  const dollars = +card.body.match(/\$([\d,]+)/)[1].replace(/,/g, '');
  const exactGain = Math.abs(card.simGot - card.got);
  ok(clients === Math.round(exactGain),
     `card prints ${clients} clients, engine says ${exactGain.toFixed(2)}`);
  ok(Math.abs(dollars - Math.round(exactGain * 12 * card.worth)) <= 1,
     `card prints $${dollars}, clients x 12 x worth = ${Math.round(exactGain * 12 * card.worth)}`);

  await page.locator('.fun-grip.g2').focus();
  const before = await page.evaluate(() => S.simGot);
  await page.keyboard.press('ArrowUp');
  await page.waitForTimeout(50);
  ok(await page.evaluate(() => S.simGot) !== before, 'arrow keys move the second neck');

  await page.click('#funreset');
  await page.waitForTimeout(50);
  ok(await page.evaluate(() => S.simEnq === '' && S.simGot === ''), 'reset clears both levers');
  ok(await page.locator('.fun-sim').count() === 0, 'and the outline goes away');
  ok(errs.length === 0, 'no console errors through the funnel: ' + errs.join(' | '));
  await ctx.close();
}

console.log('>> section 9 (funnel on a phone)');
{
  const { ctx, page, errs } = await fresh(390, 844);
  await FILL(page);
  ok(await page.locator('.fung').count() === 3, 'three gutter rows at 390px');
  const over = await page.evaluate(() => {
    const bad = [];
    document.querySelectorAll('#channels *').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.right > 390.5) bad.push(el.className + ' right=' + Math.round(r.right));
    });
    return bad.slice(0, 6);
  });
  ok(over.length === 0, 'funnel section does not overflow 390px: ' + over.join(' | '));
  ok(errs.length === 0, 'no console errors at 390px: ' + errs.join(' | '));
  await ctx.close();
}

await browser.close();
console.log(`\n${pass}/${pass + fail} passed` + (fail ? `  — ${fail} FAILED` : ''));
process.exit(fail ? 1 : 0);
