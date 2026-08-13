#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The house style - the fifth thing - drawn as six complete pages.

WHAT THIS IS

`ops/redesign-37signals-products.html` drew the site four times, once in each
37signals product's own identity, and ended with a recommendation that was
none of them:

    Basecamp's structure and restraint. Fizzy's label system on the six
    paths. Campfire's signature at the end. Exactly one HEY slab per page,
    for the claim that matters.

This document is that recommendation, built. Not fragments and not a mood
board - six full pages, top to bottom, with every band a real page would
carry: navigation, hero, the paths, the shelf, the tool, the slab, the
signature, the newsletter, the footer, the fine print.

WHY A FIFTH THING RATHER THAN ONE OF THE FOUR

Each of the four is optimized for something this site is not. Basecamp is
built for a product people open daily - closest, and the reason it is the
base. HEY sells one idea to a stranger once, which is a home page and nothing
else. Campfire is a 29em manifesto, which is an about page. Fizzy is a
product with structured data in it, which is what the six paths are.

Taking the decision each got right is what their own designers do. Copying
one wholesale is costume.

THE FOUR BORROWED MOVES, AND THE RULE ON EACH

  BASECAMP   Restraint is the default. Tinted paper, never pure white. Small
             type by marketing standards - 16.5px body - because these pages
             are 6,000 words with tables in them. One accent. Flat fills.
  FIZZY      Six hues, one per path, used as a chip and a left rule and
             nothing else. Never as a background, never as body text.
  CAMPFIRE   A handwritten signature closes any page that makes a claim about
             who checked the numbers. Home, about, and every article.
  HEY        One slab per page. One. It is the loudest thing on the page and
             it goes to the single claim that page is making.

The last rule is the one that will be broken first, so there is a guard for
it below: no page in this document may carry two slabs.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DONOR = os.path.join(SITE, "ops", "stage-architecture.html")
OUT = os.path.join(SITE, "ops", "house-style.html")
UPDATED = "13 August 2026"

NAV = [("system", "The system"), ("home", "Home"),
       ("assoc", "Associate landing"), ("article", "Content page"),
       ("dir", "Directory"), ("email", "Email sign-up"), ("about", "About"),
       ("build", "How to build it")]

PATHS = [
    ("01", "Deciding", "Is this worth it?", "73", "p1"),
    ("02", "In a program", "Nobody will take me for practicum.", "31", "p2"),
    ("03", "The gap", "Can I work before my number arrives?", "4", "p3"),
    ("04", "Counting hours", "547 hours and nobody will hire me.", "21", "p4"),
    ("05", "Newly licensed", "Do I go on panels or not?", "19", "p5"),
    ("06", "Running a practice", "How do I do this ethically?", "24", "p6"),
]

TOKENS = [
    ("--paper", "#F6F8F6", "Page. Tinted, never pure white. Basecamp.", 1),
    ("--card", "#FFFFFF", "Raised surfaces only.", 1),
    ("--ink", "#1B2420", "Body text. 13.9:1 on paper.", 0),
    ("--dim", "#5F6A64", "Secondary. 5.2:1 on paper.", 0),
    ("--line", "#DFE4E0", "Hairlines and table rules.", 1),
    ("--pine", "#2C6350", "The one accent. Links, buttons, the slab.", 0),
    ("--deep", "#123C30", "Slab background and footer.", 0),
    ("--gold", "#FFE7A3", "The marker underline and the highlight.", 1),
]
HUES = [("p1", "#2F6FDB", "Deciding"), ("p2", "#7A5AF8", "In a program"),
        ("p3", "#0E8FA8", "The gap"), ("p4", "#17864A", "Counting hours"),
        ("p5", "#B0730B", "Newly licensed"), ("p6", "#BC3F86",
                                              "Running a practice")]

