#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A whole-site redesign in the 37signals house style, drawn three ways.

WHY THIS EXISTS

`ops/home-page-options.html` applied the 37signals discipline to one page and
the answer came back: do the whole site that way. So this document takes the
same rules down to the identity - logo, type, color, navigation, footer - and
then draws every surface the site actually has, in three complete skins, so
the choice is between finished directions rather than between adjectives.

The six paths are the spine. `ops/stage-architecture.html` established them
and nothing here changes them: deciding, in a program, the gap between the
degree and the number, counting hours, newly licensed, running a practice.
What changes is that in this design they are the primary navigation rather
than a band two thirds of the way down the home page.

THREE SKINS, NOT THIRTY OPTIONS

Every mockup below is drawn in one of three complete systems, and each one is
internally consistent - type, color, spacing and voice move together:

  A - THE PRODUCT PAGE.  White, near-black, one green accent, heavy grotesque.
      Basecamp's own posture. Loudest, most confident, least editorial.
  B - THE FIELD NOTE.    Warm paper, deep ink, burnt accent, serif headlines
      over a mono eyebrow. Closest to the site's existing rates page, and the
      most obviously "made by a person who checked."
  C - THE MANUAL.        Near-white, black, red rule, a single narrow column
      and almost no ornament at all. Shape Up. The most severe, and the one
      that ages best.

Picking a skin picks everything else. That is the point of drawing them whole.

ON RAILS

The user plans to move hosting to Ruby on Rails. Nothing in this document
depends on the static build - it is HTML, CSS and one system font stack, and
the layer that would change is the publishing pipeline, not the design. A note
in the last section says what actually moves and what does not.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DONOR = os.path.join(SITE, "ops", "stage-architecture.html")
OUT = os.path.join(SITE, "ops", "redesign-37signals.html")
UPDATED = "13 August 2026"

NAV = [("moves", "The moves"), ("logo", "Logo"), ("type", "Typography"),
       ("color", "Color"), ("chrome", "Nav and footer"),
       ("home", "The home page"), ("paths", "The six paths"),
       ("pages", "Every other page"), ("pick", "What to ship")]

# The six, from ops/stage-architecture.html. The reader's own words, never a
# persona noun - that document's objection 4, and it still stands.
PATHS = [
    ("01", "Deciding", "Is this worth it?",
     "Weighing the degree, the debt and whether the arithmetic works.", "73"),
    ("02", "In a program", "Nobody will take me for practicum.",
     "Enrolled, with placement coming and no idea whose job it is.", "31"),
    ("03", "The gap", "Can I work before my number arrives?",
     "Degree in hand, registration pending, and hours quietly at risk.", "4"),
    ("04", "Counting hours", "547 hours and nobody will hire me.",
     "The longest stage, the loudest room, and the most to lose.", "21"),
    ("05", "Newly licensed", "Do I go on panels or not?",
     "Two years of decisions that set what the practice pays for a decade.",
     "19"),
    ("06", "Running a practice", "How do I do this ethically?",
     "Incorporating, hiring associates, and what a caseload owes people.",
     "24"),
]

SKINS = {
    "a": ("A", "The product page",
          "White, near-black, one green. Heavy grotesque, tight leading, "
          "generous air. Basecamp&rsquo;s own posture."),
    "b": ("B", "The field note",
          "Warm paper, deep ink, a burnt accent. Serif headline over a mono "
          "eyebrow &mdash; the site&rsquo;s rates page, promoted to the whole "
          "site."),
    "c": ("C", "The manual",
          "Near-white, black, one red rule. A single narrow column and "
          "almost no ornament. Shape Up."),
}

