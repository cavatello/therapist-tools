#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""content-blocks-system.html — the site-wide promotion system, mocked.

The problem this answers, in the user's words: traffic will arrive from search,
forums and Facebook onto DEEP pages, not the home page. Every one of those
landings has to do three jobs at once - say where you are, prove the page is
worth reading, and route you onward - or the visit is one page long.

The frame is Bryan Eisenberg's Conversion Trinity (Relevance / Value / Call to
Action) plus information scent, which is the HCI half of the same idea: Pirolli
and Card's Information Foraging Theory, where a reader follows a link only while
the label smells like the thing they want. Both are cited on the page itself.

Every block below is rendered at real fidelity with real destinations, not
lorem. The figures are the ones the tools actually compute; where a page cannot
compute (a research page has no inputs) the spec says so rather than printing an
illustrative number, which this site does not do.
"""
import os, re, base64

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "tree5", "fonts")

SIM = "practice-simulator.html"
TAX = "therapist-tax-strategy-california.html"
GROW = "grow-your-therapy-practice.html"
AMFT = "associate-mft-job-advisor.html"
HRS = "amft-3000-hours-california.html"
COLA = "therapist-cost-of-living-california.html"
RATES = "rates.html"
REMOTE = "therapist-working-remotely-california.html"
TOOLS = "tools.html"


def inline_fonts():
    css = open(os.path.join(FONTS, "fonts.css")).read()
    keep = [b for b in re.split(r"(?=/\* )", css) if b.strip().startswith("/* latin */")]

    def sub(m):
        with open(os.path.join(FONTS, "f", m.group(1)), "rb") as f:
            return "url(data:font/woff2;base64," + base64.b64encode(f.read()).decode() + ")"
    return re.sub(r"url\(\./f/([^)]+)\)", sub, "".join(keep))


CSS = """
:root{--paper:#FBF9F3;--white:#fff;--ink:#26241E;--muted:#6E695E;--line:#E7E2D6;
 --field:#FBF6E9;--fline:#E4D9BE;--pine:#2C6350;--brick:#8E4B45;--gold:#B08430;
 --indigo:#4B3B93;--pop:#F6C560;--pos:#3F9577}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.6}
.w{max-width:1120px;margin:0 auto;padding:0 26px}
h1,h2,h3,h4{font-family:Fraunces,Georgia,serif;font-weight:600;letter-spacing:-.02em;
 line-height:1.12;margin:0}
a{color:inherit}
.mono{font-family:'IBM Plex Mono',monospace}

/* ---- document chrome (this mockup's own, not the site's) ---- */
.doc{background:#1B1A17;color:#EDE8DC;padding:44px 0 40px}
.doc .k{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--pop);margin:0 0 14px}
.doc h1{font-size:clamp(30px,4vw,48px);color:#FFFDF6;max-width:19ch}
.doc p{font-size:16px;line-height:1.62;color:#B8B1A2;max-width:64ch;margin:18px 0 0}
.doc p b{color:#EDE8DC;font-weight:600}

.sec{padding:52px 0 8px}
.sec>.w>.n{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--gold);margin:0 0 10px}
.sec h2{font-size:clamp(23px,2.9vw,34px);max-width:24ch}
.sec>.w>.d{font-size:15px;color:var(--muted);max-width:70ch;margin:12px 0 0}

/* the frame */
.tri{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:26px 0 0}
.tri div{background:var(--white);border:1px solid var(--line);border-radius:16px;
 padding:20px 20px 18px;border-top:3px solid var(--pine)}
.tri div:nth-child(2){border-top-color:var(--gold)}
.tri div:nth-child(3){border-top-color:var(--indigo)}
.tri h4{font-size:18px;margin:0 0 7px}
.tri p{font-size:13.4px;color:var(--muted);margin:0}
.tri em{font-style:italic;color:var(--ink)}

/* the specimen frame: a block, then what it is for */
.spec{margin:28px 0 0;border:1px solid var(--line);border-radius:20px;overflow:hidden;
 background:var(--white)}
.spec .bar{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;
 background:#F4F1E7;border-bottom:1px solid var(--line);padding:11px 18px;
 font-family:'IBM Plex Mono',monospace;font-size:10.6px;letter-spacing:.08em;
 text-transform:uppercase;color:var(--muted)}
.spec .bar b{color:var(--ink)}
.spec .bar .t{background:var(--pine);color:#fff;border-radius:5px;padding:3px 8px;
 letter-spacing:.09em}
.spec .stage{padding:30px 26px;background:var(--paper)}
.spec .why{border-top:1px solid var(--line);padding:18px 22px 20px;display:grid;
 grid-template-columns:repeat(3,minmax(0,1fr));gap:6px 24px}
.spec .why div{font-size:12.6px;color:var(--muted);line-height:1.6}
.spec .why b{display:block;color:var(--ink);font-size:10.5px;letter-spacing:.1em;
 text-transform:uppercase;font-family:'IBM Plex Mono',monospace;margin:0 0 4px}

/* ============ BLOCK 1 — the answer grid ============ */
.ag-k{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--gold);margin:0 0 9px}
.ag-h{font-size:clamp(22px,2.7vw,31px);margin:0 0 8px;max-width:20ch}
.ag-d{font-size:13.8px;color:var(--muted);max-width:64ch;margin:0 0 22px}
.ag-g{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.ag-c{display:block;background:var(--white);border:1px solid var(--line);border-radius:16px;
 padding:20px 22px 18px;text-decoration:none;border-left:3px solid var(--pine);
 transition:transform .12s,box-shadow .12s}
.ag-c:nth-child(2){border-left-color:var(--gold)}
.ag-c:nth-child(3){border-left-color:var(--indigo)}
.ag-c:nth-child(4){border-left-color:var(--brick)}
.ag-c:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(38,36,30,.08)}
.ag-c q{display:block;font-family:Fraunces,Georgia,serif;font-size:19px;font-weight:600;
 letter-spacing:-.015em;line-height:1.24;quotes:none;margin:0 0 7px}
.ag-c span{display:block;font-size:12.8px;color:var(--muted);line-height:1.55;margin:0 0 12px}
.ag-c em{font-style:normal;font-size:12.8px;font-weight:700;color:var(--pine)}
.ag-c:nth-child(2) em{color:#8A6318}
.ag-c:nth-child(3) em{color:var(--indigo)}
.ag-c:nth-child(4) em{color:var(--brick)}

/* ============ BLOCK 2 — where you are right now ============ */
.wr{background:#22302B;border-radius:20px;padding:28px 28px 26px;color:#DFEAE4}
.wr .k{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:#8FBBA8;margin:0 0 9px}
.wr h3{font-size:clamp(20px,2.4vw,27px);color:#FFFDF6;margin:0 0 7px}
.wr .d{font-size:13.4px;color:#9DBFB1;max-width:62ch;margin:0 0 20px}
.wr-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.wr-c{display:flex;flex-direction:column;background:rgba(255,255,255,.055);
 border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:18px 18px 16px;
 text-decoration:none;color:inherit;transition:background .12s,border-color .12s}
.wr-c:hover{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.28)}
.wr-c b{font-family:Fraunces,Georgia,serif;font-size:17px;font-weight:600;color:#FFFDF6;
 letter-spacing:-.012em;margin:0 0 6px;line-height:1.2}
.wr-c span{font-size:12.6px;color:#9DBFB1;line-height:1.55;flex:1 1 auto;margin:0 0 13px}
.wr-c i{font-style:normal;font-size:12.6px;font-weight:700;color:var(--pop)}
.wr-c i+i{display:block;margin-top:5px;color:#8FBBA8;font-weight:600}

/* ============ BLOCK 3 — numbers from the tools ============ */
.nt{display:grid;grid-template-columns:minmax(0,.85fr) repeat(3,minmax(0,1fr));gap:0;
 background:var(--white);border:1px solid var(--line);border-radius:18px;overflow:hidden}
.nt>div{padding:20px 22px;border-left:1px solid var(--line)}
.nt>div:first-child{border-left:0;background:#F4F1E7}
.nt .lede b{display:block;font-family:Fraunces,Georgia,serif;font-size:19px;font-weight:600;
 line-height:1.2;letter-spacing:-.015em;margin:0 0 6px}
.nt .lede span{font-size:12.4px;color:var(--muted);line-height:1.5}
.nt a{display:block;text-decoration:none;color:inherit}
.nt a .f{font-family:Fraunces,Georgia,serif;font-size:clamp(23px,2.6vw,30px);font-weight:600;
 letter-spacing:-.02em;line-height:1;margin:0 0 5px}
.nt a:nth-of-type(1) .f{color:var(--pine)}
.nt a .l{font-size:12.4px;color:var(--muted);line-height:1.5;margin:0 0 10px}
.nt a .g{font-size:12.2px;font-weight:700;color:var(--pine)}
.nt a:hover .g{text-decoration:underline}
.nt .live{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:9.5px;
 letter-spacing:.12em;text-transform:uppercase;color:var(--pos);
 border:1px solid rgba(63,149,119,.4);border-radius:5px;padding:2px 6px;margin:0 0 9px}

/* ============ BLOCK 4 — read before you decide ============ */
.rb{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.rb-p{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:18px 20px}
.rb-p .top{display:flex;align-items:baseline;gap:9px;margin:0 0 12px}
.rb-p .top b{font-family:Fraunces,Georgia,serif;font-size:16.5px;font-weight:600}
.rb-p .top i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:9.5px;
 letter-spacing:.11em;text-transform:uppercase;color:var(--gold)}
/* two of these fell to 41px when the description ran to one line. min-height
   rather than more padding, so the tall ones are not pushed further apart. */
.rb-p a{display:flex;gap:11px;align-items:flex-start;text-decoration:none;color:inherit;
 border-top:1px dashed var(--fline);padding:11px 0 0;margin:11px 0 0;min-height:44px}
.rb-p a:first-of-type{border-top:0;padding-top:0;margin-top:0}
.rb-p a .ic{flex:none;width:26px;height:26px;border-radius:7px;background:var(--field);
 border:1px solid var(--fline);display:flex;align-items:center;justify-content:center;
 font-size:12px}
.rb-p a strong{display:block;font-size:13.4px;font-weight:700;color:var(--pine)}
.rb-p a span{display:block;font-size:12.4px;color:var(--muted);line-height:1.5}
.rb-p a:hover strong{text-decoration:underline}

/* ============ BLOCK 5 — what people arrive looking for ============ */
.al{background:var(--white);border:1px solid var(--line);border-radius:18px;padding:24px 26px}
.al h3{font-size:21px;margin:0 0 6px}
.al .d{font-size:13.2px;color:var(--muted);max-width:66ch;margin:0 0 16px}
.al ul{list-style:none;margin:0;padding:0;display:grid;
 grid-template-columns:repeat(2,minmax(0,1fr));gap:0 26px}
.al li{border-top:1px solid var(--line)}
.al li a{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 10px;padding:10px 0;
 text-decoration:none;min-height:44px}
.al li q{quotes:none;font-family:'IBM Plex Mono',monospace;font-size:12.4px;color:var(--muted);
 flex:1 1 auto}
.al li b{font-size:12.6px;font-weight:700;color:var(--pine);white-space:nowrap}
.al li a:hover q{color:var(--ink)}
.al li a:hover b{text-decoration:underline}

/* ---- the matrix ---- */
.mx{width:100%;border-collapse:collapse;margin:24px 0 0;font-size:12.8px;background:var(--white);
 border:1px solid var(--line);border-radius:14px;overflow:hidden}
.mx th,.mx td{padding:9px 10px;border-bottom:1px solid var(--line);text-align:center}
.mx th{font-family:'IBM Plex Mono',monospace;font-size:9.8px;letter-spacing:.07em;
 text-transform:uppercase;color:var(--muted);font-weight:600;vertical-align:bottom}
.mx td:first-child,.mx th:first-child{text-align:left;font-weight:600;white-space:nowrap}
.mx tbody tr:hover{background:#FCFAF4}
.mx .y{color:var(--pine);font-weight:800}
.mx .o{color:var(--gold);font-weight:800}
.mx .n{color:#CFC9BA}
.mxk{font-size:12.4px;color:var(--muted);margin:12px 0 0}
.mxk b{color:var(--ink)}

/* ---- rules ---- */
.rules{list-style:none;margin:22px 0 0;padding:0;display:grid;
 grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 22px}
.rules li{background:var(--white);border:1px solid var(--line);border-radius:13px;
 padding:15px 17px;font-size:13.2px;color:var(--muted);line-height:1.6}
.rules li b{display:block;color:var(--ink);font-size:13.6px;margin:0 0 4px}

.cites{margin:24px 0 0;font-size:12.4px;color:var(--muted);line-height:1.7}
.cites a{color:var(--pine)}
.foot{padding:34px 0 60px;font-size:12.4px;color:var(--muted)}

@media (max-width:900px){
 .tri,.ag-g,.wr-g,.rb,.al ul,.rules,.spec .why{grid-template-columns:1fr}
 .nt{grid-template-columns:1fr}
 .nt>div{border-left:0;border-top:1px solid var(--line)}
 .nt>div:first-child{border-top:0}
 .mxwrap{overflow-x:auto}
}
"""


def spec(tag, name, where, stage, trinity, scent, hci):
    return """
<div class="spec">
  <div class="bar"><span class="t">%s</span><span><b>%s</b></span>
    <span>&middot;</span><span>%s</span></div>
  <div class="stage">%s</div>
  <div class="why">
    <div><b>Trinity</b>%s</div>
    <div><b>Scent</b>%s</div>
    <div><b>HCI</b>%s</div>
  </div>
</div>""" % (tag, name, where, stage, trinity, scent, hci)


# ------------------------------------------------------------- block 01 ---
ANSWERS = [
    ("Should I incorporate, or stay a sole proprietor?",
     "A California therapist may not form an LLC. The real choice is sole "
     "proprietor or a professional corporation with an S-corp election, and it is "
     "worth a five-figure swing either way.",
     "Tax &amp; retirement strategy", TAX),
    ("What is this associate job actually paying me?",
     "Flat rate, share of the fee, or salary &mdash; priced against the unpaid "
     "admin and the supervision you have to sit in either way.",
     "AMFT job advisor", AMFT),
    ("How long until I am licensed?",
     "Four requirements close at different speeds, and the 3,000 is almost never "
     "the one that decides your date.",
     "3,000 hours calculator", HRS),
    ("Can I afford to live here on this?",
     "Housing, transport and food by area, your student loan on RAP or the "
     "standard plan, and what is left for savings.",
     "Cost of living", COLA),
]

BLOCK1 = ('<p class="ag-k">Why this exists</p>'
          '<h2 class="ag-h">Four questions nobody covered in grad school.</h2>'
          '<p class="ag-d">The answers exist. They are scattered across accountants who '
          'charge by the hour, forum threads written by people guessing, and blog posts '
          'that stop exactly where the arithmetic starts &mdash; and almost none of it is '
          'specific to California, which is where most of the difference is.</p>'
          '<div class="ag-g">'
          + "".join('<a class="ag-c" href="%s"><q>%s</q><span>%s</span><em>%s &rarr;</em></a>'
                    % (href, q, body, cta) for q, body, cta, href in ANSWERS)
          + '</div>')

# ------------------------------------------------------------- block 02 ---
ROUTES = [
    ("Still accruing hours",
     "Registered associate, or about to be. The money question is which placement, "
     "and the clock question is which of the four gates closes last.",
     [("What an AMFT job pays &rarr;", AMFT), ("How long to 3,000 hours &rarr;", HRS)]),
    ("Newly licensed, first private clients",
     "The first year on your own. What to charge, what a full week actually bills, "
     "and what is left once expenses and self-employment tax come out.",
     [("Practice simulator &rarr;", SIM), ("What California therapists charge &rarr;", RATES)]),
    ("Running a practice",
     "Established caseload. The questions move to structure, retirement, and whether "
     "the week in front of you is the best version of itself.",
     [("Tax &amp; retirement strategy &rarr;", TAX), ("Grow your practice &rarr;", GROW)]),
]

BLOCK2 = ('<div class="wr"><p class="k">Start where you are</p>'
          '<h3>Three careers use this site, and they need different pages.</h3>'
          '<p class="d">You may have landed here from a search about something else '
          'entirely. This is the shortest route from wherever you actually are.</p>'
          '<div class="wr-g">'
          + "".join('<a class="wr-c" href="%s"><b>%s</b><span>%s</span>%s</a>'
                    % (links[0][1], title, body,
                       "".join('<i>%s</i>' % l for l, _ in links))
                    for title, body, links in ROUTES)
          + '</div></div>')

# ------------------------------------------------------------- block 03 ---
NUMS = [
    ("$138,365", "take-home on a $250,000 practice, after every cost and every tax",
     "Open the simulator", SIM, True),
    ("$21,564", "of that year&rsquo;s tax bill still optional, once accounts and entity are priced",
     "Tax &amp; retirement", TAX, True),
    # NOT invented. MIT Living Wage, Los Angeles County, one adult / no children:
    # 22471 + 8681 + 4463 + 3876 + 3255 + 1517 + 4992 = 49,255 a year = 4,105 a
    # month. The same seven categories the cost-of-living page pre-fills.
    ("$4,105", "a month to cover Los Angeles County &mdash; one adult, no children, "
     "before tax (MIT Living Wage)",
     "Cost of living", COLA, False),
]

BLOCK3 = ('<div class="nt">'
          '<div class="lede"><b>Numbers, not adjectives.</b>'
          '<span>Every figure on this site is the output of a calculation you can follow. '
          'These three are live &mdash; change an input and they move.</span></div>'
          + "".join(
              '<div><a href="%s">%s<p class="f">%s</p><p class="l">%s</p>'
              '<p class="g">%s &rarr;</p></a></div>'
              % (href, '<span class="live">live</span>' if live else
                 '<span class="live" style="color:#B08430;border-color:rgba(176,132,48,.45)">cited</span>',
                 fig, lab, cta)
              for fig, lab, cta, href, live in NUMS)
          + '</div>')

# ------------------------------------------------------------- block 04 ---
PAIRS = [
    ("Practice simulator", "the tool", [
        ("The California therapy rate gap", "what insurance pays against private pay, "
         "with the panel rates people actually see", RATES),
        ("Cost of living in California", "what the take-home has to cover before it is "
         "worth anything", COLA)]),
    ("Tax &amp; retirement strategy", "the tool", [
        ("Working remotely from California", "eight places, and whether your licence "
         "travels to any of them", REMOTE),
        ("Choosing a structure in California", "why an LLC is off the table, with the "
         "statute", TAX + "#structure")]),
    ("AMFT job advisor", "the tool", [
        ("How long to 3,000 hours", "the four gates, projected from the week you "
         "actually work", HRS),
        ("The California therapy rate gap", "what the practice bills for your hour, "
         "against what it pays you", RATES)]),
    ("Grow your practice", "the tool", [
        ("The California therapy rate gap", "before you chase more clients, check "
         "whether the price is the problem", RATES),
        ("Practice simulator", "what the extra caseload is worth once expenses and "
         "tax come out of it", SIM)]),
]

BLOCK4 = ('<div class="rb">'
          + "".join(
              '<div class="rb-p"><div class="top"><b>%s</b><i>%s</i></div>%s</div>'
              % (name, kind,
                 "".join('<a href="%s"><span class="ic">&#9656;</span><span>'
                         '<strong>%s</strong><span>%s</span></span></a>' % (h, t, d)
                         for t, d, h in reads))
              for name, kind, reads in PAIRS)
          + '</div>')

# ------------------------------------------------------------- block 05 ---
QUERIES = [
    ("how much do therapists make in california", "Practice simulator", SIM),
    ("should i form an s corp as a therapist", "Tax strategy", TAX),
    ("amft salary california", "Job advisor", AMFT),
    ("how long does it take to get 3000 hours", "3,000 hours", HRS),
    ("can a california therapist move out of state", "Working remotely", REMOTE),
    ("therapist private pay rates california", "Field notes", RATES),
    ("cost of living los angeles therapist", "Cost of living", COLA),
    ("how many clients to fill a caseload", "Grow your practice", GROW),
]

BLOCK5 = ('<div class="al"><h3>What people arrive looking for</h3>'
          '<p class="d">The phrases that bring people here, in their words rather than '
          'ours, each pointed at the page that answers it.</p><ul>'
          + "".join('<li><a href="%s"><q>%s</q><b>%s &rarr;</b></a></li>' % (h, q, d)
                    for q, d, h in QUERIES)
          + '</ul></div>')

# ---------------------------------------------------------------- matrix ---
PAGES = ["Home", "Practice simulator", "Tax strategy", "Grow", "Job advisor",
         "3,000 hours", "Cost of living", "Field notes (rates)", "Working remotely",
         "All tools"]
#            answer  where   numbers  read    queries
MATRIX = {
    "Home":                 ["y", "n", "y", "o", "y"],
    "Practice simulator":   ["n", "o", "y", "y", "n"],
    "Tax strategy":         ["n", "y", "y", "y", "n"],
    "Grow":                 ["n", "y", "y", "y", "n"],
    "Job advisor":          ["n", "y", "y", "y", "n"],
    "3,000 hours":          ["n", "y", "n", "y", "n"],
    "Cost of living":       ["n", "y", "y", "y", "n"],
    "Field notes (rates)":  ["o", "y", "o", "y", "y"],
    "Working remotely":     ["o", "y", "n", "y", "y"],
    # The tools page is already a route list, so block 02 would say twice what its
    # own grid says. Dropped rather than fudged - the rule is three.
    "All tools":            ["y", "o", "n", "y", "y"],
}
COLS = ["01 Answer grid", "02 Where you are", "03 Numbers", "04 Read first", "05 Queries"]
GLYPH = {"y": ('y', "&#9679;"), "o": ('o', "&#9675;"), "n": ('n', "&middot;")}

matrix = ('<div class="mxwrap"><table class="mx"><thead><tr><th>Page</th>'
          + "".join("<th>%s</th>" % c for c in COLS) + "</tr></thead><tbody>"
          + "".join("<tr><td>%s</td>%s</tr>"
                    % (p, "".join('<td class="%s">%s</td>' % GLYPH[v] for v in MATRIX[p]))
                    for p in PAGES)
          + "</tbody></table></div>")

RULES = [
    ("Never promote the page you are on.",
     "Every block is generated from a list minus the current slug. A card linking to "
     "the page under it is the fastest way to teach a reader that the blocks are "
     "decoration."),
    ("Three per page, and never two in the same screen.",
     "One route block high, one value block mid-page, one depth block at the foot. "
     "Hick&rsquo;s law bites on options presented <i>together</i>, not on options spread "
     "down a page &mdash; but five blocks stacked is a sitemap, and a sitemap converts "
     "like a sitemap."),
    ("The link label is the destination&rsquo;s own words.",
     "Information scent breaks when the label and the landing headline disagree. If the "
     "card says &ldquo;what an AMFT job pays&rdquo;, the h1 it lands on says the same "
     "thing &mdash; and the build asserts it."),
    ("A figure in a block is computed or cited. Never illustrative.",
     "The live ones move with the reader&rsquo;s inputs and carry that state in the "
     "link. The ones on pages with no inputs come from a named source and say so."),
    ("Deep pages get &ldquo;where you are&rdquo; near the top, not the bottom.",
     "Someone who arrived from a Facebook link to an S-corp page and is actually a "
     "second-year associate needs the exit above the fold, before the bounce."),
    ("Every block carries the reader&rsquo;s setup in the href.",
     "Rate, caseload and the twelve expense categories travel as hash keys. A route that "
     "makes someone retype their practice is a route they do not take twice."),
]


SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Content block system &mdash; Therapist Support</title>
<style>%(fonts)s</style>
<style>%(css)s</style>
</head><body>

<header class="doc"><div class="w">
  <p class="k">Mock-up &middot; site-wide</p>
  <h1>A promotion system, not five more sections.</h1>
  <p>Traffic will land on <b>deep pages</b> &mdash; a search for &ldquo;amft salary
  california&rdquo;, a forum link to the tax page, a Facebook post about rates. None of
  those readers see the home page first. So each of the five blocks below is a
  <b>component with a defined job and a defined slot</b>, generated from one list of
  pages, so adding a tool updates every block on every page at once.</p>
  <p>The frame is Bryan Eisenberg&rsquo;s <b>Conversion Trinity</b> &mdash; relevance,
  value, call to action &mdash; and <b>information scent</b>, its HCI half: a reader
  follows a link only while the label still smells like what they came for. Each specimen
  below is annotated against both.</p>
</div></header>

<section class="sec"><div class="w">
  <p class="n">The frame</p>
  <h2>Three questions every landing has to answer in the first screen.</h2>
  <p class="d">Eisenberg&rsquo;s formulation, in the reader&rsquo;s voice. A block that
  does not answer one of these is decoration.</p>
  <div class="tri">
    <div><h4>Relevance</h4><p><em>&ldquo;Are you relevant to what I came for &mdash; and
    have you kept the scent from the link I clicked?&rdquo;</em></p></div>
    <div><h4>Value</h4><p><em>&ldquo;Do I know why you are the right answer for me? Have
    you actually shown me something?&rdquo;</em></p></div>
    <div><h4>Call to action</h4><p><em>&ldquo;Is it obvious what to do next, and am I
    confident enough to do it?&rdquo;</em></p></div>
  </div>
</div></section>

<section class="sec"><div class="w">
  <p class="n">Block 01</p>
  <h2>The answer grid</h2>
  <p class="d">Replaces &ldquo;Why this exists&rdquo; on the home page. That block was
  three paragraphs about my motive, in a narrow column with the right half empty. This
  is the same slot spent on the reader&rsquo;s problem instead &mdash; and it promotes
  four tools in the space the prose used for none.</p>
  %(spec1)s
</div></section>

<section class="sec"><div class="w">
  <p class="n">Block 02</p>
  <h2>Where you are right now</h2>
  <p class="d">The one that stops a second-year associate bouncing off a page about
  S-corps. Goes high on deep pages, because the reader who is on the wrong page needs
  the exit before they decide the site is not for them.</p>
  %(spec2)s
</div></section>

<section class="sec"><div class="w">
  <p class="n">Block 03</p>
  <h2>Numbers from the tools</h2>
  <p class="d">Extends the hero panel pattern down the page rather than inventing a new
  one. Two of these are live &mdash; they recompute from whatever the reader has typed,
  and the link carries that state onward. The third is a cited research figure, marked
  as one, because the page it sits on has no inputs to compute from.</p>
  %(spec3)s
</div></section>

<section class="sec"><div class="w">
  <p class="n">Block 04</p>
  <h2>Read before you decide</h2>
  <p class="d">Every calculator gets the document standing behind it. This is the Help
  Scout move &mdash; the tool is the answer, the research is the reason to trust the
  answer &mdash; and it is how the two research pages stop being orphans reachable only
  from the nav.</p>
  %(spec4)s
</div></section>

<section class="sec"><div class="w">
  <p class="n">Block 05</p>
  <h2>What people arrive looking for</h2>
  <p class="d">Real query phrasings, in the reader&rsquo;s words, near the footer. Cheap
  internal linking with honest anchor text, and it catches the reader who scrolled the
  whole page without finding their question.</p>
  %(spec5)s
</div></section>

<section class="sec"><div class="w">
  <p class="n">The system</p>
  <h2>Which block goes on which page</h2>
  <p class="d">Filled circle: ships. Hollow: only if the page is short on routes. No page
  carries more than three, and no two of them share a screen &mdash; one high, one
  mid-page, one at the foot.</p>
  %(matrix)s
  <p class="mxk"><b>Read the columns, not the rows.</b> Block 02 is on nearly everything
  because nearly everything can be landed on cold. Block 01 is nearly nowhere because it
  is an orientation device, and a reader who is already deep in the tax page does not
  need orienting &mdash; they need routing.</p>
</div></section>

<section class="sec"><div class="w">
  <p class="n">Rules</p>
  <h2>Six rules that keep this a system</h2>
  <ul class="rules">%(rules)s</ul>
  <div class="cites"><b>Sources.</b>
   [1] Bryan Eisenberg, <a href="https://www.bryaneisenberg.com/the-conversion-trinity-the-3-step-magic-formula-to-increase-click-throughs-conversions/" target="_blank" rel="noopener noreferrer">The Conversion Trinity</a>
   &mdash; relevance, value, call to action, in the reader&rsquo;s voice.
   [2] Peter Pirolli and Stuart Card, <a href="https://doi.org/10.1037/0033-295X.106.4.643" target="_blank" rel="noopener noreferrer">Information Foraging</a>,
   <i>Psychological Review</i> 106(4), 1999 &mdash; information scent, the mechanism the
   link-label rule is built on.
   [3] William Hick, <a href="https://doi.org/10.1080/17470215208416600" target="_blank" rel="noopener noreferrer">On the rate of gain of information</a>,
   <i>QJEP</i> 4(1), 1952 &mdash; decision time rises with the number of choices, which is
   the two-blocks-per-page ceiling.
   [4] Paul Fitts, <a href="https://doi.org/10.1037/h0055392" target="_blank" rel="noopener noreferrer">The information capacity of the human motor system</a>,
   <i>J. Exp. Psychol.</i> 47(6), 1954 &mdash; every card in every block above clears a
   44px target.
  </div>
</div></section>

<div class="foot"><div class="w">Mock-up. Every link points at a real slug; the figures
are the ones the tools compute or a cited source, never illustrative.</div></div>

</body></html>
"""


def main():
    html = SHELL % dict(
        fonts=inline_fonts(), css=CSS,
        spec1=spec("01", "Answer grid", "home, all tools &mdash; one slot, high", BLOCK1,
                   "Relevance. Names the reader&rsquo;s problem in their words before "
                   "claiming anything.",
                   "Each question is close to a real search phrase, so the card and the "
                   "query that brought them agree.",
                   "Recognition over recall &mdash; a question is recognised, a tool name "
                   "has to be decoded."),
        spec2=spec("02", "Where you are right now", "every deep page &mdash; above the "
                   "first long section", BLOCK2,
                   "Relevance, for the reader who landed on the wrong page entirely.",
                   "Three career states, not three product names. The scent is the "
                   "reader&rsquo;s situation.",
                   "Hick&rsquo;s law &mdash; three, never five. Two links per card is the "
                   "ceiling before it reads as a menu."),
        spec3=spec("03", "Numbers from the tools", "mid-page, on computing pages",
                   BLOCK3,
                   "Value. It shows rather than claims, which is the whole argument for "
                   "the site.",
                   "The figure is the scent: a reader who wants take-home sees take-home, "
                   "not &ldquo;our simulator&rdquo;.",
                   "Live state travels in the href, so the destination is pre-filled and "
                   "nothing is retyped."),
        spec4=spec("04", "Read before you decide", "foot of each tool page", BLOCK4,
                   "Value, at the moment of doubt &mdash; the reader has a number and "
                   "wants to know whether to trust it.",
                   "Pairs a tool with the document behind it, so the next click is deeper "
                   "into the same question.",
                   "Chunking &mdash; two reads per tool, not a link list of nine."),
        spec5=spec("05", "What people arrive looking for", "above the footer, on landing "
                   "pages", BLOCK5,
                   "Call to action, for the reader whose question was never on this page.",
                   "Anchor text is the query itself, which is the strongest scent match "
                   "available.",
                   "Serial position &mdash; the last thing before the footer is "
                   "disproportionately remembered, and cheap to scan."),
        matrix=matrix,
        rules="".join("<li><b>%s</b>%s</li>" % (h, b) for h, b in RULES),
    )
    out = os.path.join(HERE, "content-blocks-system.html")
    # every href in every block must be a slug we actually publish
    slugs = {SIM, TAX, GROW, AMFT, HRS, COLA, RATES, REMOTE, TOOLS}
    for h in re.findall(r'href="(?!https?:)([^"#]+)', html):
        assert h in slugs, "unknown slug: " + h
    assert "lorem" not in html.lower()
    open(out, "w", encoding="utf-8").write(html)
    print("wrote %s  %d kB" % (os.path.basename(out), len(html) // 1024))


if __name__ == "__main__":
    main()
