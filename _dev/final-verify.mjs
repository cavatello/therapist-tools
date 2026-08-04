const TAXQ = e => e + '&tax';   // tax content lives on its own page now
import { chromium } from '/home/claude/.npm-global/lib/node_modules/playwright/index.mjs';
const mk = st => Buffer.from(encodeURIComponent(JSON.stringify(st))).toString('base64')
  .replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
const full = {rate:200,sessions:25,taxAge:40,retireAge:67,investReturn:11,sCorpSalaryInput:102000,
  payrollSvcCost:600,corpReturnCost:1000,statementOfInfoCost:25,filingStatus:"single",entityType:"sole_prop"};
const empty = {rate:200,sessions:25,filingStatus:"single",entityType:"sole_prop"};
const b = await chromium.launch();
const errs=[];
for (const [nm, st, w] of [["desktop-full",full,1280],["desktop-empty",empty,1280],["phone-full",full,390]]) {
  const pg = await b.newPage({viewport:{width:w,height:w>500?1000:844}});
  pg.on('pageerror',e=>errs.push(nm+': '+e.message));
  pg.on('console',m=>{if(m.type()==='error')errs.push(nm+': '+m.text().slice(0,120));});
  await pg.goto('http://localhost:8123/local.html?n='+Math.random()+'#s='+TAXQ(mk(st)),{waitUntil:'load'});
  await pg.waitForTimeout(1600);
  // The structure detail is gated behind a button for sole proprietors, so
  // open it before counting anything that lives inside it.
  const gate = pg.locator('.sgate-b');
  if (await gate.count()) { await gate.click(); await pg.waitForTimeout(500); }
  await pg.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
  await pg.waitForTimeout(500);
  const c = {};
  for (const sel of ['.opener','.rail-step','.stepcard','.sfield','.cmp-table','tr.cmp-row','.peek',
                     '.ssd-tbl','.ssd-row','.fkey span','.wagea','.wrow',
                     '.setuptl .stl','.habit','.exitnote','.locret','.resid-retnote','.jumpnav-prog','.expert-q'])
    c[sel]=await pg.locator(sel).count();
  console.log(nm.padEnd(14), JSON.stringify(c));
  console.log('               h-scroll:', await pg.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1));
  const txt = await pg.locator('.planner').innerText();
  const bad = ['NaN','undefined','Infinity','practice-income-planner'].filter(x=>txt.includes(x));
  if(bad.length) console.log('               !! BAD TOKENS', bad);
  if(nm==='desktop-full'){
    await pg.locator('.rlev').screenshot({path:'/home/claude/site/f-rlev.png'});
    await pg.locator('.ssd').screenshot({path:'/home/claude/site/f-ss.png'});
    await pg.locator('.wagea').screenshot({path:'/home/claude/site/f-wage.png'});
    await pg.locator('.rail-wrap').screenshot({path:'/home/claude/site/f-rail.png'});
  }
  if(nm==='desktop-empty') await pg.locator('.peek').screenshot({path:'/home/claude/site/f-peek.png'});
  await pg.close();
}
console.log('ERRORS:', errs.length?errs.slice(0,6):'none');
await b.close();
