#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Six ways the home page could open, drawn in the 37signals discipline.

WHY THIS EXISTS

`ops/information-architecture.html` section 03 proposed a home page built
around a five-card band - Thinking about it / In a program / Counting hours /
Licensed / Running a practice - sitting above three trust cards. That was
rejected on sight, and the objection is worth writing down properly because it
is the same objection that killed the first associates hero:

    A band of five equal cards is a menu of menus. It asks a stranger to
    classify themselves before anybody has told them what the site is, it
    expresses no opinion about where to start, and it is made of the same
    bordered-card texture as the eleven blocks under it - so it does not read
    as a front door at all. It reads as one more shelf.

The brief was: mock up more options, 37signals styled. So this document does
three things. It writes down what that house style actually consists of, in
moves rather than adjectives. It draws six home pages that apply it. And it
picks one, with the trade-off stated in each case rather than a preference
asserted.

WHAT IS BORROWED AND WHAT IS NOT

The layout discipline is borrowed: one column, few elements, big plain type,
prose instead of card grids, one clear thing to do, a stated point of view.
The typeface is not - the mockups keep this site's own headline face, because
the argument here is about structure and swapping the type at the same time
would make it impossible to tell which change did the work.

The one place the style is deliberately broken is the bottom of the page. The
37signals home page can end after four screens because it sells one product.
This site is 202 pages, most arrivals are cold from a search, and a large
plain index is genuinely useful to the half of the audience who have been
here before. So every option below keeps an index; they differ in what comes
before it.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DONOR = os.path.join(SITE, "ops", "stage-architecture.html")
OUT = os.path.join(SITE, "ops", "home-page-options.html")
UPDATED = "12 August 2026"

NAV = [("style", "The style"), ("wrong", "Why the band failed"),
       ("options", "Six options"), ("compare", "Side by side"),
       ("pick", "The recommendation"), ("else", "What else changes")]

