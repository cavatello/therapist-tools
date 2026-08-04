#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Page CSS — LIGHT.

Rewritten from the dark version. Every class name is unchanged, so no renderer
had to move: this is a theme swap, not a rebuild.

Chapter identity used to come from a saturated slab per section (pine, carbon,
brick, indigo). On white that reads as four different websites, so the identity
moves to a 3px rule across the top of an otherwise white card, in the same
colour. The page becomes one surface with five markers on it rather than five
surfaces.

The palette is the site's own design system, not a new one:

  paper   #FBF9F3   the page
  white   #FFFFFF   section surfaces and read-only cards
  ink     #26241E   text
  muted   #6E695E   secondary text
  line    #E7E2D6   borders
  field   #FBF6E9   editable inputs, with #E4D9BE at the edge
  pine    #2C6350   primary accent
  gold    #B08430   figures and accent TEXT  (#F6C560 is fills only - it is
                    1.5:1 on white and cannot carry a word)
  pos/neg #3F9577 / #B5483F

Everything scoped under .tax so it cannot reach the shared masthead. Bare
single-class selectors are checked against the site chrome at build time.
"""

CSS = r"""
.tax{--paper:#FBF9F3;--white:#FFFFFF;--ink:#26241E;--muted:#6E695E;--line:#E7E2D6;
 --field:#FBF6E9;--fieldline:#E4D9BE;
 --pine:#2C6350;--brick:#8E4B45;--gold:#B08430;--carbon:#26241E;--indigo:#4B3B93;
 --pop:#F6C560;--neg:#B5483F;--pos:#3F9577;
 background:var(--paper);color:var(--ink)}
.tax *{box-sizing:border-box}
.tax .in{max-width:1060px;margin:0 auto;padding:0 26px}
.tax button{font:inherit}