EXTRA = """
/* ---------------------------------------------------------------- skins */
.mk{--pad:34px}
@media(max-width:700px){.mk{--pad:20px}}
.mk *{box-sizing:border-box}
.mk .body{padding:var(--pad)}
.mk p{margin:0 0 14px}
.mk a{text-decoration:none}

.sk-a{--bg:#fff;--fg:#111311;--dim:#5B615C;--acc:#0E7A4F;--acc2:#E8F3ED;
  --line:#E3E6E3;--fam:'Inter',system-ui,sans-serif;--head:'Inter',system-ui,
  sans-serif;--hw:800;--ls:-.032em}
.sk-b{--bg:#F7F3E9;--fg:#1B211C;--dim:#6A6355;--acc:#B4531F;--acc2:#F0E4D3;
  --line:#DED5C2;--fam:'Inter',system-ui,sans-serif;
  --head:'Newsreader','Fraunces',Georgia,serif;--hw:600;--ls:-.014em}
.sk-c{--bg:#FCFCFB;--fg:#0B0B0B;--dim:#666;--acc:#D02B20;--acc2:#FBECEA;
  --line:#E2E2E0;--fam:'Inter',system-ui,sans-serif;
  --head:'Inter',system-ui,sans-serif;--hw:700;--ls:-.022em}
.mk{background:var(--bg);color:var(--fg);font-family:var(--fam);
  font-size:15px;line-height:1.55}
.mk h1,.mk h2,.mk h3{font-family:var(--head);font-weight:var(--hw);
  letter-spacing:var(--ls);line-height:1.04;margin:0 0 16px;color:var(--fg)}
.mk h1{font-size:46px;max-width:16ch}
.mk h2{font-size:29px;max-width:22ch}
.mk h3{font-size:20px;line-height:1.15}
@media(max-width:700px){.mk h1{font-size:29px}.mk h2{font-size:22px}}
.mk .lede{font-size:18px;line-height:1.5;color:var(--dim);max-width:56ch;
  margin:0 0 22px}
.mk .eyebrow{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.15em;text-transform:uppercase;color:var(--acc);
  display:block;margin-bottom:12px}
.sk-c .eyebrow{color:var(--dim)}
.mk .btn{display:inline-block;background:var(--acc);color:#fff;
  font-weight:700;font-size:16px;padding:13px 22px;border-radius:7px;
  font-family:var(--fam)}
.sk-c .btn{border-radius:0}
.sk-b .btn{border-radius:2px}
.mk .btn.ghost{background:transparent;color:var(--acc);
  border:2px solid var(--acc)}
.mk .fine{font-size:12.5px;color:var(--dim);margin:10px 0 0}
.mk hr{border:0;border-top:1px solid var(--line);margin:28px 0}
.sk-c hr{border-top:2px solid var(--fg)}

/* ------------------------------------------------------------ site chrome */
.mk .bar2{display:flex;align-items:center;gap:22px;padding:16px var(--pad);
  border-bottom:1px solid var(--line);flex-wrap:wrap}
.sk-c .bar2{border-bottom:2px solid var(--fg)}
.mk .bar2 .sp{margin-left:auto}
.mk .navlink{font-size:14.5px;color:var(--fg);font-weight:500}
.mk .navlink.on{color:var(--acc);font-weight:700}
.mk .pill{font-size:13.5px;font-weight:700;color:#fff;background:var(--acc);
  padding:8px 14px;border-radius:6px}
.sk-c .pill{border-radius:0}

/* logo marks */
.lg{display:inline-flex;align-items:center;gap:9px;font-family:var(--head);
  font-weight:800;letter-spacing:-.03em;font-size:20px;color:var(--fg)}
.lg .dot{color:var(--acc)}
.lg .sq{width:26px;height:26px;border-radius:7px;background:var(--acc);
  color:#fff;display:grid;place-items:center;font-size:12.5px;font-weight:800;
  letter-spacing:0}
.lg .ring{width:24px;height:24px;border-radius:50%;border:3.5px solid var(--acc);
  border-right-color:transparent;transform:rotate(-38deg)}
.lg.url{font-family:'IBM Plex Mono',ui-monospace,monospace;font-weight:600;
  font-size:16px;letter-spacing:-.01em}
.lg.stack{flex-direction:column;align-items:flex-start;gap:1px;line-height:1}
.lg.stack .sub{font-family:'IBM Plex Mono',ui-monospace,monospace;
  font-size:9.5px;letter-spacing:.19em;text-transform:uppercase;
  color:var(--dim);font-weight:400}

/* the six paths */
.paths{display:grid;gap:0;border-top:1px solid var(--line)}
.paths a{display:grid;grid-template-columns:46px 1fr auto;gap:16px;
  align-items:baseline;padding:17px 2px;border-bottom:1px solid var(--line);
  color:var(--fg)}
.paths .num{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12px;
  color:var(--dim)}
.paths .t{font-family:var(--head);font-weight:var(--hw);font-size:24px;
  letter-spacing:var(--ls);line-height:1.1}
.paths .q{display:block;font-family:var(--fam);font-weight:400;font-size:14px;
  color:var(--dim);margin-top:3px;letter-spacing:0}
.paths .c{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.5px;
  color:var(--dim);white-space:nowrap}
.paths a:hover .t{color:var(--acc)}
@media(max-width:700px){.paths .t{font-size:18px}}
.pcards{display:grid;gap:12px}
@media(min-width:720px){.pcards{grid-template-columns:1fr 1fr 1fr}}
.pcards a{display:block;padding:16px 17px;border:1px solid var(--line);
  border-radius:10px;color:var(--fg);background:var(--bg)}
.sk-c .pcards a{border-radius:0;border:2px solid var(--fg)}
.pcards .t{font-family:var(--head);font-weight:var(--hw);font-size:19px;
  display:block;letter-spacing:var(--ls)}
.pcards .q{font-size:13px;color:var(--dim);display:block;margin-top:5px}
.pcards .c{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  color:var(--acc);display:block;margin-top:10px;letter-spacing:.09em;
  text-transform:uppercase}

/* index and listings */
.cols{display:grid;gap:22px 34px}
@media(min-width:760px){.cols{grid-template-columns:1fr 1fr 1fr}}
.cols h4{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10.5px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--dim);
  margin:0 0 8px;padding-bottom:6px;border-bottom:1px solid var(--line)}
.cols ul{list-style:none;margin:0;padding:0}
.cols li{font-size:13.5px;line-height:1.5;margin-bottom:4px}
.cols li b{font-weight:600}
.cols li span{color:var(--dim)}
.rowlist{border-top:1px solid var(--line)}
.rowlist .r{display:grid;grid-template-columns:1fr auto;gap:14px;
  padding:13px 2px;border-bottom:1px solid var(--line);align-items:baseline}
.rowlist .n{font-weight:600;font-size:15px}
.rowlist .m{font-size:12.5px;color:var(--dim);display:block;margin-top:2px}
.rowlist .k{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.5px;
  color:var(--dim);white-space:nowrap;text-align:right}
.rowlist .k b{display:block;font-family:var(--head);font-size:17px;
  color:var(--fg)}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 16px}
.filters span{font-size:12.5px;border:1px solid var(--line);padding:6px 12px;
  border-radius:20px;color:var(--dim)}
.filters span.on{background:var(--acc);color:#fff;border-color:var(--acc)}
.sk-c .filters span{border-radius:0}

/* article */
.art{max-width:60ch}
.art p{font-size:16.5px;line-height:1.65}
.sk-b .art p{font-size:17.5px}
.art .pull{font-family:var(--head);font-weight:var(--hw);font-size:22px;
  line-height:1.25;border-left:4px solid var(--acc);padding-left:18px;
  margin:24px 0;color:var(--fg);letter-spacing:var(--ls)}
.sk-c .art .pull{border-left:0;border-top:2px solid var(--acc);
  border-bottom:2px solid var(--acc);padding:14px 0}
.art .meta{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11.5px;
  color:var(--dim);letter-spacing:.06em;margin-bottom:18px}
.side{border:1px solid var(--line);border-radius:10px;padding:15px 17px;
  font-size:13.5px;color:var(--dim);margin:22px 0}
.sk-c .side{border-radius:0;border:0;border-left:3px solid var(--fg);
  padding-left:16px}
.side b{color:var(--fg);display:block;margin-bottom:5px;font-size:14.5px}
.toc{font-size:13.5px;color:var(--dim)}
.toc b{display:block;color:var(--fg);font-family:'IBM Plex Mono',
  ui-monospace,monospace;font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;margin-bottom:8px}
.toc a{display:block;color:var(--dim);padding:4px 0;
  border-bottom:1px solid var(--line)}
.split{display:grid;gap:30px}
@media(min-width:860px){.split{grid-template-columns:1fr 210px}}

/* newsletter */
.news{border:2px solid var(--fg);border-radius:12px;padding:22px 24px}
.sk-c .news{border-radius:0}
.sk-b .news{border-radius:3px;background:var(--acc2)}
.news .f{display:flex;gap:9px;margin-top:14px;flex-wrap:wrap}
.news .in{flex:1 1 220px;border:1px solid var(--line);border-radius:7px;
  padding:12px 14px;background:var(--bg);color:var(--dim);font-size:14px}
.sk-c .news .in{border-radius:0;border:2px solid var(--fg)}
.newsbar{display:flex;gap:16px;align-items:center;flex-wrap:wrap;
  border-top:2px solid var(--fg);border-bottom:2px solid var(--fg);
  padding:16px 0;margin:24px 0}
.newsbar .t{font-family:var(--head);font-weight:var(--hw);font-size:19px;
  flex:1 1 260px;letter-spacing:var(--ls)}

/* footer */
.ft{padding:30px var(--pad);border-top:1px solid var(--line);
  background:var(--bg)}
.sk-c .ft{border-top:2px solid var(--fg)}
.ft .g{display:grid;gap:22px}
@media(min-width:760px){.ft .g{grid-template-columns:1.4fr 1fr 1fr 1fr}}
.ft h5{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin:0 0 9px}
.ft a{display:block;font-size:13.5px;color:var(--fg);padding:2px 0}
.ft .say{font-size:13.5px;color:var(--dim);max-width:34ch}
.ft .base{margin-top:24px;padding-top:16px;border-top:1px solid var(--line);
  font-size:12px;color:var(--dim);display:flex;gap:14px;flex-wrap:wrap}

/* about */
.face{width:74px;height:74px;border-radius:50%;background:var(--acc2);
  border:2px solid var(--acc);display:grid;place-items:center;
  font-family:var(--head);font-weight:800;font-size:26px;color:var(--acc)}
.sig{font-family:var(--head);font-size:17px;line-height:1.6;max-width:56ch}

/* phones */
.phrow{display:grid;gap:16px;margin:14px 0}
@media(min-width:760px){.phrow{grid-template-columns:repeat(3,minmax(0,300px))}}
.ph .lab2{font-family:var(--mono);font-size:10px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.ph .scr{border:3px solid var(--ink);border-radius:16px;overflow:hidden;
  height:520px;overflow-y:auto;background:#fff}
.ph .scr .mk{font-size:14px}
.ph .scr .mk h1{font-size:25px}

/* type specimen */
.spec{border:2px solid var(--ink);background:#fff;padding:22px 24px;
  margin:12px 0}
.spec .r{border-top:1px solid #E6E2D6;padding:13px 0;display:grid;
  grid-template-columns:96px 1fr;gap:18px;align-items:baseline}
.spec .r:first-of-type{border-top:0}
.spec .lb{font-family:var(--mono);font-size:10px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted)}
.swatches{display:flex;gap:0;margin:10px 0;border:2px solid var(--ink);
  overflow:hidden}
.swatches div{flex:1;height:62px;display:grid;place-items:end center;
  padding-bottom:5px;font-family:var(--mono);font-size:9px;color:#fff}
.swatches div.dk{color:#16211B}

/* document furniture */
.opt{border:2px solid var(--ink);background:var(--cream);
  box-shadow:6px 6px 0 var(--ink);padding:14px 16px;margin:26px 0 0}
.opt .top{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;
  margin-bottom:5px}
.opt .let{font-family:var(--fig);font-weight:800;font-size:25px;
  color:var(--pine);line-height:1}
.opt h3{margin:0;font-size:19px}
.opt .tag{margin-left:auto;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.12em;text-transform:uppercase;border:2px solid var(--ink);
  padding:3px 8px;background:#fff}
.opt .tag.win{background:var(--pine);color:#fff;border-color:var(--pine)}
.opt p{font-size:14px;margin:0;max-width:76ch}
.pros{display:grid;gap:10px;margin:12px 0 0}
@media(min-width:820px){.pros{grid-template-columns:1fr 1fr}}
.pros div{border:2px solid var(--ink);background:#fff;padding:10px 12px}
.pros .h{display:block;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.12em;text-transform:uppercase;margin-bottom:5px}
.pros .up .h{color:var(--green)}
.pros .dn .h{color:var(--red)}
.pros p{font-size:13px;margin:0;line-height:1.45;color:#39473F}
.moves{border:2px solid var(--ink);background:#fff;box-shadow:5px 5px 0
  var(--ink);margin:14px 0}
.moves .row{display:grid;grid-template-columns:40px 1fr;
  border-top:1px solid var(--line)}
.moves .row:first-child{border-top:0}
.moves .n{background:var(--deep);color:var(--gold);font-family:var(--mono);
  font-size:12px;display:grid;place-items:center;font-weight:600}
.moves .b{padding:10px 13px}
.moves h4{font-size:15px;margin:0 0 3px}
.moves p{font-size:13.5px;margin:0;color:#39473F}
.note{border-left:5px solid var(--gold);padding:2px 0 2px 16px;margin:16px 0}
.note p{font-size:14.5px;margin:0 0 6px}
code{font-family:var(--mono);font-size:12.5px;background:#fff;
  border:1px solid var(--line);padding:1px 5px}
"""


