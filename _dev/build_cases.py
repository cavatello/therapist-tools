#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the discipline case library: one hub plus thirty case pages.

WHY THIS EXISTS

The insurance page answers "what should I buy". It cannot answer "what actually
happens", because the honest answer to that is not a table of sublimits - it is
thirty real California decisions. A therapist reading a $35,000 board-defense
sublimit has no way to know whether that is generous or derisory until they have
seen that a contested boundary case costs $7,644 in the Board's costs alone,
before their own lawyer, and that the probation afterwards is uninsured.

So this library is the evidence behind the insurance page, and the insurance
page is the practical consequence of this library. They link both ways.

WHAT IS DELIBERATELY NOT HERE

Names. Every one is public record and the site does not republish them; the
reasoning is written out in case_data.py and stated on the hub page itself.
Every case carries its case number and effective date, and the hub documents
the exact route to the signed decision, so nothing here is unverifiable.

STRUCTURE

    therapist-discipline-cases-california.html   the hub - AIDA hero, the
        aggregate picture, the subdivision map, the cost bands, the fifteen
        probation conditions, and the thirty cases grouped by what went wrong

    discipline-case-<slug>.html   x30 - what happened, what was charged with a
        real link to each code section, the outcome, the money, what the rule
        actually requires, where insurance reaches, and what would have changed
        it

Chrome, and its scripts, are lifted from a donor article page. That "and its
scripts" is not decorative: this project shipped a page whose nav markup was
present and whose nav did nothing, because the binding script lives after
</footer> in the donor and the header slice stopped at </header>. The guard at
the bottom refuses to write a page whose nav cannot open.

Run:  python3 _dev/build_cases.py
Then: restyle -> extract_css -> css_cdo_fix -> css_dedupe -> seo_sitemap
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from case_data import (CASES, GROUPS, AGGREGATE, SUBD_COUNTS, PROBATION_TERMS,  # noqa: E402
                       COST_BANDS, CITATION_GROUNDS, CHECKED, NEWSLETTERS,
                       LAWSREGS, DISPGUID, SUNSET, BROCHURE)
# The discussion layer. Kept in its own module so that `case_data.py` stays a
# record of what the decisions say and nothing else - see the header of
# `case_depth.py` for why that separation is load-bearing rather than tidy.
from case_depth import DEPTH  # noqa: E402

HUB = "therapist-discipline-cases-california.html"
CHROME_FROM = os.path.join(SITE, "hiring-first-associate-california-therapist.html")
INSURANCE = "therapy-liability-insurance-california.html"

