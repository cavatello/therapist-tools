#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Page CSS — LIGHT, matching the tax and grow pages.

Same move as those two: chapter identity used to be a saturated slab per
section; on white that reads as five different websites, so it becomes a 3px
rule across the top of a white card in the same colour. The hero stays coloured
— it is the only saturated surface on the page and it carries the illustration.

Every class name is unchanged from the dark version, so no renderer moved.

Palette is the site design system:
  paper #FBF9F3 · white #FFFFFF · ink #26241E · muted #6E695E · line #E7E2D6
  field #FBF6E9 on #E4D9BE · pine #2C6350 · gold #B08430 (accent TEXT)
  pop #F6C560 is FILLS ONLY — 1.5:1 on white, it cannot carry a word.

Scoped under .adv so it cannot reach the shared masthead.
"""

CSS = r"""
.adv{--paper:#FBF9F3;--white:#FFFFFF;--ink:#26241E;--muted:#6E695E;--line:#E7E2D6;
 --field:#FBF6E9;--fieldline:#E4D9BE;
 --pine:#2C6350;--brick:#8E4B45;--gold:#B08430;--carbon:#26241E;--indigo:#4B3B93;
 --pop:#F6C560;--neg:#B5483F;--pos:#3F9577;
 background:var(--paper);color:var(--ink)}
.adv *{box-sizing:border-box}
.adv .in{max-width:1060px;margin:0 auto;padding:0 26px}
/* The hidden ATTRIBUTE is styled by the UA sheet as `[hidden]{display:none}`,
   the weakest rule in the cascade. Every field here is a `.f` label carrying
   `display:block` — a class selector — which beat it outright, so `el.hidden`
   did nothing and the salary box stayed on screen in hourly mode. This rule has
   to travel with the `.f` pattern wherever that pattern goes. */
.adv [hidden]{display:none !important}
.adv button{font:inherit}

