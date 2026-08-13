#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three Basecamp-flavored home pages, and the five pages behind each.

WHY A THIRD DESIGN DOCUMENT

`ops/house-style.html` settled the system - tinted paper, one accent, the six
path hues, one slab per page, the site's own Bricolage/Fraunces/Plex Mono
type. What it did not do is explore the home page itself. It drew one.

This draws three, and they are meant to be genuinely different arguments
about what the front door is for, not three arrangements of the same blocks:

  A  THE PRODUCT PAGE.  Leads with the tool, drawn as a real interface. The
     claim is "this thing works, here it is running." Basecamp's own marketing
     posture - show the product, then explain it.
  B  THE BENTO.         Leads with the six paths as a tiled grid, each tile
     carrying its own figure. The claim is "whatever you are, there is a room
     for you." Closest to Basecamp's "everything in one place" band.
  C  THE NUMBER.        Leads with one worked calculation drawn as a chart:
     $250,000 in, $138,940 out. The claim is "we do arithmetic, not advice."

Every one keeps the same welcome sentence, the same six paths, and the same
index, so the comparison is about structure rather than about copy.

ENTIRELY NEW STYLESHEET

`.bc2` is self-contained and shares nothing with the earlier documents. It is
written the way it would ship - tokens at the top, components below, no
dependency on the ops chrome except the browser-window frame.

THE INFOGRAPHICS

37signals draws its own product rather than photographing it, and its charts
are flat, few-colored and labelled in plain words. Four are drawn here in CSS
with no images and no libraries:

  1. The take-home waterfall  - gross, minus expenses, minus tax, net
  2. The path track           - six stops with a "you are here" marker
  3. The tool interface       - two inputs and one large answer
  4. The binding-requirement  - four bars where only one is the constraint
     chart

All four use real figures from the live site, because a chart with invented
numbers in a design document is how invented numbers reach production.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DONOR = os.path.join(SITE, "ops", "stage-architecture.html")
OUT = os.path.join(SITE, "ops", "home-basecamp-three.html")
UPDATED = "13 August 2026"

NAV = [("a", "A · The product page"), ("b", "B · The bento"),
       ("c", "C · The number"), ("assoc", "Associate entry"),
       ("dir", "Program directory"), ("content", "Content page"),
       ("email", "Email sign-up"), ("about", "About"), ("pick", "Which one")]

# The six, relabelled. WHAT WAS WRONG WITH THE OLD LABELS
#
# They were the taxonomy's names, not the reader's. "Deciding" is a gerund
# with no object. "The gap" means nothing to anybody who has not read the
# architecture document. "Counting hours" only parses if you already know
# about the 3,000 - which is precisely the knowledge a cold arrival does not
# have. Six labels that each need decoding is six decisions before the first
# decision.
#
# The fix is three fields where there was one, and it follows how people
# actually navigate: they match a SITUATION they would say out loud, confirm
# it with a CREDENTIAL or life-stage they hold, and choose on the OUTCOME
# they would get. So:
#
#   claim    - first person, present tense, something a reader would say
#   who      - the status, so somebody can confirm they are in the right room
#   gets     - what the path gives them, not how many pages it contains
#
# The page count moves to the quiet end of the row. It measures our inventory;
# it was never a reason to click.
PATHS = [
    ("01", "I am thinking about becoming a therapist",
     "Considering the career &middot; not yet applied",
     "What the degree costs, how long the license takes, and what the work "
     "actually pays", "73", "h1", "Deciding"),
    ("02", "I am in a master&rsquo;s program",
     "Student or trainee &middot; practicum ahead",
     "Finding a practicum site, the trainee hour rules, and getting to "
     "graduation without losing hours", "31", "h2", "In a program"),
    ("03", "I have graduated and I am waiting on my number",
     "Degree awarded &middot; registration pending",
     "The 90-day rule, Live Scan before you work, and why hours in this "
     "window vanish if the order is wrong", "4", "h3", "The gap"),
    ("04", "I am registered and building hours",
     "AMFT &middot; ASW &middot; APCC",
     "Which jobs count, what they pay, how to find a supervisor, and what "
     "really decides your license date", "21", "h4", "Counting hours"),
    # 5 and 6 were "Newly licensed" and "Running a practice", split on
    # tenure - first two years against everybody after. That boundary was
    # wrong twice over. It asked the reader to classify on a dimension nobody
    # thinks in ("am I in year two?"), and the content did not respect it:
    # rates, panels, entity choice and taxes serve both.
    #
    # The seam that is actually there is WHETHER ANYONE ELSE WORKS FOR YOU.
    # A reader knows the answer instantly, and it changes the law rather than
    # the emphasis - payroll and employer tax, supervision liability, and the
    # 4980.43.4 employment nexus all switch on at exactly that line. Every
    # page in row 06 is downstream of a second person existing.
    ("05", "I am licensed and it is just me",
     "LMFT &middot; LCSW &middot; LPCC &middot; solo practice",
     "What to charge, panels or private pay, sole proprietor or corporation, "
     "and filling the week", "19", "h5", "Solo practice"),
    ("06", "I have people working for me",
     "Employer &middot; supervisor &middot; group practice",
     "Hiring an associate and what one really costs, payroll and employer "
     "tax, supervision liability, and growth", "24", "h6", "Employer"),
]

