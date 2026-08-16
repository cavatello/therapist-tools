import { chromium } from 'playwright';
const BASE='http://localhost:8901/';
const PAGES=['for/associates.html','bbs-fees-california-2026.html',
 'university-of-san-francisco-mft.html','loan-forgiveness-employers-california.html',
 'amft-3000-hours-california.html','about.html','index.html'];
const VPS=[375,768,1440,2560];
const lum=(r,g,b)=>{const f=c=>{c/=255;return c<=.03928?c/12.92:((c+.055)/1.055)**2.4};
 return .2126*f(r)+.7152*f(g)+.0722*f(b)};
const ratio=(a,b)=>{const l1=lum(...a),l2=lum(...b);return (Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05)};
const browser=await chromium.launch();
let fails=0, lows=0;
for(const p of PAGES){
 for(const w of VPS){
  const pg=await browser.newPage({viewport:{width:w,height:900}});
  const errs=[]; pg.on('pageerror',e=>errs.push(String(e)));
  await pg.goto(BASE+p,{waitUntil:'networkidle'});
  const sw=await pg.evaluate(()=>document.documentElement.scrollWidth);
  if(sw>w+1){console.log(`OVERFLOW ${p} @${w}: scrollWidth ${sw}`);fails++}
  if(errs.length){console.log(`JSERR ${p} @${w}: ${errs.join(' | ')}`);fails++}
  if(w===1440){
   // open the ledger tiles on the door before the contrast walk
   if(p.startsWith('for/')){
     await pg.fill('#lgTotal','1284');await pg.fill('#lgDirect','742');
     await pg.fill('#lgRel','228');await pg.fill('#lgWeeks','61');
     await pg.fill('#lgRate','18');await pg.waitForTimeout(300);
   }
   const rows=await pg.evaluate(()=>{
    const sels='h1,h2,h3,h4,.pk-k,.pk-d,.hk,.hl,.hpriv,.hj a,.tsk,.tsa,.tsfig,.lg-in label,.lg-read,.lg-note,.lg-mk span,.lg-g .k,.lg-g .v,.lg-g .s,.ask q,.ask .an,.ask p,.ask a,.start .q,.start .s,.shelf .t,.shelf .n,.pk-src li,.pk-fine,.tsbadge,.tswhat,.bcr,.bcr a,.dek,.kick,.artmeta,.scmeta,label';
    const out=[];
    for(const el of document.querySelectorAll(sels)){
     const r=el.getBoundingClientRect();
     if(r.width<2||r.height<2)continue;
     const cs=getComputedStyle(el);
     if(cs.visibility==='hidden')continue;
     const col=cs.color.match(/\d+(\.\d+)?/g).map(Number);
     if((col[3]??1)===0)continue;
     let n=el,bg=null,grad=false;
     while(n&&n!==document.documentElement){
      const s=getComputedStyle(n);
      if(s.backgroundImage!=='none'){grad=true;break}
      const m=s.backgroundColor.match(/\d+(\.\d+)?/g);
      if(m){const a=m.length>3?Number(m[3]):1;if(a>0.9){bg=m.map(Number);break}}
      n=n.parentElement;
     }
     if(grad||!bg)continue;
     out.push({t:(el.textContent||'').trim().slice(0,40),cls:el.className&&el.className.baseVal===undefined?String(el.className):'',tag:el.tagName,col:col.slice(0,3),bg:bg.slice(0,3),op:Number(cs.opacity)});
    }
    return out;
   });
   for(const e of rows){
    // blend opacity toward bg
    const col=e.op<1? e.col.map((c,i)=>Math.round(c*e.op+e.bg[i]*(1-e.op))) : e.col;
    const rt=ratio(col,e.bg);
    if(rt<4.5){lows++;console.log(`LOWCONTRAST ${p} <${e.tag} class="${e.cls}"> "${e.t}" ${rt.toFixed(2)}:1 col=${col} bg=${e.bg}`)}
   }
   if(p.startsWith('for/')){
    const gold=await pg.evaluate(()=>{
     const bad=[];
     for(const el of document.querySelectorAll('main *')){
      const c=getComputedStyle(el).color;
      if(c==='rgb(255, 217, 118)'&&el.textContent.trim())bad.push(el.tagName+'.'+el.className);
     }
     return bad;});
    if(gold.length){console.log('GOLD TYPE on door: '+gold.join(', '));fails++}
   }
  }
  await pg.close();
 }
}
console.log(`gate done: ${PAGES.length*VPS.length} overflow/JS checks, ${fails} failures, ${lows} low-contrast`);
await browser.close();