# ------------------------------------------------------------------ helpers
def frame(url, skin, inner, chrome=True):
    """A browser window around one mockup, in one skin."""
    return ('<div class="frame"><div class="bar"><span class="dot"></span>'
            '<span class="dot"></span><span class="dot"></span>'
            '<span class="url">therapistsupport.org%s</span></div>'
            '<div class="mk sk-%s">%s</div></div>' % (url, skin, inner))


def phones(items):
    """The same layouts at 390px. A design that only exists at desktop width
    is half a proposal - most of this site's traffic arrives on a phone, and
    the six paths as rows are the piece most likely to break there."""
    o = ['<div class="phrow">']
    for skin, label, inner in items:
        o.append('<div class="ph"><div class="lab2">%s</div>'
                 '<div class="scr"><div class="mk sk-%s">%s</div></div></div>'
                 % (label, skin, inner))
    o.append("</div>")
    return "".join(o)


def logo(kind, skin="a"):
    if kind == "word":
        return ('<span class="lg">therapistsupport<span class="dot">.</span>'
                "</span>")
    if kind == "mono":
        return ('<span class="lg"><span class="sq">TS</span>'
                "Therapist Support</span>")
    if kind == "ring":
        return ('<span class="lg"><span class="ring"></span>'
                "Therapist Support</span>")
    if kind == "url":
        return '<span class="lg url">therapistsupport.org</span>'
    if kind == "stack":
        return ('<span class="lg stack"><span>Therapist Support</span>'
                '<span class="sub">California &middot; free</span></span>')
    return ""


def navbar(skin, mark="word", on=None):
    items = ["The six paths", "Calculators", "Library", "About"]
    o = ['<div class="bar2">%s' % logo(mark, skin)]
    o.append('<span class="sp"></span>')
    for i in items:
        o.append('<a class="navlink%s">%s</a>'
                 % (" on" if i == on else "", i))
    o.append('<a class="pill">Open a calculator</a></div>')
    return "".join(o)


def pathrows(limit=6):
    o = ['<div class="paths">']
    for n, name, q, _d, c in PATHS[:limit]:
        o.append('<a><span class="num">%s</span><span class="t">%s'
                 '<span class="q">&ldquo;%s&rdquo;</span></span>'
                 '<span class="c">%s pages &rarr;</span></a>' % (n, name, q, c))
    o.append("</div>")
    return "".join(o)


def pathcards():
    o = ['<div class="pcards">']
    for n, name, q, d, c in PATHS:
        o.append('<a><span class="t">%s</span><span class="q">%s</span>'
                 '<span class="c">%s pages &rarr;</span></a>' % (name, d, c))
    o.append("</div>")
    return "".join(o)


INDEX = (
    '<div class="cols">'
    "<div><h4>Calculators</h4><ul>"
    "<li><b>Practice Simulator</b> <span>&mdash; what it pays you</span></li>"
    "<li><b>Tax &amp; Retirement</b></li><li><b>Associate Job Advisor</b></li>"
    "<li><b>Grow Your Practice</b></li><li><b>3,000 Hours</b></li>"
    "<li><b>Cost of Living</b></li></ul></div>"
    "<div><h4>Money</h4><ul><li>Sole proprietor or corporation</li>"
    "<li>The S&#8209;corp payroll gap</li><li>Estimated taxes</li>"
    "<li>Solo 401(k), SEP or SIMPLE</li><li>What you can deduct</li></ul></div>"
    "<div><h4>Licensure</h4><ul><li>Becoming an MFT</li>"
    "<li>Finding a supervisor</li><li>BBS fees, 2026</li>"
    "<li>Continuing education</li><li>The practicum year</li></ul></div>"
    "<div><h4>Getting paid</h4><ul><li>The Rate Gap</li>"
    "<li>Insurance panels</li><li>What Medicare pays</li>"
    "<li>Headway, Alma or Grow</li><li>Superbills and GFEs</li></ul></div>"
    "<div><h4>Practice</h4><ul><li>Hiring your first associate</li>"
    "<li>Liability insurance</li><li>48 discipline decisions</li>"
    "<li>SimplePractice, priced</li><li>Working remotely</li></ul></div>"
    "<div><h4>Training and jobs</h4><ul><li>78 MFT programs</li>"
    "<li>Every PsyD in the state</li><li>All 58 county job portals</li>"
    "<li>What counties pay</li><li>Loan forgiveness</li></ul></div>"
    "</div>")


def footer(skin, variant="full"):
    if variant == "one":
        return ('<div class="ft"><div class="base" style="margin:0;border:0;'
                'padding:0">%s<span>California only.</span>'
                "<span>Free, and no email box.</span>"
                "<span>Written by one licensed therapist.</span>"
                "<span>Corrections welcome.</span></div></div>"
                % logo("url", skin))
    if variant == "say":
        return ('<div class="ft"><div class="g">'
                '<div>%s<p class="say" style="margin-top:12px">Every figure '
                "here is the output of a calculation you can follow, on "
                "numbers you typed in. When a rule moves, the change is "
                "listed rather than quietly swapped in.</p></div>"
                "<div><h5>The six paths</h5>%s</div>"
                "<div><h5>Tools</h5><a>Practice Simulator</a>"
                "<a>Tax &amp; Retirement</a><a>Job Advisor</a>"
                "<a>3,000 Hours</a></div>"
                "<div><h5>This site</h5><a>About</a><a>What changed</a>"
                "<a>Every question</a><a>Corrections</a></div></div>"
                '<div class="base"><span>&copy; 2026</span>'
                "<span>Not legal, tax or career advice.</span>"
                "<span>No trackers, no ads, no email box.</span></div></div>"
                % (logo("stack", skin),
                   "".join("<a>%s</a>" % p[1] for p in PATHS)))
    return ('<div class="ft"><div class="g">'
            "<div>%s<p class=\"say\" style=\"margin-top:12px\">Free tools and "
            "checked reference for California therapists.</p></div>"
            "<div><h5>Paths</h5>%s</div>"
            "<div><h5>Topics</h5><a>Money</a><a>Licensure</a>"
            "<a>Getting paid</a><a>Practice</a><a>Training</a></div>"
            "<div><h5>This site</h5><a>About</a><a>What changed</a>"
            "<a>Corrections</a></div></div>"
            '<div class="base"><span>&copy; 2026 Therapist Support</span>'
            "<span>California only</span><span>Not advice</span></div></div>"
            % (logo("mono", skin),
               "".join("<a>%s</a>" % p[1] for p in PATHS[:4])))