# The .bc2 sheet used to live here as an 18 KB string. Rollout step 1
# lifted it into css/house.css - the real stylesheet, shipped unused
# until step 2 relies on it. This builder reads it back, so the design
# document and the shipped sheet are one file and cannot drift.
CSS = open(os.path.join(SITE, "css", "house.css"), encoding="utf-8").read()

BARS = [("#2F6FDB", 15), ("#BC3F86", 10), ("#B0730B", 18), ("#17864A", 12),
        ("#0E8FA8", 8)]


def logo():
    return ('<span class="lg"><span class="bars">%s</span>'
            "<span><span class=\"wm\">Therapist Support</span>"
            '<span class="sub">California &middot; free</span></span></span>'
            % "".join('<i style="background:%s;height:%dpx"></i>' % (c, h)
                      for c, h in BARS))


def nav(on=None):
    o = ['<div class="nav">%s<span class="sp"></span>' % logo()]
    for l in ["The six paths", "Calculators", "Library", "About"]:
        o.append('<a class="%s">%s</a>' % ("on" if l == on else "", l))
    o.append('<a class="btn">Open a calculator</a></div>')
    return "".join(o)


# ------------------------------------------------------------ infographics
def waterfall():
    rows = [("Gross revenue", "24 clients a week at $200", 250000, 100,
             "#3C7A64", ""),
            ("Running costs", "twelve categories, itemized", -41650, 17,
             "#B9C7BE", "neg"),
            ("Tax", "self-employment plus California", -69410, 28,
             "#B9C7BE", "neg"),
            ("Reaches your account", "after every cost and every tax",
             138940, 56, "", "")]
    o = ['<div class="wf">']
    for i, (lb, sub, amt, pct, color, cls) in enumerate(rows):
        net = " net" if i == len(rows) - 1 else ""
        sign = "&minus;" if amt < 0 else ""
        o.append('<div class="row%s"><div class="lb">%s<span>%s</span></div>'
                 '<div class="track"><i class="barr" style="width:%d%%;%s">'
                 '</i></div><div class="amt %s">%s$%s</div></div>'
                 % (net, lb, sub, pct,
                    "background:%s" % color if color else "", cls, sign,
                    format(abs(amt), ",d")))
    o.append("</div>")
    return "".join(o)


def track(here=4):
    """The track keeps the SHORT name, because a track is a diagram.

    A six-stop diagram cannot carry a nine-word first-person sentence at each
    stop and stay readable, so this is the one place the short label survives
    - and it survives only because the row list above it has already taught
    the reader what each one means. A diagram may use shorthand the page has
    defined; navigation may not.
    """
    o = ['<div class="track6">']
    for n, claim, who, gets, c, hue, short in PATHS:
        cur = int(n) == here
        o.append('<a style="color:var(--%s)">%s<span class="pin"></span>'
                 '<span class="st">%s</span><span class="c">%s</span></a>'
                 % (hue,
                    '<span class="here">You are here</span>' if cur else "",
                    short, who.split("&middot;")[0].strip()))
    o.append("</div>")
    return "".join(o)


def tool_ui():
    return ('<div class="ui"><div class="top"><i></i><i></i><i></i>'
            "<span>Practice Simulator</span></div>"
            '<div class="in"><div class="fields">'
            '<div><label>Your session rate</label>'
            '<div class="fld live">$200</div></div>'
            '<div><label>Sessions a week</label><div class="fld">24</div></div>'
            "</div>"
            '<div class="out"><span class="big">$138,940</span>'
            '<span class="cap">reaches your bank account, after every '
            "running cost and every tax.</span></div></div>"
            '<div class="strip">'
            "<div><b>$250,000</b><span>gross revenue</span></div>"
            "<div><b>$41,650</b><span>running costs</span></div>"
            "<div><b>$69,410</b><span>tax, $18,244 of it optional</span></div>"
            "</div></div>")


def bind_chart():
    rows = [("Total hours", 547, 3000, False),
            ("Supervised weeks", 19, 104, True),
            ("Individual or triadic weeks", 19, 52, False),
            ("Direct client hours", 402, 1750, False)]
    o = ['<div class="bind">']
    for name, have, need, hit in rows:
        pct = int(round(have / float(need) * 100))
        o.append('<div class="r%s"><div class="n">%s%s</div>'
                 '<div class="bar"><i style="width:%d%%"></i></div>'
                 '<div class="v">%s / %s</div></div>'
                 % (" hit" if hit else "", name,
                    '<span class="flag">binding</span>' if hit else "",
                    max(2, pct), format(have, ",d"), format(need, ",d")))
    o.append("</div>")
    return "".join(o)


def rows_paths():
    """Claim first, status second, outcome third, inventory last."""
    o = ['<div class="rows">']
    for n, claim, who, gets, c, hue, short in PATHS:
        o.append('<a class="%s"><span class="who">%s</span>'
                 '<span class="t">%s</span>'
                 '<span class="gets">%s</span>'
                 '<span class="c">%s guides &rarr;</span></a>'
                 % (hue, who, claim, gets, c))
    o.append("</div>")
    return "".join(o)


def bento():
    o = ['<div class="bento">']
    for n, claim, who, gets, c, hue, short in PATHS:
        o.append('<a class="%s"><span class="num">%s</span>'
                 '<span class="t">%s</span><span class="q">%s</span>'
                 '<span class="go">%s guides &rarr;</span></a>'
                 % (hue, who, claim, gets, c))
    o.append("</div>")
    return "".join(o)