/* ---------- hero: the one coloured surface ---------- */
.ahero{background:linear-gradient(135deg,#173B2E 0%,#2C6350 52%,#3F9577 100%);
 color:#EFF5F2;padding:40px 0 38px}
.ahero .in{display:grid;grid-template-columns:1.1fr .9fr;gap:32px;align-items:center}
.akick{font-size:9.5px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;
 color:var(--pop);margin:0 0 11px}
.ahero h1{font-family:Fraunces,Georgia,serif;font-size:clamp(28px,3.6vw,42px);line-height:1.04;
 letter-spacing:-.024em;margin:0 0 10px;color:#fff;font-weight:600;max-width:17ch}
.ahero h1 em{font-style:normal;color:var(--pop)}
.atag{font-family:Fraunces,Georgia,serif;font-size:clamp(16px,1.8vw,21px);color:var(--pop);
 margin:0 0 13px}
.alede{font-size:14.2px;line-height:1.72;color:rgba(255,255,255,.86);margin:0 0 16px;
 max-width:58ch}
.alede b{color:#fff}
.aherocta{display:flex;gap:9px;flex-wrap:wrap;align-items:stretch}
.aherocta a,.aherocta button{background:var(--pop);color:#2A2010;border:0;border-radius:11px;
 padding:11px 18px;font-size:13.5px;font-weight:800;cursor:pointer;text-decoration:none;
 display:inline-flex;align-items:center;min-height:44px;white-space:nowrap}
.aherocta .ghost{background:none;color:#fff;border:1.5px solid rgba(255,255,255,.5);
 font-weight:700}
.aherocta a:hover,.aherocta button:hover{filter:brightness(1.06)}
.apanel{background:rgba(0,0,0,.24);border:1px solid rgba(255,255,255,.18);border-radius:20px;
 padding:18px 20px 17px}
.aart{display:block;width:100%;height:auto;margin:0 0 14px;border-radius:12px}
.apanel .arow{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;
 align-items:baseline;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.14)}
.apanel .arow:last-of-type{border-bottom:0}
.apanel .arow span{font-size:11.4px;color:rgba(255,255,255,.62);line-height:1.4}
.apanel .arow b{font-family:Fraunces,Georgia,serif;font-size:23px;color:#fff;line-height:1;
 white-space:nowrap}
.apanel .arow b.gold{color:var(--pop)}
.apanel .anote{font-size:10.6px;color:rgba(255,255,255,.5);margin:11px 0 0;line-height:1.55}

/* ---------- slabs: white cards, identity in a 3px top rule ---------- */
.adv .slab{max-width:1060px;margin:16px auto 0;border-radius:16px;padding:28px 30px 32px;
 background:var(--white);border:1px solid var(--line);border-top:3px solid var(--line);
 box-shadow:0 1px 2px rgba(40,50,40,.03);scroll-margin-top:70px;color:var(--ink)}
.adv .slab.pine{border-top-color:var(--pine)}
.adv .slab.carbon{border-top-color:var(--carbon)}
.adv .slab.brick{border-top-color:var(--brick)}
.adv .slab.indigo{border-top-color:var(--indigo)}
.adv .slab.gold{border-top-color:var(--gold)}
.ch-h{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:5px}
.ch-h h2{font-family:Fraunces,Georgia,serif;font-size:clamp(21px,2.5vw,28px);margin:0;
 font-weight:600;letter-spacing:-.02em;color:var(--ink)}
.ch-n{font-size:9px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;
 color:var(--gold)}
.slab.pine .ch-n{color:var(--pine)}
.slab.brick .ch-n{color:var(--brick)}
.slab.indigo .ch-n{color:var(--indigo)}
.dek{font-size:13.4px;line-height:1.7;margin:0 0 18px;color:var(--muted);max-width:68ch}
.dek b{color:var(--ink);font-weight:600}

/* ---------- the one field pattern ---------- */
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
.f.sm .fv{font-size:16px}

/* ---------- the offer columns ---------- */
.jobs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:4px}
/* one job on the page = one column, capped at a readable form width rather
   than stretched across 1060px */
.jobs.solo{grid-template-columns:minmax(0,620px)}
.job{background:var(--paper);border:1px solid var(--line);border-radius:16px;
 padding:17px 18px 19px;min-width:0}
.job.b{border-style:dashed;border-color:var(--fieldline)}
.jobhead{display:flex;align-items:center;gap:10px;margin-bottom:13px;flex-wrap:wrap}
.jobtag{flex:none;width:26px;height:26px;border-radius:8px;background:var(--pine);color:#fff;
 font-family:Fraunces,Georgia,serif;font-size:14px;font-weight:700;display:flex;
 align-items:center;justify-content:center}
.jobhead .jn{flex:1;min-width:100px}
/* padding, not height: the name field is a bare input rather than a wrapped .f
   label, so nothing else gives it a 40px touch surface. */
.jobhead .jn input{width:100%;background:none;border:0;border-bottom:1.5px dashed
 var(--fieldline);color:var(--ink);font-family:Fraunces,Georgia,serif;font-size:16px;
 font-weight:600;padding:9px 0;outline:none;min-height:40px}
.jobhead .jn input:focus{border-bottom-color:var(--gold)}
.fgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}
.fgrid .wide{grid-column:1 / -1}
.fsub{font-size:8.5px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;
 color:var(--gold);margin:16px 0 8px}
.jobfoot{font-size:11.9px;line-height:1.64;color:var(--muted);margin:11px 0 0}
.jobfoot b{color:var(--ink)}
.addb{display:inline-flex;align-items:center;gap:8px;background:var(--white);
 border:1.5px solid var(--fieldline);border-radius:11px;padding:9px 16px;
 font-size:12.5px;font-weight:700;color:var(--ink);cursor:pointer;min-height:44px}
.addb:hover{background:var(--field);border-color:var(--gold)}

/* ---------- receipt rows ---------- */
.rec{display:grid;grid-template-columns:minmax(0,1fr) 108px;gap:12px;align-items:baseline;
 padding:9px 0;border-bottom:1px solid var(--line)}
.rec:last-child{border-bottom:0}
.rec b{font-size:13.2px;font-weight:600;color:var(--ink)}
.rec i{font-style:normal;font-size:11.5px;color:var(--muted);display:block;margin-top:3px;
 line-height:1.5}
.rec .v{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:13.2px;text-align:right;
 white-space:nowrap;color:var(--ink)}
.rec .v.neg{color:var(--neg)}
.rec.tot{border-top:2px solid var(--ink);border-bottom:0;margin-top:6px;padding-top:12px}
.rec.tot b{font-family:Fraunces,Georgia,serif;font-size:16px}
.rec.tot .v{font-family:Fraunces,Georgia,serif;font-size:19px;color:var(--gold)}

/* ---------- stat tiles ---------- */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;
 margin-top:16px}