# ------------------------------------------------------------------ mockups
def home(variant, skin):
    n = navbar(skin, {"a": "word", "b": "stack", "c": "url"}[skin],
               on="The six paths" if variant == 2 else None)
    if variant == 1:
        inner = (
            '<div class="body">'
            "<h1>Running a practice is a second job nobody trained you "
            "for.</h1>"
            '<p class="lede">Free calculators and checked reference for '
            "California therapists &mdash; what you keep, what you owe, what "
            "a client is worth, and what a job offer is really paying.</p>"
            '<a class="btn">See what your practice pays you</a> '
            '<span class="fine" style="display:inline-block;margin-left:10px">'
            "Written and checked by one licensed therapist in California."
            "</span>"
            "<hr>"
            '<span class="eyebrow">Or start where you are</span>'
            + pathrows() +
            "<hr>" + INDEX + "</div>")
    elif variant == 2:
        inner = (
            '<div class="body">'
            '<span class="eyebrow">Six paths &middot; 203 pages &middot; '
            "California only</span>"
            "<h1>Where are you?</h1>"
            '<p class="lede">Everything on this site is written for one of '
            "six moments. Pick the one you are in and the rest of it "
            "rearranges around you.</p>"
            + pathcards() +
            "<hr>"
            '<div class="newsbar"><span class="t">Most people start with one '
            "number: what the practice actually pays them.</span>"
            '<a class="btn">Open the simulator</a></div>'
            + INDEX + "</div>")
    elif variant == 3:
        inner = (
            '<div class="body">'
            "<h1>Nobody teaches therapists the business half.</h1>"
            '<p class="sig" style="font-size:17.5px;line-height:1.62;'
            'max-width:58ch;color:var(--fg)">I am a licensed therapist in '
            "California. Every number I needed to run a practice &mdash; a "
            "fair rate, what an associate job really pays, whether to "
            "incorporate, what insurance actually reimburses &mdash; I had to "
            "work out myself, from statutes and fee schedules and other "
            "people&rsquo;s guesses.</p>"
            '<p class="sig" style="font-size:17.5px;line-height:1.62;'
            'max-width:58ch;color:var(--fg)">So I built the tools I wanted and '
            "wrote down everything I checked. It is free, it asks for "
            "nothing, and every figure says where it came from and when it "
            "was last looked at.</p>"
            '<p class="fine" style="font-family:\'IBM Plex Mono\',monospace">'
            "&mdash; Shawn, LMFT &middot; California</p>"
            '<a class="btn">Start with the money</a>'
            "<hr>" + pathrows() + "<hr>" + INDEX + "</div>")
    else:
        inner = (
            '<div class="body">'
            "<h1>Six ways into the same 203 pages.</h1>"
            '<p class="lede">A reference for California therapists, indexed '
            "by the moment you are in rather than by our filing system. "
            "Free, no account, every figure dated against its source.</p>"
            + pathcards() +
            "<hr>"
            '<div class="split"><div>'
            '<span class="eyebrow">If you would rather just look</span>'
            + INDEX + "</div>"
            '<div class="news"><b style="font-family:var(--head);'
            'font-size:17px;display:block;margin-bottom:6px">When a number '
            "moves</b>"
            '<p class="fine" style="margin:0">One short email when a rule '
            "changes or a tool lands. Nothing else, ever.</p>"
            '<div class="f"><span class="in">you@example.com</span>'
            '<a class="btn">Get it</a></div></div></div></div>')
    return frame("/", skin, n + inner + footer(skin, "say"))


def path_page(skin, variant=1):
    p = PATHS[3]
    n = navbar(skin, "word", on="The six paths")
    top = ('<div class="body">'
           '<span class="eyebrow">Path %s of six &middot; for AMFTs, ASWs and '
           "APCCs</span><h1>You are counting toward 3,000.</h1>"
           '<p class="lede">Twenty-one pages written for this stage, every '
           "figure with a named source. The job, the hours, the supervisor, "
           "the money and the paperwork that decides your date.</p>"
           % p[0])
    if variant == 1:
        inner = (top +
                 '<a class="btn">Start with what is holding up your date</a> '
                 '<a class="btn ghost" style="margin-left:8px">See all 21</a>'
                 "<hr>"
                 '<span class="eyebrow">The three questions this room is '
                 "actually asking</span>"
                 '<div class="rowlist">'
                 '<div class="r"><div><span class="n">&ldquo;547 hours and '
                 "nobody will hire me.&rdquo;</span>"
                 '<span class="m">Where the jobs are, what they pay, and '
                 "which employers can lawfully bill for you</span></div>"
                 '<span class="k">4 pages</span></div>'
                 '<div class="r"><div><span class="n">&ldquo;How do I find a '
                 "supervisor?&rdquo;</span>"
                 '<span class="m">Every list that exists, and the rule that '
                 "decides whether yours counts</span></div>"
                 '<span class="k">2 pages</span></div>'
                 '<div class="r"><div><span class="n">&ldquo;Am I being '
                 "underpaid?&rdquo;</span>"
                 '<span class="m">What associates are paid in LA and the Bay, '
                 "and what unpaid work costs</span></div>"
                 '<span class="k">3 pages</span></div></div>'
                 "<hr>" + INDEX + "</div>")
    else:
        inner = (top +
                 '<div class="split"><div>'
                 '<div class="side"><b>What differs if you are an ASW</b>'
                 "1,700 of your hours and 13 of your 52 weeks have to be "
                 "under an LCSW. APCCs have no equivalent rule. Both "
                 "differences are handled on the supervisor page.</div>"
                 + INDEX +
                 '</div><div class="toc"><b>On this path</b><a>Getting hired'
                 "</a><a>Finding a supervisor</a><a>The 3,000-hour tool</a>"
                 "<a>What associates are paid</a><a>Unpaid hours</a>"
                 "<a>Hours by telehealth</a><a>County job portals</a>"
                 "<a>Loan forgiveness</a></div></div></div>")
    return frame("/paths/counting-hours", skin, n + inner + footer(skin))


def article(skin, variant=1):
    n = navbar(skin, "word")
    lead = ('<div class="body"><div class="art">'
            '<p class="meta">Licensure &middot; checked 13 August 2026 '
            "&middot; 30 sources</p>"
            "<h1>Finding a clinical supervisor in California.</h1>"
            '<p class="lede">The Board does not certify supervisors and keeps '
            "no roster, so here is where the lists actually are &mdash; and "
            "the rule that decides whether the person you find can count your "
            "hours at all.</p>"
            "<p>California licenses 165,000 people and publishes a list of "
            "exactly zero supervisors. What exists instead is nine county "
            "chapter directories, one statewide association list with no "
            "contact details on it, and two commercial products.</p>"
            '<p class="pull">In a private practice, you cannot simply hire '
            "your own supervisor. The statute requires them to be on your "
            "employer&rsquo;s books.</p>"
            "<p>That is the single most expensive misunderstanding in "
            "California supervision, and it is an easy one to hold, because "
            "paying somebody for their professional time is normally all it "
            "takes.</p></div>")
    if variant == 1:
        inner = lead + '<div class="news" style="margin-top:26px">' \
                       '<b style="font-family:var(--head);font-size:17px;' \
                       'display:block;margin-bottom:5px">Told when this ' \
                       'changes</b><p class="fine" style="margin:0">The BBS ' \
                       "moves these rules every couple of years. One email " \
                       'when they do.</p><div class="f">' \
                       '<span class="in">you@example.com</span>' \
                       '<a class="btn">Get it</a></div></div></div>'
    else:
        inner = ('<div class="body"><div class="split"><div class="art">'
                 + lead[len('<div class="body"><div class="art">'):]
                 + '<div class="toc" style="margin-top:6px"><b>Sections</b>'
                   "<a>Where the lists are</a><a>The private-practice trap</a>"
                   "<a>Whether they may supervise you</a>"
                   "<a>What the week looks like</a><a>What it costs</a>"
                   "<a>Three deadlines</a><a>What to ask</a>"
                   '<div class="side" style="margin-top:18px"><b>On this '
                   "page</b>Nine of 23 CAMFT chapters publish a supervisor "
                   "list. Three of the addresses people are still sent to no "
                   "longer exist.</div></div></div></div>")
    return frame("/finding-a-clinical-supervisor-california", skin,
                 n + inner + footer(skin))