IX = [("Calculators", ["Practice Simulator", "Tax &amp; Retirement",
                       "Associate Job Advisor", "Grow Your Practice",
                       "3,000 Hours", "Cost of Living"]),
      ("Money and tax", ["Sole proprietor or corporation",
                         "The S-corp payroll gap", "Estimated taxes",
                         "Solo 401(k), SEP or SIMPLE", "What you can deduct"]),
      ("Licensure", ["Becoming an MFT", "Finding a clinical supervisor",
                     "BBS fees, 2026", "Continuing education",
                     "The practicum year"]),
      ("Getting paid", ["The California Therapy Rate Gap", "Insurance panels",
                        "What Medicare and Medi-Cal pay",
                        "Headway, Alma or Grow", "Superbills and GFEs"]),
      ("Running a practice", ["Hiring your first associate",
                              "Liability insurance", "48 discipline decisions",
                              "SimplePractice, priced", "Working remotely"]),
      ("Training and jobs", ["78 California MFT programs",
                             "Every PsyD in the state",
                             "All 58 county job portals",
                             "What counties pay clinicians",
                             "Loan forgiveness employers"])]


def index():
    o = ['<div class="ix">']
    for h, items in IX:
        o.append("<div><h5>%s</h5><ul>%s</ul></div>"
                 % (h, "".join("<li>%s</li>" % i for i in items)))
    o.append("</div>")
    return "".join(o)


def news(t="One email when a number moves.",
         s="Six last year. Each one because a rule changed."):
    return ('<div class="news"><span class="t">%s<span class="fine" '
            'style="display:block;font-family:var(--body);font-weight:400;'
            'margin-top:4px">%s</span></span>'
            '<span class="in">you@example.com</span>'
            '<a class="btn">Subscribe</a></div>' % (t, s))


def made(said):
    return ('<div class="made"><span class="eb">How this is made</span>'
            "<p>%s</p>"
            '<p class="who">Written and checked by a licensed marriage and '
            "family therapist in California &middot; "
            '<a href="#">how corrections work &rarr;</a></p></div>' % said)


def foot():
    return ('<div class="ft"><div class="g">'
            '<div><span class="wm">Therapist Support</span>'
            '<span class="sub" style="font-family:var(--mn);font-size:9px;'
            'letter-spacing:.18em;text-transform:uppercase;color:#79A08F;'
            'display:block">California &middot; free</span>'
            '<p style="margin-top:14px;max-width:32ch">Free calculators and '
            "checked reference for California therapists. Every figure "
            "carries the date it was last checked against its source.</p>"
            "</div>"
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
            "<span>Nothing sold here</span></div></div>"
            % "".join("<a>%s</a>" % p[6] for p in PATHS))


def frame(url, inner):
    return ('<div class="frame"><div class="bar"><span class="dot"></span>'
            '<span class="dot"></span><span class="dot"></span>'
            '<span class="url">therapistsupport.org%s</span></div>'
            '<div class="bc2">%s</div></div>' % (url, inner))


WELCOME = ("The complete source for California therapists &mdash; the money, "
           "the license, the job, and the practice.")


# ------------------------------------------------------------- home pages
def home_a():
    return frame("/", nav() + '<div class="band"><div class="split">'
                 "<div><h1>Running a practice is a <span class=\"scr\">second "
                 "job</span> nobody trained you for.</h1>"
                 '<p class="lede">%s Free, checked, and California only.</p>'
                 '<p><a class="btn big">See what your practice pays you</a> '
                 '<a class="btn ghost big">Browse all 203 pages</a></p>'
                 '<p class="fine">No account. No email box. Nothing sold.</p>'
                 "</div>"
                 '<div class="toc" style="align-self:end"><b>What is '
                 "inside</b>"
                 '<a><b style="display:inline;font-family:var(--figs);'
                 'font-size:17px;color:var(--ink);letter-spacing:0">6</b> '
                 "calculators</a>"
                 '<a><b style="display:inline;font-family:var(--figs);'
                 'font-size:17px;color:var(--ink);letter-spacing:0">203</b> '
                 "checked pages</a>"
                 '<a><b style="display:inline;font-family:var(--figs);'
                 'font-size:17px;color:var(--ink);letter-spacing:0">58</b> '
                 "county portals</a>"
                 '<a><b style="display:inline;font-family:var(--figs);'
                 'font-size:17px;color:var(--ink);letter-spacing:0">$0</b> '
                 "forever</a></div></div></div>" % WELCOME
                 + '<div class="band tight">' + tool_ui()
                 + '<p class="fine" style="margin-top:14px">Two inputs. '
                   "Everything else on the site &mdash; the tax pages, the "
                   "growth math, the eight-location comparison &mdash; picks "
                   "up the same two numbers. <b>Nothing you type leaves your "
                   "browser.</b></p></div>"
                 + '<div class="band sunk"><span class="eb">Or start where '
                   "you are</span><h2>Which one of these is you right now?</h2>""<p class=\"fine\" style=\"font-size:16.5px;max-width:54ch;margin:-8px 0 26px\">Every page on this site is written for one of six moments. Pick the sentence that sounds like your week.</p>"
                 + rows_paths() + "</div>"
                 + '<div class="slab"><span class="eb">Why you can use these '
                   "numbers</span><h2>Every dollar here is the output of a "
                   "calculation you can follow.</h2>"
                   "<p>Run on numbers you typed in. No illustrative figures, "
                   "no worked examples standing in for your practice, and "
                   "when a threshold moves it is listed on a page rather than "
                   "<span class=\"mark\">quietly swapped in</span>.</p></div>"
                 + '<div class="band"><h2>Everything on the site.</h2>'
                 + index() + news() + made(
                     "Every number here was needed by somebody running a "
                     "California practice before it was published, and worked "
                     "out from statutes and fee schedules rather than from "
                     "anybody&rsquo;s guess.") + "</div>" + foot())