EXTRA = """
/* ================= the house style, as it would really ship ============ */
.hs{--paper:#F6F8F6;--card:#fff;--ink:#1B2420;--dim:#5F6A64;--line:#DFE4E0;
  --pine:#2C6350;--deepp:#123C30;--goldp:#FFE7A3;--pad:38px;
  --p1:#2F6FDB;--p2:#7A5AF8;--p3:#0E8FA8;--p4:#17864A;--p5:#B0730B;
  --p6:#BC3F86;
  background:var(--paper);color:var(--ink);
  font-family:'Inter',system-ui,sans-serif;font-size:17.5px;line-height:1.62;
  letter-spacing:-.011em}
@media(max-width:700px){.hs{--pad:20px;font-size:16px}}
.hs *{box-sizing:border-box}
.hs a{text-decoration:none;color:var(--pine)}
.hs p{margin:0 0 16px}
.hs .wrap2{padding:0 var(--pad)}
.hs .band{padding:54px var(--pad)}
@media(max-width:700px){.hs .band{padding:32px var(--pad)}}
.hs h1,.hs h2,.hs h3,.hs h4{font-family:'Inter',system-ui,sans-serif;
  font-weight:800;letter-spacing:-.038em;line-height:1.02;margin:0 0 20px;
  color:var(--ink);text-wrap:balance}
.hs h1{font-size:68px;max-width:17ch}
.hs h2{font-size:42px;max-width:22ch;letter-spacing:-.034em}
.hs h3{font-size:25px;line-height:1.14;letter-spacing:-.028em}
.hs h4{font-size:19px;line-height:1.2;margin-bottom:6px;letter-spacing:-.026em}
@media(max-width:920px){.hs h1{font-size:50px}.hs h2{font-size:33px}}
@media(max-width:700px){.hs h1{font-size:34px}.hs h2{font-size:26px}
  .hs h3{font-size:21px}}
.hs .lede{font-size:22px;line-height:1.42;color:var(--dim);max-width:48ch;
  margin-bottom:26px;letter-spacing:-.017em}
@media(max-width:700px){.hs .lede{font-size:18px}}
.hs .eb{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.15em;text-transform:uppercase;color:var(--dim);display:block;
  margin-bottom:12px}
.hs .fine{font-size:13.5px;color:var(--dim)}
.hs .btn{display:inline-block;background:var(--pine);color:#fff;font-weight:700;
  font-size:17px;padding:.78em 1.15em;border-radius:6px;
  box-shadow:0 1px 2px rgba(18,60,48,.14),0 4px 14px rgba(18,60,48,.08)}
.hs .btn.o{background:var(--card);color:var(--ink);
  box-shadow:0 1px 2px rgba(27,36,32,.08),0 0 0 1px var(--line)}
.hs .card{background:var(--card);border-radius:10px;padding:18px 20px;
  box-shadow:0 1px 2px rgba(27,36,32,.05),0 6px 20px rgba(27,36,32,.045),
    0 0 0 1px rgba(27,36,32,.055)}
.hs .scribble{background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 12'><path d='M2 8 C 22 3, 44 10, 66 5 S 106 3, 118 7' fill='none' stroke='%23FFE7A3' stroke-width='6' stroke-linecap='round'/><path d='M6 10 C 26 6, 48 12, 70 8 S 108 6, 116 9' fill='none' stroke='%23FFE7A3' stroke-width='4' stroke-linecap='round' opacity='.7'/></svg>") bottom center/100% .36em no-repeat;padding-bottom:.05em}
.hs .hl{background:var(--goldp);padding:0 .2em;border-radius:2px}

/* --- the one slab per page. HEY's move, this site's color --------------- */
.hs .slab{background:var(--deepp);color:#fff;padding:58px var(--pad);
  -webkit-mask:radial-gradient(9px at 50% 0,transparent 98%,#000) repeat-x 0 0/30px 10px,
    radial-gradient(9px at 50% 100%,transparent 98%,#000) repeat-x 0 100%/30px 10px,
    linear-gradient(#000,#000) no-repeat 0 10px/100% calc(100% - 20px);
  mask:radial-gradient(9px at 50% 0,transparent 98%,#000) repeat-x 0 0/30px 10px,
    radial-gradient(9px at 50% 100%,transparent 98%,#000) repeat-x 0 100%/30px 10px,
    linear-gradient(#000,#000) no-repeat 0 10px/100% calc(100% - 20px)}
.hs .slab h2,.hs .slab h3{color:#fff;max-width:22ch}
.hs .slab p{color:#CBDDD5;max-width:58ch;margin:0}
.hs .slab .eb{color:var(--goldp)}
.hs .slab .hl{background:var(--goldp);color:var(--deepp)}
.hs .slab .figs{display:grid;gap:14px;margin-top:22px}
@media(min-width:700px){.hs .slab .figs{grid-template-columns:repeat(4,1fr)}}
.hs .slab .figs b{display:block;font-family:'IBM Plex Mono',monospace;
  font-size:34px;color:#fff;line-height:1.05;font-weight:600}
.hs .slab .figs span{font-size:12.5px;color:#9FBDB1;display:block;margin-top:3px}

/* --- navigation --------------------------------------------------------- */
.hs .nb{display:flex;align-items:center;gap:20px;padding:14px var(--pad);
  background:var(--paper);border-bottom:1px solid var(--line);flex-wrap:wrap}
.hs .nb .sp{margin-left:auto}
.hs .nb a{font-size:14.5px;color:var(--ink);font-weight:500}
.hs .nb a.on{color:var(--pine);font-weight:600}
.hs .lgw{display:inline-flex;align-items:center;gap:9px}
.hs .lgw .chip{display:inline-flex;align-items:flex-end;gap:2.5px;
  background:var(--card);border-radius:8px;padding:6px 7px;
  box-shadow:0 1px 2px rgba(27,36,32,.12),0 0 0 1px rgba(27,36,32,.06)}
.hs .lgw .chip i{display:block;width:4px;border-radius:3px}
.hs .lgw .wm{font-weight:600;font-size:18px;letter-spacing:-.03em;
  color:var(--ink);line-height:1.05}
.hs .lgw .sub{display:block;font-family:'IBM Plex Mono',monospace;font-size:9px;
  letter-spacing:.18em;text-transform:uppercase;color:var(--dim);font-weight:400}

/* --- the six paths, Fizzy's label system -------------------------------- */
.hs .paths a{display:grid;grid-template-columns:32px 1fr auto;gap:16px;
  align-items:baseline;padding:20px 0 20px 16px;border-top:1px solid var(--line);
  color:var(--ink);border-left:4px solid transparent}
.hs .paths a:last-child{border-bottom:1px solid var(--line)}
.hs .paths a.p1{border-left-color:var(--p1)}
.hs .paths a.p2{border-left-color:var(--p2)}
.hs .paths a.p3{border-left-color:var(--p3)}
.hs .paths a.p4{border-left-color:var(--p4)}
.hs .paths a.p5{border-left-color:var(--p5)}
.hs .paths a.p6{border-left-color:var(--p6)}
.hs .paths .n{font-family:'IBM Plex Mono',monospace;font-size:11.5px;
  color:var(--dim)}
.hs .paths .t{font-size:30px;font-weight:800;letter-spacing:-.034em;
  display:block;line-height:1.15}
.hs .paths .q{display:block;font-size:15.5px;color:var(--dim);margin-top:3px;
  font-weight:400;letter-spacing:0}
.hs .paths .c{font-family:'IBM Plex Mono',monospace;font-size:11px;
  color:var(--dim);white-space:nowrap}
.hs .dot{display:inline-block;width:10px;height:10px;border-radius:3px;
  margin-right:8px;vertical-align:middle}
.d1{background:#2F6FDB}.d2{background:#7A5AF8}.d3{background:#0E8FA8}
.d4{background:#17864A}.d5{background:#B0730B}.d6{background:#BC3F86}

/* --- the signature, Campfire's move ------------------------------------- */
.hs .sign{border-top:1px solid var(--line);padding-top:20px;margin-top:8px}
.hs .sign .who{font-family:'IBM Plex Mono',monospace;font-size:12.5px;
  color:var(--dim);margin:0}
.hs .sign p.said{max-width:50ch;font-size:21px;line-height:1.42;
  letter-spacing:-.017em;color:var(--ink);margin:0 0 14px;font-weight:500}

/* --- shelves, tables, lists --------------------------------------------- */
.hs .ix{display:grid;gap:20px 32px}
@media(min-width:760px){.hs .ix{grid-template-columns:repeat(3,1fr)}}
.hs .ix h5{font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin:0 0 8px;
  padding-bottom:6px;border-bottom:1px solid var(--line)}
.hs .ix ul{list-style:none;margin:0;padding:0}
.hs .ix li{font-size:15px;line-height:1.55;margin-bottom:5px}
.hs .ix li span{color:var(--dim)}
.hs .list .r{display:grid;grid-template-columns:1fr auto;gap:16px;
  padding:14px 0;border-top:1px solid var(--line);align-items:baseline}
.hs .list .nm2{font-size:19px;font-weight:700;letter-spacing:-.024em}
.hs .list .mt{display:block;font-size:13.5px;color:var(--dim);margin-top:2px}
.hs .list .kk{font-family:'IBM Plex Mono',monospace;font-size:11px;
  color:var(--dim);text-align:right;white-space:nowrap}
.hs .list .kk b{display:block;font-size:20px;color:var(--ink);font-weight:600}
.hs table{border-collapse:collapse;width:100%;font-size:14.5px;margin:0 0 16px}
.hs th{background:var(--deepp);color:#fff;font-family:'IBM Plex Mono',monospace;
  font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  text-align:left;padding:10px 12px;font-weight:600}
.hs td{padding:11px 12px;border-top:1px solid var(--line);vertical-align:top;
  background:var(--card)}
.hs .tw{border-radius:10px;overflow:hidden;
  box-shadow:0 1px 2px rgba(27,36,32,.05),0 0 0 1px rgba(27,36,32,.055)}
.hs .chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}
.hs .chips span{font-size:13px;background:var(--card);color:var(--dim);
  padding:6px 13px;border-radius:20px;box-shadow:0 0 0 1px var(--line)}
.hs .chips span.on{background:var(--pine);color:#fff;box-shadow:none}
.hs .g2{display:grid;gap:16px}
@media(min-width:820px){.hs .g2{grid-template-columns:1fr 1fr}}
.hs .g3{display:grid;gap:14px}
@media(min-width:760px){.hs .g3{grid-template-columns:repeat(3,1fr)}}
.hs .split{display:grid;gap:34px}
@media(min-width:900px){.hs .split{grid-template-columns:1fr 216px}}
.hs .toc{font-size:14px}
.hs .toc b{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--dim);
  margin-bottom:9px}
.hs .toc a{display:block;padding:6px 0;color:var(--dim);
  border-bottom:1px solid var(--line)}
.hs .toc a.on{color:var(--pine);font-weight:600}
.hs .aside{border-left:3px solid var(--goldp);padding-left:16px;margin:22px 0}
.hs .aside p{margin:0;font-size:15.5px}
.hs .pull{font-size:31px;font-weight:800;letter-spacing:-.032em;line-height:1.2;
  border-left:4px solid var(--pine);padding-left:20px;margin:26px 0;
  max-width:40ch}
.hs .meta{font-family:'IBM Plex Mono',monospace;font-size:11px;
  letter-spacing:.08em;color:var(--dim);margin-bottom:14px}
.hs ol.src{padding-left:1.3em;font-size:14px;color:var(--dim)}
.hs ol.src li{margin-bottom:5px}
.hs .steps{counter-reset:s;list-style:none;padding:0;margin:0}
.hs .steps li{counter-increment:s;position:relative;padding-left:38px;
  margin-bottom:16px}
.hs .steps li::before{content:counter(s);position:absolute;left:0;top:1px;
  width:25px;height:25px;border-radius:7px;background:var(--deepp);
  color:var(--goldp);font-family:'IBM Plex Mono',monospace;font-size:12px;
  display:grid;place-items:center;font-weight:600}

/* --- newsletter --------------------------------------------------------- */
.hs .news{border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);
  padding:20px 0;margin:30px 0;display:flex;gap:18px;align-items:center;
  flex-wrap:wrap}
.hs .news .t{font-size:25px;font-weight:800;letter-spacing:-.03em;
  flex:1 1 300px}
.hs .news .in{flex:1 1 210px;background:var(--card);border-radius:6px;
  padding:11px 13px;color:var(--dim);font-size:14.5px;
  box-shadow:0 0 0 1px var(--line)}

/* --- footer ------------------------------------------------------------- */
.hs .ft{background:var(--deepp);color:#B7CCC3;padding:34px var(--pad);
  font-size:13.5px}
.hs .ft .g{display:grid;gap:22px}
@media(min-width:760px){.hs .ft .g{grid-template-columns:1.5fr 1fr 1fr 1fr}}
.hs .ft h6{font-family:'IBM Plex Mono',monospace;font-size:9.5px;
  letter-spacing:.14em;text-transform:uppercase;color:#7FA294;margin:0 0 9px}
.hs .ft a{display:block;padding:3px 0;color:#fff;font-size:13.5px}
.hs .ft .wm{color:#fff;font-weight:600;font-size:17px;letter-spacing:-.03em}
.hs .ft .sub{font-family:'IBM Plex Mono',monospace;font-size:9px;
  letter-spacing:.18em;text-transform:uppercase;color:#7FA294;display:block}
.hs .ft .base{margin-top:26px;padding-top:16px;border-top:1px solid #24564A;
  display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:#7FA294}

/* --- document furniture -------------------------------------------------- */
.tok{border:2px solid var(--ink);background:#fff;box-shadow:5px 5px 0 var(--ink);
  margin:14px 0;overflow:hidden}
.tok .r{display:grid;grid-template-columns:46px 128px 1fr;
  border-top:1px solid var(--line);align-items:center}
.tok .r:first-child{border-top:0}
.tok .sw2{height:44px}
.tok .nm3{font-family:var(--mono);font-size:12px;padding:0 10px}
.tok .ds{font-size:13.5px;color:#39473F;padding:9px 12px}
.huerow{display:grid;gap:8px;margin:12px 0}
@media(min-width:700px){.huerow{grid-template-columns:repeat(6,1fr)}}
.huerow div{border:2px solid var(--ink);padding:8px 10px}
.huerow b{display:block;font-family:var(--mono);font-size:10px;
  margin-bottom:5px}
.huerow i{display:block;height:16px;margin-bottom:6px}
.huerow span{font-size:11.5px;color:#39473F}
.moves{border:2px solid var(--ink);background:#fff;box-shadow:5px 5px 0
  var(--ink);margin:14px 0}
.moves .row{display:grid;grid-template-columns:104px 1fr;
  border-top:1px solid var(--line)}
.moves .row:first-child{border-top:0}
.moves .n{background:var(--deep);color:var(--gold);font-family:var(--mono);
  font-size:10.5px;display:grid;place-items:center;font-weight:600;
  letter-spacing:.1em;padding:8px 4px}
.moves .b{padding:11px 14px}
.moves h4{font-size:15px;margin:0 0 3px}
.moves p{font-size:13.5px;margin:0;color:#39473F}
.lab2{font-family:var(--mono);font-size:10px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--muted);margin:20px 0 6px;display:block}
.note{border-left:5px solid var(--gold);padding:2px 0 2px 16px;margin:16px 0}
.note p{font-size:14.5px;margin:0 0 6px}
code{font-family:var(--mono);font-size:12.5px;background:#fff;
  border:1px solid var(--line);padding:1px 5px}
"""

