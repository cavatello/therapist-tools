import { chromium } from 'playwright';
const files = process.argv.slice(2);
function lum(c){const m=c.match(/[\d.]+/g).map(Number);const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)};return 0.2126*f(m[0])+0.7152*f(m[1])+0.0722*f(m[2])}
const b = await chromium.launch();
const p = await (await b.newContext({viewport:{width:1440,height:1000}})).newPage();
for (const f of files){
  await p.goto('file://'+process.cwd()+'/'+f,{waitUntil:'load'});
  const bad = await p.evaluate((L)=>{
    const lum = eval('('+L+')');
    const out=[];
    const bg=(el)=>{let e=el;while(e){const c=getComputedStyle(e).backgroundColor;
      if(c && !/rgba\(0, 0, 0, 0\)|transparent/.test(c)) return c; e=e.parentElement;} return 'rgb(255,255,255)'};
    document.querySelectorAll('main *, header *').forEach(el=>{
      if(!el.childNodes.length) return;
      const t=[...el.childNodes].filter(n=>n.nodeType===3&&n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');
      if(!t) return;
      const s=getComputedStyle(el);
      if(s.display==='none'||s.visibility==='hidden'||parseFloat(s.opacity)===0) return;
      const fg=s.color, b=bg(el);
      const l1=lum(fg), l2=lum(b);
      const r=(Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
      const size=parseFloat(s.fontSize), bold=parseInt(s.fontWeight)>=700;
      const floor=(size>=24||(size>=18.66&&bold))?3:4.5;
      if(r<floor) out.push({r:+r.toFixed(2),floor,sel:el.tagName.toLowerCase()+'.'+(el.className||''),fg,bg:b,size,t:t.slice(0,60)});
    });
    return out;
  }, lum.toString());
  console.log('### '+f+'  ('+bad.length+' below floor)');
  bad.slice(0,12).forEach(x=>console.log('   %s  %s on %s  %spx  [%s]  "%s"', String(x.r).padEnd(5), x.fg, x.bg, x.size, x.sel.slice(0,34), x.t));
}
await b.close();
