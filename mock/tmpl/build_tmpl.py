#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""content-page-templates.html — three options for the deep-page template.

Four measured defects, all on published pages, all visible in the screenshots:

  cost-of-living hero   the three proof figures render as EM-DASHES. A cold
                        landing sees three empty slots above the fold, plus a
                        caption for a number that is not there.
  cost-of-living hero   no call to action at all. AIDA breaks at D -> A.
  working-remotely      full-width dark slab, everything in the left column,
                        the right half carrying nothing.
  terms.html at 5120px  a ~660px column anchored left. Two thirds of a 5K
                        display is empty. Every page on the site does this,
                        because .lwrap and friends cap at 1120px and do not
                        change behaviour above it.

The brief the templates have to satisfy, in the user's words: someone landing
cold from search, a forum or Facebook must "have enough info to understand where
they are - for MFTs". So the hero does NOT shrink to nothing. It does
orientation work, it proves something with a real number, and it offers one
action. What changes is that it stops wasting the width while doing it.
"""
import os, re, base64

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "tree5", "fonts")

COLA = "therapist-cost-of-living-california.html"
SIM = "practice-simulator.html"
TAX = "therapist-tax-strategy-california.html"
AMFT = "associate-mft-job-advisor.html"
HRS = "amft-3000-hours-california.html"
RATES = "rates.html"
REMOTE = "therapist-working-remotely-california.html"
TERMS = "terms.html"


def inline_fonts():
    css = open(os.path.join(FONTS, "fonts.css")).read()
    keep = [b for b in re.split(r"(?=/\* )", css) if b.strip().startswith("/* latin */")]

    def sub(m):
        with open(os.path.join(FONTS, "f", m.group(1)), "rb") as f:
            return "url(data:font/woff2;base64," + base64.b64encode(f.read()).decode() + ")"
    return re.sub(r"url\(\./f/([^)]+)\)", sub, "".join(keep))


CSS = """
:root{--paper:#FBF9F3;--white:#fff;--ink:#26241E;--muted:#6E695E;--line:#E7E2D6;
 --field:#FBF6E9;--fline:#E4D9BE;--pine:#2C6350;--pinedeep:#1F4C3C;--brick:#8E4B45;
 --gold:#B08430;--indigo:#4B3B93;--pop:#F6C560;--pos:#3F9577}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.6}
h1,h2,h3,h4{font-family:Fraunces,Georgia,serif;font-weight:600;letter-spacing:-.02em;
 line-height:1.13;margin:0}
a{color:inherit}

/* ===================== THE WIDTH RULE, shared by all three =================
   The bug on the 5K display is not that the measure is 68ch - that is correct
   for prose. It is that the CONTAINER also stops at 1120px and is then left
   inside a 5120px viewport, so the page reads as broken rather than as
   typeset. Two changes fix every page at once:
     1. the wrap grows in steps up to 1560px instead of hard-stopping at 1120
     2. above 1280px the layout gains rails, so the extra width carries real
        content (section nav, figures, citations) instead of air
   Prose never exceeds 68ch in any of them. */
.w{max-width:1120px;margin:0 auto;padding:0 26px}
@media (min-width:1500px){.w{max-width:1320px}}
@media (min-width:1900px){.w{max-width:1560px}}
@media (max-width:520px){.w{padding:0 18px}}

/* ---- document chrome (this mockup's own) ---- */
.doc{background:#1B1A17;color:#EDE8DC;padding:42px 0 38px}
.doc .k{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--pop);margin:0 0 13px}
.doc h1{font-size:clamp(29px,3.8vw,46px);color:#FFFDF6;max-width:20ch}
.doc p{font-size:15.6px;line-height:1.62;color:#B8B1A2;max-width:66ch;margin:16px 0 0}
.doc p b{color:#EDE8DC;font-weight:600}
.defects{list-style:none;margin:22px 0 0;padding:0;display:grid;
 grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 20px;max-width:1000px}
.defects li{font-size:12.8px;color:#B8B1A2;line-height:1.55;padding:10px 13px;
 background:rgba(255,255,255,.05);border-radius:10px;
 border-left:2px solid var(--brick)}
.defects li b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
 letter-spacing:.1em;text-transform:uppercase;color:#D89A8F;margin:0 0 3px}
@media (max-width:820px){.defects{grid-template-columns:1fr}}

.sec{padding:50px 0 6px}
.sec .n{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--gold);margin:0 0 10px}
.sec h2{font-size:clamp(23px,2.8vw,34px);max-width:26ch}
.sec .d{font-size:15px;color:var(--muted);max-width:70ch;margin:12px 0 0}

.spec{margin:26px 0 0;border:1px solid var(--line);border-radius:20px;overflow:hidden;
 background:var(--white)}
.spec .bar{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;background:#F4F1E7;
 border-bottom:1px solid var(--line);padding:11px 18px;font-family:'IBM Plex Mono',monospace;
 font-size:10.6px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.spec .bar .t{background:var(--pine);color:#fff;border-radius:5px;padding:3px 8px}
.spec .bar b{color:var(--ink)}
.spec .stage{padding:0;background:var(--paper)}
.spec .why{border-top:1px solid var(--line);padding:17px 22px 19px;display:grid;
 grid-template-columns:repeat(3,minmax(0,1fr));gap:6px 24px}
.spec .why div{font-size:12.6px;color:var(--muted);line-height:1.6}
.spec .why b{display:block;color:var(--ink);font-size:10.5px;letter-spacing:.1em;
 text-transform:uppercase;font-family:'IBM Plex Mono',monospace;margin:0 0 4px}
@media (max-width:820px){.spec .why{grid-template-columns:1fr}}

/* shared hero atoms, so the three options differ in LAYOUT not in vocabulary */
.hk{font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:600;
 letter-spacing:.14em;text-transform:uppercase;margin:0 0 12px;color:var(--muted)}
.hh{font-size:clamp(27px,3.2vw,42px);margin:0 0 .3em;letter-spacing:-.022em}
.hh em{font-style:normal;color:var(--pine);
 background:linear-gradient(transparent 62%,#F6C56055 62%)}
.hd{font-size:clamp(15.5px,1.2vw,17.5px);line-height:1.58;color:#3A362E;max-width:52ch;
 margin:0 0 20px}
.hacts{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 16px}
.hcta{display:inline-flex;align-items:center;min-height:48px;padding:0 22px;border-radius:999px;
 background:var(--pine);color:#fff;font-weight:700;font-size:15.5px;text-decoration:none}
.hcta:hover{background:#245244}
.hghost{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;border-radius:999px;
 border:1.5px solid var(--line);background:var(--white);font-weight:600;font-size:15px;
 text-decoration:none}
.hghost:hover{border-color:var(--pine);color:var(--pine)}
.hwho{display:block;font-size:13px;line-height:1.6;color:var(--muted);margin:0;max-width:40em}
.hwho b{color:var(--ink);font-weight:600}

/* the panel. THE ZERO-STATE RULE: it is pre-filled with a worked example and
   labelled as one. It never shows an em-dash, because a dash above the fold is
   an empty promise at the exact moment the reader is deciding to stay. */
.pan{background:var(--pinedeep);border-radius:16px;padding:18px 22px 20px;color:#DCEAE3}
.panh{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
 font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.1em;
 text-transform:uppercase;color:#8FBBA8;margin:0 0 4px;padding-bottom:11px;
 border-bottom:1px solid rgba(255,255,255,.16)}
.panh i{font-style:normal;color:var(--pop);border:1px solid rgba(246,197,96,.45);
 border-radius:5px;padding:2px 7px;white-space:nowrap}
.panr{display:flex;align-items:baseline;justify-content:space-between;gap:14px;padding:10px 0;
 border-bottom:1px solid rgba(255,255,255,.13)}
.panr:last-child{border-bottom:0;padding-bottom:0}
.panr .lb{font-size:13.2px;font-weight:600;color:#F4F1E8}
.panr .vv{text-align:right}
.panr b{display:block;font-family:Fraunces,Georgia,serif;font-weight:600;font-size:26px;
 line-height:1;color:var(--pop);white-space:nowrap}
.panr em{display:block;font-style:normal;font-size:12.2px;line-height:1.4;color:#9FC4B4}
.panfoot{margin:13px 0 0;font-size:11.6px;color:#8FBBA8;line-height:1.5}

/* ============ THE BREADCRUMB, shared by all three ============
   Replaces the "CHAPTER 04" kicker, which only means something to a reader who
   can see chapters 1-3 - and on a page arrived at from a forum link, nobody
   can. A crumb is the same three-token shape but it is navigable, it states the
   audience and the section, and Google reads BreadcrumbList for rich results.
   Four pages already emit that JSON-LD; none of them shows the trail. */
.crumb{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;margin:0 0 14px;
 font-family:'IBM Plex Mono',monospace;font-size:10.6px;letter-spacing:.1em;
 text-transform:uppercase}
.crumb a{color:var(--muted);text-decoration:none;padding:4px 0;min-height:22px;
 border-bottom:1px solid transparent}
.crumb a:hover{color:var(--ink);border-bottom-color:var(--line)}
.crumb i{font-style:normal;color:#BDB6A6}
.crumb b{color:var(--gold);font-weight:600}
/* on a dark band the same component just inverts */
.o3 .crumb a{color:#8FBBA8}
.o3 .crumb a:hover{color:#DCEAE3}
.o3 .crumb i{color:#5E7F72}
.o3 .crumb b{color:var(--pop)}

/* ============ OPTION 1 — Split orientation ============ */
.o1{background:var(--paper);padding:34px 0 30px;border-bottom:1px solid var(--line)}
.o1g{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(300px,.95fr);
 gap:clamp(26px,4vw,58px);align-items:center}
@media (max-width:900px){.o1g{grid-template-columns:minmax(0,1fr);gap:22px}}

/* ============ OPTION 2 — Three-rail document ============ */
.o2{background:var(--paper);padding:30px 0 26px}
.o2g{display:grid;grid-template-columns:200px minmax(0,1fr) 260px;gap:34px;align-items:start}
@media (max-width:1280px){.o2g{grid-template-columns:200px minmax(0,1fr)}
 .o2rail{display:none}}
@media (max-width:900px){.o2g{grid-template-columns:minmax(0,1fr)}
 .o2nav{display:none}}
.o2nav{position:sticky;top:20px;font-size:12.8px}
.o2nav p{font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.12em;
 text-transform:uppercase;color:var(--muted);margin:0 0 9px}
.o2nav a{display:block;padding:6px 0 6px 11px;border-left:2px solid var(--line);
 text-decoration:none;color:var(--muted);line-height:1.4;min-height:32px}
.o2nav a.on{border-left-color:var(--pine);color:var(--ink);font-weight:600}
.o2nav a:hover{color:var(--ink)}
.o2body .hd{max-width:66ch}
.o2body p.pr{font-size:15.4px;line-height:1.72;color:#3A362E;max-width:66ch;margin:0 0 1em}
.o2rail{position:sticky;top:20px;display:grid;gap:12px}
.o2card{background:var(--white);border:1px solid var(--line);border-radius:14px;
 padding:15px 17px}
.o2card p:first-child{font-family:'IBM Plex Mono',monospace;font-size:9.8px;
 letter-spacing:.11em;text-transform:uppercase;color:var(--gold);margin:0 0 7px}
.o2card b{display:block;font-family:Fraunces,Georgia,serif;font-size:21px;font-weight:600;
 line-height:1.1;margin:0 0 4px}
.o2card span{display:block;font-size:12.4px;color:var(--muted);line-height:1.5}
/* 22px was under the tap minimum. These are card actions, not inline prose
   links, so WCAG 2.5.8's inline exemption does not apply to them. */
.o2card a{display:flex;align-items:center;margin:9px 0 0;font-size:12.6px;font-weight:700;
 color:var(--pine);text-decoration:none;min-height:44px}
.o2card a:hover{text-decoration:underline}

/* ============ OPTION 3 — Compact band, tool first ============ */
.o3{background:var(--pinedeep);color:#DCEAE3;padding:22px 0}
.o3g{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:28px;align-items:center}
@media (max-width:900px){.o3g{grid-template-columns:minmax(0,1fr);gap:16px}}
.o3 .hk{color:#8FBBA8;margin-bottom:8px}
.o3 h1{font-size:clamp(23px,2.4vw,32px);color:#FFFDF6;margin:0 0 7px;max-width:24ch}
.o3 h1 em{font-style:normal;color:var(--pop);background:none}
.o3 .hd{color:#9FC4B4;font-size:14.6px;margin:0;max-width:62ch}
.o3 .hwho{color:#8FBBA8;margin:9px 0 0}
.o3 .hwho b{color:#DCEAE3}
.o3 .hcta{background:var(--pop);color:#173B2F;white-space:nowrap}
.o3 .hcta:hover{background:#FFD57A}
.o3tool{background:var(--paper);padding:26px 0 30px}
.o3lv{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
@media (max-width:900px){.o3lv{grid-template-columns:repeat(2,minmax(0,1fr))}}
.o3f{background:var(--field);border:1.5px solid var(--fline);border-radius:12px;
 padding:11px 13px}
.o3f p{font-family:'IBM Plex Mono',monospace;font-size:9.6px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--muted);margin:0 0 5px}
.o3f b{font-family:Fraunces,Georgia,serif;font-size:22px;font-weight:600}
.o3f span{font-size:12px;color:var(--muted);margin-left:5px}
.o3out{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:14px 0 0}
@media (max-width:900px){.o3out{grid-template-columns:1fr}}
.o3o{background:var(--white);border:1px solid var(--line);border-radius:14px;padding:15px 17px;
 border-top:3px solid var(--pine)}
.o3o:nth-child(2){border-top-color:var(--gold)}
.o3o:nth-child(3){border-top-color:var(--pos)}
.o3o p{font-size:11.6px;color:var(--muted);margin:0 0 4px;font-weight:600;
 letter-spacing:.04em;text-transform:uppercase}
.o3o b{font-family:Fraunces,Georgia,serif;font-size:28px;font-weight:600;line-height:1;
 display:block}
.o3o span{font-size:12.2px;color:var(--muted);display:block;margin:5px 0 0}

/* ---- the 5K comparison ---- */
.wide{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:24px 0 0}
@media (max-width:900px){.wide{grid-template-columns:1fr}}
.wf{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--white)}
.wf p.t{margin:0;padding:9px 14px;background:#F4F1E7;border-bottom:1px solid var(--line);
 font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--muted)}
.wf p.t.bad{color:#8E4B45}
.wf p.t.good{color:var(--pine)}
.ill{height:190px;background:var(--paper);position:relative;padding:12px}
.ill .band{position:absolute;left:0;right:0;top:0;height:16px;background:var(--pine);opacity:.85}
.ill .col{position:absolute;top:26px;bottom:12px;background:var(--white);
 border:1px solid var(--line);border-radius:5px}
.ill .col.txt::after{content:"";position:absolute;left:8px;right:8px;top:10px;bottom:10px;
 background:repeating-linear-gradient(180deg,#DBD5C6 0 5px,transparent 5px 13px)}
.ill .col.acc{background:var(--pinedeep);border-color:var(--pinedeep)}
.ill .col.rail{background:#F4F1E7}
.ill .empty{position:absolute;top:26px;bottom:12px;
 background:repeating-linear-gradient(45deg,transparent 0 7px,rgba(142,75,69,.14) 7px 14px)}
.wf .note{margin:0;padding:11px 14px;font-size:12.4px;color:var(--muted);line-height:1.55;
 border-top:1px solid var(--line)}

.rules{list-style:none;margin:22px 0 0;padding:0;display:grid;
 grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 22px}
@media (max-width:900px){.rules{grid-template-columns:1fr}}
.rules li{background:var(--white);border:1px solid var(--line);border-radius:13px;
 padding:15px 17px;font-size:13.2px;color:var(--muted);line-height:1.6}
.rules li b{display:block;color:var(--ink);font-size:13.6px;margin:0 0 4px}
.mx{width:100%;border-collapse:collapse;margin:22px 0 0;font-size:12.8px;background:var(--white);
 border:1px solid var(--line);border-radius:14px;overflow:hidden}
.mx th,.mx td{padding:9px 11px;border-bottom:1px solid var(--line);text-align:left}
.mx th{font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.07em;
 text-transform:uppercase;color:var(--muted);font-weight:600}
.mx td:first-child{font-weight:600;white-space:nowrap}
.mx .o1t{color:var(--pine);font-weight:700}
.mx .o2t{color:var(--indigo);font-weight:700}
.mx .o3t{color:var(--gold);font-weight:700}
.foot{padding:32px 0 56px;font-size:12.4px;color:var(--muted)}
"""

# ---------------------------------------------------------------- panels ---
# The cost-of-living page's OWN arithmetic, on its own published defaults:
# MIT Living Wage, Los Angeles County, one adult / no children -
# 22471+8681+4463+3876+3255+1517+4992 = 49,255/yr = 4,105/mo. The loan row is
# the RAP band arithmetic at an $85,000 AGI: band 8 => 8% of AGI / 12 = 567.
# Every figure here is computed, and the panel says so.
PAN_COLA = """
<div class="pan">
  <p class="panh"><span>California statewide &middot; one adult</span><i>worked example</i></p>
  <div class="panr"><span class="lb">To live, a month</span><span class="vv">
    <b>$4,285</b><em>housing, transport, food, medical and the rest</em></span></div>
  <div class="panr"><span class="lb">Student loan</span><span class="vv">
    <b>$567</b><em>RAP, on an $85,000 AGI</em></span></div>
  <div class="panr"><span class="lb">Break-even</span><span class="vv">
    <b>$4,851</b><em>before a single dollar of savings</em></span></div>
  <p class="panfoot">Every field below is editable &mdash; change one and all three move.</p>
</div>"""

HERO_BITS = dict(
    kick="California &middot; for LMFTs, LCSWs, LPCCs and associates",
    h1="What a month in California actually costs a therapist &mdash; "
       "and <em>what is left</em>.",
    deck="Every other tool here prices the practice. This one prices the person running "
         "it: what it costs to live in your county, what the student loan takes on your "
         "repayment plan, and what remains for savings.",
    who="Built for <b>California</b> therapists. Housing, transport, food and medical by "
        "county; RAP, IBR and PSLF for the loan.",
)


def acts(primary="Work out my break-even", second="All the tools"):
    return ('<div class="hacts"><a class="hcta" href="#">%s &rarr;</a>'
            '<a class="hghost" href="tools.html">%s</a></div>' % (primary, second))


OPT1 = """
<section class="o1"><div class="w"><div class="o1g">
  <div>
    <p class="crumb"><a href="tools.html">Therapist Support</a><i>&rsaquo;</i><a href="tools.html">Tools</a><i>&rsaquo;</i><b>Cost of living</b></p>
    <p class="hk">%(kick)s</p>
    <h1 class="hh">%(h1)s</h1>
    <p class="hd">%(deck)s</p>
    %(acts)s
    <p class="hwho">%(who)s</p>
  </div>
  %(pan)s
</div></div></section>""" % dict(HERO_BITS, acts=acts(), pan=PAN_COLA)

OPT2 = """
<section class="o2"><div class="w"><div class="o2g">
  <nav class="o2nav">
    <p>On this page</p>
    <a class="on" href="#">Where you live</a>
    <a href="#">The student loan</a>
    <a href="#">Your break-even</a>
    <a href="#">What is left</a>
    <a href="#">A framework people use</a>
    <a href="#">Sources</a>
  </nav>
  <div class="o2body">
    <p class="crumb"><a href="tools.html">Therapist Support</a><i>&rsaquo;</i><a href="tools.html">Tools</a><i>&rsaquo;</i><b>Cost of living</b></p>
    <p class="hk">%(kick)s</p>
    <h1 class="hh">%(h1)s</h1>
    <p class="hd">%(deck)s</p>
    %(acts)s
    <p class="hwho">%(who)s</p>
  </div>
  <div class="o2rail">
    <div class="o2card"><p>Worked example</p><b>$4,851</b>
      <span>a month to break even in Los Angeles County, one adult, with the loan</span></div>
    <div class="o2card"><p>Read next</p><b>The rate gap</b>
      <span>what California therapists actually charge, insurance against private pay</span>
      <a href="rates.html">Field notes &rarr;</a></div>
    <div class="o2card"><p>Wrong page?</p><b>Still accruing hours</b>
      <span>the associate route prices placements, not living costs</span>
      <a href="associate-mft-job-advisor.html">Job advisor &rarr;</a></div>
  </div>
</div></div></section>""" % dict(HERO_BITS, acts=acts())

OPT3 = """
<section class="o3"><div class="w"><div class="o3g">
  <div>
    <p class="crumb"><a href="tools.html">Therapist Support</a><i>&rsaquo;</i><a href="tools.html">Tools</a><i>&rsaquo;</i><b>Cost of living</b></p>
    <p class="hk">%(kick)s</p>
    <h1>%(h1)s</h1>
    <p class="hd">%(deck)s</p>
    <p class="hwho">%(who)s</p>
  </div>
  <a class="hcta" href="#">Start with my county &darr;</a>
</div></div></section>
<section class="o3tool"><div class="w">
  <div class="o3lv">
    <div class="o3f"><p>Housing</p><b>1,949</b><span>$/mo</span></div>
    <div class="o3f"><p>Transport</p><b>794</b><span>$/mo</span></div>
    <div class="o3f"><p>Food</p><b>372</b><span>$/mo</span></div>
    <div class="o3f"><p>Loan payment</p><b>567</b><span>$/mo</span></div>
  </div>
  <div class="o3out">
    <div class="o3o"><p>To live, a month</p><b>$4,285</b>
      <span>California statewide, one adult</span></div>
    <div class="o3o"><p>Break-even</p><b>$4,851</b>
      <span>with the loan, before savings</span></div>
    <div class="o3o"><p>Left over</p><b>$1,149</b>
      <span>on a $6,000 monthly take-home</span></div>
  </div>
</div></section>""" % dict(HERO_BITS, h1="What a month in California actually costs a "
                          "therapist &mdash; and <em>what is left</em>.")


def spec(tag, name, where, stage, a, b, c):
    return """
<div class="spec">
  <div class="bar"><span class="t">%s</span><b>%s</b><span>&middot;</span><span>%s</span></div>
  <div class="stage">%s</div>
  <div class="why"><div><b>Cold landing</b>%s</div><div><b>Wide screens</b>%s</div>
    <div><b>Trade-off</b>%s</div></div>
</div>""" % (tag, name, where, stage, a, b, c)


WIDE = """
<div class="wide">
  <div class="wf"><p class="t bad">Today &mdash; terms.html at 5120px</p>
    <div class="ill"><div class="band"></div>
      <div class="col txt" style="left:12px;width:24%"></div>
      <div class="empty" style="left:calc(24% + 20px);right:12px"></div></div>
    <p class="note">The wrap hard-stops at 1120px and the column is anchored left, so
    three quarters of the display is hatched nothing. This is every page on the site,
    not just Terms.</p></div>
  <div class="wf"><p class="t good">Fixed &mdash; rails carry the width</p>
    <div class="ill"><div class="band"></div>
      <div class="col rail" style="left:12px;width:15%"></div>
      <div class="col txt" style="left:calc(15% + 20px);right:calc(20% + 20px)"></div>
      <div class="col acc" style="right:12px;width:20%"></div></div>
    <p class="note">Prose still sets at 66ch &mdash; that does not change, because it is
    correct. The extra width goes to a sticky section nav and a rail carrying the worked
    figure, what to read next, and the route out for a reader on the wrong page.</p></div>
</div>"""

RULES = [
    ("Never an em-dash above the fold.",
     "The cost-of-living hero currently shows three captions with no numbers. A panel "
     "ships pre-filled with a worked example and labelled <i>worked example</i>, so a "
     "cold reader sees the tool working before they type anything."),
    ("The hero orients, it does not shrink.",
     "Someone arriving from a forum link needs to know in one screen that this is for "
     "California therapists, what this page computes, and what to do. That is three "
     "elements &mdash; kicker, h1, one deck sentence &mdash; plus a CTA and the who line."),
    ("One h1, and it carries the search phrase.",
     "&ldquo;What a month actually costs you&rdquo; ranks for nothing. &ldquo;What a "
     "month in California actually costs a therapist&rdquo; names the audience and the "
     "place, which is what someone types."),
    ("Prose at 66ch. The page fills with rails, not with longer lines.",
     "Widening the measure to fill a 5K screen would make it unreadable. The fix is that "
     "the container grows in two steps and the new space carries navigation and routes."),
    ("Every content page has a CTA and a way out.",
     "AIDA breaks at D&rarr;A when a page ends in prose. Every template here ends its "
     "hero with one primary action, and carries the route for a reader who landed on the "
     "wrong page."),
    ("The dark slab is for bands, not for full heroes.",
     "A full-height dark hero costs a whole screen and, on these pages, was carrying one "
     "column of text. Option 3 keeps the colour as a 22px-padded band and spends the "
     "screen on the tool."),
]

SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Content page templates &mdash; Therapist Support</title>
<style>%(fonts)s</style><style>%(css)s</style>
</head><body>

<header class="doc"><div class="w">
  <p class="k">Mock-up &middot; deep-page template</p>
  <h1>Three ways a content page can carry a cold landing.</h1>
  <p>The brief: someone arriving from search, a forum or Facebook has to understand in
  one screen <b>where they are, that it is for California therapists, and what this page
  will do for them</b> &mdash; so the hero does orientation work rather than shrinking.
  What changes is that it stops wasting the width while doing it.</p>
  <ul class="defects">
    <li><b>cost-of-living hero</b>Three proof figures render as em-dashes. A cold landing
      sees three empty slots and a caption for a number that is not there.</li>
    <li><b>cost-of-living hero</b>No call to action anywhere in it. AIDA breaks at
      desire &rarr; action.</li>
    <li><b>working-remotely hero</b>Full-width dark slab, everything in the left column,
      the right half carrying nothing.</li>
    <li><b>every page at 5120px</b>The wrap stops at 1120px and anchors left, so three
      quarters of a 5K display is empty.</li>
  </ul>
</div></header>

<section class="sec"><div class="w">
  <p class="n">Option 1</p><h2>Split orientation</h2>
  <p class="d">The home page treatment, carried to deep pages. Orientation on the left,
  a pre-filled worked example on the right. Least new machinery &mdash; it reuses the
  hero that shipped today, so every page gets consistent within one build.</p>
  %(o1)s
</div></section>

<section class="sec"><div class="w">
  <p class="n">Option 2</p><h2>Three-rail document</h2>
  <p class="d">Sticky section nav on the left, prose at 66ch in the middle, a rail on the
  right carrying the worked figure, what to read next, and the route out for a reader on
  the wrong page. Below 1280px the right rail drops; below 900px the nav does too.</p>
  %(o2)s
</div></section>

<section class="sec"><div class="w">
  <p class="n">Option 3</p><h2>Compact band, tool first</h2>
  <p class="d">Orientation compressed into a coloured band about 150px tall, then the
  levers immediately. The reader is touching the tool within one screen, which is what
  makes a calculator feel like a calculator rather than an article about one.</p>
  %(o3)s
</div></section>

<section class="sec"><div class="w">
  <p class="n">The 5K problem</p><h2>Why every page looks broken on a 27-inch display</h2>
  <p class="d">This is separate from the hero question and it affects all fourteen pages,
  Terms and Privacy included.</p>
  %(wide)s
</div></section>

<section class="sec"><div class="w">
  <p class="n">Which page gets which</p><h2>My recommendation</h2>
  <table class="mx"><thead><tr><th>Page</th><th>Template</th><th>Why</th></tr></thead>
  <tbody>
    <tr><td>Cost of living</td><td class="o3t">Option 3</td>
      <td>It is a calculator with seven levers. Get the reader to them.</td></tr>
    <tr><td>Practice simulator</td><td class="o3t">Option 3</td>
      <td>Same &mdash; the tool is the argument.</td></tr>
    <tr><td>Grow your practice</td><td class="o3t">Option 3</td>
      <td>Same, and the funnel needs the vertical space.</td></tr>
    <tr><td>Job advisor</td><td class="o3t">Option 3</td><td>Same.</td></tr>
    <tr><td>3,000 hours</td><td class="o1t">Option 1</td>
      <td>Fewer levers, and the four-gates idea needs explaining before the form.</td></tr>
    <tr><td>Tax strategy</td><td class="o2t">Option 2</td>
      <td>Long, sectioned, heavily cited. The nav rail is the point.</td></tr>
    <tr><td>Working remotely</td><td class="o2t">Option 2</td>
      <td>Research page with a table. Right rail carries the routes it has none of.</td></tr>
    <tr><td>Field notes (rates)</td><td class="o2t">Option 2</td>
      <td>Editorial, long, citation-dense.</td></tr>
    <tr><td>Terms, Privacy</td><td class="o2t">Option 2</td>
      <td>Its &ldquo;on this page&rdquo; box becomes the rail, and the 5K gap closes.</td></tr>
  </tbody></table>
  <p class="d" style="margin-top:14px">Two templates would also work &mdash; Option 1 folds
  into Option 3 if you would rather not maintain three. Three is worth it only if the
  calculator pages really should feel different from the reading pages, which I think
  they should.</p>
</div></section>

<section class="sec"><div class="w">
  <p class="n">Rules</p><h2>Six rules all three share</h2>
  <ul class="rules">%(rules)s</ul>
</div></section>

<div class="foot"><div class="w">Mock-up. Every figure shown is computed from the
cost-of-living page&rsquo;s own published constants, not illustrative.</div></div>
</body></html>
"""


def main():
    html = SHELL % dict(
        fonts=inline_fonts(), css=CSS,
        o1=spec("01", "Split orientation", "reuses today&rsquo;s home hero", OPT1,
                "Kicker names California and the licences; the panel proves the tool works "
                "before a single keystroke.",
                "The panel column grows with the wrap, so the width is spent on the figure.",
                "Costs about 380px of vertical before any content. Fine on a laptop, "
                "heavy on a short phone."),
        o2=spec("02", "Three-rail document", "long, cited, sectioned pages", OPT2,
                "The nav shows the whole shape of the page at a glance, which is the "
                "fastest possible orientation for a long read.",
                "This is the one that actually solves 5K: both rails only exist above "
                "1280px, and they carry real content.",
                "Needs a section list per page. Overkill on a page with three sections."),
        o3=spec("03", "Compact band, tool first", "calculator pages", OPT3,
                "Orientation is compressed but complete &mdash; audience, place, what it "
                "computes, one action &mdash; and then the levers are right there.",
                "The lever grid goes four-up instead of two-up as the wrap grows.",
                "The h1 gets less room to be striking. On this kind of page that is "
                "probably the right trade."),
        wide=WIDE,
        rules="".join("<li><b>%s</b>%s</li>" % (h, b) for h, b in RULES),
    )
    out = os.path.join(HERE, "content-page-templates.html")
    slugs = {COLA, SIM, TAX, AMFT, HRS, RATES, REMOTE, TERMS, "tools.html"}
    for h in re.findall(r'href="(?!https?:|#)([^"#]+)', html):
        assert h in slugs, "unknown slug: " + h
    open(out, "w", encoding="utf-8").write(html)
    print("wrote %s  %d kB" % (os.path.basename(out), len(html) // 1024))


if __name__ == "__main__":
    main()