BUB = [("#2F6FDB", 15), ("#BC3F86", 10), ("#B0730B", 18), ("#17864A", 12),
       ("#0E8FA8", 8)]


def logo(dark=False):
    return ('<span class="lgw"><span class="chip">%s</span>'
            "<span><span class=\"wm\">Therapist Support</span>"
            '<span class="sub">California &middot; free</span></span></span>'
            % "".join('<i style="background:%s;height:%dpx"></i>' % (c, h)
                      for c, h in BUB))


def nb(on=None):
    o = ['<div class="nb">%s<span class="sp"></span>' % logo()]
    for l in ["The six paths", "Calculators", "Library", "About"]:
        o.append('<a class="%s">%s</a>' % ("on" if l == on else "", l))
    o.append('<a class="btn">Open a calculator</a></div>')
    return "".join(o)


def paths(cur=None):
    o = ['<div class="paths">']
    for n, name, q, c, hue in PATHS:
        o.append('<a class="%s"><span class="n">%s</span><span class="t">%s'
                 '<span class="q">&ldquo;%s&rdquo;</span></span>'
                 '<span class="c">%s pages &rarr;</span></a>'
                 % (hue, n, name, q, c))
    o.append("</div>")
    return "".join(o)


def slab(eb, h, p, figs=None):
    o = ['<div class="slab"><span class="eb">%s</span><h2>%s</h2><p>%s</p>'
         % (eb, h, p)]
    if figs:
        o.append('<div class="figs">')
        for v, l in figs:
            o.append("<div><b>%s</b><span>%s</span></div>" % (v, l))
        o.append("</div>")
    o.append("</div>")
    return "".join(o)


def sign(said):
    """The made-by band. It used to be a signature with a name in it.

    The name is out at the author's request, so what is left has to carry the
    same job - who checked this and what happens when it is wrong - without
    the person. That turns out to be a fair trade: the sentence was always
    doing more work than the signature was, and an unsigned first-person
    sentence still reads as a person rather than as a company.
    """
    return ('<div class="sign"><span class="eb">How this is made</span>'
            '<p class="said">%s</p>'
            '<p class="who">Written and checked by a licensed marriage and '
            "family therapist in California &middot; "
            '<a href="#">how corrections work &rarr;</a></p></div>' % said)


IX = [
    ("Calculators", [("Practice Simulator", "what it pays you"),
                     ("Tax &amp; Retirement", "what is optional"),
                     ("Associate Job Advisor", "is this offer fair"),
                     ("Grow Your Practice", "what a client is worth"),
                     ("3,000 Hours", "what holds up your date"),
                     ("Cost of Living", "what a month costs")]),
    ("Money and tax", [("Sole proprietor or corporation", ""),
                       ("The S-corp payroll gap", ""),
                       ("Estimated taxes, four dates", ""),
                       ("Solo 401(k), SEP or SIMPLE", ""),
                       ("What you can deduct", ""),
                       ("The home office, both methods", "")]),
    ("Licensure", [("Becoming an MFT in California", ""),
                   ("Finding a clinical supervisor", "new"),
                   ("BBS fees, 2026", ""),
                   ("Continuing education", ""),
                   ("The practicum year", ""),
                   ("Out-of-state to California", "")]),
    ("Getting paid", [("The California Therapy Rate Gap", ""),
                      ("Insurance panels, and which are open", ""),
                      ("What Medicare and Medi-Cal pay", ""),
                      ("Headway, Alma or Grow, priced", ""),
                      ("Superbills and good faith estimates", "")]),
    ("Running a practice", [("Hiring your first associate", ""),
                            ("Liability insurance, eight programs", ""),
                            ("48 real discipline decisions", ""),
                            ("SimplePractice, priced properly", ""),
                            ("Working remotely, and the Board&rsquo;s answer",
                             "")]),
    ("Training and jobs", [("78 California MFT programs", ""),
                           ("Every PsyD in the state", ""),
                           ("All 58 county job portals", ""),
                           ("What counties pay clinicians", ""),
                           ("Loan forgiveness employers", "")]),
]


