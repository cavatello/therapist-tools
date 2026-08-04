#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Grow-page CSS. Built on the tax page's proven vocabulary, plus the funnel
pieces. Every class is checked at build time against the shared site chrome -
three separate silent failures on the tax page came from a name collision with
the lifted stylesheet, and that check now runs on every build."""

import importlib.util, os
# Loaded by path rather than by name: this module is also called css, and a plain
# import finds itself.
_spec = importlib.util.spec_from_file_location(
    "taxcss", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tax", "css.py"))
_tax = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_tax)
BASE = _tax.CSS

# The shared shell, renamed from .tax to .gro so the two pages cannot fight if
# they ever share a document (they do not today, but the cost of this is zero).
CSS = BASE.replace(".tax", ".gro").replace(".thero", ".ghero") \
          .replace(".tkick", ".gkick").replace(".tlede", ".glede") \
          .replace(".therocta", ".gherocta").replace(".tpanel", ".gpanel") \
          .replace(".tcta", ".gcta")

CSS += r"""
/* ---------- hero: LIGHT. The tax page keeps a black hero because it opens on a
   number you are about to lose. This page opens on an idea, and a dark band
   would make the two pages look like the same argument. ---------- */
.ghero{background:var(--paper);color:var(--ink);padding:44px 0 40px;
 border-bottom:1px solid var(--line)}