.tile{border-radius:13px;padding:13px 15px 14px;background:var(--white);
 border:1px solid var(--line);min-width:0}
.tile.hi{background:#FDF4DF;border-color:#E8D3A0}
.tile em{display:block;font-style:normal;font-size:8.5px;font-weight:800;letter-spacing:.11em;
 text-transform:uppercase;color:#7C766A;margin-bottom:5px;line-height:1.35}
.tile b{font-family:Fraunces,Georgia,serif;font-size:24px;display:block;line-height:1.02;
 color:var(--ink)}
.tile.hi b{color:var(--gold)}
.tile u{text-decoration:none;display:block;font-size:10.5px;color:#8A8477;margin-top:4px;
 line-height:1.45}

/* ---------- compare table ---------- */
.cmpwrap{overflow-x:auto;overflow-y:hidden;margin-top:18px;-webkit-overflow-scrolling:touch}
.cmp{width:100%;border-collapse:collapse;min-width:520px}
.cmp th,.cmp td{text-align:right;padding:11px 12px;font-size:13px;
 border-bottom:1px solid var(--line)}
.cmp th:first-child,.cmp td:first-child{text-align:left}
.cmp thead th{font-family:Fraunces,Georgia,serif;font-size:15px;font-weight:600;
 border-bottom:2px solid var(--ink);color:var(--ink)}
.cmp td.n{font-family:'IBM Plex Mono',ui-monospace,monospace;white-space:nowrap;
 color:var(--ink)}
.cmp td .lab{font-weight:600;display:block;color:var(--ink)}
.cmp td .sub{font-size:11.2px;color:var(--muted);display:block;margin-top:3px;line-height:1.5}
.win{position:relative;background:#F3FAF6}
.win:after{content:"BETTER";position:absolute;top:50%;right:8px;transform:translateY(-50%);
 font-size:7.5px;font-weight:800;letter-spacing:.1em;background:var(--pos);color:#fff;
 padding:3px 6px;border-radius:4px}
.cmp td.win{padding-right:64px}
.verdict{margin-top:18px;background:#FDF4DF;border:1.5px solid #E8D3A0;border-radius:16px;
 padding:19px 21px}
.verdict h3{font-family:Fraunces,Georgia,serif;font-size:clamp(19px,2.4vw,25px);margin:0 0 9px;
 color:var(--ink);font-weight:600;letter-spacing:-.016em}
.verdict h3 b{color:var(--gold);font-weight:600}
.verdict p{font-size:13px;line-height:1.72;color:#4E4940;margin:0;max-width:70ch}
.verdict p + p{margin-top:10px}

/* ---------- the hours ladder ---------- */
.gates{display:grid;gap:11px;margin-top:18px}
.gate{background:var(--paper);border:1px solid var(--line);border-radius:14px;
 padding:14px 17px 15px}
.gate.block{border-color:#E8D3A0;background:#FDF4DF}
.gatehead{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:baseline;
 margin-bottom:9px}
.gatehead b{font-family:Fraunces,Georgia,serif;font-size:16px;color:var(--ink)}
.gatehead .num{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12.5px;
 white-space:nowrap;color:var(--muted)}
.gtrack{height:15px;background:var(--white);border:1px solid var(--line);border-radius:5px;
 overflow:hidden;position:relative}
.gtrack i{display:block;height:100%;border-radius:4px;transition:width .35s ease;
 background:var(--pos)}
.gate.block .gtrack i{background:var(--gold)}
.gate p{font-size:11.7px;line-height:1.62;color:var(--muted);margin:9px 0 0;max-width:76ch}
.gate .eta{font-size:12px;color:#4E4940;margin:8px 0 0;font-weight:600}
.gate .eta b{color:var(--gold)}
.finish{margin-top:16px;background:#FDF4DF;border:1.5px solid #E8D3A0;border-radius:16px;
 padding:19px 21px}
.finish em{display:block;font-style:normal;font-size:9px;font-weight:800;letter-spacing:.14em;
 text-transform:uppercase;color:#8A6620;margin-bottom:7px}
.finish b{font-family:Fraunces,Georgia,serif;font-size:clamp(26px,4vw,40px);color:var(--ink);
 display:block;line-height:1.05}
.finish p{font-size:12.8px;line-height:1.7;color:#4E4940;margin:10px 0 0;max-width:72ch}
.finish p b{display:inline;font-family:inherit;font-size:inherit;color:#8A6620}

/* ---------- warnings ---------- */
.warns{display:grid;gap:9px;margin-top:16px}
.warn{display:flex;gap:11px;align-items:flex-start;border-radius:12px;padding:12px 15px;
 font-size:12.5px;line-height:1.64;background:#FBEFEC;border:1px solid #EBC7BE;
 color:#4E4940}
.warn.ok{background:#EFF7F3;border-color:#BEDFD1}
.warn .ic{flex:none;font-style:normal;font-weight:800;color:var(--neg)}
.warn.ok .ic{color:var(--pos)}
.warn b{color:var(--ink)}

/* ---------- rules and flags ---------- */
.rules{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:18px}
.rule{background:var(--paper);border:1px solid var(--line);border-radius:14px;
 padding:15px 17px 16px;min-width:0}
.rule b{display:block;font-family:Fraunces,Georgia,serif;font-size:15.5px;margin-bottom:7px;
 color:var(--ink);line-height:1.28}
.rule p{font-size:12.5px;line-height:1.7;color:var(--muted);margin:0}
.rule .src{display:inline-block;margin-top:9px;font-family:'IBM Plex Mono',ui-monospace,monospace;
 font-size:9.5px;letter-spacing:.04em;color:var(--gold)}
.flags{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:16px}
.flag{background:var(--paper);border:1px solid var(--line);border-left:3px solid var(--neg);
 border-radius:0 13px 13px 0;padding:13px 16px 14px;min-width:0}
.flag b{display:block;font-family:Fraunces,Georgia,serif;font-size:15px;margin-bottom:6px;
 color:var(--ink)}
.flag p{font-size:12.4px;line-height:1.68;color:var(--muted);margin:0}
.ribbon{display:inline-block;background:var(--indigo);color:#fff;font-size:9.5px;font-weight:800;
 letter-spacing:.16em;text-transform:uppercase;padding:5px 13px;border-radius:5px;
 margin-bottom:12px}

/* ---------- pay reference + fees ---------- */
.paytab{width:100%;border-collapse:collapse;margin-top:15px}
.paytab th,.paytab td{text-align:left;padding:10px 12px;font-size:12.7px;
 border-bottom:1px solid var(--line);color:#4E4940}
.paytab td:last-child,.paytab th:last-child{text-align:right;
 font-family:'IBM Plex Mono',ui-monospace,monospace;white-space:nowrap}
.paytab thead th{font-size:8.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;
 color:#8A8477}
.paytab td i{font-style:normal;display:block;font-size:11.2px;color:#8A8477;margin-top:3px}

/* ---------- deep detail ---------- */
.how{margin-top:17px;background:var(--paper);border:1px solid var(--line);border-radius:13px;
 overflow:hidden}
.how > summary{list-style:none;cursor:pointer;padding:13px 16px;display:flex;
 align-items:baseline;gap:10px;flex-wrap:wrap;min-height:44px}
.how > summary::-webkit-details-marker{display:none}
.how > summary:after{content:"\25BE";margin-left:auto;color:#9A9384;font-size:11px;
 transition:transform .2s}
.how[open] > summary:after{transform:rotate(180deg)}
.how[open]{background:var(--white)}
.how > summary b{font-family:Fraunces,Georgia,serif;font-size:15px;color:var(--ink)}
.how > summary span{font-size:11.7px;color:var(--muted)}
.howb{padding:2px 17px 17px;border-top:1px solid var(--line)}
.howb p,.howb li{font-size:12.7px;line-height:1.74;color:#4E4940;max-width:76ch}
.howb ul{margin:0;padding-left:19px}
.howb li{margin-bottom:8px}
.howb b{color:var(--ink)}

/* ---------- closing CTA ---------- */
.acta{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;
 width:100%;text-align:center;background:var(--pop);color:#2A2010;border-radius:16px;
 padding:clamp(20px,2.6vw,30px) clamp(18px,3vw,38px);text-decoration:none;margin-top:18px;
 box-shadow:0 6px 0 rgba(140,96,18,.35);transition:transform .1s,box-shadow .1s,background .15s;
 min-height:44px}
.acta:hover{background:#FFD57A}
.acta:active{transform:translateY(5px);box-shadow:0 1px 0 rgba(140,96,18,.35)}
.acta:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.acta strong{font-family:Fraunces,Georgia,serif;font-size:clamp(22px,3vw,38px);font-weight:600;
 line-height:1.1;letter-spacing:-.018em;max-width:22ch}
.acta span{font-size:clamp(12px,1.1vw,14.5px);font-weight:700;opacity:.66}
.alist{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 22px;margin:18px 0 0;
 padding:17px 0 0;border-top:1px solid var(--line)}
.alist div{display:flex;gap:9px;font-size:12.6px;line-height:1.6;color:var(--muted)}
.alist i{font-style:normal;color:var(--gold);flex:none}
.alist b{color:var(--ink);font-weight:600}

/* ---------- citations + footer ---------- */
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
 .ahero .in{grid-template-columns:1fr;gap:24px}
 .jobs,.rules,.flags,.alist{grid-template-columns:1fr}
}
@media (max-width:640px){
 .adv .slab{border-radius:0;border-left:0;border-right:0;padding:22px 18px 26px;
   box-shadow:none;margin-top:12px}
 .adv .in{padding:0 18px}
 .cites,.disc{padding-left:18px;padding-right:18px}
 .fgrid{grid-template-columns:1fr}
 .rec{grid-template-columns:minmax(0,1fr) 92px;gap:10px}
 .tiles{grid-template-columns:1fr}
}
@media (prefers-reduced-motion:reduce){.adv *{transition:none !important;animation:none !important}}

/* --- the Board's supervision minimum, checked against the offer.
   `supreq` rather than `req` or `note`: the chrome styles both of those. */
.supreq{margin:10px 0 0;padding:11px 13px;border-radius:10px;font-size:13.4px;
  line-height:1.55;border-left:3px solid var(--line);background:var(--paper)}
.supreq:empty{display:none;padding:0;border:0}
.supreq.ok{border-left-color:var(--pos);background:#F1F7F4;color:#2F5E4E}
.supreq.short{border-left-color:var(--neg);background:#FBF1F0;color:#7A3A34}
.supreq b{font-weight:700}

/* ---------- placeholders that cannot be mistaken for values ----------
   The hours plan looked broken to a reader who had filled in the banked hours
   but not the weekly caseload: the four empty boxes showed 12 / 12 / 0 / 10 in
   the same 19px Fraunces 600 as a real entry, just a little greyer, so the
   section appeared to have data and to be refusing to compute. Italic at a
   lighter weight is the cheapest unmistakable signal in a serif face. */
.f input::placeholder{font-style:italic;font-weight:400;color:#BDB6A6;opacity:1}
.f input::-webkit-input-placeholder{font-style:italic;font-weight:400;color:#BDB6A6}

/* A field the section is waiting on. Set by render(), cleared as soon as the
   section can compute, so it is a prompt rather than an error. */
.f.wait{border-style:dashed;border-color:var(--gold);background:#FFFCF4}
.f.wait em{color:#8A6A2A}
.waitnote{margin:10px 0 0;font-size:12.6px;line-height:1.55;color:#8A6A2A;
  background:#FFFCF4;border-left:3px solid var(--gold);border-radius:0 8px 8px 0;
  padding:9px 12px}
.waitnote:empty{display:none;padding:0;border:0}

/* biweekly / semi-monthly / monthly, on each offer */
.biwk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:14px 0 0;
  padding-top:14px;border-top:1px solid var(--line)}
@media (max-width:520px){.biwk{grid-template-columns:minmax(0,1fr)}}
.bw{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.bw em{display:block;font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:9.5px;
  font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.bw b{display:block;font-family:Fraunces,Georgia,serif;font-size:20px;line-height:1;
  margin:4px 0 3px}
.bw i{display:block;font-style:normal;font-size:11px;color:var(--muted)}
"""