def index():
    o = ['<div class="ix">']
    for h, items in IX:
        o.append("<div><h5>%s</h5><ul>" % h)
        for t, note in items:
            o.append("<li>%s%s</li>"
                     % (t, ' <span>&mdash; %s</span>' % note if note else ""))
        o.append("</ul></div>")
    o.append("</div>")
    return "".join(o)


def news(t="One email when a number moves.",
         s="Six last year. Each one because a rule changed."):
    return ('<div class="news"><span class="t">%s<span class="fine" '
            'style="display:block;font-weight:400;margin-top:3px">%s</span>'
            '</span><span class="in">you@example.com</span>'
            '<a class="btn">Subscribe</a></div>' % (t, s))


def foot():
    return ('<div class="ft"><div class="g">'
            '<div><span class="wm">Therapist Support</span>'
            '<span class="sub">California &middot; free</span>'
            '<p style="margin-top:12px;max-width:32ch">Free calculators and '
            "checked reference for California therapists. Every figure "
            "carries the date it was last checked against its source.</p></div>"
            "<div><h6>The six paths</h6>%s</div>"
            "<div><h6>Tools</h6><a>Practice Simulator</a>"
            "<a>Tax &amp; Retirement</a><a>Associate Job Advisor</a>"
            "<a>Grow Your Practice</a><a>3,000 Hours</a>"
            "<a>Cost of Living</a></div>"
            "<div><h6>This site</h6><a>About</a><a>What changed</a>"
            "<a>Every question</a><a>Corrections</a><a>Updates by email</a>"
            "</div></div>"
            '<div class="base"><span>&copy; 2026 Therapist Support</span>'
            "<span>California only</span>"
            "<span>Not legal, tax or career advice</span>"
            "<span>No trackers, no ads, nothing sold</span></div></div>"
            % "".join("<a>%s</a>" % p[1] for p in PATHS))


def frame(url, inner):
    return ('<div class="frame"><div class="bar"><span class="dot"></span>'
            '<span class="dot"></span><span class="dot"></span>'
            '<span class="url">therapistsupport.org%s</span></div>'
            '<div class="hs">%s</div></div>' % (url, inner))


# =========================================================== the six pages
def page_home():
    o = [nb()]
    o.append('<div class="band">'
             "<h1>Running a practice is a <span class=\"scribble\">second "
             "job</span> nobody trained you for.</h1>"
             '<p class="lede">Free calculators and checked reference for '
             "California therapists &mdash; what you keep, what you owe, what "
             "a client is worth, and what a job offer is really paying.</p>"
             '<p style="margin-bottom:10px"><a class="btn">See what your '
             'practice pays you</a> <a class="btn o">Or browse all 203 '
             "pages</a></p>"
             '<p class="fine">Written and checked by one licensed therapist '
             "in California. No account, no email box, nothing sold.</p>"
             "</div>")
    o.append('<div class="band" style="padding-top:6px">'
             '<span class="eb">Or start where you are</span>' + paths()
             + "</div>")
    o.append(slab("Why you can use these numbers",
                  "Every dollar here is the output of a calculation you can "
                  "follow.",
                  "Run on numbers you typed in. There are no illustrative "
                  "figures and no worked examples standing in for your "
                  "practice. When a threshold moves it is listed on a page "
                  "rather than <span class=\"hl\">quietly swapped in</span>.",
                  [("203", "pages, California only"),
                   ("6", "free calculators"),
                   ("58", "county portals checked by hand"),
                   ("$0", "and no email box")]))
    o.append('<div class="band"><h2>Six tools. Each answers one question.</h2>'
             '<div class="g3">')
    for t, q, n in [
        ("Practice Simulator", "What does my practice actually pay me?",
         "$138,940 take-home on a $250,000 practice"),
        ("Tax &amp; Retirement", "How much of my tax bill is optional?",
         "$18,244 of a $69,410 bill"),
        ("Associate Job Advisor", "Is this associate job worth taking?",
         "3,000 hours, priced in weeks"),
        ("Grow Your Practice", "Where do my next ten clients come from?",
         "What one client is worth over their whole time with you"),
        ("3,000 Hours", "What is actually holding up my date?",
         "104 weeks, and the requirement that usually binds"),
        ("Cost of Living", "What does a month cost, and what is left?",
         "Eight places, one practice"),
    ]:
        o.append('<div class="card"><h4>%s</h4>'
                 '<p class="fine" style="margin-bottom:8px">%s</p>'
                 '<p class="fine" style="margin:0;color:var(--pine)">%s</p>'
                 "</div>" % (t, q, n))
    o.append("</div></div>")
    o.append('<div class="band" style="padding-top:8px">'
             "<h2>Everything on the site.</h2>" + index() + "</div>")
    o.append('<div class="band" style="padding-top:0">' + news() + "</div>")
    o.append('<div class="band" style="padding-top:0">'
             + sign("Every number on this site was needed by somebody running a "
                    "California practice before it was published here, and "
                    "worked out from statutes and fee schedules rather than "
                    "from anybody&rsquo;s guess. When a figure turns out to "
                    "be wrong it is fixed and the correction is listed, with "
                    "its date, on the changes page.")
             + "</div>")
    o.append(foot())
    return frame("/", "".join(o))