def home_b():
    return frame("/", nav(on="The six paths")
                 + '<div class="band"><h1>Whatever you are right now, there '
                   "is a room for it.</h1>"
                   '<p class="lede">%s Six paths, 203 checked pages, six free '
                   "calculators.</p></div>" % WELCOME
                 + '<div class="band tight">' + bento() + "</div>"
                 + '<div class="band sunk"><div class="split"><div>'
                   '<span class="eb">Most people start here</span>'
                   "<h2>What does your practice actually pay you?</h2>"
                   '<p class="fine" style="font-size:16px;max-width:46ch">One '
                   "rate and one caseload. Every other tool on the site picks "
                   "up the same two numbers, so you type them once.</p>"
                   '<p><a class="btn big">Open the simulator</a></p></div>'
                 + '<div>' + waterfall() + "</div></div></div>"
                 + '<div class="slab"><span class="eb">What this is</span>'
                   "<h2>The complete source, and it is free because it costs "
                   "almost nothing to run.</h2>"
                   "<p>No account, no email box on the tools, no course at "
                   "the end, and <span class=\"mark\">nothing sold "
                   "here</span>. If that ever changes it will be said here "
                   "first.</p></div>"
                 + '<div class="band"><h2>Everything on the site.</h2>'
                 + index() + news() + made(
                     "When a figure turns out to be wrong it is fixed and the "
                     "correction is listed, with its date, on the changes "
                     "page &mdash; including the embarrassing ones, of which "
                     "there have been three.") + "</div>" + foot())


def home_c():
    return frame("/", nav()
                 + '<div class="band"><span class="eb">A $250,000 practice, '
                   "worked all the way through</span>"
                   "<h1>You keep <span class=\"fig\" style=\"color:var(--pine)"
                   "\">$138,940</span> of it.</h1>"
                   '<p class="lede">%s This is what the arithmetic looks like '
                   "when somebody actually does it.</p>" % WELCOME
                 + waterfall()
                 + '<p style="margin-top:24px"><a class="btn big">Run it on '
                   'your own numbers</a> <a class="btn ghost big">See how it '
                   "is calculated</a></p></div>"
                 + '<div class="band sunk"><span class="eb">Where you are on '
                   "the path</span><h2>Six stages, and the site knows which "
                   "one you are in.</h2>" + track(here=0)
                 + '<p class="fine" style="margin-top:26px">Each stage is a '
                   "real legal status with different rules, different money "
                   "and a different question &mdash; not a marketing "
                   "persona.</p></div>"
                 + '<div class="slab"><span class="eb">The rule everything '
                   "follows from</span><h2>It computes, it doesn&rsquo;t "
                   "opine.</h2>"
                   "<p>Every dollar on this site is the output of a "
                   "calculation you can follow, run on numbers you typed in. "
                   "There are no illustrative figures, and "
                   "<span class=\"mark\">nothing you type leaves your "
                   "browser</span>.</p></div>"
                 + '<div class="band"><h2>Everything on the site.</h2>'
                 + index() + news() + made(
                     "The numbers a California practice runs on are not "
                     "published anywhere as a set. They were worked out one "
                     "at a time here, and every one shows its source.")
                 + "</div>" + foot())


# ------------------------------------------------------- the other surfaces
def page_assoc():
    return frame("/paths/counting-hours", nav(on="The six paths")
                 + '<div class="band" style="border-left:6px solid var(--h4)">'
                   '<span class="eb">Path 04 of six &middot; for AMFTs, ASWs '
                   "and APCCs</span>"
                   "<h1>You are counting toward 3,000.</h1>"
                   '<p class="lede">Twenty-one pages for this stage, every '
                   "figure with a named source and a date.</p>"
                   '<p><a class="btn big">Find out what is holding up your '
                   'date</a> <a class="btn ghost big">See all 21</a></p>'
                   "</div>"
                 + '<div class="band tight"><div class="card">'
                   '<span class="eb">The tool</span>'
                   "<h3>Four requirements run at once. Only one is usually "
                   "the constraint.</h3>" + bind_chart()
                 + '<p class="fine" style="margin:14px 0 0">The 3,000 is '
                   "almost never what decides your date. <b>The weeks "
                   "are.</b></p></div></div>"
                 + '<div class="band sunk"><h2>The three questions this room '
                   "is actually asking.</h2>"
                   '<div class="lst">'
                   '<div class="r"><div><span class="nm">&ldquo;547 hours and '
                   "nobody will hire me.&rdquo;</span>"
                   '<span class="mt">Where the jobs are, what they pay, and '
                   "which employers can lawfully bill for a pre-licensed "
                   'clinician</span></div><span class="kk">5 pages</span>'
                   "</div>"
                   '<div class="r"><div><span class="nm">&ldquo;How do I even '
                   "find a supervisor?&rdquo;</span>"
                   '<span class="mt">Every list that exists, checked &mdash; '
                   "and the rule that decides whether the one you find can "
                   'count your hours</span></div><span class="kk">2 pages'
                   "</span></div>"
                   '<div class="r"><div><span class="nm">&ldquo;Am I being '
                   "underpaid?&rdquo;</span>"
                   '<span class="mt">What associates are actually paid in LA '
                   "and the Bay, and what unpaid work really costs</span>"
                   '</div><span class="kk">4 pages</span></div></div></div>'
                 + '<div class="slab"><span class="eb">What differs by '
                   "registration</span><h2>If you are an ASW, two rules apply "
                   "that nobody else has.</h2>"
                   "<p><b>1,700 of your 3,000 hours</b> must be supervised by "
                   "an LCSW, and <b>13 of your 52</b> individual or triadic "
                   "weeks must be too. They are independent &mdash; meeting "
                   "one does not meet the other.</p></div>"
                 + '<div class="band"><h2>Everything for this stage.</h2>'
                 + index() + news("Told when the Board moves a rule.",
                                  "It changes these every couple of years.")
                 + "</div>" + foot())