.ghero .in{display:grid;grid-template-columns:1.12fr .88fr;gap:32px;align-items:center}
.gkick{color:var(--pine)}
.ghero h1{color:var(--ink)}
.ghero h1 em{color:var(--pine)}
.glede{color:var(--muted)}
.glede b{color:var(--ink);font-weight:600}
.gherocta a{background:var(--ink);color:#fff;box-shadow:0 2px 0 rgba(38,36,30,.25)}
.gherocta .ghost{background:none;color:var(--ink);border:1.5px solid var(--fieldline);
 box-shadow:none}
.gherocta .ghost:hover{background:var(--field);border-color:var(--gold)}
.gpanel{background:var(--white);border:1px solid var(--line);border-radius:16px;
 padding:20px 22px}
.gpanel .pr{border-bottom:1px solid var(--line)}
.gpanel .pr em{color:#7C766A}
.gpanel .pr b{color:var(--ink)}
.gpanel .pr b.gold{color:var(--gold)}
.gpanel .pn{color:#8A8477}

/* ---------- the funnel stages ---------- */
.stages{display:grid;gap:9px;margin-top:4px}
.stg{--w:100%;position:relative;background:var(--white);border:1px solid var(--line);
 border-radius:12px;padding:14px 17px;width:var(--w);min-width:190px;
 transition:width .35s ease}
.stg em{display:block;font-style:normal;font-size:8.5px;font-weight:800;letter-spacing:.11em;
 text-transform:uppercase;color:#7C766A;margin-bottom:4px}
.stg b{font-family:Fraunces,Georgia,serif;font-size:26px;line-height:1;color:var(--ink);
 display:inline-block}
.stg i{font-style:normal;font-size:11.2px;color:#8A8477;margin-left:9px}
.stg:last-child{background:#EFF7F3;border-color:#BEDFD1}
.stg:last-child b{color:var(--pos)}

/* ---------- per-channel cards ---------- */
.chans{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:18px}
.ch{background:var(--white);border:1px solid var(--line);border-radius:14px;
 padding:15px 17px 16px;min-width:0}
.ch.fix{border-color:#E8D3A0;background:#FDF4DF}
.ch .chh{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin-bottom:3px}
.ch .chh b{font-family:Fraunces,Georgia,serif;font-size:16px;color:var(--ink)}
.gpill{font-size:8.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;
 background:var(--gold);color:#fff;border-radius:5px;padding:3px 7px;white-space:nowrap}
.chn2{font-size:11.4px;line-height:1.5;color:#8A8477;margin:0 0 11px}
.chrow{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:9px;align-items:baseline;
 padding:7px 0;border-bottom:1px solid var(--line);font-size:12.3px}
.chrow span{color:var(--muted)}
.chrow b{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:13px;color:var(--ink)}
.chrow i{font-style:normal;font-size:10.6px;color:#9A9384;min-width:32px;text-align:right}
.chv{font-size:12px;line-height:1.62;color:var(--muted);margin:11px 0 0}
.chv b{color:#2F6E56}
.chm{font-size:11.7px;line-height:1.64;color:var(--muted);margin:8px 0 0;padding-top:8px;
 border-top:1px dashed var(--fieldline)}
.chm b{color:#8A6620}

/* ---------- capacity ---------- */
.fillbar{position:relative;height:34px;background:var(--paper);border-radius:9px;
 overflow:hidden;border:1px solid var(--line)}
.fillbar i{display:block;height:100%;transition:width .4s ease;background:var(--pos)}
.fillbar span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 font-size:12px;font-weight:800;letter-spacing:.06em;color:var(--ink)}

/* ---------- channel input grid ---------- */
.cinputs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:4px}
.cbox{background:var(--paper);border:1px solid var(--line);border-radius:14px;
 padding:15px 16px 16px;min-width:0}
.cbox > b{display:block;font-family:Fraunces,Georgia,serif;font-size:15.5px;margin-bottom:2px;
 color:var(--ink)}
.cbox > i{display:block;font-style:normal;font-size:11.2px;color:#8A8477;margin-bottom:11px;
 line-height:1.5}

/* ---------- seasonality: the shape editor ----------
   Class names are deliberately NOT .sb/.sbt - the lifted tax stylesheet already
   owns .sb and .sb.on (a dark toggle button), and ".on" is exactly the modifier
   this block needs. That collision would have styled every month bar as a
   button and shipped looking broken. */
.sh3{font-family:Fraunces,Georgia,serif;font-size:16.5px;font-weight:600;color:var(--ink);
 margin:22px 0 5px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.shhint{font-family:Inter,system-ui,sans-serif;font-size:10.5px;font-weight:600;
 letter-spacing:.05em;text-transform:uppercase;color:#9A9384}
.shn{font-size:12.4px;line-height:1.62;color:var(--muted);margin:0 0 11px}
.shn b{color:var(--ink);font-weight:600}
.shrst{font:inherit;font-size:12.4px;background:none;border:0;padding:0;cursor:pointer;
 color:var(--pine);text-decoration:underline;text-underline-offset:2px}
.shrst:hover{color:var(--gold)}

.shp{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px;margin-bottom:6px}
.shc{text-align:left;background:var(--white);border:1.5px solid var(--line);border-radius:11px;
 padding:11px 13px;cursor:pointer;font:inherit;min-width:0;transition:border-color .15s,
 background .15s}
.shc:hover{background:var(--field);border-color:var(--fieldline)}
.shc.on{border-color:var(--pine);background:#EFF7F3}
.shc b{display:block;font-family:Fraunces,Georgia,serif;font-size:14px;color:var(--ink);
 line-height:1.25;margin-bottom:3px}
.shc i{display:block;font-style:normal;font-size:11px;line-height:1.45;color:#8A8477}
.shc.on i{color:#4A7A66}

.seas{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:4px;margin-bottom:10px}
.smo{display:flex;flex-direction:column;align-items:center;gap:4px;cursor:ns-resize;
 touch-action:none;border-radius:7px;padding:3px 1px}
.smo:focus-visible{outline:2px solid var(--gold);outline-offset:1px}
.smo u{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:9.5px;text-decoration:none;
 color:#9A9384;letter-spacing:-.02em}
.smo.on u{color:var(--gold);font-weight:700}
.smot{position:relative;width:100%;height:104px;background:var(--paper);
 border:1px solid var(--line);border-radius:6px;display:flex;align-items:flex-end;
 overflow:hidden}
/* the 100% line, drawn once per track so it reads as one rule across the year */
.smot::before{content:"";position:absolute;left:0;right:0;bottom:50%;
 border-top:1px dashed #C9C2B0;z-index:1}
.smot i{display:block;width:100%;background:var(--pine);border-radius:0 0 5px 5px;
 transition:height .12s ease;position:relative;z-index:2;opacity:.82}
.smo.on .smot i{background:var(--gold);opacity:1}
.smo em{font-style:normal;font-size:10px;font-weight:600;color:#8A8477;letter-spacing:.02em}

/* ---------- seasonality: the caseload consequence ---------- */
.ldwrap{position:relative;margin-top:4px}
.ldg{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:4px}
.ld{display:flex;flex-direction:column;align-items:center;gap:4px}
.ldt{width:100%;height:118px;background:var(--paper);border:1px solid var(--line);
 border-radius:6px;display:flex;align-items:flex-end;overflow:hidden}
.ldt i{display:block;width:100%;background:#9DBDAF;border-radius:0 0 5px 5px;
 transition:height .18s ease}
.ld.hi .ldt i{background:var(--pos)}
.ld.lo .ldt i{background:var(--neg)}
.ld em{font-style:normal;font-size:10px;font-weight:600;color:#8A8477}
.ld.hi em{color:var(--pos)}
.ld.lo em{color:var(--neg)}
/* the ceiling, positioned inside a box the exact height of the tracks so the
   month labels underneath cannot push it off register */
.ldcap{position:absolute;left:0;right:0;top:0;height:118px;pointer-events:none;z-index:3}
.ldcap b{position:absolute;left:0;right:0;border-top:2px dashed var(--gold)}
.ldcap span{position:absolute;right:0;top:-15px;font-size:9.5px;font-weight:700;
 letter-spacing:.05em;text-transform:uppercase;color:var(--gold);background:var(--white);
 padding:0 4px;border-radius:3px;white-space:nowrap}

/* Twelve columns are kept at every width. Wrapping the year onto two rows of
   six saves horizontal space and destroys the only thing the block is for -
   you cannot read a shape that has been cut in half. The bars narrow instead. */
@media (max-width:760px){
 .shp{grid-template-columns:repeat(2,minmax(0,1fr))}
 .seas,.ldg{gap:3px}
 .smot{height:88px}
 .ldt{height:96px}
 .ldcap{height:96px}
 .smo em,.ld em{font-size:9px}
}
@media (max-width:520px){
 .seas,.ldg{gap:2px}
 .smo{padding:3px 0}
 .smo u{display:none}          /* 26px of column will not hold "145%" honestly */
 .smo em,.ld em{font-size:8.5px;letter-spacing:-.02em}
 .ldcap span{font-size:9px}
}

@media (max-width:900px){.ghero .in{grid-template-columns:1fr;gap:24px}}
@media (max-width:820px){
 .chans,.cinputs{grid-template-columns:1fr}
 .stg{width:100% !important;min-width:0}
}

/* the old h1, demoted to a deck: the subject moved up into the h1 so the
   page is findable, and this line kept because it is the better sentence. */
.gtag{font-family:Fraunces,Georgia,serif;font-size:clamp(17px,1.7vw,22px);
  font-weight:400;font-style:italic;line-height:1.3;margin:0 0 .7em;opacity:.86}
"""