def page_assoc():
    o = [nb(on="The six paths")]
    o.append('<div class="band" style="border-left:6px solid var(--p4)">'
             '<span class="eb"><span class="dot d4"></span>Path 04 of six '
             "&middot; for AMFTs, ASWs and APCCs</span>"
             "<h1>You are counting toward 3,000.</h1>"
             '<p class="lede">Twenty-one pages written for this stage, every '
             "figure with a named source and a date. The job, the hours, the "
             "supervisor, the money, and the paperwork that decides your "
             "date.</p>"
             '<p><a class="btn">Start with what is holding up your date</a> '
             '<a class="btn o">See all 21 pages</a></p></div>')
    o.append('<div class="band" style="padding-top:0">'
             "<h2>The three questions this room is actually asking.</h2>"
             '<p class="fine" style="max-width:60ch;margin-bottom:18px">Taken '
             "from what people ask each other, in their words rather than "
             "ours.</p>"
             '<div class="list">')
    for q, sub, n in [
        ("&ldquo;547 hours and nobody will hire me.&rdquo;",
         "Where the jobs are, what they pay, and which employers can lawfully "
         "bill for a pre-licensed clinician", "5 pages"),
        ("&ldquo;How do I even find a supervisor?&rdquo;",
         "Every list that exists, checked &mdash; and the rule that decides "
         "whether the one you find can count your hours at all", "2 pages"),
        ("&ldquo;Am I being underpaid?&rdquo;",
         "What associates are actually paid in LA and the Bay, what unpaid "
         "work costs, and what a flat rate per clinical hour really means",
         "4 pages"),
    ]:
        o.append('<div class="r"><div><span class="nm2">%s</span>'
                 '<span class="mt">%s</span></div>'
                 '<span class="kk">%s &rarr;</span></div>' % (q, sub, n))
    o.append("</div></div>")
    o.append('<div class="band" style="padding-top:22px"><div class="card">'
             '<span class="eb">The tool</span>'
             "<h3>What is actually holding up your date</h3>"
             '<p class="fine" style="max-width:56ch">Four requirements run at '
             "once and only one of them is usually binding. Put your hours in "
             "and it says which. <b>Nothing you type leaves your "
             "browser.</b></p>"
             '<div class="tw" style="margin-top:14px"><table>'
             "<tr><th>Requirement</th><th>You have</th><th>Needed</th>"
             "<th>Binding?</th></tr>"
             "<tr><td>Total hours</td><td>547</td><td>3,000</td>"
             "<td>&mdash;</td></tr>"
             "<tr><td>Supervised weeks</td><td>19</td><td>104</td>"
             "<td><b>Yes &mdash; this is your date</b></td></tr>"
             "<tr><td>Individual or triadic weeks</td><td>19</td><td>52</td>"
             "<td>&mdash;</td></tr>"
             "<tr><td>Direct client hours</td><td>402</td><td>1,750</td>"
             "<td>&mdash;</td></tr></table></div>"
             '<p class="fine" style="margin:12px 0 0">The 3,000 is almost '
             "never what decides your date. The weeks are.</p></div></div>")
    o.append(slab("What differs by registration",
                  "If you are an ASW, two rules apply that nobody else has.",
                  "<b>1,700 of your 3,000 hours</b> must be supervised by an "
                  "LCSW, and <b>13 of your 52</b> individual or triadic weeks "
                  "must be too. They are independent &mdash; meeting one does "
                  "not meet the other. APCCs have no equivalent rule, and "
                  "neither do AMFTs."))
    o.append('<div class="band"><h2>Everything for this stage.</h2>'
             '<div class="ix">')
    for h, items in [
        ("Getting the job", [
            ("Getting hired as a California associate",
             "what employers actually screen on"),
            ("All 58 county job portals", "seven guessable URLs are wrong"),
            ("What counties pay clinicians", "from the payroll file"),
            ("Associate pay, LA and the Bay", "19 employer scales"),
            ("Loan forgiveness employers", "and the test each one meets")]),
        ("The hours themselves", [
            ("What is holding up your 3,000", "the tool above"),
            ("Finding a clinical supervisor", "every list, checked"),
            ("Unpaid associate work", "what it costs, and what the Labor "
                                      "Commissioner says"),
            ("Hours by telehealth, out of state", "the Board&rsquo;s answer"),
            ("Hours trackers compared", "including the ones to avoid")]),
        ("The paperwork and the risk", [
            ("BBS fees, 2026", "halved in July, reverting in 2030"),
            ("Continuing education", "36 hours, and the 62% that fail"),
            ("48 real discipline decisions", "de-identified"),
            ("Liability insurance", "eight programs priced"),
            ("Exam pass rates", "from the Board&rsquo;s own statistics")]),
    ]:
        o.append("<div><h5>%s</h5><ul>" % h)
        for t, note in items:
            o.append("<li>%s <span>&mdash; %s</span></li>" % (t, note))
        o.append("</ul></div>")
    o.append("</div></div>")
    o.append('<div class="band" style="padding-top:0">'
             + news("Told when the Board moves a rule.",
                    "The BBS changes these every couple of years. One email "
                    "when it does.")
             + sign("This page exists because none of it was written down in one "
                    "place. If something here has gone out of date, say so "
                    "&mdash; it gets fixed and the change is listed with its "
                    "date rather than quietly swapped in.")
             + "</div>")
    o.append(foot())
    return frame("/paths/counting-hours", "".join(o))


def page_article():
    o = [nb()]
    o.append('<div class="band"><div class="split"><div>'
             '<p class="meta">LICENSURE &middot; CHECKED 13 AUGUST 2026 '
             "&middot; 30 SOURCES</p>"
             "<h1>Finding a clinical supervisor in California.</h1>"
             '<p class="lede">The Board does not certify supervisors and '
             "keeps no roster, so this is where the lists actually are "
             "&mdash; and the rule that decides whether the person you find "
             "can count your hours at all.</p>"
             "<p>California licenses 165,000 people and publishes a list of "
             "exactly <span class=\"scribble\">zero</span> supervisors. It "
             "does not approve them in advance, does not keep a register of "
             "them, and its license lookup has no supervisor field. What "
             "exists instead is nine county chapter directories, one "
             "statewide association list with no contact details on it, and "
             "two commercial products.</p>"
             '<p class="pull">In a private practice, you cannot simply hire '
             "your own supervisor.</p>"
             "<p>BPC &sect;4980.43.4(b)(1) requires a supervisor of an "
             "associate in a private practice to be <b>employed by, "
             "contracted by, or an owner of the associate&rsquo;s "
             "employer</b>. Those are the three permitted statuses. "
             "&ldquo;Paid by the associate&rdquo; is not one of them, and "
             "weeks under a privately retained supervisor are not "
             "creditable.</p>"
             '<div class="aside"><p><b>There is a lawful route, and it needs '
             "your employer to act.</b> The employer contracts the "
             "supervisor, and a written oversight agreement is signed "
             "<b>before supervision starts</b> &mdash; not within any grace "
             "period.</p></div>"
             "<h2>Where the lists actually are</h2>"
             "<p>Every candidate was fetched on 13 August 2026. Nine of the "
             "twenty-three CAMFT chapters publish a supervisor list; fourteen "
             "do not, and two of the chapters that are supposed to carry one "
             "no longer exist as organizations.</p>"
             '<div class="tw"><table>'
             "<tr><th>List</th><th>Who runs it</th><th>Entries</th></tr>"
             "<tr><td>LA-CAMFT, Supervision Offered</td><td>CAMFT chapter</td>"
             "<td>314</td></tr>"
             "<tr><td>CAMFT Certified Supervisors</td><td>Association</td>"
             "<td>302</td></tr>"
             "<tr><td>East Bay CAMFT Supervision Finder</td>"
             "<td>CAMFT chapter</td><td>150</td></tr>"
             "<tr><td>Marin CAMFT</td><td>CAMFT chapter</td><td>116</td></tr>"
             "</table></div>"
             '<p class="fine">Counts are what each source reports on its own '
             "page. Nothing from any of these directories is reproduced here "
             "&mdash; they are other people&rsquo;s membership lists.</p>"
             "<h2>What it costs</h2>"
             "<p>There is no fee schedule for supervision in California and "
             "no survey of what supervisors charge. What exists is one "
             "question in the Board&rsquo;s own 2024 Pathway to Licensure "
             "survey: <b>18% of 3,168 respondents paid at all</b>, and of "
             "those who did, <b>35% paid more than $300 a month</b>.</p>"
             "<h3>Sources</h3>"
             '<ol class="src"><li>BPC &sect;4980.03(g) &mdash; supervisor '
             "qualifications</li>"
             "<li>BPC &sect;4980.43.4 &mdash; the private-practice rule and "
             "the oversight agreement</li>"
             "<li>16 CCR &sect;1833 &mdash; the 60-day supervision "
             "agreement</li>"
             "<li>BBS 2025 Sunset Review Report, Attachment C-1C &mdash; the "
             "cost figures</li></ol>"
             "</div>"
             '<div class="toc"><b>On this page</b>'
             '<a class="on">Where the lists are</a>'
             "<a>The private-practice trap</a><a>Whether they may supervise "
             "you</a><a>What the week looks like</a><a>What it costs</a>"
             "<a>Three deadlines</a><a>What to ask</a><a>Sources</a>"
             '<div class="card" style="margin-top:18px;padding:14px 15px">'
             '<span class="eb" style="margin-bottom:6px">In this stage</span>'
             '<p class="fine" style="margin:0"><span class="dot d4"></span>'
             "Counting hours &mdash; 21 pages</p></div>"
             "</div></div></div>")
    o.append(slab("The one thing to take away",
                  "A privately retained supervisor is not a supervisor, in a "
                  "private practice.",
                  "Somebody who spends three months paying a supervisor they "
                  "found themselves, at a practice that never contracted "
                  "them, has <span class=\"hl\">bought nothing</span>. Ask "
                  "the question before the first session, not at the end."))
    o.append('<div class="band">' + news() +
             sign("Every statute on this page is linked to its own text, so "
                  "none of it has to be taken on trust. People lose months "
                  "to the rule above; that is why it is at the top.") + "</div>")
    o.append(foot())
    return frame("/finding-a-clinical-supervisor-california", "".join(o))


