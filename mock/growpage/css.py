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