/* ---------- hero: the one dark surface on the page ---------- */
.thero{background:linear-gradient(135deg,#141712 0%,#1E241C 55%,#2C6350 100%);color:#EFF5F2;
 padding:44px 0 40px}
.thero .in{display:grid;grid-template-columns:1.12fr .88fr;gap:32px;align-items:center}
.tkick{font-size:9.5px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;
 color:var(--pop);margin:0 0 11px}
.thero h1{font-family:Fraunces,Georgia,serif;font-size:clamp(28px,3.7vw,44px);line-height:1.04;
 letter-spacing:-.024em;margin:0 0 11px;color:#fff;font-weight:600;max-width:17ch}
.thero h1 em{font-style:normal;color:var(--pop)}
.tlede{font-size:14.2px;line-height:1.72;color:rgba(255,255,255,.85);margin:0 0 16px;
 max-width:58ch}
.tlede b{color:#fff}
.therocta{display:flex;gap:9px;flex-wrap:wrap}
.therocta a{background:var(--pop);color:#2A2010;border-radius:11px;padding:11px 18px;
 font-size:13.5px;font-weight:800;text-decoration:none;display:inline-flex;align-items:center;
 min-height:44px}
.therocta .ghost{background:none;color:#fff;border:1.5px solid rgba(255,255,255,.5);
 font-weight:700}
.tpanel{background:rgba(0,0,0,.26);border:1px solid rgba(255,255,255,.18);border-radius:20px;
 padding:20px 22px}
.tpanel .pr{padding:11px 0;border-bottom:1px solid rgba(255,255,255,.14)}
.tpanel .pr:last-of-type{border-bottom:0}
.tpanel .pr em{display:block;font-style:normal;font-size:10px;font-weight:800;
 letter-spacing:.11em;text-transform:uppercase;color:rgba(255,255,255,.5);margin-bottom:5px}
.tpanel .pr b{font-family:Fraunces,Georgia,serif;font-size:clamp(28px,3.6vw,38px);color:#fff;
 line-height:1;display:block}
.tpanel .pr b.gold{color:var(--pop)}
.tpanel .pn{font-size:10.6px;color:rgba(255,255,255,.5);margin:12px 0 0;line-height:1.55}

/* ---------- slabs: white cards, identity in a 3px top rule ---------- */
.tax .slab{max-width:1060px;margin:16px auto 0;border-radius:16px;padding:28px 30px 32px;
 background:var(--white);border:1px solid var(--line);border-top:3px solid var(--line);
 box-shadow:0 1px 2px rgba(40,50,40,.03);scroll-margin-top:70px;color:var(--ink)}
.tax .slab.pine{border-top-color:var(--pine)}
.tax .slab.carbon{border-top-color:var(--carbon)}
.tax .slab.brick{border-top-color:var(--brick)}
.tax .slab.indigo{border-top-color:var(--indigo)}
.tax .slab.gold{border-top-color:var(--gold)}
.tax .slab.paper{background:var(--paper)}
.chh{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:5px}
.chh h2{font-family:Fraunces,Georgia,serif;font-size:clamp(21px,2.5vw,28px);margin:0;
 font-weight:600;letter-spacing:-.02em;color:var(--ink)}
.chn{font-size:9px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;
 color:var(--gold)}
.slab.pine .chn{color:var(--pine)}
.slab.brick .chn{color:var(--brick)}
.slab.indigo .chn{color:var(--indigo)}
.dek{font-size:13.4px;line-height:1.7;margin:0 0 18px;color:var(--muted);max-width:68ch}
.dek b{color:var(--ink);font-weight:600}
.empty{font-size:13.4px;line-height:1.72;color:var(--muted);margin:0;max-width:64ch}
.note{font-size:12.4px;line-height:1.68;color:var(--muted);margin:14px 0 0;max-width:74ch}
.fine{font-size:11.9px;line-height:1.72;color:#8A8477;margin:16px 0 0;max-width:78ch}
.fine b{color:var(--muted)}

/* ---------- fields: the site's editable-input pattern ---------- */
.f{background:var(--field);border:1.5px solid var(--fieldline);border-radius:12px;
 padding:8px 12px 9px;position:relative;display:block;cursor:text;min-width:0;
 transition:border-color .15s,box-shadow .15s}
.f:hover{border-color:var(--gold)}
.f:focus-within{border-color:var(--gold);box-shadow:0 0 0 3px rgba(176,132,48,.16)}
.f em{display:block;font-style:normal;font-size:8.5px;font-weight:800;letter-spacing:.1em;
 text-transform:uppercase;color:#7C766A;margin-bottom:3px;line-height:1.35}
.f .fv{display:flex;align-items:baseline;gap:3px;font-family:Fraunces,Georgia,serif;
 font-weight:600;font-size:19px;color:var(--ink)}
.f input,.f select{width:100%;min-width:0;background:none;border:0;padding:0;font:inherit;
 color:inherit;-moz-appearance:textfield;outline:none}
.f input::-webkit-outer-spin-button,.f input::-webkit-inner-spin-button{
 -webkit-appearance:none;margin:0}
.f select{font-size:14.5px;cursor:pointer}
.f select option{color:#26241E}
.f .unit{flex:none;font-family:Inter,sans-serif;font-size:10.5px;font-weight:700;
 letter-spacing:.05em;text-transform:uppercase;color:#9A9384;white-space:nowrap}
.fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.fsub{font-size:8.5px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;
 color:var(--gold);margin:18px 0 9px}

/* ---------- equation, tiles, rows ---------- */
.eq{display:grid;grid-template-columns:minmax(0,1fr) 24px minmax(0,1fr) 24px minmax(0,1fr);
 gap:10px;align-items:center;background:var(--paper);border:1px solid var(--line);
 border-radius:14px;padding:18px 20px}
.ei em{display:block;font-style:normal;font-size:8.5px;font-weight:800;letter-spacing:.11em;
 text-transform:uppercase;color:#7C766A;margin-bottom:5px;line-height:1.3}
.ei b{font-family:Fraunces,Georgia,serif;font-size:clamp(19px,2.6vw,28px);line-height:1;
 color:var(--ink);display:block}
.ei b.neg{color:var(--neg)}.ei b.gold{color:var(--gold)}
.eo{font-family:Fraunces,Georgia,serif;font-size:19px;color:#B6AF9E;text-align:center}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;
 margin-top:16px}
.tiles > .tl{border-radius:13px;padding:14px 16px 15px;background:var(--white);
 border:1px solid var(--line);min-width:0}
.tiles > .tl.hi,.tiles > .tl.big{background:#FDF4DF;border-color:#E8D3A0}
.tiles > .tl.good{background:#EFF7F3;border-color:#BEDFD1}
.tiles > .tl.warn{background:#FBEFEC;border-color:#EBC7BE}
.tiles > .tl em{display:block;font-style:normal;font-size:8.5px;font-weight:800;
 letter-spacing:.11em;text-transform:uppercase;color:#7C766A;margin-bottom:5px;line-height:1.35}
.tiles > .tl b{font-family:Fraunces,Georgia,serif;font-size:25px;display:block;line-height:1.02;
 color:var(--ink)}
.tiles > .tl.hi b,.tiles > .tl.big b{color:var(--gold)}
.tiles > .tl.good b{color:var(--pos)}
.tiles > .tl.warn b{color:var(--neg)}
.tiles > .tl u{text-decoration:none;display:block;font-size:10.6px;color:#8A8477;margin-top:4px;
 line-height:1.45}
/* the reference prose ships an <ol class="tl"> task list; it must not meet the
   tile rule above, which is why every tile selector is a direct child of .tiles */
.txb ol.tl{margin:12px 0 0;padding:0;list-style:none;counter-reset:tl}
.txb ol.tl li{counter-increment:tl;position:relative;padding-left:30px;margin:0 0 9px;
 font-size:12.6px;line-height:1.68;color:var(--muted)}
.txb ol.tl li:before{content:counter(tl);position:absolute;left:0;top:1px;width:21px;
 height:21px;border-radius:6px;background:#F3E8CC;color:#8A6620;
 font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;font-weight:600;
 display:flex;align-items:center;justify-content:center}
.rws{margin-top:17px}
.rw{display:grid;grid-template-columns:minmax(0,1fr) 118px;gap:12px;align-items:baseline;
 padding:11px 0;border-bottom:1px solid var(--line)}
.rw:last-child{border-bottom:0}
.rw b{font-size:13.2px;font-weight:600;color:var(--ink)}
.rw i{font-style:normal;font-size:11.6px;color:var(--muted);display:block;margin-top:3px;
 line-height:1.55}
.rw .v{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:13.2px;text-align:right;
 white-space:nowrap;color:var(--ink)}
.rw.neg .v{color:var(--neg)}
.rw.tot{border-top:2px solid var(--ink);border-bottom:0;margin-top:6px;padding-top:13px}
.rw.tot b{font-family:Fraunces,Georgia,serif;font-size:16px}
.rw.tot .v{font-family:Fraunces,Georgia,serif;font-size:20px;color:var(--gold)}

/* ---------- the split bar ---------- */
.bar{display:flex;height:52px;border-radius:10px;overflow:hidden;margin:0 0 9px;
 border:1px solid var(--line)}
.bar div{display:flex;flex-direction:column;align-items:center;justify-content:center;
 font-size:10.5px;font-weight:800;line-height:1.2;padding:0 6px;text-align:center;min-width:0}
.bar .a{background:#EDEAE0;color:#5C574D}
.bar .b{background:#F7F4EC;color:#8A8477}
.bar .c{background:var(--pop);color:#2A2010}
.bar strong{font-family:Fraunces,Georgia,serif;font-size:16px;font-weight:600}
.barn{font-size:11.8px;color:var(--muted);margin:0}

/* ---------- planner ---------- */
.cur{margin-top:15px;background:#FDF4DF;border:1px solid #E8D3A0;border-radius:13px;
 padding:15px 17px}
.cur b{display:block;font-family:Fraunces,Georgia,serif;font-size:16px;margin-bottom:6px;
 color:var(--ink)}
.cur span{display:block;font-size:12.6px;line-height:1.68;color:#5C574D;max-width:74ch}
.cur .gap{margin-top:7px;color:#8A6620;font-weight:600}
.cur .gap.done{color:var(--pos)}
.maxbtn{margin-top:10px;background:var(--pop);color:#2A2010;border:0;border-radius:11px;
 padding:11px 18px;font-size:13px;font-weight:800;cursor:pointer;min-height:44px;
 box-shadow:0 2px 0 rgba(140,96,18,.3)}
.maxbtn:hover{filter:brightness(1.04)}

/* ---------- sorting bar ---------- */
.sbar{background:var(--paper);border:1px solid var(--line);border-radius:14px;
 padding:15px 17px;margin:0 0 16px}
.tsr{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.tsr + .tsr{margin-top:9px;padding-top:9px;border-top:1px solid var(--line)}
.tsr > b{font-size:9.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;
 color:#8A8477;min-width:112px}
.sb{background:var(--white);border:1px solid var(--fieldline);color:var(--ink);
 border-radius:999px;padding:9px 15px;font-size:12.5px;font-weight:600;cursor:pointer;
 min-height:40px}
.sb:hover{background:var(--field);border-color:var(--gold)}
.sb.on{background:var(--ink);border-color:var(--ink);color:#fff}
.sout{margin-top:11px;padding-top:11px;border-top:1px solid var(--line);
 font-size:9.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#8A8477}
.sout b{display:block;font-family:Fraunces,Georgia,serif;font-size:28px;color:var(--gold);
 letter-spacing:0;text-transform:none;margin:4px 0 2px}
.sout span{display:block;font-size:11.8px;font-weight:600;letter-spacing:0;
 text-transform:none;color:var(--muted)}
.blk{border:1px solid var(--line);border-radius:13px;margin:0 0 11px;background:var(--white);
 overflow:hidden}
.blk.in{border-color:#E8D3A0}
.blk.top{border-color:#BEDFD1;background:#F6FBF8}
.blkh{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:14px;align-items:center;
 padding:15px 18px;cursor:pointer;list-style:none;min-height:44px}
.blkh::-webkit-details-marker{display:none}
.rank{width:26px;height:26px;border-radius:8px;background:var(--paper);color:#8A8477;
 font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center;
 flex:none}
.blk.in .rank{background:var(--gold);color:#fff}
.blk.top .rank{background:var(--pos);color:#fff}
.bt b{display:block;font-family:Fraunces,Georgia,serif;font-size:16.5px;font-weight:600;
 line-height:1.25;color:var(--ink)}
.bt i{display:block;font-style:normal;font-size:12.2px;line-height:1.55;color:var(--muted);
 margin-top:3px}
.bv{font-family:Fraunces,Georgia,serif;font-size:20px;font-weight:600;white-space:nowrap;
 text-align:right;color:var(--gold)}
.blk.top .bv{color:var(--pos)}
.bv small{display:block;font-family:Inter,sans-serif;font-size:9px;font-weight:700;
 letter-spacing:.09em;text-transform:uppercase;color:#9A9384;margin-top:3px}
.blk.out{background:var(--paper);border-style:dashed}
.blk.out .blkh{padding:12px 18px;cursor:default}
.blk.out .bt b{font-family:Inter,sans-serif;font-size:13.5px;color:#8A8477}
.blk.out .bt i{font-size:11.9px;color:#9A9384}
.blk.out .bv{font-family:Inter,sans-serif;font-size:9.5px;font-weight:800;letter-spacing:.1em;
 text-transform:uppercase;color:#A9A292}
.blkb{padding:0 18px 17px;border-top:1px solid var(--line);padding-top:14px}
.blkb p{font-size:12.9px;line-height:1.74;color:#4E4940;margin:0;max-width:76ch}
.blkb ul{margin:11px 0 0;padding:0;list-style:none}
.blkb li{position:relative;padding-left:18px;margin:0 0 7px;font-size:12.6px;line-height:1.68;
 color:var(--muted)}
.blkb li:before{content:"";position:absolute;left:0;top:7px;width:7px;height:7px;
 border-radius:2px;background:var(--gold)}
.blkb b{color:var(--ink)}
.half{margin-top:11px !important;font-size:12px !important;color:#8A8477 !important}

/* ---------- verdict + structure ---------- */
.verdict{border-radius:16px;padding:19px 21px;margin-bottom:6px}
.verdict.good{background:#EFF7F3;border:1.5px solid #BEDFD1}
.verdict.bad{background:#FBEFEC;border:1.5px solid #EBC7BE}
.verdict.flat{background:var(--paper);border:1.5px solid var(--line)}
.verdict em{display:block;font-style:normal;font-size:9px;font-weight:800;letter-spacing:.13em;
 text-transform:uppercase;color:#7C766A;margin-bottom:7px}
.verdict b{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(24px,3.4vw,38px);
 color:var(--ink);line-height:1.05}
.verdict.good b{color:#2F6E56}
.verdict.bad b{color:#9C3F37}
.verdict p{font-size:13px;line-height:1.72;color:#4E4940;margin:9px 0 0;max-width:72ch}
.slider{margin-top:17px;background:var(--paper);border:1px solid var(--line);
 border-radius:13px;padding:15px 17px}
.slider label{display:block;font-size:8.5px;font-weight:800;letter-spacing:.12em;
 text-transform:uppercase;color:#7C766A;margin-bottom:9px}
.slider input[type=range]{width:100%;min-height:40px;accent-color:#B08430}
.slider .out{font-family:Fraunces,Georgia,serif;font-size:19px;color:var(--gold);margin-top:4px}
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:16px}
.side{background:var(--paper);border:1px solid var(--line);border-radius:13px;
 padding:15px 17px;min-width:0}
.side em{display:block;font-style:normal;font-size:8.5px;font-weight:800;letter-spacing:.12em;
 text-transform:uppercase;color:#7C766A;margin-bottom:6px}
.side b{display:block;font-family:Fraunces,Georgia,serif;font-size:26px;color:var(--gold);
 line-height:1.05;margin-bottom:7px}
.side span{font-size:12.4px;line-height:1.68;color:#4E4940}
.side span b{display:inline;font-family:inherit;font-size:inherit;color:var(--gold)}

/* ---------- reference blocks ---------- */
.txref{background:var(--paper);border:1px solid var(--line);border-radius:13px;
 overflow:hidden;margin-bottom:10px}
.txref > summary{list-style:none;cursor:pointer;padding:14px 17px;display:grid;
 grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center;min-height:44px}
.txref > summary::-webkit-details-marker{display:none}
.txref > summary:after{content:"\25BE";color:#9A9384;font-size:11px;transition:transform .2s}
.txref[open] > summary:after{transform:rotate(180deg)}
.txref[open]{background:var(--white)}
.txref > summary b{display:block;font-family:Fraunces,Georgia,serif;font-size:15.5px;
 color:var(--ink)}
.txref > summary i{display:block;font-style:normal;font-size:11.9px;color:var(--muted);
 margin-top:3px;line-height:1.5}
.txb{padding:2px 17px 17px;border-top:1px solid var(--line)}
.txb p,.txb li{font-size:12.8px;line-height:1.74;color:#4E4940;max-width:78ch}
.txb b{color:var(--ink)}
.txb a{color:var(--pine);font-weight:600}
.txb .tw{overflow-x:auto;overflow-y:hidden;margin:12px 0 0}
.txb table.cmp{width:100%;border-collapse:collapse;min-width:460px;font-size:12.4px}
.txb table.cmp th,.txb table.cmp td{text-align:right;padding:9px 11px;
 border-bottom:1px solid var(--line)}
.txb table.cmp thead th,.txb table.cmp tbody th{text-align:left;font-weight:600}
.txb table.cmp thead th{font-size:8.5px;font-weight:800;letter-spacing:.11em;
 text-transform:uppercase;color:#8A8477}
/* the shared chrome defines a bare .band for its hero; the lifted prose tables
   use <tr class="band"> as a divider. Restated here, not reordered. */
.txb table.cmp tr.band{background:none;color:inherit;padding:0}
.txb table.cmp tr.band td{background:var(--paper);font-weight:700;text-align:left;
 font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#7C766A}
.txb table.cmp tfoot td{font-size:11.6px;color:#8A8477;line-height:1.6;text-align:left;
 padding-top:11px}
.txb p.flag{background:#FDF4DF;border-left:3px solid var(--gold);border-radius:0 10px 10px 0;
 padding:13px 16px;margin:14px 0 0;font-size:12.7px;line-height:1.7;color:#4E4940}
.txb p.flag b{color:#8A6620}
.txb .brs{margin-top:12px}
.txb .br{display:grid;grid-template-columns:minmax(0,150px) minmax(0,1fr) 92px;gap:11px;
 align-items:center;padding:6px 0;font-size:12.3px}
.txb .br > span{color:#4E4940}
.txb .br .track{height:14px;background:var(--paper);border:1px solid var(--line);
 border-radius:4px;overflow:hidden}
.txb .br .track > div{height:100%;border-radius:4px}
.txb .br .track .pos{background:var(--pos)}
.txb .br .track .neg{background:var(--neg)}
.txb .br .track .flat{background:#D6D0C0}
.txb .br > b{font-family:'IBM Plex Mono',ui-monospace,monospace;text-align:right;
 font-size:12.3px}
.txb .br > b.pos{color:#2F6E56}.txb .br > b.neg{color:#9C3F37}
.txb .br > i{grid-column:1 / -1;font-style:normal;font-size:11.4px;color:#8A8477;margin-top:-2px}

/* ---------- closing CTA ---------- */
.tcta{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;
 width:100%;text-align:center;background:var(--pop);color:#2A2010;border-radius:16px;
 padding:clamp(20px,2.6vw,30px) clamp(18px,3vw,38px);text-decoration:none;margin-top:18px;
 box-shadow:0 6px 0 rgba(140,96,18,.35);transition:transform .1s,box-shadow .1s,background .15s;
 min-height:44px}
.tcta:hover{background:#FFD57A}
.tcta:active{transform:translateY(5px);box-shadow:0 1px 0 rgba(140,96,18,.35)}
.tcta:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.tcta strong{font-family:Fraunces,Georgia,serif;font-size:clamp(22px,3vw,38px);font-weight:600;
 line-height:1.1;letter-spacing:-.018em;max-width:22ch}
.tcta span{font-size:clamp(12px,1.1vw,14.5px);font-weight:700;opacity:.66}
.alist{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 22px;margin:18px 0 0;
 padding:17px 0 0;border-top:1px solid var(--line)}
.alist div{display:flex;gap:9px;font-size:12.7px;line-height:1.6;color:var(--muted)}
.alist i{font-style:normal;color:var(--gold);flex:none}
.alist b{color:var(--ink);font-weight:600}

/* ---------- citations + disclaimer ---------- */
.cites{max-width:1060px;margin:20px auto 0;padding:0 26px}
.cites h3{font-family:Fraunces,Georgia,serif;font-size:17px;margin:0 0 10px;color:var(--ink)}
.cite{display:grid;grid-template-columns:34px minmax(0,1fr);gap:8px;padding:8px 0;
 border-bottom:1px solid var(--line);font-size:12.3px;line-height:1.64;color:var(--muted)}
.cite:last-of-type{border-bottom:0}
.cite .n{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;color:var(--gold)}
.cite a{color:var(--pine);font-weight:600}
.cite b{color:var(--ink)}
.disc{max-width:1060px;margin:6px auto 0;padding:14px 26px 40px;font-size:11.8px;
 line-height:1.72;color:#8A8477}
.disc b{color:var(--ink)}

/* ---------- responsive ---------- */
@media (max-width:900px){
 .thero .in{grid-template-columns:1fr;gap:24px}
 .two{grid-template-columns:1fr}
 .alist{grid-template-columns:1fr}
}
@media (max-width:700px){
 .eq{grid-template-columns:1fr;gap:12px}
 .eo{text-align:left;font-size:16px}
}
@media (max-width:640px){
 .tax .slab{border-radius:0;border-left:0;border-right:0;padding:22px 18px 26px;
   box-shadow:none;margin-top:12px}
 .tax .in{padding:0 18px}
 .cites,.disc{padding-left:18px;padding-right:18px}
 .tsr > b{min-width:100%}
 .blkh{grid-template-columns:auto minmax(0,1fr)}
 .bv{grid-column:2;text-align:left;margin-top:6px}
 .rw{grid-template-columns:minmax(0,1fr) 96px;gap:10px}
 .bar{height:66px}
}
/* --- 06 working remotely. Class names checked against the lifted chrome by
   the guard in build_tax.py; `r`-prefixed here because .row, .bar and .name
   are all taken somewhere on this site. */
.rrow{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(90px,1.5fr) minmax(0,120px);
  gap:14px;align-items:center;padding:11px 0;border-bottom:1px solid var(--line)}
.rrow:first-child{border-top:1px solid var(--line)}
.rrow.rhome{background:#F4F1E7;border-radius:8px;padding-left:10px;padding-right:10px}
.rname b{display:block;font-size:15px;font-weight:700;line-height:1.25}
.rname b i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:10px;
  font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--pine);
  border:1px solid var(--pine);border-radius:999px;padding:2px 7px;margin-left:6px;
  vertical-align:2px}
.rname em{display:block;font-style:normal;font-size:12.3px;line-height:1.45;
  color:var(--muted);margin-top:3px}
.rbar{height:26px;background:#EDEAE0;border-radius:6px;overflow:hidden}
.rbar span{display:block;height:100%;background:var(--pine);border-radius:6px}
.rhome .rbar span{background:var(--gold)}
.rfig{text-align:right}
.rfig b{display:block;font-family:Fraunces,Georgia,serif;font-size:19px;line-height:1}
.rfig em{display:block;font-style:normal;font-size:11.6px;margin-top:4px}
.rfig .rup{color:var(--pos);font-weight:600}
.rfig .rdn{color:var(--neg)}
.rfig .rz{color:var(--muted)}
@media (max-width:700px){
  .rrow{grid-template-columns:minmax(0,1fr) auto;gap:6px 12px}
  .rbar{grid-column:1/-1;height:18px}
  .rfig{text-align:right}
}
@media (prefers-reduced-motion:reduce){.tax *{transition:none !important}}

/* the old h1, demoted to a deck: the subject moved up into the h1 so the
   page is findable, and this line kept because it is the better sentence. */
.ttag{font-family:Fraunces,Georgia,serif;font-size:clamp(17px,1.7vw,22px);
  font-weight:400;font-style:italic;line-height:1.3;margin:0 0 .7em;opacity:.86}
"""