def page_dir():
    o = [nb()]
    o.append('<div class="band">'
             '<p class="meta">DIRECTORY &middot; EVERY ENTRY FETCHED '
             "13 AUGUST 2026</p>"
             "<h1>Where a California supervisor list actually is.</h1>"
             '<p class="lede">Fifteen candidates fetched and counted. Nine of '
             "the twenty-three CAMFT chapters publish one, fourteen do not, "
             "and three of the addresses people are still sent to no longer "
             "exist.</p>"
             '<div class="chips"><span class="on">All 15</span>'
             "<span>Free to browse</span><span>CAMFT chapters</span>"
             "<span>Statewide</span><span>Shows availability</span>"
             "<span>Bay Area</span><span>Southern California</span></div>"
             '<div class="list">')
    for nm, mt, k in [
        ("Psychology Today, clinical supervision", "Statewide &middot; "
         "self-declared category &middot; has contact details", "3,875"),
        ("LA-CAMFT, Supervision Offered",
         "Los Angeles &middot; name, phone, city &middot; free", "314"),
        ("CAMFT Certified Supervisors",
         "Statewide &middot; name and city only &middot; free", "302"),
        ("East Bay CAMFT Supervision Finder",
         "East Bay &middot; supervision type and credentials", "150"),
        ("Marin CAMFT Supervisor Directory",
         "North Bay &middot; phone and supervision type", "116"),
        ("Redwood Empire CAMFT", "Sonoma and the North Coast", "99"),
        ("Orange County CAMFT",
         "Orange County &middot; the only real list south of LA", "63"),
        ("Zencare, clinical supervision",
         "Statewide &middot; the only source showing live availability", "49"),
    ]:
        o.append('<div class="r"><div><span class="nm2">%s</span>'
                 '<span class="mt">%s</span></div>'
                 '<span class="kk"><b>%s</b>entries</span></div>' % (nm, mt, k))
    o.append("</div></div>")
    o.append(slab("The finding",
                  "Coverage is not where the people are.",
                  "Marin publishes 116 names and Redwood Empire 99, for a "
                  "combined population under a million. <b>San Diego, "
                  "Sacramento, San Francisco, Santa Clara Valley, the San "
                  "Fernando Valley and Ventura publish none at all</b> "
                  "&mdash; which is most of the state&rsquo;s associates."))
    o.append('<div class="band"><div class="g2">'
             '<div><h3>Checked, and there is nothing there</h3>'
             '<p class="fine">Nine places people are sent that publish no '
             "list: the Board itself, NASW California, CALPCC, CalSWEC, "
             "TherapyDen, Open Path, Alma and Headway, CounselingCalifornia, "
             "and CalMHSA &mdash; which buys supervision in bulk and sells it "
             "to counties, not to people.</p></div>"
             '<div><h3>Still ranked, no longer there</h3>'
             '<p class="fine"><code>rrccamft.org</code> resolves and lands on '
             "an unrelated commercial site &mdash; the domain was sold. "
             "<code>sierrafoothillscamft.com</code> and "
             "<code>supervisiondirectory.com</code> do not resolve at all. "
             "CAMFT&rsquo;s own chapter-links page still points at two of "
             "them.</p></div></div>"
             '<p class="fine" style="max-width:70ch;margin-top:18px">Counts '
             "are what each source reports about itself. Nothing from any of "
             "these directories is reproduced here, and a link is an address "
             "rather than a recommendation &mdash; this site has not met "
             "these supervisors and takes nothing from anybody for a "
             "mention.</p></div>")
    o.append('<div class="band" style="padding-top:0">' + news() + "</div>")
    o.append(foot())
    return frame("/finding-a-clinical-supervisor-california#lists",
                 "".join(o))


def page_email():
    o = [nb()]
    o.append('<div class="band"><div class="split"><div>'
             "<h1>One email when a number <span class=\"scribble\">moves"
             "</span>.</h1>"
             '<p class="lede">The Board changes its fees, the IRS changes a '
             "threshold, a payer quietly re-prices a code. That is when this "
             "sends. Not weekly, not a digest, not a funnel.</p>"
             '<div class="card"><h3>What actually gets sent</h3>'
             '<ol class="steps" style="margin-top:14px">'
             "<li><b>A rule changed</b>, and what it does to your arithmetic. "
             "The change, the source, the new number, and which page moved."
             "</li>"
             "<li><b>A new calculator</b>, once, when one lands.</li>"
             "<li><b>A correction</b>, when I get something wrong. These go "
             "out even when it is embarrassing.</li></ol>"
             '<div class="news" style="margin:20px 0 0;border-bottom:0;'
             'padding-bottom:0"><span class="in">you@example.com</span>'
             '<a class="btn">Subscribe</a></div>'
             '<p class="fine" style="margin:12px 0 0">Unsubscribe link in '
             "every one. The list is never used for anything else, never "
             "sold, and never rented.</p></div>"
             "<h2 style=\"margin-top:32px\">Everything sent last year.</h2>"
             '<p class="fine" style="max-width:58ch">Six emails. The claim is '
             "a number rather than an adjective, so you can check it before "
             "you subscribe.</p>"
             '<div class="list">')
    for d, t in [
        ("14 Jul 2026", "BBS fees halved &mdash; what it saves you, and the "
                        "2030 reversion"),
        ("02 May 2026", "The 2026 federal brackets, and the one that changes "
                        "S-corp math"),
        ("19 Mar 2026", "Correction: the CIIS tuition card was wrong for six "
                        "days"),
        ("28 Jan 2026", "Medi-Cal rates re-priced per code"),
        ("11 Nov 2025", "New: the Associate Job Advisor"),
        ("03 Sep 2025", "Supervision agreement form renumbered to 37M-300"),
    ]:
        o.append('<div class="r"><div><span class="nm2">%s</span></div>'
                 '<span class="kk">%s</span></div>' % (t, d))
    o.append("</div></div>"
             '<div class="toc"><b>Why trust the list</b>'
             '<p class="fine" style="margin:0 0 12px">No tracking pixel. The '
             "email does not know whether you opened it.</p>"
             '<p class="fine" style="margin:0 0 12px">No segmentation, no '
             "drip sequence, no re-engagement campaign.</p>"
             '<p class="fine" style="margin:0">Nothing is sold here, so there '
             "is nothing to sell you later.</p></div>"
             "</div></div>")
    o.append(slab("The promise, as a number",
                  "Six emails in twelve months.",
                  "Every one of them because a figure on this site changed. "
                  "You can read all six above <span class=\"hl\">before you "
                  "subscribe</span>, which is not a thing most newsletters "
                  "let you do."))
    o.append('<div class="band">'
             + sign("If the list ever becomes something other than this, the "
                    "email that changes it will say so, and you can leave "
                    "from that same email.") + "</div>")
    o.append(foot())
    return frame("/updates", "".join(o))