def directory(skin, variant=1):
    n = navbar(skin, "word")
    rows = [("CAMFT Certified Supervisors", "Statewide &middot; name and city "
             "only &middot; free", "302", "entries"),
            ("LA-CAMFT, Supervision Offered", "Los Angeles &middot; phone and "
             "city &middot; free", "314", "entries"),
            ("East Bay CAMFT Supervision Finder", "East Bay &middot; "
             "supervision type and credentials &middot; free", "150",
             "entries"),
            ("Marin CAMFT", "North Bay &middot; phone and type &middot; free",
             "116", "entries"),
            ("Redwood Empire CAMFT", "Sonoma and the North Coast &middot; "
             "free", "99", "entries"),
            ("Orange County CAMFT", "Orange County &middot; free", "63",
             "entries")]
    body = ['<div class="body">'
            '<span class="eyebrow">Directory &middot; fetched 13 August '
            "2026</span><h1>Where a supervisor list actually is.</h1>"
            '<p class="lede">Every candidate fetched and counted. Nine of the '
            "twenty-three CAMFT chapters publish one; fourteen do not, and "
            "two of the chapters that are supposed to no longer exist.</p>"]
    if variant == 1:
        body.append('<div class="filters"><span class="on">All 15</span>'
                    "<span>Free to browse</span><span>Chapters</span>"
                    "<span>Statewide</span><span>Shows availability</span>"
                    "<span>Southern California</span>"
                    "<span>Bay Area</span></div>")
        body.append('<div class="rowlist">')
        for name, meta, big, unit in rows:
            body.append('<div class="r"><div><span class="n">%s</span>'
                        '<span class="m">%s</span></div>'
                        '<span class="k"><b>%s</b>%s</span></div>'
                        % (name, meta, big, unit))
        body.append("</div>")
        body.append('<p class="fine">Counts are what each source reports on '
                    "its own page. Nothing from any of these directories is "
                    "copied here.</p>")
    else:
        body.append('<div class="split"><div><div class="rowlist">')
        for name, meta, big, unit in rows:
            body.append('<div class="r"><div><span class="n">%s</span>'
                        '<span class="m">%s</span></div>'
                        '<span class="k"><b>%s</b>%s</span></div>'
                        % (name, meta, big, unit))
        body.append('</div></div><div class="toc"><b>Filter</b>'
                    "<a>Free to browse</a><a>CAMFT chapters</a>"
                    "<a>Statewide</a><a>Shows availability</a>"
                    "<a>Bay Area</a><a>Southern California</a>"
                    '<div class="side" style="margin-top:16px"><b>Checked and '
                    "empty</b>Nine places people are sent that publish no "
                    "list at all, including the Board itself.</div></div>"
                    "</div>")
    body.append("</div>")
    return frame("/finding-a-clinical-supervisor-california#lists", skin,
                 n + "".join(body) + footer(skin, "one"))


def about(skin, variant=1):
    n = navbar(skin, "word", on="About")
    if variant == 1:
        inner = ('<div class="body">'
                 '<div style="display:flex;gap:18px;align-items:center;'
                 'margin-bottom:20px"><span class="face">S</span>'
                 "<div><h1 style=\"font-size:34px;margin:0\">Who made this, "
                 "and what I want from you.</h1></div></div>"
                 '<p class="sig">Nothing. There is no email box, no account, '
                 "no course at the end and no affiliate link on any figure "
                 "that matters. I am a licensed therapist in California and I "
                 "built the tools I could not find.</p>"
                 '<p class="sig">Every dollar on this site is the output of a '
                 "calculation you can follow, run on numbers you typed in. "
                 "There are no illustrative figures. When a rule moves, the "
                 "change gets listed on a page rather than quietly swapped "
                 "in. If a number here is wrong, tell me and I will fix it "
                 "and say so.</p>"
                 '<p class="fine" style="font-family:\'IBM Plex Mono\','
                 'monospace">&mdash; Shawn, LMFT</p><hr>'
                 '<div class="cols"><div><h4>What this is</h4><ul>'
                 "<li>Six calculators</li><li>203 checked pages</li>"
                 "<li>California only</li></ul></div>"
                 "<div><h4>What it is not</h4><ul><li>Legal or tax advice</li>"
                 "<li>A directory that takes payment</li>"
                 "<li>A lead magnet</li></ul></div>"
                 "<div><h4>How it is paid for</h4><ul><li>It is not. It costs "
                 "very little to run</li></ul></div></div></div>")
    else:
        inner = ('<div class="body">'
                 '<span class="eyebrow">About</span>'
                 "<h1>No email box. No account. No course at the end.</h1>"
                 '<p class="lede">The three questions every free site raises '
                 "and almost none answer.</p>"
                 '<div class="rowlist">'
                 '<div class="r"><div><span class="n">Who made it?</span>'
                 '<span class="m">One licensed marriage and family therapist '
                 "in California, who needed these numbers first.</span></div>"
                 "</div>"
                 '<div class="r"><div><span class="n">What do they want?'
                 '</span><span class="m">Nothing. There is no list to join '
                 "and nothing is sold here.</span></div></div>"
                 '<div class="r"><div><span class="n">Why should you believe '
                 'a figure?</span><span class="m">Because it says where it '
                 "came from and when it was last checked, and because the "
                 "ones that moved are listed on a page instead of being "
                 "quietly replaced.</span></div></div></div></div>")
    return frame("/about", skin, n + inner + footer(skin, "say"))


def newsletter(skin, variant=1):
    n = navbar(skin, "word")
    if variant == 1:
        inner = ('<div class="body"><h1>One email when a number moves.</h1>'
                 '<p class="lede">The Board changes its fees, the IRS changes '
                 "its thresholds, and a payer quietly re-prices a code. That "
                 "is when this sends. Not weekly, not a digest, not a "
                 "funnel.</p>"
                 '<div class="news" style="max-width:560px">'
                 '<b style="font-family:var(--head);font-size:19px;'
                 'display:block;margin-bottom:6px">What actually gets sent'
                 "</b>"
                 '<p class="fine" style="margin:0 0 4px">&bull; A rule '
                 "changed, and what it does to your arithmetic<br>"
                 "&bull; A new calculator, once<br>"
                 "&bull; A correction, when I get something wrong</p>"
                 '<div class="f"><span class="in">you@example.com</span>'
                 '<a class="btn">Subscribe</a></div>'
                 '<p class="fine">Six emails last year. Unsubscribe link in '
                 "every one, and the list is never used for anything "
                 "else.</p></div></div>")
    else:
        inner = ('<div class="body">'
                 '<div class="newsbar"><span class="t">Six emails last year, '
                 "each one because a number moved.</span>"
                 '<span class="in" style="flex:0 1 220px">you@example.com'
                 '</span><a class="btn">Subscribe</a></div>'
                 '<p class="fine" style="max-width:60ch">That bar is the '
                 "whole promotion, and it sits once at the foot of an "
                 "article rather than in a corner, a slide-up and an exit "
                 "overlay. The claim is a number, not an adjective: a reader "
                 "can check it against the archive.</p></div>")
    return frame("/updates", skin, n + inner + footer(skin, "one"))