INK = "#16211B"
PINE = "#2C6350"
GOLD = "#F6C560"
PAPER = "#F4F0E6"
CREAM = "#FBF9F3"
MUTED = "#635E53"
RED = "#B5483F"
FLOOR = 4.5


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (_lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


CONTRAST = [
    ("body on cream", MUTED, CREAM, FLOOR),
    ("body on white", MUTED, "#FFFFFF", FLOOR),
    ("body on paper", MUTED, PAPER, FLOOR),
    ("heading on cream", INK, CREAM, 3.0),
    ("label pine on cream", PINE, CREAM, FLOOR),
    ("label pine on paper", PINE, PAPER, FLOOR),
    ("ink on gold", INK, GOLD, FLOOR),
    ("white on pine", "#FFFFFF", PINE, FLOOR),
    ("gold on pine", "#FFD37A", PINE, FLOOR),
    ("gold on ink", GOLD, INK, FLOOR),
    ("white on ink", "#FFFFFF", INK, FLOOR),
    ("caution red on cream", RED, CREAM, FLOOR),
]

# ---------------------------------------------------------------------- CSS
# One block, shared by all 31 pages, so extract_css hoists it once.
CSS = """<style>/* _dev/build_cases.py */
.dc-wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.dc-sec{margin:34px 0}
.dc-k{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.14em;text-transform:uppercase;color:%(pine)s;margin:0 0 6px}
.dc-h{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.032em;font-size:27px;line-height:1.12;color:%(ink)s;margin:0 0 9px}
.dc-d{font-size:15.4px;line-height:1.68;color:%(muted)s;margin:0 0 16px;max-width:68ch}
.dc-d b{color:%(ink)s}
.dc-d i{color:%(ink)s;font-style:italic}

/* ------------------------------------------------------------- the hero */
.dc-hero{border:2px solid %(ink)s;border-radius:16px;box-shadow:8px 8px 0 %(ink)s;
  background:%(pine)s;color:#fff;padding:30px 30px 26px;margin:0 0 26px}
.dc-hero .hk{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.15em;text-transform:uppercase;color:#FFD37A;margin:0 0 12px}
.dc-hero h1{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.034em;font-size:41px;line-height:1.03;color:#fff;margin:0 0 14px;
  max-width:19ch}
.dc-hero .hl{font-size:17px;line-height:1.6;color:rgba(255,255,255,.9);margin:0 0 18px;
  max-width:62ch}
.dc-hero .hl b{color:%(gold)s}
.dc-figs{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border:2px solid %(ink)s;
  border-radius:12px;overflow:hidden;margin:0 0 18px;background:%(ink)s}
.dc-figs>div{background:%(cream)s;padding:14px 15px}
.dc-figs .n{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:29px;
  line-height:1;color:%(ink)s;display:block;letter-spacing:-.02em}
.dc-figs .l{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.1em;text-transform:uppercase;color:%(pine)s;display:block;
  margin:8px 0 0;line-height:1.5}
.dc-hero .hj{display:flex;flex-wrap:wrap;gap:9px;margin:0}
.dc-hero .hj a{display:inline-block;font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;
  border:2px solid %(ink)s;border-radius:999px;padding:8px 14px;background:%(gold)s;
  color:%(ink)s;box-shadow:3px 3px 0 %(ink)s}
.dc-hero .hj a:hover{transform:translate(1px,1px);box-shadow:2px 2px 0 %(ink)s}

/* --------------------------------------------------------- the name note */
.dc-note{border:2px solid %(ink)s;border-left-width:9px;border-radius:12px;
  background:%(cream)s;padding:17px 19px;margin:0 0 26px;box-shadow:4px 4px 0 %(gold)s}
.dc-note h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.028em;font-size:18px;color:%(ink)s;margin:0 0 7px}
.dc-note p{font-size:14.4px;line-height:1.66;color:%(muted)s;margin:0 0 8px;max-width:70ch}
.dc-note p:last-child{margin:0}
.dc-note a{color:%(pine)s}

/* ----------------------------------------------------------- group index */
.dc-grp{border:2px solid %(ink)s;border-radius:14px;background:#fff;
  box-shadow:6px 6px 0 %(ink)s;padding:21px 22px 8px;margin:0 0 22px}
.dc-grp>h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.03em;font-size:22px;color:%(ink)s;margin:0 0 7px}
.dc-grp>p.gl{font-size:14.6px;line-height:1.66;color:%(muted)s;margin:0 0 16px;max-width:70ch}
.dc-row{display:block;text-decoration:none;border-top:2px solid #E6E0D2;padding:14px 0}
.dc-row:hover{background:%(cream)s}
.dc-row .rt{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.026em;font-size:17px;line-height:1.24;color:%(ink)s;display:block;
  margin:0 0 5px}
.dc-row .rd{font-size:14px;line-height:1.6;color:%(muted)s;display:block;margin:0 0 8px;
  max-width:72ch}
.dc-row .rm{display:flex;flex-wrap:wrap;gap:7px}
.dc-row .rm span{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.07em;text-transform:uppercase;border:1.5px solid #CFC7B2;
  border-radius:999px;padding:3px 9px;color:#4A4436;background:%(cream)s}
.dc-row .rm span.o{background:%(ink)s;color:#fff;border-color:%(ink)s}
.dc-row .rm span.c{background:%(gold)s;color:%(ink)s;border-color:%(ink)s}

/* ------------------------------------------------------------ the filter */
/* Chips, not a select. A reader scanning a library wants to see the whole set
   of ways in before choosing one, and a collapsed <select> hides exactly that.
   The count line below them is the honest part - it says what is showing. */
.dc-filt{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}
.dc-fb{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.08em;text-transform:uppercase;border:2px solid %(ink)s;
  border-radius:999px;padding:8px 14px;background:#fff;color:%(ink)s;
  cursor:pointer;box-shadow:3px 3px 0 %(ink)s;line-height:1}
.dc-fb:hover{background:%(cream)s}
.dc-fb[aria-pressed="true"]{background:%(gold)s;box-shadow:2px 2px 0 %(ink)s;
  transform:translate(1px,1px)}
.dc-count{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.1em;text-transform:uppercase;color:%(pine)s;margin:0 0 18px}
.dc-grp[hidden]{display:none}

/* the two repeat DUI write-ups: kept, published, and deliberately quiet */
.dc-more{border-top:2px solid #E6E0D2;margin:10px 0 0;padding:12px 0 4px}
.dc-more>p{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.1em;text-transform:uppercase;color:%(muted)s;margin:0 0 8px}
.dc-min{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;
  text-decoration:none;padding:6px 0}
.dc-min:hover{background:%(cream)s}
.dc-min .rt{font-size:14.4px;line-height:1.4;color:%(ink)s;font-weight:600}
.dc-min .rm{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.07em;text-transform:uppercase;color:%(muted)s}

/* ------------------------------------------- discussion, on the case page */
/* Visually distinct from every block above it, on purpose. Everything higher
   up the page is what the decision says; this is argument about it, and the
   reader is entitled to see which is which without reading a disclaimer. */
.dc-why{border:2px solid %(pine)s;border-left-width:9px;border-radius:12px;
  background:%(paper)s;padding:15px 18px;margin:0 0 22px}
.dc-why p{font-size:15.4px;line-height:1.62;color:%(ink)s;margin:0;max-width:66ch}
.dc-why .l{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.12em;text-transform:uppercase;color:%(pine)s;display:block;
  margin:0 0 6px}
.dc-disc{border:2px dashed #9CB3A6;border-radius:14px;background:#fff;
  padding:21px 23px;margin:0 0 22px}
.dc-disc h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.028em;font-size:20px;color:%(ink)s;margin:0 0 4px}
.dc-disc .sub{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.11em;text-transform:uppercase;color:%(pine)s;margin:0 0 12px}
.dc-disc p{font-size:15.4px;line-height:1.74;color:#3A3529;margin:0 0 13px;max-width:68ch}
.dc-disc p:last-child{margin:0}
.dc-disc p b{color:%(ink)s}
.dc-ask{border:2px solid %(ink)s;border-radius:14px;background:%(cream)s;
  box-shadow:6px 6px 0 %(pine)s;padding:20px 23px;margin:0 0 22px}
.dc-ask h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.028em;font-size:20px;color:%(ink)s;margin:0 0 4px}
.dc-ask .sub{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.11em;text-transform:uppercase;color:%(pine)s;margin:0 0 13px}
.dc-ask ol{margin:0;padding:0 0 0 21px}
.dc-ask li{font-size:15.2px;line-height:1.7;color:#3A3529;margin:0 0 11px;max-width:66ch}
.dc-ask li:last-child{margin:0}

/* ------------------------------------------------- contents, on a case page */
.dc-toc{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 24px}
.dc-toc a{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.08em;text-transform:uppercase;text-decoration:none;
  border:1.5px solid #CFC7B2;border-radius:999px;padding:6px 12px;
  color:#4A4436;background:%(cream)s}
.dc-toc a:hover{border-color:%(ink)s;background:%(gold)s;color:%(ink)s}

/* ------------------------------------------------------------- the table */
.dc-tw{overflow-x:auto;border:2px solid %(ink)s;border-radius:12px;
  box-shadow:5px 5px 0 %(ink)s;background:#fff;margin:0 0 14px}
.dc-t{border-collapse:collapse;width:100%%;min-width:520px}
.dc-t th,.dc-t td{text-align:left;padding:11px 14px;border-bottom:1.5px solid #E6E0D2;
  font-size:14px;line-height:1.55;color:#3A3529;vertical-align:top;
  overflow-wrap:break-word}
.dc-t th{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.11em;text-transform:uppercase;color:%(pine)s;background:%(cream)s;
  white-space:nowrap}
.dc-t tr:last-child td{border-bottom:0}
.dc-t td.f{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:17px;
  color:%(ink)s;white-space:nowrap}
.dc-t td.m{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12.5px;
  color:%(ink)s;white-space:nowrap}

/* -------------------------------------------------------- the case page */
.dc-crumb{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.1em;text-transform:uppercase;margin:0 0 14px}
.dc-crumb a{color:%(pine)s;text-decoration:none;border-bottom:1.5px solid #BFD3C7}
.dc-crumb span{color:%(muted)s}
.dc-title{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.034em;font-size:37px;line-height:1.06;color:%(ink)s;margin:0 0 12px;
  max-width:20ch}
.dc-dek{font-size:17.5px;line-height:1.58;color:%(muted)s;margin:0 0 20px;max-width:60ch}
.dc-dek b{color:%(ink)s}
.dc-facts{border:2px solid %(ink)s;border-radius:14px;background:%(cream)s;
  box-shadow:6px 6px 0 %(gold)s;padding:22px 24px;margin:0 0 26px}
.dc-facts p{font-size:15.6px;line-height:1.72;color:#3A3529;margin:0 0 13px;max-width:68ch}
.dc-facts p:last-child{margin:0}
.dc-facts p b{color:%(ink)s}

/* the docket strip */
.dc-dock{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:2px solid %(ink)s;
  border-radius:12px;overflow:hidden;background:%(ink)s;margin:0 0 24px}
.dc-dock>div{background:#fff;padding:13px 15px}
.dc-dock .l{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.11em;text-transform:uppercase;color:%(pine)s;display:block;margin:0 0 5px}
.dc-dock .v{font-size:14.6px;line-height:1.45;color:%(ink)s;display:block;font-weight:600}

/* what was charged */
.dc-chg{border:2px solid %(ink)s;border-radius:12px;background:#fff;
  box-shadow:5px 5px 0 %(ink)s;overflow:hidden;margin:0 0 24px}
.dc-chg>div{padding:15px 18px;border-bottom:1.5px solid #E6E0D2}
.dc-chg>div:last-child{border-bottom:0}
.dc-chg .cc{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12.5px;
  letter-spacing:.03em;color:%(ink)s;font-weight:600;display:block;margin:0 0 6px}
.dc-chg .cc a{color:%(pine)s}
.dc-chg p{font-size:14.6px;line-height:1.62;color:%(muted)s;margin:0;max-width:70ch}
.dc-chg p b{color:%(ink)s}

/* the outcome band */
.dc-out{border:2px solid %(ink)s;border-radius:14px;background:%(ink)s;color:#fff;
  padding:21px 24px;margin:0 0 26px}
.dc-out h2{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.15em;text-transform:uppercase;color:%(gold)s;margin:0 0 9px;font-weight:400}
.dc-out p{font-size:16.4px;line-height:1.6;color:#fff;margin:0 0 12px;max-width:66ch}
.dc-out p:last-child{margin:0}
.dc-out .cost{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:31px;
  color:%(gold)s;display:block;line-height:1.1;margin:4px 0 3px}
.dc-out .costl{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.11em;text-transform:uppercase;color:rgba(255,255,255,.82);display:block}

/* the two explainer blocks */
.dc-ex{border:2px solid %(ink)s;border-radius:12px;padding:19px 21px;margin:0 0 20px;
  background:#fff;box-shadow:5px 5px 0 %(ink)s}
.dc-ex.ins{background:%(paper)s;box-shadow:5px 5px 0 %(pine)s}
.dc-ex h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.028em;font-size:20px;color:%(ink)s;margin:0 0 9px}
.dc-ex p{font-size:15.2px;line-height:1.7;color:%(muted)s;margin:0;max-width:70ch}
.dc-ex p b{color:%(ink)s}
.dc-ex ul{margin:10px 0 0;padding:0 0 0 19px}
.dc-ex li{font-size:15.2px;line-height:1.68;color:%(muted)s;margin:0 0 9px;max-width:68ch}
.dc-ex li:last-child{margin:0}
.dc-ex li b{color:%(ink)s}

/* prev / next */
.dc-nav{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:28px 0 0}
.dc-nav a{display:block;text-decoration:none;border:2px solid %(ink)s;border-radius:12px;
  background:%(cream)s;padding:14px 16px;box-shadow:4px 4px 0 %(ink)s}
.dc-nav a:hover{transform:translate(1px,1px);box-shadow:3px 3px 0 %(ink)s}
.dc-nav .l{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.11em;text-transform:uppercase;color:%(pine)s;display:block;margin:0 0 5px}
.dc-nav .t{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-weight:800;
  letter-spacing:-.024em;font-size:15px;line-height:1.28;color:%(ink)s;display:block}
.dc-nav a.nx{text-align:right}

.dc-fine{font-size:13.4px;line-height:1.68;color:%(muted)s;margin:26px 0 0;max-width:74ch}
.dc-fine b{color:%(ink)s}
.dc-fine a{color:%(pine)s}

@media (max-width:900px){
  .dc-figs{grid-template-columns:1fr 1fr}
  .dc-hero h1{font-size:32px}
  .dc-title{font-size:29px;max-width:none}
}
@media (max-width:640px){
  .dc-hero{padding:22px 20px 20px}
  .dc-hero h1{font-size:27px;max-width:none}
  .dc-dock{grid-template-columns:1fr}
  .dc-dock>div{border-bottom:2px solid %(ink)s}
  .dc-dock>div:last-child{border-bottom:0}
  .dc-nav{grid-template-columns:1fr}
  .dc-nav a.nx{text-align:left}
  .dc-facts{padding:18px 17px}
  .dc-t th,.dc-t td{padding:10px 11px;font-size:13.4px;overflow-wrap:break-word}
}
</style>"""


# ---------------------------------------------------------------- filter JS
# Deliberately tiny and dependency-free. It hides whole groups rather than
# individual rows, so the group heading and its lede - which carry as much of
# the teaching as the rows do - travel with the cases they describe.
#
# Note what it does NOT do: no URL state, no analytics on the chip, no
# animation. The site's tracking promise is that nothing a reader touches is
# reported with a value attached, and a filter that wrote itself into the
# query string would be the one place that leaked what someone was reading.
FILTER_JS = """<script>
(function(){
  var chips=[].slice.call(document.querySelectorAll('.dc-fb')),
      groups=[].slice.call(document.querySelectorAll('.dc-grp')),
      out=document.getElementById('dc-count');
  if(!chips.length||!groups.length)return;
  function total(g){
    return g.querySelectorAll('.dc-row').length+g.querySelectorAll('.dc-min').length;
  }
  function pick(key){
    var n=0;
    groups.forEach(function(g){
      var on=(key==='all'||g.getAttribute('data-g')===key);
      g.hidden=!on; if(on)n+=total(g);
    });
    chips.forEach(function(c){
      c.setAttribute('aria-pressed', c.getAttribute('data-g')===key?'true':'false');
    });
    if(out)out.textContent=(key==='all'?'Showing all ':'Showing ')+n+
      ' case'+(n===1?'':'s');
  }
  chips.forEach(function(c){
    c.addEventListener('click',function(){pick(c.getAttribute('data-g'));});
  });
})();
</script>"""


def esc(x):
    return html.escape(str(x), quote=False) if x is not None else ""


def by_group(key):
    return [c for c in CASES if c["group"] == key]


def grp(key):
    for g in GROUPS:
        if g["key"] == key:
            return g
    raise KeyError(key)


# ---------------------------------------------------------------- the hub
def hub_body():
    o = ['<article class="dc-wrap">']

    # ---------------------------------------------------------------- hero
    # An AIDA hero, per the standing rule for every directory on this site: say
    # what this is, what is in it, and what the reader gets, above the fold and
    # with measured figures rather than adjectives.
    o.append('<section class="dc-hero">')
    o.append('<p class="hk">Case library &middot; California &middot; 2024&ndash;2026</p>')
    o.append("<h1>What actually gets a California therapist disciplined</h1>")
    # ONE sentence. The hero used to carry two long paragraphs plus the
    # In-short card plus four figures plus the jump nav, and the reader could
    # not see a single case without scrolling twice. Everything that was in
    # those paragraphs - the two audiences, the method, the no-names rule - is
    # still on the page; it is just no longer the first thing.
    o.append('<p class="hl">Real BBS decisions, de-identified. <b>What happened,'
             '</b> what it was charged under, and what it cost.</p>')
    # Three figures, not four. The fourth was "62 of 103 cite 4982(a)", which
    # is the finding of the section immediately below it and does not need
    # saying twice before the reader has seen anything.
    o.append('<div class="dc-figs">')
    for n, l in (("103", "decisions read"),
                 ("30", "written up"),
                 ("$15,883", "largest cost recovery")):
        o.append('<div><span class="n">%s</span><span class="l">%s</span></div>' % (n, l))
    o.append("</div>")
    o.append('<p class="hj">')
    o.append('<a href="#the-shape">The shape of it</a>')
    o.append('<a href="#cases">The thirty cases</a>')
    o.append('<a href="#what-it-costs">What it costs</a>')
    o.append('<a href="%s">Insurance that answers for it</a>' % INSURANCE)
    o.append("</p>")
    o.append("</section>")

    # ------------------------------------------------------------- the shape
    o.append('<section class="dc-sec" id="the-shape">')
    o.append('<p class="dc-k">The shape of it</p>')
    o.append('<h2 class="dc-h">Discipline does not usually start with a client.</h2>')
    o.append('<p class="dc-d">This is the finding that surprises most therapists, '
             'and it is not an interpretation &mdash; it is the Board\'s own '
             'reporting. In FY 2023&ndash;24 more complaints came from government '
             'agencies than from members of the public, and the largest single '
             'driver of MFT discipline in California is the Department of Justice '
             'conviction and arrest feed under Penal Code &sect;11105.2. '
             '<b>Sixty-two of the 103 decisions read for this library cite '
             '&sect;4982(a), a substantially related conviction.</b> Most of '
             'those are a DUI. None of them began with someone complaining about '
             'therapy.</p>')
    o.append('<div class="dc-tw"><table class="dc-t">')
    o.append("<tr><th>Figure</th><th>What it is</th><th>Context</th></tr>")
    for n, what, ctx in AGGREGATE:
        o.append("<tr><td class='f'>%s</td><td>%s</td><td>%s</td></tr>" % (n, what, ctx))
    o.append("</table></div>")
    o.append('<p class="dc-d">Source: the Board\'s <a href="%s" target="_blank" '
             'rel="noopener">2025 Sunset Review Report</a>, section 4.</p>' % SUNSET)

    o.append('<h3 class="dc-h" style="font-size:22px;margin-top:30px">Which '
             'subdivision of &sect;4982, and how often</h3>')
    o.append('<p class="dc-d">Counted from the text of the 103 decisions. A '
             'single case can cite several.</p>')
    o.append('<div class="dc-tw"><table class="dc-t">')
    o.append("<tr><th>Subd.</th><th>What it prohibits</th><th>Cases</th>"
             "<th>Note</th></tr>")
    for sub, what, n, note in SUBD_COUNTS:
        o.append("<tr><td class='m'>%s</td><td>%s</td><td class='f'>%d</td>"
                 "<td>%s</td></tr>" % (sub, what, n, note))
    o.append("</table></div>")
    o.append('<p class="dc-d">The complete subdivision list, (a) through (ab), is '
             'in the Board\'s <a href="%s" target="_blank" rel="noopener">Statutes '
             'and Regulations</a> at article 2.</p>' % LAWSREGS)

    o.append('<h3 class="dc-h" style="font-size:22px;margin-top:30px">And what '
             'gets cited, short of an accusation</h3>')
    o.append('<p class="dc-d">A citation and fine is not formal discipline, and it '
             'is far more common. These are the five grounds the Board reports '
             'citing most often, in its own order:</p>')
    o.append('<div class="dc-ex"><ul>')
    for g in CITATION_GROUNDS:
        o.append("<li>%s</li>" % g)
    o.append("</ul></div>")
    o.append('<p class="dc-d">Two of those five are about continuing education and '
             'one is about confidentiality. None of them is clinical.</p>')
    o.append("</section>")

    # ------------------------------------------------------------- the cases
    o.append('<section class="dc-sec" id="cases">')
    o.append('<p class="dc-k">The library</p>')
    o.append('<h2 class="dc-h">Thirty cases, grouped by what went wrong.</h2>')
    o.append('<p class="dc-d">Each one opens to a full write-up: the facts as the '
             'decision states them, every statute charged with a link to the code '
             'section, the disposition, the cost recovery, what the rule actually '
             'requires, where a liability policy does and does not reach, a '
             'discussion of what the Board was deciding, and three questions for '
             'a class.</p>')

    # ------------------------------------------------------------ the filter
    # Chips over a <select>, and one group per chip rather than a tag system,
    # because the groups ARE the taxonomy - inventing a second one would give a
    # reader two mental models of the same thirty cases.
    o.append('<div class="dc-filt" role="group" aria-label="Filter cases">')
    o.append('<button class="dc-fb" type="button" data-g="all" '
             'aria-pressed="true">All thirty</button>')
    for g in GROUPS:
        o.append('<button class="dc-fb" type="button" data-g="%s" '
                 'aria-pressed="false">%s <span aria-hidden="true">&middot; '
                 '%d</span></button>' % (g["key"], g["short"], len(by_group(g["key"]))))
    o.append("</div>")
    o.append('<p class="dc-count" id="dc-count">Showing all 30 cases</p>')

    for g in GROUPS:
        cs = by_group(g["key"])
        main = [c for c in cs if not c.get("minor")]
        minor = [c for c in cs if c.get("minor")]
        o.append('<div class="dc-grp" id="g-%s" data-g="%s">' % (g["key"], g["key"]))
        o.append("<h2>%s <span style='font-family:Fraunces,Georgia,serif;"
                 "font-weight:600;color:%s'>&middot; %d</span></h2>"
                 % (g["n"], PINE, len(cs)))
        o.append('<p class="gl">%s</p>' % g["lede"])
        for c in main:
            # The parenthesis matters: `"%s" % x + ".html"` binds as
            # `("%s" % x) + ".html"`, which puts the extension OUTSIDE the
            # attribute and produces thirty dead links that the internal-link
            # guard cannot see, because `href="slug"` does not match its
            # `[a-z0-9-]+\.html` pattern. It shipped once, here, and the
            # reachable-from-the-hub guard below is what caught it.
            o.append('<a class="dc-row" href="%s.html">' % c["slug"])
            o.append('<span class="rt">%s</span>' % c["t"])
            o.append('<span class="rd">%s</span>' % c["dek"])
            o.append('<span class="rm">')
            o.append("<span>%s</span>" % c["role"])
            o.append("<span>%s</span>" % c["eff"].split(";")[0])
            o.append("<span class='o'>%s</span>" % short_outcome(c))
            amt, _note = cost_parts(c["cost"])
            if amt:
                o.append("<span class='c'>%s</span>" % amt)
            o.append("</span></a>")
        if minor:
            o.append('<div class="dc-more"><p>Also in the record, same lesson</p>')
            for c in minor:
                o.append('<a class="dc-min" href="%s.html">' % c["slug"])
                o.append('<span class="rt">%s</span>' % c["t"])
                # The cost figure travels with the quiet rows too. The hub
                # guard checks every case's amount appears intact somewhere on
                # this page, and a row that dropped it would make the guard
                # into a thing that fires for a formatting reason rather than a
                # correctness one.
                amt, _n = cost_parts(c["cost"])
                o.append('<span class="rm">%s &middot; %s%s</span>'
                         % (c["eff"].split(";")[0], short_outcome(c),
                            (" &middot; " + amt) if amt else ""))
                o.append("</a>")
            o.append("</div>")
        o.append("</div>")
    o.append(FILTER_JS)
    o.append("</section>")

    # ------------------------------------------------------------ what it costs
    o.append('<section class="dc-sec" id="what-it-costs">')
    o.append('<p class="dc-k">What it costs</p>')
    o.append('<h2 class="dc-h">Cost recovery is the number therapists most '
             'underestimate.</h2>')
    o.append('<p class="dc-d">Business and Professions Code &sect;125.3 lets an '
             'administrative law judge order a licensee found in violation to pay '
             'the reasonable costs of investigating and enforcing the case, '
             'including the Attorney General\'s charges. It is separate from your '
             'own lawyer, separate from any fine, and <b>no insurance policy sold '
             'to therapists pays it</b>. The judge can reduce it. The judge cannot '
             'increase it.</p>')
    o.append('<div class="dc-tw"><table class="dc-t">')
    o.append("<tr><th>Ordered</th><th>Typical fact pattern</th></tr>")
    for band, what in COST_BANDS:
        o.append("<tr><td class='f'>%s</td><td>%s</td></tr>" % (band, what))
    o.append("</table></div>")
    o.append('<p class="dc-d">None of that includes your own defence counsel, the '
             'psychological or psychiatric evaluation the order requires you to '
             'pay for, the practice-supervision arrangement, the remedial '
             'coursework that <b>cannot</b> be counted toward your continuing '
             'education, or the income lost during a suspension.</p>')

    o.append('<h3 class="dc-h" style="font-size:22px;margin-top:30px">The fifteen '
             'probation conditions</h3>')
    o.append('<p class="dc-d">These appear in essentially every probation order '
             'the Board writes. Two of them are the ones therapists never think '
             'about until they are living under them.</p>')
    o.append('<div class="dc-tw"><table class="dc-t">')
    o.append("<tr><th>Condition</th><th>What it means in practice</th></tr>")
    for name, note in PROBATION_TERMS:
        o.append("<tr><td class='m'>%s</td><td>%s</td></tr>"
                 % (name, note or "&mdash;"))
    o.append("</table></div>")
    o.append('<p class="dc-d">The penalty attached to each violation is set out in '
             'the Board\'s <a href="%s" target="_blank" rel="noopener">Uniform '
             'Standards and Disciplinary Guidelines</a>, which is the document the '
             'Board uses to price every settlement it offers.</p>' % DISPGUID)
    o.append("</section>")

    # ----------------------------------------------------------- insurance tie
    o.append('<section class="dc-sec" id="insurance">')
    o.append('<div class="dc-ex ins">')
    o.append("<h2>Where insurance actually reaches</h2>")
    o.append("<p>Read the thirty cases and the pattern is hard to miss: almost "
             "none of them is a malpractice claim. Nobody sued. The Board saw "
             "<b>seven</b> malpractice settlement reports in four years, against "
             "2,127 complaints in a single year. The $1,000,000 limit that every "
             "therapist shops on is not the number that matters here &mdash; the "
             "<b>board-defense sublimit</b> is, and depending on the program it is "
             "$5,000, $25,000 or $35,000.</p>")
    o.append("<ul>")
    o.append("<li><b>Board defense</b> is the coverage you are statistically most "
             "likely to use, and it is the smallest number on the policy.</li>")
    o.append("<li><b>Sexual misconduct is defense only</b> on every program a "
             "California therapist can buy. There is no indemnity, and some "
             "policies condition even the defence on the allegation being "
             "unfounded.</li>")
    o.append("<li><b>Cost recovery is not a defence cost.</b> No sublimit pays "
             "it, on any policy, ever.</li>")
    o.append("<li><b>Probation is entirely uninsured</b> &mdash; monitoring fees "
             "of roughly $1,200 a year, ordered evaluations, supervised practice, "
             "and coursework that does not count toward your CE.</li>")
    o.append("<li><b>Associates are usually not named insureds</b> on an "
             "employer's policy, and the employer has no reason to carry "
             "board-defense cover for someone else's registration.</li>")
    o.append("</ul>")
    o.append('<p style="margin-top:13px"><a href="%s">Every program a California '
             'MFT can buy, with what each publishes and what people report '
             'actually paying &rarr;</a></p>' % INSURANCE)
    o.append("</div>")
    o.append("</section>")

    # -------------------------------------------- the name note, at the end
    # It used to sit second, above the library. It is a policy statement
    # about the site, not a way in to the material, and a reader who has
    # just arrived has no reason to care yet. Moved here, where someone
    # who has read a case and wondered about the missing names will find
    # it.
    o.append('<section class="dc-note">')
    o.append("<h2>There are no names on this site, and that is deliberate</h2>")
    o.append("<p>Every name is public record. The Board publishes them in its own "
             "quarterly newsletter and the Department of Consumer Affairs hosts "
             "the signed decisions. This site does not republish them, for an "
             "editorial reason rather than a legal one: a page that names people "
             "becomes a page people arrive at by searching a name, and at that "
             "point it has stopped teaching anything.</p>")
    o.append("<p>Nothing has been softened. Conduct, statute, outcome and dollar "
             "figure are exactly as each decision states them. Cities, employers "
             "and client initials are removed. Every case below carries its case "
             "number and effective date.</p>")
    o.append('<p><b>To verify any case here:</b> open the Board\'s quarterly '
             'newsletter archive at <a href="%s" target="_blank" rel="noopener">'
             'bbs.ca.gov/resources/general.html</a>, find the &ldquo;Formal '
             'Disciplinary Actions&rdquo; section of the issue covering the '
             'effective date, and match the case number. Each licensee name in '
             'those PDFs is a live link to the signed Decision and Order.</p>'
             % NEWSLETTERS)
    o.append("</section>")

    # ------------------------------------------------------------------- fine
    o.append('<p class="dc-fine"><b>How this library was built.</b> The Board does '
             'not publish a browsable list of its decisions. It publishes a '
             'quarterly newsletter, and in the &ldquo;Formal Disciplinary '
             'Actions&rdquo; section of each issue every licensee name is a live '
             'hyperlink to the signed Decision and Order, Stipulated Settlement or '
             'Accusation hosted by the Department of Consumer Affairs. Eight '
             'issues cover July 2023 through March 2026 with no gap. Reading all '
             'eight yields 286 disciplinary entries across every BBS licence type; '
             '152 are LMFT or AMFT; 104 took effect in 2024, 2025 or 2026. 103 of '
             'those 104 source documents were retrieved and read in full &mdash; '
             'one entry had no hyperlink in the newsletter. Checked %s.<br><br>'
             '<b>Most of these are stipulated settlements.</b> In a stipulated '
             'settlement the licensee does not admit the allegations; they agree '
             'the Board could establish a prima facie case, and they accept the '
             'discipline. Where a case went to a full hearing instead, the case '
             'page says so.<br><br><b>This is not legal advice.</b> We are not '
             'lawyers. If you are facing a Board matter, the single most useful '
             'thing on this page is the observation that a licensing attorney and '
             'a criminal defence attorney are different jobs, and that you '
             'probably want both. The Board\'s brochure on therapist sexual '
             'misconduct, which &sect;728 requires therapists to provide in '
             'certain circumstances, is <a href="%s" target="_blank" '
             'rel="noopener">here</a>.</p>' % (CHECKED, BROCHURE))

    o.append("</article>")
    return "".join(o)


# Grouped digits, ending on a digit. `^\$[\d,]+` also swallows the comma that
# ENDS the amount - "$12,515, payable in full..." came out as "$12,515," with a
# trailing comma sitting in a pill on the index.
MONEY = re.compile(r"^\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?")


def cost_parts(cost):
    """('$12,515', 'payable in full before any new license could issue').

    `cost.split(",")[0]` was the first version, and it splits "$7,644" on its
    THOUSANDS SEPARATOR. The In-short card on one page shipped reading "$7".
    Same shape as every other bug in this project's history: the code was
    looking for a clause boundary and the data had a comma that was not one."""
    if not cost:
        return (None, None)
    cost = cost.strip()
    m = MONEY.match(cost)
    if not m:
        return (None, cost)
    rest = cost[m.end():].lstrip(" ,;").strip()
    return (m.group(0), rest or None)


def short_outcome(c):
    """A three-word version of the disposition, for the index chip."""
    o = re.sub(r"<[^>]+>", "", c["outcome"]).lower()
    if "revoked outright" in o or ("revoked" in o and "stayed" not in o):
        return "Revoked"
    if "surrender" in o:
        return "Surrendered"
    if "reproval" in o:
        return "Public reproval"
    if "extended" in o:
        return "Probation extended"
    m = re.search(r"(\w+|\d+) years? of probation", o)
    if m:
        return "%s yrs probation" % m.group(1)
    if "probation" in o:
        return "Probation"
    return "Discipline"


# ---------------------------------------------------------------- case page
def case_body(c, prev, nxt):
    g = grp(c["group"])
    o = ['<article class="dc-wrap">']

    o.append('<p class="dc-crumb"><a href="%s">Case library</a> '
             '<span>&nbsp;/&nbsp;</span> <a href="%s#g-%s">%s</a></p>'
             % (HUB, HUB, g["key"], g["n"]))
    o.append('<h1 class="dc-title">%s</h1>' % c["t"])
    o.append('<p class="dc-dek">%s</p>' % c["dek"])

    # docket
    o.append('<div class="dc-dock">')
    o.append('<div><span class="l">Licence type</span><span class="v">%s</span></div>'
             % c["role"])
    o.append('<div><span class="l">Effective</span><span class="v">%s</span></div>'
             % c["eff"])
    o.append('<div><span class="l">Case number</span><span class="v">%s</span></div>'
             % (c["case"] or "Not stated in the newsletter"))
    o.append("</div>")

    d = DEPTH.get(c["slug"])

    # A contents rail. These pages run long now, and a reader who came for the
    # statute should not have to scroll through the narrative to find it.
    o.append('<div class="dc-toc">')
    for href, label in (("#what-happened", "What happened"),
                        ("#charged", "What it was charged as"),
                        ("#outcome", "The outcome"),
                        ("#rule", "The rule"),
                        ("#discussion", "Discussion"),
                        ("#insurance", "Insurance"),
                        ("#questions", "Questions")):
        if href == "#discussion" and not d:
            continue
        if href == "#questions" and not d:
            continue
        o.append('<a href="%s">%s</a>' % (href, label))
    o.append("</div>")

    if d:
        o.append('<div class="dc-why"><span class="l">Why this case is '
                 'here</span><p>%s</p></div>' % d["why"])

    o.append('<p class="dc-k" id="what-happened">What happened</p>')
    o.append('<div class="dc-facts">')
    for p in c["facts"]:
        o.append("<p>%s</p>" % p)
    o.append("</div>")

    o.append('<p class="dc-k" id="charged">What it was charged as</p>')
    o.append('<div class="dc-chg">')
    for cite, url, plain in c["charges"]:
        if url:
            o.append('<div><span class="cc"><a href="%s" target="_blank" '
                     'rel="noopener">%s</a></span><p>%s</p></div>'
                     % (url, cite, plain))
        else:
            o.append('<div><span class="cc">%s</span><p>%s</p></div>' % (cite, plain))
    o.append("</div>")

    o.append('<div class="dc-out" id="outcome">')
    o.append("<h2>The outcome</h2>")
    o.append("<p>%s</p>" % c["outcome"])
    if c["hear"]:
        o.append("<p style='font-size:14px;color:rgba(255,255,255,.8)'>%s</p>"
                 % c["hear"])
    amt, note = cost_parts(c["cost"])
    if amt:
        o.append('<span class="cost">%s</span>'
                 '<span class="costl">ordered in cost recovery under '
                 'B&amp;P &sect;125.3%s</span>'
                 % (amt, (" &mdash; " + note) if note else ""))
    elif note:
        o.append('<span class="costl">Cost recovery: %s</span>' % note)
    else:
        o.append('<span class="costl">No cost recovery stated in the order</span>')
    o.append("</div>")

    o.append('<div class="dc-ex" id="rule">')
    o.append("<h2>What the rule actually says</h2>")
    o.append("<p>%s</p>" % c["rule"])
    o.append("</div>")

    # The discussion. Dashed border and a label, because everything above it is
    # what the decision says and this is argument about it. A reader should be
    # able to tell them apart at a glance rather than by reading a disclaimer.
    if d:
        o.append('<div class="dc-disc" id="discussion">')
        o.append("<h2>Discussion</h2>")
        o.append('<p class="sub">Analysis, not part of the decision</p>')
        for para in d["disc"]:
            o.append("<p>%s</p>" % para)
        o.append("</div>")

    o.append('<div class="dc-ex ins" id="insurance">')
    o.append("<h2>Where insurance reaches, and where it does not</h2>")
    o.append("<p>%s</p>" % c["ins"])
    o.append('<p style="margin-top:11px"><a href="%s">Compare what each program '
             'actually covers &rarr;</a></p>' % INSURANCE)
    o.append("</div>")

    o.append('<div class="dc-ex">')
    o.append("<h2>What would have changed it</h2>")
    o.append("<ul>")
    for p in c["prevent"]:
        o.append("<li>%s</li>" % p)
    o.append("</ul>")
    o.append("</div>")

    if d:
        o.append('<div class="dc-ask" id="questions">')
        o.append("<h2>Questions</h2>")
        o.append('<p class="sub">For a law and ethics seminar, or for yourself</p>')
        o.append("<ol>")
        for q in d["ask"]:
            o.append("<li>%s</li>" % q)
        o.append("</ol>")
        o.append("</div>")

    # prev / next
    o.append('<div class="dc-nav">')
    if prev:
        o.append('<a href="%s.html"><span class="l">&larr; Previous</span>'
                 '<span class="t">%s</span></a>' % (prev["slug"], prev["t"]))
    else:
        o.append('<a href="%s"><span class="l">&larr; Back</span>'
                 '<span class="t">All thirty cases</span></a>' % HUB)
    if nxt:
        o.append('<a class="nx" href="%s.html"><span class="l">Next &rarr;</span>'
                 '<span class="t">%s</span></a>' % (nxt["slug"], nxt["t"]))
    else:
        o.append('<a class="nx" href="%s"><span class="l">Next &rarr;</span>'
                 '<span class="t">The whole case library</span></a>' % HUB)
    o.append("</div>")

    o.append('<p class="dc-fine"><b>Source.</b> This write-up is drawn from the '
             'signed public decision in the case number above. Names, cities and '
             'employers have been removed &mdash; <a href="%s">why</a>. To pull '
             'the original, open the Board\'s <a href="%s" target="_blank" '
             'rel="noopener">quarterly newsletter archive</a>, find the issue '
             'covering %s, and match the case number in the Formal Disciplinary '
             'Actions section. Not legal advice.</p>'
             % (HUB, NEWSLETTERS, c["eff"].split(";")[0]))

    o.append("</article>")
    return "".join(o)


# ------------------------------------------------------------------- chrome
def chrome_parts():
    if not os.path.exists(CHROME_FROM):
        sys.exit("build_cases: the chrome donor page is missing")
    chrome = open(CHROME_FROM, encoding="utf-8").read()

    head = chrome[:chrome.index("</head>")]
    head = re.sub(r"<title>[\s\S]*?</title>", "", head)
    head = re.sub(r'<meta name="description"[^>]*>', "", head)
    head = re.sub(r'<meta property="og:[^>]*>', "", head)
    head = re.sub(r'<link rel="canonical"[^>]*>', "", head)
    head = re.sub(r'<meta name="ts:[^>]*>', "", head)
    head = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>', "", head)
    head = re.sub(r"<!-- _dev/[\s\S]*?-->", "", head)

    body_open_end = chrome.index(">", chrome.index("<body")) + 1
    header_end = chrome.index("</header>") + len("</header>")
    header = chrome[body_open_end:header_end]
    foot_start = chrome.rindex("<footer")
    footer = chrome[foot_start:chrome.index("</footer>", foot_start) + len("</footer>")]
    links = re.findall(r'<link rel="stylesheet" href="css/[0-9a-f]{12}\.css">', chrome)

    # The behaviour has to come with the markup. The nav-panel binding lives
    # after </footer> in the donor; a page assembled from someone else's chrome
    # that takes the header alone ships a masthead where every button is dead.
    tail = chrome[chrome.index("</footer>", foot_start) + len("</footer>"):]
    scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>[\s\S]*?</script>", tail)
    return head, header, footer, links, scripts


def assemble(meta, body, parts, css):
    head, header, footer, links, scripts = parts
    return ('<!DOCTYPE html>\n<html lang="en">\n' + head + meta + "</head>\n"
            "<body>" + header + "<main>" + body + "</main>" + footer
            + "\n" + "\n".join(links) + "\n" + css
            + "\n" + "\n".join(scripts) + "\n</body>\n</html>\n")


def metablock(slug, title, desc, question, outcome, number, weight, fmt="case"):
    return (
        "<title>%s</title>\n"
        '<meta name="description" content="%s" />\n'
        '<link rel="canonical" href="https://therapistsupport.org/%s">\n'
        '<meta name="ts:topic" content="practice">\n'
        '<meta name="ts:format" content="%s">\n'
        '<meta name="ts:question" content="%s">\n'
        '<meta name="ts:outcome" content="%s">\n'
        '<meta name="ts:number" content="%s">\n'
        '<meta name="ts:weight" content="%s">\n'
        '<meta name="ts:stale" content="false">\n'
        % (title, desc, slug, fmt, question, outcome, number, weight))


def seo_title(t):
    """A title a search result will actually show.

    The budget is about 68 characters; past that the tail is replaced with an
    ellipsis. The first version of this appended a fixed 35-character suffix to
    every case headline and produced twenty-odd titles between 76 and 101
    characters - so the only part a reader saw cut was the part that identified
    the case. The suffix is now what gets dropped, and if the headline itself
    is too long it is cut at a comma the author already put there, never
    mid-clause."""
    t = plain(t)
    for tail in (" — a California BBS discipline case", " — a BBS discipline case",
                 " — BBS discipline case", ""):
        if len(t) + len(tail) <= 68:
            return t + tail
    # A colon and an em dash are boundaries too, and on these headlines they are
    # usually the better cut: "Two DUIs, five years of probation: the most common
    # case in California" is 69 characters, and the only comma in it falls after
    # eight.
    for m in reversed(list(re.finditer(r"\s*[:—–]\s*|,\s", t))):
        if 24 <= m.start() <= 68:
            return t[:m.start()].rstrip()
    return t


def plain(s, n=None):
    t = re.sub(r"<[^>]+>", "", s)
    t = (t.replace("&sect;", "section ").replace("&mdash;", "-")
          .replace("&ndash;", "-").replace("&amp;", "and")
          .replace("&ldquo;", "").replace("&rdquo;", "")
          .replace("&rsquo;", "'").replace("&middot;", "-")
          .replace("&hellip;", "...").replace("&rarr;", "").replace("&larr;", ""))
    t = re.sub(r"\s+", " ", t).strip()
    return t[:n].rstrip(" ,.;") if n else t


def main():
    print("colours, measured:")
    bad = 0
    for label, fg, bg, floor in CONTRAST:
        r = ratio(fg, bg)
        ok = r >= floor
        print("  %-22s %5.2f:1 (floor %.1f) %s"
              % (label, r, floor, "ok" if ok else "FAILS"))
        if not ok:
            bad += 1
    if bad:
        sys.exit("%d colour(s) under the floor" % bad)

    # slugs must be unique, or one case silently overwrites another
    slugs = [c["slug"] for c in CASES]
    if len(set(slugs)) != len(slugs):
        dupes = sorted(s for s in set(slugs) if slugs.count(s) > 1)
        sys.exit("duplicate slug(s): %s" % ", ".join(dupes))
    for c in CASES:
        if c["group"] not in {g["key"] for g in GROUPS}:
            sys.exit("case %s has unknown group %s" % (c["slug"], c["group"]))

    parts = chrome_parts()
    css = CSS % {"ink": INK, "pine": PINE, "gold": GOLD, "cream": CREAM,
                 "paper": PAPER, "muted": MUTED, "red": RED}

    # ------------------------------------------------------------------ hub
    meta = metablock(
        HUB,
        "What actually gets a California therapist disciplined",
        "Thirty real California BBS disciplinary decisions for LMFTs and AMFTs, "
        "de-identified: what happened, which subdivision of B&amp;P &sect;4982 it "
        "was charged under, how it resolved, and what the cost recovery was. Read "
        "from 103 signed decisions.",
        "What actually gets a California therapist disciplined?",
        "Thirty real cases, the exact code section each was charged under, and "
        "what each one cost",
        "103 decisions read, 30 written up",
        "5", fmt="reference")
    open(os.path.join(SITE, HUB), "w", encoding="utf-8").write(
        assemble(meta, hub_body(), parts, css))
    print("\nwrote %s" % HUB)

    # ---------------------------------------------------------------- cases
    order = []
    for g in GROUPS:
        order += by_group(g["key"])
    written = 0
    for i, c in enumerate(order):
        prev = order[i - 1] if i else None
        nxt = order[i + 1] if i + 1 < len(order) else None
        t = plain(c["t"])
        meta = metablock(
            c["slug"] + ".html",
            seo_title(c["t"]),
            plain(c["dek"] + " " + c["rule"], 300),
            t + "?",
            plain(c["outcome"], 120),
            cost_parts(c["cost"])[0] or plain(short_outcome(c)),
            "3")
        doc = assemble(meta, case_body(c, prev, nxt), parts, css)
        open(os.path.join(SITE, c["slug"] + ".html"), "w", encoding="utf-8").write(doc)
        written += 1
    print("wrote %d case page(s)" % written)

    # --------------------------------------------------------------- guards
    bad = 0
    pages = [HUB] + [c["slug"] + ".html" for c in CASES]
    for rel in pages:
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if s.count("<h1") != 1:
            print("GUARD %s: %d h1" % (rel, s.count("<h1"))); bad += 1
        if "<footer" not in s or "sitenav" not in s:
            print("GUARD %s: chrome missing" % rel); bad += 1
        if 'id="navpanel"' not in s:
            print("GUARD %s: the nav panel markup is missing" % rel); bad += 1
        if "getElementById('navpanel')" not in s:
            print("GUARD %s: nav panel has no script - every button is dead" % rel)
            bad += 1
        if "<title>" not in s or 'rel="canonical"' not in s:
            print("GUARD %s: missing title or canonical" % rel); bad += 1
        # A title past ~68 characters is truncated in the result, and on these
        # pages the truncated part is the part that says which case it is.
        t = re.search(r"<title>([\s\S]*?)</title>", s)
        if t and len(html.unescape(t.group(1)).strip()) > 68:
            print("GUARD %s: title is %d chars"
                  % (rel, len(html.unescape(t.group(1)).strip()))); bad += 1
        # no internal link may point at a file that does not exist
        for href in set(re.findall(r'href="([a-z0-9-]+\.html)"', s)):
            if not os.path.exists(os.path.join(SITE, href)):
                print("GUARD %s: links %s which does not exist" % (rel, href))
                bad += 1
        # A relative href with no extension is the shape of the bug above: it
        # slips past the check directly overhead, because that check only looks
        # at things already ending in .html.
        for href in set(re.findall(r'href="(?!https?:|mailto:|#|/)([^"#?]+)"', s)):
            if not href.endswith((".html", ".pdf", ".xml", ".ico", ".png",
                                  ".svg", ".css", ".js", "/")):
                print("GUARD %s: href=%r has no extension" % (rel, href))
                bad += 1
        for url, attrs in re.findall(r'<a href="(https?://[^"]+)"([^>]*)>', s):
            if 'target="_blank"' in attrs and "noopener" not in attrs:
                print("GUARD %s: %s opens a tab without noopener" % (rel, url[:44]))
                bad += 1

    # THE POINT OF THE WHOLE LIBRARY IS THAT NOTHING HERE NAMES ANYBODY.
    # A name reaching a published page would not throw an error, would not fail
    # a link check and would not look wrong - so it gets its own guard. Two
    # capitalised words in a row inside a facts paragraph is the signature, and
    # the allow-list below is every legitimate proper noun in this corpus.
    ALLOW = {
        "Board", "Business", "Professions", "Code", "Penal", "Health", "Safety",
        "California", "Behavioral", "Sciences", "Department", "Justice",
        "Consumer", "Affairs", "Attorney", "General", "Medical", "Arizona",
        "Weekly", "Summary", "Experience", "In-State", "Verification",
        "Notice", "Privacy", "Practices", "Formal", "Disciplinary", "Actions",
        "Decision", "Order", "Stipulated", "Settlement", "Accusation",
        "Behavioural", "Examiners", "New", "Year", "Whom", "It", "May",
        "Concern", "Dear", "One", "My", "Candle", "Light", "Super", "Spirit",
        "Have", "If", "Take", "Put", "Not", "Do", "Asking", "Here", "Wait",
        "Molly", "Xanax", "MDMA", "Schedule", "Medi-Cal", "Elder", "Abuse",
        "Fraud", "Hope", "Faith", "Love", "Condition", "Probation", "Program",
        "Uniform", "Standards", "Guidelines", "Sunset", "Review", "Report",
        "Statutes", "Regulations", "Psychology", "Clinical", "Counsellor",
        "Disneyland", "BDSM", "EMDR", "CPT", "HIPAA", "NPI", "BreEZe", "DUI",
        "Burns", "Depression", "Checklist", "Always", "You", "I", "When",
        "Gorgeous", "Light.", "Administrative", "Hearings", "Office",
        # Sentence-openers and fragments of hyphenated proper nouns. "Her
        # Medi-Cal billings" tripped this on the first run: the pattern sees
        # "Her" + "Medi" and has no way to know the second is half a word.
        "Her", "His", "She", "He", "They", "The", "That", "This", "There",
        "Medi", "Cal", "And", "But", "After", "Across", "Asked", "Within",
        "Each", "Every", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
        "Eight", "Nine", "Ten", "Sixty", "Staff", "Police", "Texting", "Gifts",
        "Physical", "Four", "Convictions", "Charged", "Sentenced", "Per",
        "Reading", "Nothing", "Read", "Note", "Because", "Where", "While",
        "Outside", "Report", "Update", "Never", "Comply", "Call", "Keep",
        "Put", "Get", "Ask", "Answer", "Diary", "Tell", "Take", "Give",
        "Respond", "File", "Understand", "Reconcile", "Consultation",
        "Escalation", "Supervision", "Warmth", "Billing", "Fifty", "Forty",
        "Multi", "Board", "Holding", "Confirm", "Its", "Entirely", "Nobody",
    }
    NAMEISH = re.compile(r"\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b")
    for c in CASES:
        for para in c["facts"] + [c["t"], c["dek"], c["rule"]]:
            txt = re.sub(r"<[^>]+>", " ", para)
            for a, b in NAMEISH.findall(txt):
                if a not in ALLOW and b not in ALLOW:
                    print("GUARD %s: possible name %r %r" % (c["slug"], a, b))
                    bad += 1
    # And nothing may link straight to a DCA decision PDF, which would name the
    # person in one click and make the de-identification cosmetic.
    for rel in pages:
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "search.dca.ca.gov/download" in s:
            print("GUARD %s: links a decision PDF, which names the licensee" % rel)
            bad += 1

    # A money figure must survive intact. "$7,644" split on its comma renders as
    # "$7", which is not an error, not a broken link and not a failing colour -
    # it is simply a wrong number, and the only way to catch it is to insist the
    # whole string is present on both the case page and the hub.
    hubs = open(os.path.join(SITE, HUB), encoding="utf-8").read()
    for c in CASES:
        amt, _ = cost_parts(c["cost"])
        if not amt:
            continue
        page = open(os.path.join(SITE, c["slug"] + ".html"), encoding="utf-8").read()
        if amt not in page:
            print("GUARD %s: cost %s is not on the page intact" % (c["slug"], amt))
            bad += 1
        if amt not in hubs:
            print("GUARD hub: cost %s for %s is not intact" % (amt, c["slug"]))
            bad += 1

    # Every case must be reachable from the hub, and every group must be used.
    hub = open(os.path.join(SITE, HUB), encoding="utf-8").read()
    for c in CASES:
        if 'href="%s.html"' % c["slug"] not in hub:
            print("GUARD: %s is not linked from the hub" % c["slug"]); bad += 1
    for g in GROUPS:
        if not by_group(g["key"]):
            print("GUARD: group %s has no cases" % g["key"]); bad += 1

    # The discussion layer must cover every case that is presented as a full
    # write-up, and must not contain an entry for a case that no longer exists.
    # A stale DEPTH key is how a rename silently drops the analysis off a page
    # without anything failing.
    slugs = {c["slug"] for c in CASES}
    for c in CASES:
        if not c.get("minor") and c["slug"] not in DEPTH:
            print("GUARD: %s has no discussion. Either write one in "
                  "_dev/case_depth.py or mark the case \"minor\"." % c["slug"])
            bad += 1
    for k in DEPTH:
        if k not in slugs:
            print("GUARD: case_depth.py has an entry for %s, which is not a "
                  "case" % k)
            bad += 1
    # And it must actually reach the page. A block that is built and then
    # dropped by a later edit is the failure mode this project has shipped
    # before, and it is invisible to a syntax check.
    for c in CASES:
        if c["slug"] not in DEPTH:
            continue
        page = open(os.path.join(SITE, c["slug"] + ".html"), encoding="utf-8").read()
        for what, mark in (("discussion", 'id="discussion"'),
                           ("questions", 'id="questions"'),
                           ("why-this-is-here", 'class="dc-why"')):
            if mark not in page:
                print("GUARD %s: the %s block never landed on the page"
                      % (c["slug"], what))
                bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)

    print("\n%d cases across %d groups" % (len(CASES), len(GROUPS)))
    costed = [c for c in CASES if c["cost"]]
    print("%d carry a cost-recovery figure" % len(costed))
    print("%d distinct code sections linked"
          % len({u for c in CASES for _, u, _ in c["charges"] if u}))
    print("guards clean - no names, no decision-PDF links, every case reachable")


if __name__ == "__main__":
    main()