def page_about():
    o = [nb(on="About")]
    o.append('<div class="band">'
             '<span class="eb">About</span>'
             "<h1>Who made this, and what I want from you.</h1>"
             '<p class="lede" style="max-width:48ch">Nothing. There is no '
             "email box on the tools, no account, no course at the end and no "
             "affiliate link on any figure that matters.</p>"
             '<div class="list" style="max-width:74ch">')
    for q, a in [
        ("Who made it?",
         "One licensed marriage and family therapist in California, who "
         "needed these numbers first and could not find them."),
        ("What do they want?",
         "Nothing is sold here. There is a newsletter and it sends about six "
         "times a year, and you can read every past issue before you give it "
         "an address."),
        ("Why should you believe a figure?",
         "Because it says where it came from and when it was last checked, "
         "and because the ones that moved are listed on a page instead of "
         "being quietly replaced."),
        ("What if it is wrong?",
         "Tell me. It gets fixed, and the correction is listed on the "
         "changes page with the date &mdash; including the embarrassing "
         "ones, of which there have been three."),
    ]:
        o.append('<div class="r"><div><span class="nm2">%s</span>'
                 '<span class="mt">%s</span></div></div>' % (q, a))
    o.append("</div></div>")
    o.append(slab("The one rule everything else follows from",
                  "It computes, it doesn&rsquo;t opine.",
                  "Every dollar on this site is the output of a calculation "
                  "you can follow, run on numbers you typed in. There are no "
                  "illustrative figures, no worked examples standing in for "
                  "your practice, and <span class=\"hl\">nothing you type "
                  "leaves your browser</span>.",
                  [("203", "pages"), ("6", "free calculators"),
                   ("0", "trackers"), ("3", "corrections published")]))
    o.append('<div class="band"><div class="g3">'
             '<div class="card"><h4>What this is</h4>'
             '<p class="fine" style="margin:0">Six calculators and 203 '
             "checked pages, for California only. Written for LMFTs, LCSWs, "
             "LPCCs, psychologists and registered associates.</p></div>"
             '<div class="card"><h4>What it is not</h4>'
             '<p class="fine" style="margin:0">Legal, tax or career advice. '
             "A directory that takes payment for a listing. A lead magnet for "
             "something else.</p></div>"
             '<div class="card"><h4>How it is paid for</h4>'
             '<p class="fine" style="margin:0">It is not. It costs very '
             "little to run, and that is the whole business model. If that "
             "ever changes it will be said here first.</p></div>"
             "</div></div>")
    o.append('<div class="band" style="padding-top:0">'
             + sign("The numbers a California practice runs on &mdash; a fair "
                    "rate, what an associate job really pays, whether to "
                    "incorporate, what insurance actually reimburses &mdash; "
                    "are not published anywhere as a set. They were worked "
                    "out one at a time here, from statutes and fee schedules, "
                    "and every one of them shows its source.")
             + "</div>")
    o.append('<div class="band" style="padding-top:0">' + news() + "</div>")
    o.append(foot())
    return frame("/about", "".join(o))


PAGES = [("home", "The home page", "/", page_home),
         ("assoc", "The associate landing page", "/paths/counting-hours",
          page_assoc),
         ("article", "A content page", "/finding-a-clinical-supervisor",
          page_article),
         ("dir", "A directory listing", "#lists", page_dir),
         ("email", "The email sign-up", "/updates", page_email),
         ("about", "About", "/about", page_about)]