def page_dir():
    o = [nav()]
    o.append('<div class="band"><span class="eb">Directory &middot; all 78 '
             "checked, August 2026</span>"
             "<h1>Every MFT program in California, on one question.</h1>"
             '<p class="lede">Whose job is it to find your practicum site? '
             "Twenty-nine programs publish nothing at all.</p>"
             '<div class="chips"><span class="on">All 78</span>'
             "<span>Guarantees placement</span><span>Places you</span>"
             "<span>Assists</span><span>You find your own</span>"
             "<span>Not published</span><span>Under $60,000</span>"
             "<span>Online</span></div>"
             '<div class="tbl"><table>'
             "<tr><th>Program</th><th>Who finds your site</th>"
             "<th>Practicum hours</th><th>Tuition</th></tr>"
             "<tr><td><b>CSU Fresno</b><br><span class=\"fine\">Fresno "
             "&middot; in person</span></td><td>Places you</td>"
             "<td>700 client hours</td><td>$37,800</td></tr>"
             "<tr><td><b>Alliant International</b><br>"
             "<span class=\"fine\">Six campuses</span></td>"
             "<td>You find your own<br><span class=\"fine\">&ldquo;you are "
             "fully responsible in securing your practicum site&rdquo;</span>"
             "</td><td>Not published</td><td>$99,180</td></tr>"
             "<tr><td><b>Pepperdine</b><br><span class=\"fine\">Los Angeles "
             "&middot; hybrid</span></td><td>Assists</td>"
             "<td>750 client hours</td><td>$118,440</td></tr>"
             "<tr><td><b>CIIS</b><br><span class=\"fine\">San Francisco"
             "</span></td><td>Assists</td><td>600 client hours</td>"
             "<td>$86,940</td></tr></table></div>"
             '<p class="fine" style="margin-top:14px">Every quote is the '
             "program&rsquo;s own words, taken from its own page, with the "
             "date it was read.</p></div>")
    o.append('<div class="slab"><span class="eb">The finding</span>'
             "<h2>Twenty-nine of seventy-eight publish nothing about who "
             "finds your site.</h2>"
             "<p>Ten say plainly that it is yours to find. Three describe "
             "themselves as assisting and then say, further down the same "
             "page, that the student is responsible &mdash; which is why the "
             "table above prints <span class=\"mark\">each program&rsquo;s "
             "own words</span> beside its category.</p></div>")
    o.append('<div class="band">' + news() + "</div>")
    o.append(foot())
    return frame("/mft-programs-california", "".join(o))


def page_content():
    return frame("/finding-a-clinical-supervisor-california", nav()
                 + '<div class="band"><div class="split"><div>'
                   '<p class="eb">Licensure &middot; checked 13 August 2026 '
                   "&middot; 30 sources</p>"
                   "<h1>Finding a clinical supervisor in California.</h1>"
                   '<p class="lede">The Board does not certify supervisors '
                   "and keeps no roster, so this is where the lists actually "
                   "are.</p>"
                   "<p>California licenses 165,000 people and publishes a "
                   "list of exactly <span class=\"scr\">zero</span> "
                   "supervisors. What exists instead is nine county chapter "
                   "directories, one statewide association list with no "
                   "contact details on it, and two commercial products.</p>"
                   '<p class="pull">In a private practice, you cannot simply '
                   "hire your own supervisor.</p>"
                   "<p>The statute requires them to be <b>employed by, "
                   "contracted by, or an owner of your employer</b>. Those "
                   "are the three permitted statuses, and weeks under a "
                   "privately retained supervisor are not creditable.</p>"
                   '<div class="aside"><p><b>There is a lawful route, and it '
                   "needs your employer to act.</b> The employer contracts "
                   "the supervisor, and a written oversight agreement is "
                   "signed before supervision starts &mdash; not within any "
                   "grace period.</p></div>"
                   "<h2>What it costs</h2>"
                   "<p>No fee schedule exists. The Board&rsquo;s own 2024 "
                   "survey found <b>18% of 3,168 respondents paid at "
                   "all</b>, and of those, <b>35% paid more than $300 a "
                   "month</b>.</p></div>"
                   '<div class="toc"><b>On this page</b>'
                   '<a class="on">Where the lists are</a>'
                   "<a>The private-practice trap</a>"
                   "<a>Whether they may supervise you</a>"
                   "<a>What the week looks like</a><a>What it costs</a>"
                   "<a>Three deadlines</a><a>What to ask</a><a>Sources</a>"
                   '<div class="card" style="margin-top:20px;padding:15px 16px">'
                   '<span class="eb" style="margin-bottom:8px">In this stage'
                   "</span>"
                   '<p style="margin:0;font-size:14.5px"><span style="display:'
                   'inline-block;width:10px;height:10px;border-radius:3px;'
                   'background:var(--h4);margin-right:7px"></span>'
                   "Counting hours &mdash; 21 pages</p></div></div>"
                   "</div></div>"
                 + '<div class="slab"><span class="eb">The one thing to take '
                   "away</span><h2>A privately retained supervisor is not a "
                   "supervisor, in a private practice.</h2>"
                   "<p>Somebody who spends three months paying a supervisor "
                   "they found themselves, at a practice that never "
                   "contracted them, has <span class=\"mark\">bought "
                   "nothing</span>. Ask before the first session, not at the "
                   "end.</p></div>"
                 + '<div class="band">' + news()
                 + made("Every statute on this page is linked to its own "
                        "text, so none of it has to be taken on trust.")
                 + "</div>" + foot())