# ------------------------------------------------------------------- build
def build():
    donor = open(DONOR, encoding="utf-8").read()
    m = re.search(r"<style>([\s\S]*?)</style>", donor)
    if not m:
        sys.exit("ops/stage-architecture.html has no <style> block")
    css = m.group(1) + EXTRA

    o = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<meta name="robots" content="noindex,nofollow">',
         "<title>A 37signals redesign, drawn three ways</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+'
         'Grotesque:opsz,wght@12..96,800&family=Fraunces:opsz,wght@9..144,600;'
         '9..144,800&family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;'
         '500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,600&'
         'display=swap" rel="stylesheet">',
         "<style>%s</style></head><body>" % css]

    o.append('<header class="mast"><div class="wrap">'
             '<span class="lab">Working document &middot; %s</span>'
             "<h1>If 37signals had built this site.</h1>"
             "<p>The whole thing, not one page: logo, type, color, "
             "navigation, footer, home, the six paths, a path page, an "
             "article, a directory, the newsletter and the about page "
             "&mdash; drawn in <b>three complete skins</b> so the choice is "
             "between finished directions rather than between adjectives. "
             "The six paths become the primary navigation, which is the "
             "structural change underneath all of it.</p>"
             '<div class="meta"><span class="chip">3 skins</span>'
             '<span class="chip">%d mockups &middot; 3 phone views</span>'
             '<span class="chip">6 paths</span>'
             '<span class="chip">No page moves required</span></div>'
             "</div></header>" % (UPDATED, 23))

    o.append('<nav class="jump"><div class="wrap"><ul>')
    for h, t in NAV:
        o.append('<li><a href="#%s">%s</a></li>' % (h, t))
    o.append("</ul></div></nav>")
    o.append('<div class="wrap">')

    # ---------------------------------------------------------------- moves
    o.append('<section id="moves"><div class="kicker"><span class="n">01</span>'
             "<h2>What is actually being borrowed</h2></div>")
    o.append('<p class="lede">37signals is not a look, it is a set of '
             "refusals. Written as refusals, they can be checked against a "
             "draft.</p>")
    o.append('<div class="moves">')
    for n, h, p in [
        ("01", "One idea per screen, stated as a sentence",
         "Headlines are sentences with verbs and a point of view. No "
         "two-word category labels, no &ldquo;Solutions.&rdquo;"),
        ("02", "Type does the work that decoration usually does",
         "Hierarchy comes from size and weight, not from boxes, gradients or "
         "shadows. Three sizes and two weights is the whole system."),
        ("03", "One accent color, used sparingly",
         "Every skin below has exactly one. If everything is emphasized, the "
         "reader has to do the sorting."),
        ("04", "Text lists instead of card grids",
         "A card is a container for things that are genuinely compared. Six "
         "paths are chosen between, not compared, so they are rows."),
        ("05", "Say who made it, out loud",
         "37signals signs everything. For a free site aimed at people who "
         "have been sold to by every other free site, that is the highest "
         "value paragraph on the page."),
        ("06", "Claims carry numbers",
         "&ldquo;Six emails last year&rdquo; instead of "
         "&ldquo;low volume.&rdquo; A number can be checked; an adjective "
         "cannot."),
        ("07", "The index stays, and that breaks the style on purpose",
         "37signals sells one product to a stranger. This is a 203-page "
         "reference and half its readers have been here before, so every "
         "layout below keeps a full index at the foot."),
    ]:
        o.append('<div class="row"><div class="n">%s</div><div class="b">'
                 "<h4>%s</h4><p>%s</p></div></div>" % (n, h, p))
    o.append("</div>")

    o.append('<div class="note"><p><b>The structural change is the six '
             "paths.</b> They exist already as an architecture proposal and "
             "as tagging in the registry; what this redesign does is promote "
             "them from a band on the home page to the site&rsquo;s primary "
             "navigation, with the topic hubs demoted to an index at the "
             "foot of every page. Nothing moves URL and nothing is "
             "duplicated &mdash; a path page is a generated view over the "
             "same library, exactly as the topic clusters already are.</p>"
             "</div>")
    rows = []
    for n, name, q, d, c in PATHS:
        rows.append('<div class="row"><div class="n">%s</div><div class="b">'
                    '<h4>%s <span style="font-weight:400;color:#635E53;'
                    'font-size:13px">&mdash; &ldquo;%s&rdquo;</span></h4>'
                    "<p>%s <b>%s pages today.</b></p></div></div>"
                    % (n, name, q, d, c))
    o.append('<div class="moves">%s</div>' % "".join(rows))
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- logo
    o.append('<section id="logo"><div class="kicker"><span class="n">02</span>'
             "<h2>Logo</h2></div>")
    o.append('<p class="lede">Five wordmarks, no icon-only options. The name '
             "is the asset; a symbol nobody has seen before is a second thing "
             "to teach and this site has no budget for teaching.</p>")
    o.append('<div class="spec">')
    for kind, name, why in [
        ("word", "Lowercase wordmark, period",
         "The Basecamp move. Set in the heaviest weight, all lowercase, one "
         "accent-colored full stop. Confident, and it works at 18px in a "
         "browser tab."),
        ("mono", "Rounded monogram plus name",
         "A square TS in the accent, then the name. The only option that "
         "gives you a usable favicon and app icon without redrawing "
         "anything."),
        ("ring", "The open ring",
         "An hour that has not closed yet &mdash; the site&rsquo;s actual "
         "subject. The most meaningful mark, and the one most likely to read "
         "as a generic loading spinner at small sizes."),
        ("url", "The URL, in mono",
         "The HEY and ONCE move: the address is the brand. Zero design debt, "
         "and it undersells a 203-page library."),
        ("stack", "Stacked, with a qualifier",
         "Name over a mono line reading &ldquo;California &middot; "
         "free.&rdquo; Says the two things that differentiate the site "
         "before anybody clicks."),
    ]:
        o.append('<div class="r"><div class="lb">%s</div><div>'
                 '<div class="mk sk-a" style="background:transparent;'
                 'padding:6px 0">%s</div>'
                 '<p style="font-size:13px;color:#39473F;margin:6px 0 0">%s'
                 "</p></div></div>" % (name, logo(kind), why))
    o.append("</div>")
    o.append('<p class="pk-d" style="font-size:14px;color:#39473F">Each is '
             "shown above in skin A&rsquo;s green. The same mark in "
             "skin B&rsquo;s burnt orange and skin C&rsquo;s red appears in "
             "the navigation mockups below, which is the honest way to judge "
             "a wordmark &mdash; in place, at real size, next to real "
             "links.</p>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- type
    o.append('<section id="type"><div class="kicker"><span class="n">03</span>'
             "<h2>Typography</h2></div>")
    o.append('<p class="lede">Three systems, one per skin. All three use a '
             "monospace for eyebrows and figures, because this site&rsquo;s "
             "whole claim is that the numbers were checked and a mono face "
             "says so without a sentence.</p>")
    for key, fam, head, body_note in [
        ("a", "Inter 800 / Inter 400 / IBM Plex Mono",
         "Headlines at -3.2% tracking, 1.04 leading",
         "One family, two weights, nothing else. Loads fast, renders "
         "identically everywhere, and is the least distinctive of the three "
         "&mdash; which is exactly the trade Basecamp makes."),
        ("b", "Newsreader 600 / Inter 400 / IBM Plex Mono",
         "Serif headline, sans body, mono eyebrow",
         "The site&rsquo;s rates page already runs this pairing and it is the "
         "most editorial of the three. Says &ldquo;somebody researched "
         "this&rdquo; before a word is read; costs one extra font file."),
        ("c", "Inter 700 / Inter 400 / IBM Plex Mono",
         "Smaller headlines, tighter measure, hard rules",
         "The Shape Up setting: type barely larger than the body, and "
         "hierarchy carried by 2px rules and whitespace instead. The most "
         "severe, and the one that survives a redesign in three years."),
    ]:
        letter, name, _d = SKINS[key]
        o.append('<div class="opt"><div class="top"><span class="let">%s</span>'
                 "<h3>%s</h3></div><p>%s &mdash; %s</p></div>"
                 % (letter, name, fam, head))
        o.append(frame("/type-specimen", key,
                       '<div class="body">'
                       '<span class="eyebrow">Licensure &middot; checked '
                       "13 August 2026</span>"
                       "<h1>What a supervisor is allowed to be.</h1>"
                       '<p class="lede">The Board sets nine tests and '
                       "publishes no list of anybody who passes them.</p>"
                       "<h2>The private-practice rule</h2>"
                       "<p>An associate in a private practice must be "
                       "supervised by somebody employed by, contracted by, or "
                       "an owner of their employer. A supervisor retained "
                       "privately does not satisfy it, and the hours are not "
                       "creditable.</p>"
                       '<h3>Nine tests, one table</h3>'
                       '<p class="fine">Figures set in IBM Plex Mono: '
                       "<b>3,000</b> hours &middot; <b>104</b> weeks &middot; "
                       "<b>$300+</b> a month &middot; <b>9 of 23</b> "
                       "chapters</p>"
                       '<a class="btn">A button, in this skin</a>'
                       "</div>"))
        o.append('<p class="pk-d" style="font-size:13.5px;color:#39473F;'
                 'margin-top:-4px">%s</p>' % body_note)
    o.append("</section><hr class=\"rule\">")

    # ---------------------------------------------------------------- color
    o.append('<section id="color"><div class="kicker">'
             '<span class="n">04</span><h2>Color</h2></div>')
    o.append('<p class="lede">One accent each, and a lot of paper. The '
             "current site runs pine, gold, cream and ink together; every "
             "skin below cuts that to one accent plus a tint of it.</p>")
    for key, sw in [
        ("a", [("#FFFFFF", "paper", 1), ("#111311", "ink", 0),
               ("#0E7A4F", "accent", 0), ("#E8F3ED", "tint", 1),
               ("#5B615C", "dim", 0)]),
        ("b", [("#F7F3E9", "paper", 1), ("#1B211C", "ink", 0),
               ("#B4531F", "accent", 0), ("#F0E4D3", "tint", 1),
               ("#6A6355", "dim", 0)]),
        ("c", [("#FCFCFB", "paper", 1), ("#0B0B0B", "ink", 0),
               ("#D02B20", "accent", 0), ("#FBECEA", "tint", 1),
               ("#666666", "dim", 0)]),
    ]:
        letter, name, why = SKINS[key]
        o.append('<div class="opt"><div class="top"><span class="let">%s'
                 "</span><h3>%s</h3></div><p>%s</p>" % (letter, name, why))
        o.append('<div class="swatches">')
        for hexv, lab, dark in sw:
            o.append('<div class="%s" style="background:%s">%s %s</div>'
                     % ("dk" if dark else "", hexv, lab, hexv))
        o.append("</div></div>")
    o.append('<div class="note"><p><b>Contrast holds in all three.</b> Body '
             "text against paper is at least 12:1 in each, the accent against "
             "paper clears 4.5:1, and white on the accent clears it too "
             "&mdash; which is what makes the button legible. The current "
             "site&rsquo;s gold-on-pine pairing is the one combination that "
             "does not survive into any of these.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # --------------------------------------------------------------- chrome
    o.append('<section id="chrome"><div class="kicker">'
             '<span class="n">05</span><h2>Navigation and footer</h2></div>')
    o.append('<p class="lede">Four links and one button. The current '
             "masthead carries seven topic dropdowns; in this design the "
             "topics move to the index at the foot of every page and the top "
             "of the page carries the paths.</p>")
    for key, mark in (("a", "word"), ("b", "stack"), ("c", "url")):
        letter, name, _ = SKINS[key]
        o.append('<div class="opt"><div class="top"><span class="let">%s'
                 "</span><h3>%s &mdash; navigation</h3></div>"
                 '<p>Logo, four links, one action. No dropdowns: a menu that '
                 "opens is a decision deferred, and the paths are the "
                 "decision.</p></div>" % (letter, name))
        o.append(frame("/", key, navbar(key, mark, on="The six paths")
                       + '<div class="body"><p class="fine" '
                         'style="margin:0">&hellip; page content &hellip;</p>'
                         "</div>"))
    o.append('<h3 style="margin:26px 0 6px">Three footers</h3>')
    o.append('<p class="pk-d">The footer is where the topic index lives, so '
             "it is doing real work rather than repeating the nav.</p>")
    for key, variant, label in (("a", "full", "Four columns, the standard"),
                                ("b", "say", "With the claim, and all six "
                                             "paths"),
                                ("c", "one", "One line, and nothing else")):
        o.append('<p class="pk-k" style="margin-top:14px">%s &middot; skin %s'
                 "</p>" % (label, SKINS[key][0]))
        o.append(frame("/", key, footer(key, variant)))
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- home
    o.append('<section id="home"><div class="kicker">'
             '<span class="n">06</span><h2>The home page, four ways</h2></div>')
    o.append('<p class="lede">Each one is the whole page, top to bottom. They '
             "differ in what the first screen asks the reader to do, and each "
             "is drawn in the skin that suits it &mdash; a statement wants "
             "skin A, a letter wants skin B.</p>")
    for v, skin, name, thesis, up, dn, tag in [
        (1, "a", "The statement",
         "One sentence, one paragraph, one button, then the paths as rows.",
         "Tells a cold arrival what this is in four seconds, and still routes "
         "&mdash; the paths are the second screen, not a competing first one.",
         "Says nothing about who made it above the fold, and the button "
         "assumes the money question is the right entry for everybody.",
         "win"),
        (2, "b", "Where are you?",
         "The six paths are the page. A two-line headline and then the grid.",
         "The most honest expression of the architecture: the site really is "
         "six rooms, and this says so immediately.",
         "Asks the reader to classify themselves before anybody has told them "
         "what the site is &mdash; the objection that killed the five-card "
         "band, at larger scale.", ""),
        (3, "b", "The letter",
         "A signed note, then the paths, then the index.",
         "Answers the question every free site raises and none address, and "
         "it is the one thing no competitor can copy.",
         "Two paragraphs before anything actionable is a real cost on a "
         "phone, and it makes a set of tools feel like a blog.", ""),
        (4, "c", "The manual",
         "Six paths as cards, the index and the newsletter side by side "
         "beneath.",
         "Densest of the four and the fastest for a returning reader: "
         "everything the site has is visible in two screens.",
         "The most impersonal. In skin C especially it reads as a reference "
         "work rather than as somebody&rsquo;s project.", ""),
    ]:
        o.append('<div class="opt"><div class="top"><span class="let">%d</span>'
                 "<h3>%s</h3><span class=\"tag %s\">Skin %s%s</span></div>"
                 "<p>%s</p>"
                 '<div class="pros"><div class="up"><span class="h">What it '
                 'does well</span><p>%s</p></div><div class="dn">'
                 '<span class="h">What it costs</span><p>%s</p></div></div>'
                 "</div>"
                 % (v, name, tag, SKINS[skin][0],
                    " &middot; recommended" if tag else "", thesis, up, dn))
        o.append(home(v, skin))
    o.append('<h3 style="margin:26px 0 6px">And on a phone</h3>')
    o.append('<p class="pk-d">The same three home pages at 390px. The paths '
             "stay rows rather than collapsing into a menu, which is the "
             "whole reason for choosing rows: a card grid at this width is "
             "six full-width boxes and four screens of scrolling before the "
             "reader sees anything else.</p>")
    o.append(phones([
        ("a", "1 &middot; The statement",
         '<div class="body"><h1>Running a practice is a second job nobody '
         "trained you for.</h1>"
         '<p class="lede" style="font-size:15px">Free calculators and checked '
         "reference for California therapists.</p>"
         '<a class="btn">See what it pays you</a><hr>'
         '<span class="eyebrow">Or start where you are</span>' + pathrows()
         + "</div>"),
        ("b", "3 &middot; The letter",
         '<div class="body"><h1>Nobody teaches therapists the business '
         "half.</h1>"
         '<p style="font-size:15.5px;line-height:1.6">I am a licensed '
         "therapist in California. Every number I needed to run a practice I "
         "had to work out myself.</p>"
         '<p class="fine" style="font-family:\'IBM Plex Mono\',monospace">'
         "&mdash; Shawn, LMFT</p>"
         '<a class="btn">Start with the money</a><hr>' + pathrows() + "</div>"),
        ("c", "4 &middot; The manual",
         '<div class="body"><h1>Six ways into the same 203 pages.</h1>'
         + pathcards() + "</div>"),
    ]))
    o.append("</section><hr class=\"rule\">")

    # ---------------------------------------------------------------- paths
    o.append('<section id="paths"><div class="kicker">'
             '<span class="n">07</span><h2>The six paths</h2></div>')
    o.append('<p class="lede">A path page is a generated view over the '
             "library, not a sub-site. Two layouts: one that opens with the "
             "questions the room is asking, and one that opens with the "
             "shelf and keeps a rail.</p>")
    o.append('<div class="opt"><div class="top"><span class="let">1</span>'
             "<h3>Questions first</h3>"
             '<span class="tag win">Recommended</span></div>'
             "<p>The strongest finding in the original research was that "
             "comments measure demand and reactions measure approval &mdash; "
             "and the posts that pulled 87 and 114 comments were "
             "&ldquo;547 hours and nobody will hire me,&rdquo; not "
             "&ldquo;resources for associates.&rdquo; This layout leads with "
             "the question in the asker&rsquo;s words and shows the shelf "
             "underneath.</p></div>")
    o.append(path_page("a", 1))
    o.append('<div class="opt"><div class="top"><span class="let">2</span>'
             "<h3>Shelf first, with a rail</h3></div>"
             "<p>Faster for somebody who already knows what they want, and "
             "the rail carries the one line about what differs for an ASW or "
             "an APCC &mdash; the license axis the architecture document "
             "said must never become a hub matrix.</p></div>")
    o.append(path_page("b", 2))
    o.append('<div class="note"><p><b>Path three is the one to watch.</b> '
             "&ldquo;The gap&rdquo; &mdash; degree awarded, number not yet "
             "issued &mdash; has four pages today and permanent consequences "
             "for anybody who works before their Live Scan. It is the "
             "smallest path and the only one where being wrong destroys "
             "hours that cannot be re-earned. Either it opens with real "
             "content or it folds into &ldquo;counting hours&rdquo; until it "
             "has some.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # ---------------------------------------------------------------- pages
    o.append('<section id="pages"><div class="kicker">'
             '<span class="n">08</span><h2>Every other page</h2></div>')
    for label, note, mocks in [
        ("A standard content page",
         "Two treatments: a single measure with a pull quote and the "
         "newsletter at the foot, or a measure plus a sticky contents rail. "
         "The rail wins on this site because the pages are long and "
         "sectioned.",
         [article("b", 1), article("a", 2)]),
        ("A directory listing",
         "The site has several &mdash; 58 county portals, 78 programs, 15 "
         "supervisor lists, 48 discipline decisions. Filter chips above the "
         "rows, or a filter rail beside them. Chips are better on a phone "
         "and the rail is better when the filters are also facts.",
         [directory("a", 1), directory("c", 2)]),
        ("The newsletter promotion",
         "A dedicated page and an in-article bar. The claim is a number "
         "&mdash; six emails last year &mdash; because a reader can check "
         "that against the archive and cannot check &ldquo;low volume.&rdquo;",
         [newsletter("b", 1), newsletter("a", 2)]),
        ("About",
         "Portrait and a signed letter, or the three questions as rows. The "
         "second is more in the house style; the first is warmer, and this "
         "audience is buying trust.",
         [about("b", 1), about("c", 2)]),
    ]:
        o.append('<h3 style="margin:26px 0 6px">%s</h3>' % label)
        o.append('<p class="pk-d">%s</p>' % note)
        for mk in mocks:
            o.append(mk)
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- pick
    o.append('<section id="pick"><div class="kicker">'
             '<span class="n">09</span><h2>What to ship</h2></div>')
    o.append('<p class="lede">One skin, one home page, and a build order '
             "where nothing has to be finished before anything else is "
             "useful.</p>")
    o.append('<div class="moves">')
    for n, h, p in [
        ("01", "Skin B, with skin A&rsquo;s home page",
         "The field note is the site&rsquo;s actual character &mdash; it is "
         "a research project, and the rates page already proved the pairing "
         "works. But the home page needs the statement&rsquo;s confidence, "
         "and skin A&rsquo;s heavier headline carries it. Mixing them is "
         "cheap: it is one headline face on one page."),
        ("02", "The stacked wordmark",
         "&ldquo;Therapist Support&rdquo; over &ldquo;California &middot; "
         "free&rdquo; in mono. It says the two differentiating facts before "
         "a click, and it degrades to the monogram for a favicon."),
        ("03", "Home page 1, the statement",
         "Sentence, paragraph, button, authorship line, then the six paths "
         "as rows, then the index. Four decisions instead of eleven blocks."),
        ("04", "Then the six path pages, questions-first",
         "Generated from the registry tagging that already exists. Path 3 "
         "stays folded into path 4 until it has content of its own."),
        ("05", "Then the article and directory templates",
         "These are the two shapes that cover 190 of the 203 pages, so they "
         "are where the redesign is actually felt."),
        ("06", "The newsletter bar last",
         "It is one component and it can land any time. It is last because "
         "it is the only piece that asks the reader for something."),
    ]:
        o.append('<div class="row"><div class="n">%s</div><div class="b">'
                 "<h4>%s</h4><p>%s</p></div></div>" % (n, h, p))
    o.append("</div>")

    o.append('<div class="note"><p><b>On moving to Rails.</b> None of this '
             "depends on how the site is served. What is drawn above is HTML, "
             "one stylesheet and one webfont link &mdash; it renders "
             "identically out of the current Python build, out of a Rails "
             "app, or out of anything else. What a move would actually change "
             "is the <b>publishing pipeline</b>: the forty passes in "
             "<code>_dev/</code>, the guards that stop a bad figure shipping, "
             "and the registry that every hub and path page is generated "
             "from. Those are the asset, not the HTML.</p>"
             "<p>Worth saying plainly: <b>a redesign and a re-platform are "
             "two projects</b> and doing them together is how both go "
             "wrong. The design above can ship this month on the current "
             "static build. If Rails comes later it inherits finished "
             "templates rather than having to invent them &mdash; and the "
             "questions Rails actually answers (accounts, saved scenarios, "
             "a supervisor availability signal, anything that has to remember "
             "a person) are product questions this document does not "
             "touch.</p></div>")
    o.append("</section>")

    o.append("</div>")
    o.append('<footer><div class="wrap"><p style="margin:0">Working document, '
             "not linked from the site and not indexable. Every mockup is a "
             "drawing &mdash; none of the links in them go anywhere. Written "
             "%s.</p></div></footer>" % UPDATED)
    o.append("</body></html>")
    return "".join(o)


def main():
    print("a 37signals redesign, three skins")
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
    if n < 23:
        print("GUARD: only %d mockups - the document claims a whole site" % n)
        bad += 1

    # All three skins must appear, or a "drawn three ways" document is not.
    for k in SKINS:
        if 'sk-%s"' % k not in html:
            print("GUARD: skin %s is never drawn" % k)
            bad += 1

    # All six paths, by name and by question, or the spine is incomplete.
    for _num, name, q, _d, _c in PATHS:
        if name not in html:
            print("GUARD: path %r is missing" % name)
            bad += 1
        if q not in html:
            print("GUARD: the question for %r is missing" % name)
            bad += 1

    for needle, what in [
        ("a redesign and a re-platform are", "the Rails answer"),
        ("set of refusals", "what the style is"),
        ("generated view over the library", "the no-duplication rule"),
        ("Path three is the one to watch", "the gap-path warning"),
    ]:
        if needle not in html:
            print("GUARD: %s is missing" % what)
            bad += 1

    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    for w in ("programme", "counselling", "centre", "whilst", "amongst",
              "recognise", "organisation", "behaviour", "enquir",
              "fulfilment", "judgement"):
        if re.search(r"\b%s" % w, t, re.I):
            print("GUARD: British spelling %r" % w)
            bad += 1
    for m in re.finditer(r"\bgates?\b", t, re.I):
        print("GUARD: %r - that word was removed sitewide" % m.group(0))
        bad += 1
    if 'name="robots" content="noindex' not in html:
        print("GUARD: working document must not be indexable")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d mockups, 3 skins, %d paths"
          % (n, len(PATHS)))


if __name__ == "__main__":
    main()