EXTRA = """
.m37{font-family:var(--body);background:#fff;color:#16211B}
.m37 *{box-sizing:border-box}
.m37 .pad{padding:30px 30px 26px}
@media(max-width:700px){.m37 .pad{padding:22px 18px 20px}}
.m37 h2{font-family:var(--sans);font-weight:800;letter-spacing:-.028em;
  line-height:1.03;font-size:38px;margin:0 0 14px;color:#16211B;max-width:19ch}
@media(max-width:700px){.m37 h2{font-size:26px}}
.m37 h2 em{font-style:normal;color:var(--pine)}
.m37 .sub{font-size:17px;line-height:1.5;margin:0 0 18px;max-width:60ch;
  color:#333B35}
@media(max-width:700px){.m37 .sub{font-size:15px}}
.m37 .sub a{color:var(--pine);text-decoration:underline;text-underline-offset:3px}
.m37 .cta{display:inline-block;background:var(--ink);color:#fff;
  font-family:var(--sans);font-weight:800;font-size:16px;padding:12px 20px;
  text-decoration:none;border:0}
.m37 .cta.g{background:var(--pine)}
.m37 .aside{font-size:13px;color:var(--muted);margin:11px 0 0}
.m37 hr{border:0;border-top:1px solid #DFDACB;margin:26px 0}
.m37 .sig{font-family:var(--fig);font-weight:600;font-size:17px;
  line-height:1.55;max-width:58ch;margin:0 0 12px;color:#22302A}
.m37 .signoff{font-family:var(--mono);font-size:12px;color:var(--muted);
  margin:14px 0 0}

/* the sentence router - big text rows, no boxes */
.rt{margin:4px 0 0;border-top:1px solid #DFDACB}
.rt a{display:flex;align-items:baseline;gap:12px;justify-content:space-between;
  padding:14px 2px;border-bottom:1px solid #DFDACB;text-decoration:none;
  color:#16211B}
.rt .q{font-family:var(--sans);font-weight:800;font-size:23px;line-height:1.12;
  letter-spacing:-.02em}
@media(max-width:700px){.rt .q{font-size:17px}}
.rt .n{font-family:var(--mono);font-size:11px;color:var(--muted);
  white-space:nowrap}
.rt a:hover .q{color:var(--pine)}

/* the plain index */
.ix{display:grid;gap:20px 34px}
@media(min-width:760px){.ix{grid-template-columns:1fr 1fr 1fr}}
.ix h5{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--muted);margin:0 0 7px;
  padding-bottom:5px;border-bottom:1px solid #DFDACB}
.ix ul{list-style:none;margin:0;padding:0}
.ix li{font-size:13.5px;line-height:1.5;margin:0 0 3px}
.ix li b{font-weight:600}
.ix li span{color:var(--muted)}

/* tool-first */
.tool{border:2px solid var(--ink);background:var(--cream);padding:16px 18px;
  margin:2px 0 0}
.tool .fr{display:grid;gap:10px;grid-template-columns:1fr 1fr}
.tool label{display:block;font-family:var(--mono);font-size:10px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--muted);
  margin-bottom:4px}
.tool .in{border:2px solid var(--ink);background:#fff;padding:8px 10px;
  font-family:var(--fig);font-weight:800;font-size:20px;color:var(--deep)}
.tool .out{margin-top:13px;border-top:2px solid var(--ink);padding-top:12px;
  display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.tool .big{font-family:var(--fig);font-weight:800;font-size:38px;
  color:var(--deep);line-height:1}
.tool .cap{font-size:13px;color:#39473F;max-width:34ch}

/* the two-up statement */
.two{display:grid;gap:26px}
@media(min-width:820px){.two{grid-template-columns:1.15fr .85fr;align-items:start}}
.two .rail{border-left:3px solid var(--gold);padding-left:16px}
.two .rail p{font-size:13.5px;line-height:1.5;margin:0 0 10px;color:#39473F}
.two .rail b{font-family:var(--sans);font-weight:800;display:block;
  font-size:14px;margin-bottom:2px;color:#16211B}

/* numbers stated as a sentence, not as stat cards */
.claim{font-family:var(--fig);font-weight:600;font-size:19px;line-height:1.45;
  max-width:52ch;margin:0;color:#22302A}
.claim b{font-weight:800;color:var(--deep)}

/* the ask */
.ask{border:2px solid var(--ink);background:var(--cream);padding:14px 16px;
  display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.ask .qq{font-family:var(--sans);font-weight:800;font-size:17px;flex:1 1 240px}
.ask .bx{flex:1 1 200px;border:2px solid var(--ink);background:#fff;
  padding:9px 11px;font-size:13px;color:var(--muted)}

/* document furniture */
.opt{border:2px solid var(--ink);background:var(--cream);
  box-shadow:6px 6px 0 var(--ink);padding:15px 17px;margin:26px 0 0}
.opt .top{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;
  margin-bottom:6px}
.opt .let{font-family:var(--fig);font-weight:800;font-size:27px;
  color:var(--pine);line-height:1}
.opt h3{margin:0;font-size:20px}
.opt .verdict{margin-left:auto;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.12em;text-transform:uppercase;border:2px solid var(--ink);
  padding:3px 8px;background:#fff}
.opt .verdict.yes{background:var(--pine);color:#fff;border-color:var(--pine)}
.opt .verdict.part{background:var(--gold)}
.opt .thesis{font-size:15px;margin:0 0 4px;max-width:74ch}
.tradeoff{display:grid;gap:11px;margin:13px 0 2px}
@media(min-width:820px){.tradeoff{grid-template-columns:1fr 1fr 1fr}}
.tradeoff div{border:2px solid var(--ink);background:#fff;padding:10px 12px}
.tradeoff .h{display:block;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.12em;text-transform:uppercase;margin-bottom:5px}
.tradeoff .works .h{color:var(--green)}
.tradeoff .costs .h{color:var(--red)}
.tradeoff .who .h{color:var(--pine)}
.tradeoff p{font-size:13px;margin:0;line-height:1.45;color:#39473F}
.moves{display:grid;gap:0;border:2px solid var(--ink);background:#fff;
  box-shadow:5px 5px 0 var(--ink);margin:14px 0}
.moves .row{display:grid;grid-template-columns:40px 1fr;
  border-top:1px solid var(--line)}
.moves .row:first-child{border-top:0}
.moves .n{background:var(--deep);color:var(--gold);font-family:var(--mono);
  font-size:12px;display:grid;place-items:center;font-weight:600}
.moves .b{padding:10px 13px}
.moves h4{font-size:15px;margin:0 0 3px}
.moves p{font-size:13.5px;margin:0;color:#39473F}
.moves .row.no .n{background:var(--red);color:#fff}
.grid6{overflow-x:auto;border:2px solid var(--ink);background:var(--cream);
  box-shadow:5px 5px 0 var(--ink);margin:14px 0}
.grid6 table{min-width:760px;margin:0}
.grid6 th{background:var(--deep)}
.grid6 td.c{text-align:center;font-family:var(--fig);font-weight:800;
  font-size:16px;color:var(--pine)}
.grid6 td.c.no{color:var(--line)}
.note{border-left:5px solid var(--gold);padding:2px 0 2px 16px;margin:16px 0}
.note p{font-size:14.5px;margin:0 0 6px}
code{font-family:var(--mono);font-size:12.5px;background:#fff;
  border:1px solid var(--line);padding:1px 5px}
@media(max-width:700px){
  .tool .fr{grid-template-columns:1fr}
  .ix{grid-template-columns:1fr}
}
"""