# =============================================================== the build
def build():
    donor = open(DONOR, encoding="utf-8").read()
    m = re.search(r"<style>([\s\S]*?)</style>", donor)
    if not m:
        sys.exit("ops/stage-architecture.html has no <style> block")
    css = m.group(1) + EXTRA

    o = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<meta name="robots" content="noindex,nofollow">',
         "<title>The house style, drawn as six complete pages</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+'
         'Grotesque:opsz,wght@12..96,800&'
         'family=Fraunces:opsz,wght@9..144,600;9..144,800&'
         'family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700;800&'
         'display=swap" rel="stylesheet">',
         "<style>%s</style></head><body>" % css]

    o.append('<header class="mast"><div class="wrap">'
             '<span class="lab">Working document &middot; %s</span>'
             "<h1>The fifth thing, built.</h1>"
             "<p>Not one of the four products &mdash; the recommendation from "
             "P7, drawn as <b>six complete pages</b>, top to bottom, with "
             "every band a real page would carry. <b>Basecamp&rsquo;s "
             "structure and restraint</b>, <b>Fizzy&rsquo;s label system</b> "
             "on the six paths, <b>Campfire&rsquo;s signature</b> at the end "
             "of anything that makes a claim about who checked the numbers, "
             "and <b>exactly one HEY slab per page</b>, for the one claim "
             "that page is making.</p>"
             '<div class="meta"><span class="chip">6 full pages</span>'
             '<span class="chip">1 slab each, no exceptions</span>'
             '<span class="chip">6 path hues</span>'
             '<span class="chip">Ready to build</span></div>'
             "</div></header>" % UPDATED)

    o.append('<nav class="jump"><div class="wrap"><ul>')
    for h, t in NAV:
        o.append('<li><a href="#%s">%s</a></li>' % (h, t))
    o.append("</ul></div></nav>")
    o.append('<div class="wrap">')

    # --------------------------------------------------------------- system
    o.append('<section id="system"><div class="kicker">'
             '<span class="n">01</span><h2>The system</h2></div>')
    o.append('<p class="lede">Four borrowed moves, one rule on each. The rule '
             "matters more than the move &mdash; three of these four fail if "
             "they are used more than the rule allows.</p>")
    o.append('<div class="moves">')
    for src, h, p in [
        ("Basecamp", "Restraint is the default",
         "Tinted paper and never pure white. One accent. Flat fills with a "
         "hairline ring and a soft shadow rather than borders. And small type "
         "by marketing standards &mdash; <b>16.5px body</b>, because these "
         "pages run six thousand words with tables in them, not four hundred "
         "words with a screenshot."),
        ("Fizzy", "Six hues, one per path",
         "Used as a 10px chip and a 4px left rule. <b>Never as a background, "
         "never as body text, never on a button.</b> The job is that a reader "
         "recognizes their path in a list without reading it, and that job is "
         "done with a rule and a dot."),
        ("Campfire", "A made-by band closes anything that makes a claim",
         "Home page, about page, and every article. Campfire ends a page with "
         "a handwritten signature; this ends it with the sentence that "
         "signature was there to support, and no name. The author does not "
         "want one on the page, so the band has to carry the job alone "
         "&mdash; who checked this, and what happens when it is wrong. That "
         "is a fair trade: the sentence was always doing more work than the "
         "signature was."),
        ("HEY", "One slab per page. One.",
         "Deep pine, scalloped top and bottom edges, and it goes to the "
         "single claim that page is making &mdash; not to a feature list. A "
         "second slab on the same page halves the value of the first, which "
         "is why the guard on this document fails a build that ships two."),
    ]:
        o.append('<div class="row"><div class="n">%s</div><div class="b">'
                 "<h4>%s</h4><p>%s</p></div></div>" % (src.upper(), h, p))
    o.append("</div>")

    o.append('<span class="lab2">Tokens</span>')
    o.append('<div class="tok">')
    for name, hexv, desc, dark in TOKENS:
        o.append('<div class="r"><div class="sw2" style="background:%s"></div>'
                 '<div class="nm3">%s</div><div class="ds">%s &middot; '
                 "<b>%s</b></div></div>" % (hexv, name, desc, hexv))
    o.append("</div>")

    o.append('<span class="lab2">The six path hues</span>')
    o.append('<div class="huerow">')
    for key, hexv, name in HUES:
        o.append('<div><i style="background:%s"></i><b>%s</b>'
                 "<span>%s</span></div>" % (hexv, hexv, name))
    o.append("</div>")
    o.append('<p class="pk-d" style="font-size:13.5px;color:#39473F">Each '
             "clears 4.5:1 against the paper, so a hue may carry a label if "
             "it ever needs to. None of them is used as a fill behind body "
             "text, which is the failure mode of every color-coded "
             "navigation ever shipped.</p>")

    o.append('<div class="note"><p><b>What is deliberately not borrowed.</b> '
             "No gradients, from anywhere. No 32px body text, which three of "
             "the four use and which would make a reference page unreadable. "
             "No full-page saturated canvas. No pill buttons &mdash; "
             "Basecamp&rsquo;s 6px is the right amount of soft for something "
             "clicked twenty times a session.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # ------------------------------------------------------------ the pages
    for i, (anchor, title, url, fn) in enumerate(PAGES, start=2):
        o.append('<section id="%s"><div class="kicker">'
                 '<span class="n">%02d</span><h2>%s</h2></div>'
                 % (anchor, i, title))
        o.append('<p class="lede">%s</p>' % {
            "home": "Statement, one action, authorship, the six paths, the "
                    "slab, the tools, the whole index, the newsletter, the "
                    "signature. Eleven blocks became nine, and four of them "
                    "are lists.",
            "assoc": "The room&rsquo;s three questions in its own words "
                     "first, then the tool, then the shelf. The path hue runs "
                     "down the left edge of the header and appears again on "
                     "every leaf page in this stage.",
            "article": "A single measure with a contents rail. The slab "
                       "carries the one thing to take away, which on this "
                       "page is the correction the whole article exists for.",
            "dir": "The shape that covers 58 county portals, 78 programs, 15 "
                   "supervisor lists and 48 discipline decisions. Filters as "
                   "chips, counts on the right, and the negative findings "
                   "given equal weight.",
            "email": "The claim is a number, and the archive is on the page "
                     "above the form &mdash; you can read every past issue "
                     "before giving an address.",
            "about": "Four questions as rows, the rule everything follows "
                     "from in the slab, and the signature doing the work it "
                     "was borrowed for.",
        }[anchor])
        o.append(fn())
        o.append("</section><hr class=\"rule\">")

    # --------------------------------------------------------------- build
    o.append('<section id="build"><div class="kicker">'
             '<span class="n">08</span><h2>How to build it</h2></div>')
    o.append('<p class="lede">In an order where nothing has to be finished '
             "before anything else is useful.</p>")
    o.append('<div class="moves">')
    for n, h, p in [
        ("STEP 1", "The tokens and the two type sizes",
         "One stylesheet. Everything above is eight color tokens, six hues, "
         "four heading sizes and one body size. It replaces the current "
         "palette rather than sitting beside it, so this is the step that "
         "cannot be half done."),
        ("STEP 2", "The navigation, the footer and the signature block",
         "Three components on 203 pages, all three generated by existing "
         "passes. The signature is a partial with one sentence that varies "
         "per page."),
        ("STEP 3", "The home page",
         "It is the page in section 02, and every link on it already exists. "
         "No URL moves."),
        ("STEP 4", "The six path pages",
         "Generated from the <code>stages</code> tagging already in "
         "<code>registry.json</code>. Path 3 stays folded into path 4 until "
         "it has content of its own &mdash; four pages is not a "
         "destination."),
        ("STEP 5", "The article and directory templates",
         "These two shapes cover roughly 190 of the 203 pages, so this is the "
         "step where the redesign is actually felt by a reader."),
        ("STEP 6", "The email page, the about page, the slab audit",
         "Last, and the audit is the part to not skip: walk every page and "
         "confirm it carries <b>exactly one</b> slab. The rule is the design."),
    ]:
        o.append('<div class="row"><div class="n">%s</div><div class="b">'
                 "<h4>%s</h4><p>%s</p></div></div>" % (n, h, p))
    o.append("</div>")
    o.append('<div class="note"><p><b>What this does not decide.</b> The '
             "typeface. Everything above is set in Inter, which is free, "
             "loads fast and is deliberately unremarkable &mdash; it is the "
             "right default and it is also the easiest thing to change later, "
             "because it is one token. If a licensed face is bought, buy it "
             "after the structure ships, not before.</p>"
             "<p><b>And still true:</b> a redesign and a move to Rails are "
             "two projects. This ships on the current static build; Rails "
             "would inherit finished templates.</p></div>")
    o.append("</section>")

    o.append("</div>")
    o.append('<footer><div class="wrap"><p style="margin:0">Working document, '
             "not linked from the site and not indexable. The six pages are "
             "drawings &mdash; no link in them goes anywhere, and the figures "
             "in them are the site&rsquo;s real ones. Written %s.</p>"
             "</div></footer>" % UPDATED)
    o.append("</body></html>")
    return "".join(o)


def main():
    print("the house style, six full pages")
    html = build()
    open(OUT, "w", encoding="utf-8").write(html)
    print("  wrote ops/%s, %s bytes"
          % (os.path.basename(OUT), format(len(html), ",d")))

    bad = 0
    for h, _ in NAV:
        if 'id="%s"' % h not in html:
            print("GUARD: the jump nav points at #%s, absent" % h)
            bad += 1
    n = html.count('class="frame"')
    if n != len(PAGES):
        print("GUARD: %d pages, expected %d" % (n, len(PAGES)))
        bad += 1

    # The rule IS the design: one slab per page, and the guard is the reason
    # the rule survives contact with a second good idea.
    for anchor, title, _u, fn in PAGES:
        k = fn().count('class="slab"')
        if k != 1:
            print("GUARD: %s carries %d slabs - the rule is exactly one"
                  % (title, k))
            bad += 1
        if 'class="sign"' not in fn() and anchor in ("home", "about",
                                                     "article", "assoc"):
            print("GUARD: %s has no signature" % title)
            bad += 1
        if '<div class="nb' not in fn() or 'class="ft"' not in fn():
            print("GUARD: %s is missing its navigation or footer - these are "
                  "whole pages, not fragments" % title)
            bad += 1

    # Every path, and every hue, or the label system is decorative.
    for _num, name, q, _c, hue in PATHS:
        if name not in html or q not in html:
            print("GUARD: path %r is incomplete" % name)
            bad += 1
    for key, hexv, _n in HUES:
        if hexv not in html:
            print("GUARD: hue %s is defined and never drawn" % hexv)
            bad += 1

    # The author asked for no name on the page. A guard, because the
    # signature pattern is the kind of thing that gets pasted back in.
    for nm in ("Shawn", "Walters", "LMFT &middot; California &middot;"):
        if nm in html:
            print("GUARD: %r appears - no personal name goes at the foot of "
                  "these pages" % nm)
            bad += 1
    if "Caveat" in html:
        print("GUARD: the handwriting face is still loaded and nothing uses it")
        bad += 1

    for needle, what in [
        ("One slab per page. One.", "the rule that carries the design"),
        ("Never as a background", "the limit on the hue system"),
        ("17.5px body", "the density decision"),
        ("two projects", "the Rails answer"),
    ]:
        if needle not in html:
            print("GUARD: %s is missing" % what)
            bad += 1

    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    for w in ("programme", "counselling", "centre", "whilst", "amongst",
              "recognise", "organisation", "behaviour", "fulfilment",
              "judgement"):
        if re.search(r"\b%s" % w, t, re.I):
            print("GUARD: British spelling %r" % w)
            bad += 1
    for mm in re.finditer(r"\bgates?\b", t, re.I):
        print("GUARD: %r - removed sitewide" % mm.group(0))
        bad += 1
    if 'name="robots" content="noindex' not in html:
        print("GUARD: working document must not be indexable")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d full pages, one slab each, %d hues"
          % (n, len(HUES)))


if __name__ == "__main__":
    main()
