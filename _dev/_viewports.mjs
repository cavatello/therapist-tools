// Every page, five viewports. The sweep that had never been run at tablet.
//
// A result from a dead server is not a result: this counts load failures and
// exits non-zero rather than reporting an empty finding set as success. That
// mistake has been made twice in this project.
import pkg from '/home/claude/.npm-global/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
import { readFileSync } from 'fs';
const BASE = process.env.BASE || 'http://127.0.0.1:8077';
const pages = readFileSync('/tmp/allpages.txt','utf8').trim().split('\n');
const VIEWS = [[390,844,'phone'],[768,1024,'tablet-p'],[834,1112,'tablet-l'],[1024,768,'laptop'],[1440,900,'desktop']];
const SCALE = [9.5,10.5,12,13.5,15,16.5,19,23,28,34,42,52,66];
const SKIP = new Set(['/practice-simulator.html','/tycoon.html','/concepts.html']);

function lum(c){const s=c.map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*s[0]+0.7152*s[1]+0.0722*s[2]}
function ratio(a,b){const l1=lum(a),l2=lum(b);return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05)}
function parse(c){const m=String(c).match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(',').map(Number);if(p.length>3&&p[3]<0.9)return null;return [p[0],p[1],p[2]]}

const br = await chromium.launch();
let err = 0;
const find = { contrast:[], overflow:[], tap:[], size:[], grad:[] };
for (const [w,h,name] of VIEWS) {
  const ctx = await br.newContext({viewport:{width:w,height:h}, hasTouch:w<900});
  const pg = await ctx.newPage();
  for (const p of ['**googletagmanager**','**fonts.googleapis**','**fonts.gstatic**','**clarity.ms**','**ahrefs.com**']) await pg.route(p,r=>r.abort());
  let n=0;
  for (const p of pages) {
    n++;
    try {
      await pg.goto(BASE+p,{waitUntil:'domcontentloaded',timeout:15000});
      const r = await pg.evaluate((args)=>{
        const {SCALE, skip} = args;
        const out = {ov:null, tap:[], size:[], grad:0, pairs:[]};
        // horizontal overflow
        const dw = document.documentElement.scrollWidth, iw = window.innerWidth;
        if (dw > iw + 2) {
          let worst=null, wx=0;
          document.querySelectorAll('body *').forEach(el=>{
            const b=el.getBoundingClientRect();
            if (b.right > iw+2 && b.width>20 && b.right>wx){wx=b.right;worst=el}
          });
          out.ov = {dw, iw, who: worst? worst.tagName.toLowerCase()+'.'+(worst.className||'').toString().slice(0,34):'?'};
        }
        document.querySelectorAll('body *').forEach(el=>{
          const s=getComputedStyle(el), b=el.getBoundingClientRect();
          if (b.width<1||b.height<1) return;
          if (s.backgroundImage && s.backgroundImage.includes('gradient')) out.grad++;
          // tap targets, only where touch applies
          const clickable = el.tagName==='A'||el.tagName==='BUTTON'||el.tagName==='INPUT'||el.tagName==='SELECT';
          if (clickable && (b.width<24||b.height<24) && el.offsetParent!==null)
            out.tap.push(el.tagName.toLowerCase()+'.'+(el.className||'').toString().slice(0,24)+' '+Math.round(b.width)+'x'+Math.round(b.height));
          if (!skip) {
            const px = Math.round(parseFloat(s.fontSize)*10)/10;
            if (px && !SCALE.includes(px) && !out.size.includes(px)) out.size.push(px);
          }
          // contrast on text-bearing leaves
          let txt=''; el.childNodes.forEach(nd=>{ if(nd.nodeType===3) txt+=nd.textContent });
          if (txt.trim().length<8) return;
          out.pairs.push({fg:s.color, cls:el.tagName.toLowerCase()+'.'+(el.className||'').toString().slice(0,28),
                          bg:(function(){let e=el;while(e){const c=getComputedStyle(e).backgroundColor;const m=c.match(/rgba?\(([^)]+)\)/);if(m){const a=m[1].split(',').map(Number);if(a.length<4||a[3]>0.9)return c}e=e.parentElement}return null})(),
                          ex: txt.trim().slice(0,34)});
        });
        return out;
      }, {SCALE, skip: SKIP.has(p)});
      if (r.ov) find.overflow.push([name,p,r.ov.dw+'>'+r.ov.iw,r.ov.who]);
      for (const t of r.tap.slice(0,3)) find.tap.push([name,p,t]);
      for (const s of r.size) find.size.push([name,p,s]);
      for (const q of r.pairs) {
        const fg=parse(q.fg), bg=parse(q.bg);
        if (!fg||!bg) continue;
        const rr=ratio(fg,bg);
        if (rr<4.5) find.contrast.push([name,p,q.cls,rr.toFixed(2),q.ex]);
      }
    } catch(e) { err++; if (err<4) console.log('ERR',name,p,String(e.message).slice(0,70)); }
  }
  console.log(`${name} ${w}x${h}: done (${n} pages)`);
  await ctx.close();
}
await br.close();
if (err) { console.log(`\nABORT: ${err} page load(s) failed - a result from a dead server is not a result`); process.exit(1); }

function group(rows, keyIdx){ const m={}; for (const r of rows){ const k=r.slice(keyIdx).join(' | '); (m[k]=m[k]||{n:0,views:new Set(),pages:new Set()}); m[k].n++; m[k].views.add(r[0]); m[k].pages.add(r[1]); } return m }
function show(title, rows, keyIdx, cap=14){
  console.log(`\n## ${title}: ${rows.length} finding(s)`);
  const g = group(rows, keyIdx);
  Object.entries(g).sort((a,b)=>b[1].pages.size-a[1].pages.size).slice(0,cap)
    .forEach(([k,v])=>console.log(`   ${String(v.pages.size).padStart(4)}p  [${[...v.views].join(',')}]  ${k}`));
}
show('HORIZONTAL OVERFLOW', find.overflow, 2);
show('CONTRAST under 4.5', find.contrast, 2);
show('TAP TARGETS under 24px', find.tap, 2);
show('FONT SIZE off the 13-step scale', find.size, 2);