# --------------------------------------------------------------------- parts

INDEX_BLOCK = (
    '<div class="ix">'
    "<div><h5>Calculators</h5><ul>"
    "<li><b>Practice Simulator</b> <span>&mdash; what a practice pays you</span></li>"
    "<li><b>Tax &amp; Retirement</b> <span>&mdash; how much of the bill is optional</span></li>"
    "<li><b>Associate Job Advisor</b> <span>&mdash; is this placement worth taking</span></li>"
    "<li><b>Grow Your Practice</b> <span>&mdash; what a client is worth</span></li>"
    "<li><b>3,000 Hours</b> <span>&mdash; what is holding up your date</span></li>"
    "<li><b>Cost of Living</b> <span>&mdash; what a month costs</span></li>"
    "</ul></div>"
    "<div><h5>Money and tax</h5><ul>"
    "<li>Sole proprietor or corporation</li>"
    "<li>The S&#8209;corp payroll gap</li>"
    "<li>Estimated taxes, four dates</li>"
    "<li>Solo 401(k), SEP or SIMPLE</li>"
    "<li>What you can deduct</li>"
    "<li>The home office, both methods</li>"
    "</ul></div>"
    "<div><h5>Licensure</h5><ul>"
    "<li>Becoming an MFT in California</li>"
    "<li>BBS fees, 2026</li>"
    "<li>Continuing education</li>"
    "<li>The practicum year</li>"
    "<li>Supervision, unit by unit</li>"
    "</ul></div>"
    "<div><h5>Getting paid</h5><ul>"
    "<li>The California Therapy Rate Gap</li>"
    "<li>Insurance panels, and which are open</li>"
    "<li>What Medicare and Medi&#8209;Cal pay</li>"
    "<li>Headway, Alma or Grow, priced</li>"
    "<li>Superbills and good faith estimates</li>"
    "</ul></div>"
    "<div><h5>Running a practice</h5><ul>"
    "<li>Hiring your first associate</li>"
    "<li>Liability insurance, eight programs</li>"
    "<li>48 real discipline decisions</li>"
    "<li>SimplePractice, priced properly</li>"
    "<li>Working remotely, and the Board&rsquo;s answer</li>"
    "</ul></div>"
    "<div><h5>Training and jobs</h5><ul>"
    "<li>78 California MFT programs</li>"
    "<li>Every PsyD in the state</li>"
    "<li>All 58 county job portals</li>"
    "<li>What counties pay clinicians</li>"
    "<li>Loan forgiveness employers</li>"
    "</ul></div>"
    "</div>"
)

ROUTER_ROWS = [
    ("I am thinking about becoming a therapist.", "73 pages"),
    ("I am in a program, and practicum is coming.", "31 pages"),
    ("I am registered and counting my hours.", "20 pages"),
    ("I am licensed and seeing my own clients.", "19 pages"),
    ("I run a practice and want it to pay better.", "24 pages"),
]


def router(rows=None, cls=""):
    o = ['<div class="rt%s">' % cls]
    for q, n in (rows or ROUTER_ROWS):
        o.append('<a href="#"><span class="q">%s</span>'
                 '<span class="n">%s &rarr;</span></a>' % (q, n))
    o.append("</div>")
    return "".join(o)


TOOL_BLOCK = (
    '<div class="tool"><div class="fr">'
    '<div><label>Your session rate</label><div class="in">$200</div></div>'
    '<div><label>Sessions a week</label><div class="in">24</div></div>'
    "</div>"
    '<div class="out"><span class="big">$138,940</span>'
    '<span class="cap">is what reaches your bank account, after every '
    "running cost, self&#8209;employment tax and California income tax."
    "</span></div></div>"
)


def frame(url, inner, tall=False):
    return ('<div class="frame"><div class="bar"><span class="dot"></span>'
            '<span class="dot"></span><span class="dot"></span>'
            '<span class="url">therapistsupport.org%s</span></div>'
            '<div class="m37"><div class="pad">%s</div></div></div>'
            % (url, inner))


# ------------------------------------------------------------------ mockups