def page_email():
    o = [nav()]
    o.append('<div class="band"><div class="split"><div>'
             "<h1>One email when a number <span class=\"scr\">moves</span>."
             "</h1>"
             '<p class="lede">The Board changes a fee, the IRS moves a '
             "threshold, a payer re-prices a code. That is when this sends. "
             "Not weekly, not a digest, not a funnel.</p>"
             '<div class="card"><h3>What actually gets sent</h3>'
             '<div class="lst">'
             '<div class="r"><div><span class="nm">A rule changed</span>'
             '<span class="mt">What it does to your arithmetic, the source, '
             "and which page moved</span></div></div>"
             '<div class="r"><div><span class="nm">A new calculator</span>'
             '<span class="mt">Once, when one lands</span></div></div>'
             '<div class="r"><div><span class="nm">A correction</span>'
             '<span class="mt">When something here turns out to be wrong. '
             "These go out even when it is embarrassing</span></div></div>"
             "</div>"
             '<div class="news" style="margin:20px 0 0;border-bottom:0;'
             'padding-bottom:0"><span class="in">you@example.com</span>'
             '<a class="btn">Subscribe</a></div>'
             '<p class="fine" style="margin:14px 0 0">Unsubscribe link in '
             "every one. Never sold, never rented, never used for anything "
             "else.</p></div>"
             '<h2 style="margin-top:36px">Everything sent last year.</h2>'
             '<p class="fine" style="max-width:56ch;font-size:16px">Six '
             "emails. The claim is a number rather than an adjective, so you "
             "can check it before you subscribe.</p>"
             '<div class="lst">')
    for d, t in [("14 Jul 2026", "BBS fees halved &mdash; what it saves, and "
                                 "the 2030 reversion"),
                 ("02 May 2026", "The 2026 brackets, and the one that changes "
                                 "S-corp math"),
                 ("19 Mar 2026", "Correction: a tuition figure was wrong for "
                                 "six days"),
                 ("28 Jan 2026", "Medi-Cal rates re-priced per code"),
                 ("11 Nov 2025", "New: the Associate Job Advisor"),
                 ("03 Sep 2025", "Supervision agreement form renumbered")]:
        o.append('<div class="r"><div><span class="nm">%s</span></div>'
                 '<span class="kk">%s</span></div>' % (t, d))
    o.append("</div></div>"
             '<div class="toc"><b>Why trust the list</b>'
             '<p class="fine" style="margin:0 0 14px">No tracking pixel. The '
             "email does not know whether you opened it.</p>"
             '<p class="fine" style="margin:0 0 14px">No segmentation, no '
             "drip sequence, no re-engagement campaign.</p>"
             '<p class="fine" style="margin:0">Nothing is sold here, so there '
             "is nothing to sell you later.</p></div></div></div>")
    o.append('<div class="slab"><span class="eb">The promise, as a number'
             "</span><h2>Six emails in twelve months.</h2>"
             "<p>Every one because a figure on this site changed. You can "
             "read all six above <span class=\"mark\">before you "
             "subscribe</span>, which is not a thing most newsletters let you "
             "do.</p></div>")
    o.append(foot())
    return frame("/updates", "".join(o))