MOCK_A = (
    "<h2>Running a practice is a second job nobody trained you for.</h2>"
    '<p class="sub">This site works out the money side of a California '
    "therapy practice &mdash; what you keep, what you owe, what a client is "
    "worth, and what a job offer is really paying. Free, no account, and "
    "every figure carries the date it was last checked against its "
    "source.</p>"
    '<a class="cta" href="#">Start with what your practice pays you &rarr;</a>'
    '<p class="aside">Or read <a href="#">the whole index</a> &mdash; 202 '
    "pages, California only.</p>"
    "<hr>"
    '<p class="claim">Six calculators. <b>78</b> training programs compared. '
    "<b>58</b> county job portals checked by hand. <b>48</b> real discipline "
    "decisions read and summarized. Written by one licensed therapist in "
    "California, for the rest of us.</p>"
    "<hr>"
    + INDEX_BLOCK
)

MOCK_B = (
    "<h2>Everything a California therapist needs to work out the money.</h2>"
    '<p class="sub">Six free calculators and 202 pages of California-specific '
    "reference. Start where you are.</p>"
    + router() +
    '<p class="aside">Not sure? Most people start with one number: '
    "<a href=\"#\">what the practice actually pays you</a>.</p>"
    "<hr>"
    + INDEX_BLOCK
)

MOCK_C = (
    "<h2>What does your practice actually pay you?</h2>"
    '<p class="sub">Put in a rate and a caseload. Everything else on this '
    "site &mdash; the tax pages, the growth math, the eight-location "
    "comparison &mdash; picks up the same two numbers.</p>"
    + TOOL_BLOCK +
    '<p class="aside">Nothing you type leaves your browser. There is no '
    "account and no email box.</p>"
    "<hr>"
    "<h2 style=\"font-size:23px;max-width:30ch\">And when you want the rest "
    "of it.</h2>"
    + router() +
    "<hr>"
    + INDEX_BLOCK
)

MOCK_D = (
    "<h2>The California therapist&rsquo;s reference.</h2>"
    '<p class="sub">Everything on one page, so you can find the thing you '
    "came for. 202 pages, six calculators, California only, all free.</p>"
    + INDEX_BLOCK +
    "<hr>"
    '<p class="claim">Every dollar here is the output of a calculation you '
    "can follow, run on numbers you typed in. There are no illustrative "
    "figures.</p>"
)

MOCK_E = (
    "<h2>Nobody teaches therapists the business half.</h2>"
    '<p class="sig">I am a licensed therapist in California. Every number I '
    "needed to run a practice &mdash; what a fair rate is, what an associate "
    "job really pays, whether to incorporate, what insurance actually "
    "reimburses &mdash; I had to work out myself, from statutes and fee "
    "schedules and other people&rsquo;s guesses in Facebook groups.</p>"
    '<p class="sig">So I built the tools I wanted, and then I wrote down '
    "everything I checked. It is free, it asks for nothing, and every figure "
    "says where it came from and when it was last looked at. If a number here "
    "is wrong, <a href=\"#\">tell me</a> and I will fix it and say so on the "
    "changes page.</p>"
    '<p class="signoff">&mdash; Shawn, LMFT &middot; California</p>'
    '<a class="cta g" href="#">See what your practice pays you &rarr;</a>'
    "<hr>"
    + router() +
    "<hr>"
    + INDEX_BLOCK
)

MOCK_F = (
    "<h2>Running a practice is a second job nobody trained you for.</h2>"
    '<p class="sub">This site works out the money side of a California '
    "therapy practice &mdash; what you keep, what you owe, what a client is "
    "worth, and what a job offer is really paying. Free, no account, and "
    "every figure carries the date it was last checked against its "
    "source.</p>"
    '<a class="cta" href="#">Start with what your practice pays you &rarr;</a>'
    '<p class="aside">Written and checked by one licensed therapist in '
    "California. <a href=\"#\">Why this exists &rarr;</a></p>"
    "<hr>"
    "<h2 style=\"font-size:23px;max-width:34ch\">Or start where you "
    "are.</h2>"
    + router() +
    "<hr>"
    '<p class="claim">Six calculators. <b>78</b> training programs compared. '
    "<b>58</b> county job portals checked by hand. <b>48</b> real discipline "
    "decisions read and summarized. <b>$0</b>, and no email box.</p>"
    "<hr>"
    + INDEX_BLOCK +
    "<hr>"
    '<div class="ask"><span class="qq">Cannot find it? Ask, and the answer '
    'becomes a page.</span><span class="bx">Type your question&hellip;'
    "</span></div>"
)

OPTIONS = [
    ("A", "The statement", "yes-ish",
     "One sentence, one paragraph, one thing to do. Nothing else above the "
     "line.",
     MOCK_A,
     "It is the only option that tells a cold arrival what this is in the "
     "first four seconds, and the numbers land as a claim in a sentence "
     "rather than as four boxes nobody reads.",
     "It expresses no opinion about where a student should go versus a "
     "practice owner, so anybody who is not here for the money question has "
     "to scroll into the index and route themselves.",
     "The stranger from a search who has never heard of the site."),
    ("B", "The sentence router", "part",
     "Five first-person sentences in big type. No boxes, no descriptions, no "
     "chips.",
     MOCK_B,
     "It is the band&rsquo;s job done properly. A reader recognizes their own "
     "sentence instantly, the rows carry a page count so the size of what is "
     "behind each one is visible, and there is no card texture to compete "
     "with the shelves below.",
     "It still asks the reader to classify themselves before they have been "
     "told what the site is, which was the original objection. On its own it "
     "is a menu with better typography.",
     "The returning visitor, and anybody arriving with a stage in mind."),
    ("C", "Tool first", "no",
     "The calculator is the front door. Two inputs and one number, above "
     "everything else.",
     MOCK_C,
     "It is the most 37signals move on the page &mdash; show the product "
     "working instead of describing it &mdash; and it is honest about what "
     "most people came for.",
     "It is the associates-hero mistake again, one level up. It assumes an "
     "oriented arrival. Somebody who came from a search about supervision "
     "hours sees a money calculator and concludes they are in the wrong "
     "place. It also puts the site&rsquo;s heaviest widget in the critical "
     "rendering path.",
     "Somebody who was sent here by a colleague specifically for the "
     "simulator."),
    ("D", "The plain index", "part",
     "No marketing at all. A headline, one line, and the whole library "
     "typeset as a table of contents.",
     MOCK_D,
     "For the second visit it is the fastest home page possible, and it is "
     "the truest description of what this site is: a reference. It also "
     "gives every page an internal link from the root, which is worth "
     "something in search.",
     "A first arrival gets no reason to trust any of it and no sense of "
     "where to begin. A wall of 202 links reads as a link farm rather than "
     "as somebody&rsquo;s careful work.",
     "The returning reader who knows the page they want."),
    ("E", "The letter", "part",
     "A signed note in the first person explaining what this is, why it "
     "exists, and why it is free.",
     MOCK_E,
     "It answers the question every free site raises and none of them "
     "address &mdash; who made this and what do they want from me. For an "
     "audience trained to look for the sales pitch behind free advice, that "
     "is the single highest-value paragraph on the page. It is also the one "
     "thing no competitor can copy.",
     "It is slower. Two paragraphs of prose before anything actionable is a "
     "real cost on mobile, and a letter that opens the page makes the site "
     "feel like a blog rather than a set of tools.",
     "The skeptic, and anybody deciding whether to trust a number here."),
    ("F", "The recommendation", "yes",
     "A&rsquo;s opening, B&rsquo;s router underneath it, E&rsquo;s "
     "authorship compressed to one line, D&rsquo;s index at the bottom, and "
     "the question box last.",
     MOCK_F,
     "Each block answers exactly one question, in the order a stranger asks "
     "them: what is this, is it for me, who made it, what is in it, what if "
     "it is not here. Nothing is a card. The whole page is four decisions "
     "instead of eleven blocks.",
     "It is longer than a real 37signals page, and the index still has to be "
     "generated and kept honest as the library grows.",
     "Everybody, in the order they arrive."),
]

MOVES = [
    ("01", "Say the hardest true thing first", False,
     "The headline is a sentence with a verb and a point of view, not a "
     "category label. &ldquo;Running a practice is a second job nobody "
     "trained you for&rdquo; is already this site&rsquo;s best line and it "
     "is currently buried under the fold."),
    ("02", "One column, one decision per screen", False,
     "No two things side by side competing for the same click. The current "
     "page has three cards, then four situations, then four tools, then two "
     "field notes, then four toolkit tiles."),
    ("03", "Prose instead of cards", False,
     "Anything that is a claim gets written as a sentence. Cards are for "
     "things a reader will genuinely compare item by item &mdash; which is "
     "the shelves, not the pitch."),
    ("04", "Numbers in a sentence, not in a grid", False,
     "&ldquo;78 programs compared, 58 county portals checked by hand, 48 "
     "discipline decisions read&rdquo; is read. The same four figures in "
     "boxes are skipped as decoration."),
    ("05", "One primary action, and it is a verb", False,
     "Not &ldquo;Practice Simulator&rdquo;. &ldquo;Start with what your "
     "practice pays you.&rdquo;"),
    ("06", "Say who made it and what they want", False,
     "37signals signs its home page. A free site aimed at people who have "
     "been sold to by every other free site needs this more, not less."),
    ("07", "But do not drop the index", True,
     "This is where the style is broken on purpose. 37signals sells one "
     "product to a stranger; this site is a reference that half its readers "
     "have used before. Ending the page after four screens would make the "
     "second visit worse to save the first one a scroll."),
]