def page_about():
    o = [nav(on="About")]
    o.append('<div class="band"><span class="eb">About</span>'
             "<h1>Who made this, and what they want from you.</h1>"
             '<p class="lede">Nothing. No email box on the tools, no account, '
             "no course at the end, and no affiliate link on any figure that "
             "matters.</p>"
             '<div class="lst" style="max-width:74ch">')
    for q, a in [("Who made it?",
                  "A licensed marriage and family therapist in California, "
                  "who needed these numbers first and could not find them."),
                 ("What do they want?",
                  "Nothing is sold here. There is a newsletter, it sends "
                  "about six times a year, and every past issue is readable "
                  "before you give it an address."),
                 ("Why believe a figure?",
                  "Because it says where it came from and when it was last "
                  "checked, and because the ones that moved are listed on a "
                  "page instead of being quietly replaced."),
                 ("What if it is wrong?",
                  "Say so. It gets fixed, and the correction is listed with "
                  "its date &mdash; including the embarrassing ones, of "
                  "which there have been three.")]:
        o.append('<div class="r"><div><span class="nm">%s</span>'
                 '<span class="mt">%s</span></div></div>' % (q, a))
    o.append("</div></div>")
    o.append('<div class="slab"><span class="eb">The rule everything follows '
             "from</span><h2>It computes, it doesn&rsquo;t opine.</h2>"
             "<p>Every dollar here is the output of a calculation you can "
             "follow, run on numbers you typed in. No illustrative figures, "
             "no worked examples standing in for your practice, and "
             "<span class=\"mark\">nothing you type leaves your "
             "browser</span>.</p></div>")
    o.append('<div class="band"><div class="bento" style="grid-template-'
             'columns:repeat(3,1fr)">'
             '<div class="card"><h4>What this is</h4><p class="fine" '
             'style="margin:0">Six calculators and 203 checked pages, '
             "California only. For LMFTs, LCSWs, LPCCs, psychologists and "
             "registered associates.</p></div>"
             '<div class="card"><h4>What it is not</h4><p class="fine" '
             'style="margin:0">Legal, tax or career advice. A directory that '
             "takes payment for a listing. A lead magnet for something "
             "else.</p></div>"
             '<div class="card"><h4>How it is paid for</h4><p class="fine" '
             'style="margin:0">It is not. It costs very little to run, and '
             "that is the whole business model.</p></div></div></div>")
    o.append('<div class="band tight">' + news() + "</div>")
    o.append(foot())
    return frame("/about", "".join(o))


HOMES = [
    ("a", "A", "The product page",
     "Leads with the tool, drawn as a real working interface, then the paths "
     "as rows. The claim is &ldquo;this thing works &mdash; here it is "
     "running.&rdquo;",
     "It is the most Basecamp move available: show the product instead of "
     "describing it. A visitor sees a real answer in a real number before "
     "any navigation, and the two-input screenshot is the single clearest "
     "explanation of what the site does.",
     "It assumes the money question is the right entry for everybody, which "
     "is wrong for a student and wrong for somebody searching about "
     "supervision hours. The paths are below the fold.", "win", home_a),
    ("b", "B", "The bento",
     "Leads with the six paths as a tiled grid, each carrying its own hue and "
     "count, with the simulator and the waterfall chart below.",
     "The most honest expression of the architecture &mdash; the site really "
     "is six rooms, and this shows all six at once with a description rather "
     "than making you scroll a list. Tiles work far better than rows for "
     "six items of unequal size.",
     "A grid of six equal tiles expresses no opinion about where to start, "
     "which is the objection that killed the original five-card band. It "
     "also puts the strongest asset &mdash; the calculator &mdash; on the "
     "second screen.", "", home_b),
    ("c", "C", "The number",
     "Leads with one worked calculation drawn as a waterfall: $250,000 in, "
     "$138,940 out, with the paths as a horizontal track underneath.",
     "It states the site&rsquo;s entire value proposition as a picture in "
     "under two seconds, and it is the only one of the three that a stranger "
     "can evaluate without clicking. The path track reads as a journey "
     "rather than a menu, which is what the six actually are.",
     "It leads with somebody else&rsquo;s numbers, and a reader whose "
     "practice looks nothing like $250,000 may bounce off it. The track is "
     "also the hardest of the three components to make work on a phone.",
     "", home_c),
]

PAGES = [("assoc", "The associate entry page", page_assoc),
         ("dir", "The program directory", page_dir),
         ("content", "A standard content page", page_content),
         ("email", "The email sign-up", page_email),
         ("about", "About", page_about)]