def build():
    donor = open(DONOR, encoding="utf-8").read()
    m = re.search(r"<style>([\s\S]*?)</style>", donor)
    if not m:
        sys.exit("ops/stage-architecture.html has no <style> block to inherit.")
    css = m.group(1) + EXTRA

    o = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<meta name="robots" content="noindex,nofollow">',
         "<title>Six home pages, in the 37signals discipline</title>",
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:'
         'opsz,wght@12..96,800&family=Fraunces:opsz,wght@9..144,600;9..144,800&'
         'family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;600;700&'
         'display=swap" rel="stylesheet">',
         "<style>%s</style></head><body>" % css]

    o.append('<header class="mast"><div class="wrap">'
             '<span class="lab">Working document &middot; %s &middot; '
             "after the five-card band was rejected</span>"
             "<h1>Six home pages, one column each.</h1>"
             "<p>The band of five stage cards was a menu of menus: it asked a "
             "stranger to classify themselves before anybody had told them "
             "what the site was, and it was built from the same bordered "
             "cards as the eleven blocks under it, so it did not read as a "
             "front door. These six are drawn in the 37signals discipline "
             "instead &mdash; <b>one column, big plain type, prose instead of "
             "grids, one thing to do</b> &mdash; with the trade&#8209;off "
             "written out rather than a preference asserted.</p>"
             '<div class="meta"><span class="chip">6 mockups</span>'
             '<span class="chip">1 recommended</span>'
             '<span class="chip">No page moves</span>'
             '<span class="chip">Replaces IA section 03</span></div>'
             "</div></header>" % UPDATED)

    o.append('<nav class="jump"><div class="wrap"><ul>')
    for h, t in NAV:
        o.append('<li><a href="#%s">%s</a></li>' % (h, t))
    o.append("</ul></div></nav>")
    o.append('<div class="wrap">')

    # ---------------------------------------------------------------- style
    o.append('<section id="style"><div class="kicker"><span class="n">01</span>'
             "<h2>What the style actually is</h2></div>")
    o.append('<p class="lede">Written as moves rather than adjectives, so it '
             "can be checked against a draft. Six of them apply here. The "
             "seventh is deliberately broken.</p>")
    o.append('<div class="moves">')
    for n, h, broken, p in MOVES:
        o.append('<div class="row%s"><div class="n">%s</div><div class="b">'
                 "<h4>%s</h4><p>%s</p></div></div>"
                 % (" no" if broken else "", n, h, p))
    o.append("</div>")
    o.append('<div class="note"><p><b>The typeface is not part of the '
             "proposal.</b> These mockups keep the site&rsquo;s own headline "
             "face. Changing the layout and the type in the same pass would "
             "make it impossible to tell which one did the work, and the type "
             "is not what failed.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # ---------------------------------------------------------------- wrong
    o.append('<section id="wrong"><div class="kicker"><span class="n">02</span>'
             "<h2>Why the band failed</h2></div>")
    o.append('<p class="lede">Worth writing down, because it is the same '
             "error as the first associates hero and it will come back "
             "otherwise.</p>")
    for h, p in [
        ("It is a menu of menus.",
         "Five cards, each holding a description, a &ldquo;start with&rdquo; "
         "link and an &ldquo;everything for this stage&rdquo; chip. That is "
         "fifteen destinations on the first screen and no opinion about any "
         "of them."),
        ("It asks the reader to classify themselves too early.",
         "Before a stranger will place themselves on a path, they need to "
         "believe the path leads somewhere. The band assumes belief that the "
         "page has not earned yet."),
        ("It has the same texture as everything under it.",
         "Bordered card, offset shadow, small caps label. Eleven blocks on "
         "the page look like that. A front door made of the same material as "
         "the shelves does not read as a front door."),
        ("Five equal cards is five equal recommendations.",
         "In practice most arrivals want one number, and the page already "
         "knows that &mdash; it says so, in a smaller paragraph, "
         "underneath."),
    ]:
        o.append("<h4 style=\"margin:14px 0 3px\">%s</h4><p>%s</p>" % (h, p))
    o.append("</section><hr class=\"rule\">")

    # -------------------------------------------------------------- options
    o.append('<section id="options"><div class="kicker">'
             '<span class="n">03</span><h2>Six options</h2></div>')
    o.append('<p class="lede">Each one is the whole home page, top to bottom, '
             "at desktop width. Every one of them keeps a full index at the "
             "bottom; they differ in what comes before it.</p>")
    lab = {"yes": "Recommended", "yes-ish": "Strong", "part": "Partly",
           "no": "Not recommended"}
    cls = {"yes": "yes", "yes-ish": "part", "part": "", "no": ""}
    for letter, name, verdict, thesis, mock, works, costs, who in OPTIONS:
        o.append('<div class="opt"><div class="top">'
                 '<span class="let">%s</span><h3>%s</h3>'
                 '<span class="verdict %s">%s</span></div>'
                 '<p class="thesis">%s</p></div>'
                 % (letter, name, cls[verdict], lab[verdict], thesis))
        o.append(frame("/", mock))
        o.append('<div class="tradeoff">'
                 '<div class="works"><span class="h">What it does well</span>'
                 "<p>%s</p></div>"
                 '<div class="costs"><span class="h">What it costs</span>'
                 "<p>%s</p></div>"
                 '<div class="who"><span class="h">Who it serves</span>'
                 "<p>%s</p></div></div>" % (works, costs, who))
    o.append("</section><hr class=\"rule\">")

    # -------------------------------------------------------------- compare
    o.append('<section id="compare"><div class="kicker">'
             '<span class="n">04</span><h2>Side by side</h2></div>')
    o.append('<p class="lede">Five questions a home page has to answer. A '
             "cross means the page answers it above the fold; a dash means "
             "it answers it eventually, or not at all.</p>")
    QS = ["What is this?", "Is it for me?", "Who made it?",
          "What is in it?", "What do I do now?"]
    SCORE = {
        "A": [1, 0, 1, 0, 1], "B": [1, 1, 0, 0, 0], "C": [0, 0, 0, 0, 1],
        "D": [1, 0, 0, 1, 0], "E": [1, 0, 1, 0, 1], "F": [1, 1, 1, 1, 1],
    }
    o.append('<div class="grid6"><table><thead><tr><th>Option</th>')
    for q in QS:
        o.append("<th>%s</th>" % q)
    o.append("<th>Screens to the index</th></tr></thead><tbody>")
    depth = {"A": "2", "B": "1", "C": "3", "D": "0", "E": "3", "F": "3"}
    for letter, name, verdict, _t, _m, _w, _c, _who in OPTIONS:
        o.append("<tr><td><b>%s</b> &mdash; %s</td>" % (letter, name))
        for v in SCORE[letter]:
            o.append('<td class="c%s">%s</td>'
                     % ("" if v else " no", "&#10003;" if v else "&mdash;"))
        o.append("<td>%s</td></tr>" % depth[letter])
    o.append("</tbody></table></div>")
    o.append('<p style="font-size:13.5px;color:#635E53;max-width:70ch">The '
             "column that matters most is the third one. Every free site "
             "answers the first two; almost none answer &ldquo;who made this "
             "and what do they want from me&rdquo;, and this audience has "
             "been sold to by all of them.</p>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- pick
    o.append('<section id="pick"><div class="kicker"><span class="n">05</span>'
             "<h2>The recommendation</h2></div>")
    o.append('<p class="lede">Ship <b>F</b>. It is four decisions long, and '
             "each one answers a different question, in the order a stranger "
             "asks them.</p>")
    o.append('<div class="two"><div>')
    for n, h, p in [
        ("01", "The statement, and one action",
         "The site&rsquo;s own best sentence, the paragraph that says what it "
         "does, and a single verb button. No cards, no figures, no chips."),
        ("02", "Then the router, as sentences",
         "Five first-person lines in big type, each with a page count. This "
         "is the band&rsquo;s job, done without card texture and placed after "
         "the reader has been told what the site is rather than before."),
        ("03", "Then the claim, in one sentence",
         "The four figures that prove the work is real, written as a "
         "sentence, not as a stat grid."),
        ("04", "Then the whole index",
         "Six columns of plain links. Fast for the second visit, and it "
         "gives every page a link from the root."),
        ("05", "And the question box last",
         "Whatever is not there yet becomes the next page. It belongs at the "
         "end, where somebody who did not find their thing actually is."),
    ]:
        o.append('<h4 style="margin:12px 0 3px">%s &middot; %s</h4><p>%s</p>'
                 % (n, h, p))
    o.append("</div>")
    o.append('<div class="rail"><b>What comes off the page</b>'
             "<p>The three trust cards become one sentence in the opening "
             "paragraph plus the authorship line. The four situation cards "
             "become the router. The four toolkit tiles and the two field "
             "notes go into the index. Eleven blocks become five.</p>"
             "<b>What does not change</b>"
             "<p>No page moves and no URL changes. Every link on the new home "
             "page already exists today.</p>"
             "<b>What is new work</b>"
             "<p>The index has to be generated from the library registry "
             "rather than hand-written, or it goes stale the first week. The "
             "question box needs the ask surface that is already queued.</p>"
             "</div></div>")
    o.append('<div class="note"><p><b>If only one thing ships, ship the '
             "opening.</b> The headline, the paragraph, the single button and "
             "the authorship line are half a day and they fix the actual "
             "complaint. The router and the index can follow.</p></div>")
    o.append("</section><hr class=\"rule\">")

    # ----------------------------------------------------------------- else
    o.append('<section id="else"><div class="kicker"><span class="n">06</span>'
             "<h2>What else changes</h2></div>")
    o.append('<p class="lede">The home page is not the only page that has '
             "this problem. Four consequences, in order of size.</p>")
    for h, p in [
        ("The five doors get the same opening.",
         "<code>/for/associates</code> is already close &mdash; statement, "
         "scope, figures, start here, shelf. What it does not have is the "
         "authorship line, and it leads with four figures rather than one "
         "sentence. The other four doors should be built to F&rsquo;s "
         "shape."),
        ("The trust cards move, they do not die.",
         "&ldquo;It computes, it doesn&rsquo;t opine&rdquo; is a real "
         "differentiator and it should not be deleted &mdash; it belongs on "
         "the about page and in one clause of the home paragraph, not in "
         "three boxes above the router."),
        ("The index needs a generator.",
         "A hand-written index of 202 pages is wrong within a month. It "
         "should be emitted from <code>mock/library/registry.json</code>, "
         "grouped by section, with a guard that fails the build if a live "
         "page is missing from it."),
        ("The &ldquo;you are here&rdquo; band is unaffected.",
         "That change is about leaf pages and it stands on its own. It gets "
         "easier if the home page router uses the same five sentences."),
    ]:
        o.append("<h4 style=\"margin:14px 0 3px\">%s</h4><p>%s</p>" % (h, p))
    o.append("</section>")

    o.append("</div>")
    o.append('<footer><div class="wrap"><p style="margin:0">Working document, '
             "not linked from anywhere on the site and not indexable. The six "
             "mockups are drawings, not live pages &mdash; none of the links "
             "in them go anywhere. Written %s.</p></div></footer>" % UPDATED)
    o.append("</body></html>")
    return "".join(o)


def main():
    print("home page options, 37signals discipline")
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
    if n != len(OPTIONS):
        print("GUARD: %d mockups, expected %d" % (n, len(OPTIONS)))
        bad += 1
    # Every option must render its own index, or the claim that they all keep
    # one is false on the page that makes it.
    if html.count('class="ix"') != len(OPTIONS):
        print("GUARD: %d indexes for %d options - one mockup dropped it"
              % (html.count('class="ix"'), len(OPTIONS)))
        bad += 1
    for needle, what in [
        ("a menu of menus", "the one-line diagnosis of the band"),
        ("second job nobody trained you for", "the site's own best sentence"),
        ("who made this", "the question the third column is about"),
        ("Ship <b>F</b>", "the actual recommendation"),
        ("does not change", "the no-page-moves assurance"),
    ]:
        if needle not in html:
            print("GUARD: %s is missing" % what)
            bad += 1

    import re as _re
    t = _re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html, flags=_re.I)
    t = _re.sub(r"<[^>]+>", " ", t)
    for w in ("programme", "counselling", "centre", "whilst", "amongst",
              "recognise", "organisation", "behaviour", "enquir",
              "fulfilment", "judgement"):
        if _re.search(r"\b%s" % w, t, _re.I):
            print("GUARD: %r - this site is written in American English" % w)
            bad += 1
    for m in _re.finditer(r"\bgates?\b", t, _re.I):
        print("GUARD: %r - that word was removed sitewide"
              % t[max(0, m.start() - 40):m.start() + 40].strip())
        bad += 1
    if 'name="robots" content="noindex' not in html:
        print("GUARD: working document must not be indexable")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d mockups, %d jump targets" % (n, len(NAV)))


if __name__ == "__main__":
    main()