def build():
    donor = open(DONOR, encoding="utf-8").read()
    m = re.search(r"<style>([\s\S]*?)</style>", donor)
    if not m:
        sys.exit("ops/stage-architecture.html has no <style> block")
    css = m.group(1) + CSS

    o = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<meta name="robots" content="noindex,nofollow">',
         "<title>Three Basecamp home pages, and the site behind them</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+'
         'Grotesque:opsz,wght@12..96,700;12..96,800&family=Fraunces:opsz,'
         'wght@9..144,600;9..144,800&family=IBM+Plex+Mono:wght@400;600&'
         'family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">',
         "<style>%s</style></head><body>" % css]

    o.append('<header class="mast"><div class="wrap">'
             '<span class="lab">Working document &middot; %s</span>'
             "<h1>Three front doors, one site.</h1>"
             "<p>Three Basecamp-flavored home pages that argue different "
             "things about what a front door is for, plus the five pages "
             "behind them &mdash; the associate entry page, the program "
             "directory, a content page, the email sign-up and about. "
             "<b>An entirely new stylesheet</b>, written the way it would "
             "ship, and <b>four infographics drawn in CSS</b> with the "
             "site&rsquo;s real figures.</p>"
             '<div class="meta"><span class="chip">3 home pages</span>'
             '<span class="chip">5 pages behind them</span>'
             '<span class="chip">4 infographics</span>'
             '<span class="chip">New stylesheet</span></div>'
             "</div></header>" % UPDATED)

    o.append('<nav class="jump"><div class="wrap"><ul>')
    for h, t in NAV:
        o.append('<li><a href="#%s">%s</a></li>' % (h, t))
    o.append("</ul></div></nav>")
    o.append('<div class="wrap">')

    for i, (anchor, letter, name, thesis, up, dn, tag, fn) in enumerate(
            HOMES, start=1):
        o.append('<section id="%s"><div class="kicker">'
                 '<span class="n">%02d</span><h2>%s &mdash; %s</h2></div>'
                 % (anchor, i, letter, name))
        o.append('<div class="optcard"><div class="top">'
                 '<span class="let">%s</span><h3>%s</h3>'
                 '<span class="tag %s">%s</span></div><p>%s</p>'
                 '<div class="pros"><div class="up"><span class="h">What it '
                 'does well</span><p>%s</p></div><div class="dn">'
                 '<span class="h">What it costs</span><p>%s</p></div></div>'
                 "</div>"
                 % (letter, name, tag,
                    "Recommended" if tag else "Alternative", thesis, up, dn))
        o.append(fn())
        o.append("</section><hr class=\"rule\">")

    for j, (anchor, title, fn) in enumerate(PAGES, start=4):
        o.append('<section id="%s"><div class="kicker">'
                 '<span class="n">%02d</span><h2>%s</h2></div>'
                 % (anchor, j, title))
        o.append(fn())
        o.append("</section><hr class=\"rule\">")

    o.append('<section id="pick"><div class="kicker">'
             '<span class="n">09</span><h2>Which one</h2></div>')
    o.append('<p class="lede">A, with one component taken from C.</p>')
    o.append('<div class="note"><p><b>Ship A, and put C&rsquo;s waterfall '
             "inside the tool card.</b> A wins because it shows the product "
             "working before it explains anything, which is the whole "
             "Basecamp argument and the thing this site can do that no "
             "competitor can. What A is missing is the picture of the answer "
             "&mdash; the tool screenshot shows one number, and C&rsquo;s "
             "waterfall shows where it came from. Put the waterfall directly "
             "under the two inputs and A carries both.</p>"
             "<p><b>B is the one to keep in reserve.</b> If the six paths "
             "become the primary navigation and traffic starts arriving on "
             "them rather than on the home page, the bento is the better "
             "front door and it can be swapped in without touching anything "
             "else.</p></div>")
    o.append('<div class="note"><p><b>On the infographics.</b> All four are '
             "CSS &mdash; no images, no chart library, no build step. That "
             "matters more than it sounds: a chart that is HTML can carry "
             "real numbers out of the same data the pages are built from, so "
             "it cannot drift from the figures beside it. A PNG of a chart "
             "always eventually disagrees with the page it sits on.</p>"
             "</div>")
    o.append("</section>")

    o.append("</div>")
    o.append('<footer><div class="wrap"><p style="margin:0">Working document, '
             "not linked from the site and not indexable. The mockups are "
             "drawings; no link in them goes anywhere, and every figure in "
             "them is one of the site&rsquo;s real ones. Written %s.</p>"
             "</div></footer>" % UPDATED)
    o.append("</body></html>")
    return "".join(o)


def main():
    print("three Basecamp home pages, and the site behind them")
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
    if n != len(HOMES) + len(PAGES):
        print("GUARD: %d mockups, expected %d" % (n, len(HOMES) + len(PAGES)))
        bad += 1

    # One slab per page, still. It is the rule that carries the design.
    for _a, _l, _nm, _t, _u, _d, _g, fn in HOMES:
        if fn().count('class="slab"') != 1:
            print("GUARD: a home page carries more than one slab")
            bad += 1
    for _a, title, fn in PAGES:
        if fn().count('class="slab"') != 1:
            print("GUARD: %s carries %d slabs, the rule is one"
                  % (title, fn().count('class="slab"')))
            bad += 1

    # All four infographics have to be present, or "four infographics" is a
    # claim the document does not keep.
    for cls, what in [("wf", "the take-home waterfall"),
                      ("track6", "the six-stop path track"),
                      ("ui", "the tool interface"),
                      ("bind", "the binding-requirement chart")]:
        if 'class="%s"' % cls not in html:
            print("GUARD: %s is defined and never drawn" % what)
            bad += 1

    # The stylesheet must be self-contained: no .hs or .mk leaking in from the
    # earlier documents, which is how three design systems become one mess.
    for stale in ('class="hs"', 'class="mk '):
        if stale in html:
            print("GUARD: %r - this document has its own stylesheet" % stale)
            bad += 1

    # Every path must appear as its CLAIM, not as its short name. The short
    # name is a filing label; if it is the only thing on the page, the
    # navigation is asking the reader to decode six words before choosing.
    for _num, claim, who, gets, _c, _h, short in PATHS:
        for field, what in ((claim, "the first-person claim"),
                            (who, "the status line"),
                            (gets, "what the reader gets")):
            if field not in html:
                print("GUARD: %s for %r is missing" % (what, short))
                bad += 1

    # And the old shorthand must not be the loud thing anywhere. A row whose
    # headline is "Deciding" is the failure this revision exists to fix.
    for _num, _claim, _who, _gets, _c, _h, short in PATHS:
        if '<span class="t">%s</span>' % short in html:
            print("GUARD: %r is being used as a headline again" % short)
            bad += 1

    # The author's name stays off the page.
    for nm in ("Shawn", "Walters"):
        if nm in html:
            print("GUARD: %r appears - no personal name on these pages" % nm)
            bad += 1

    if "Bricolage" not in html or "Fraunces" not in html:
        print("GUARD: the site's own display and figure faces are not in use")
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
    print("  guards ok - %d pages, %d home options, 4 infographics"
          % (n, len(HOMES)))


if __name__ == "__main__":
    main()
