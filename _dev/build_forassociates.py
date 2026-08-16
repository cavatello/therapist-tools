#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/for/associates - the first stage door, built as the Ledger.

WHO ACTUALLY ARRIVES HERE, WHICH THE FIRST VERSION GOT WRONG

The first build opened with "One bar. Four requirements. Nothing you type here leaves
this browser." That headline describes a widget. It was written for somebody
arriving from a link posted in a group - already oriented, wanting the tool -
and that is not who mostly arrives. Most arrive cold, from a search for one
specific question, and a cold arrival needs to learn three things in the first
screen:

    am I in the right place, is this the whole thing, and where do I start

The old hero answered none of them. Two of its four blocks were about privacy,
which is a trust signal and not a reason to stay, and its four figures were the
statute - 3,000, 1,750, 500, 104 - numbers a registered associate already
knows. Nothing said "everything for this stage, in one place", so the page read
as a single calculator rather than a hub over twenty pages.

So the order is now: what this is and how much of it there is, then the four
places most people start, then the tool, then the shelf grouped by subject.
The privacy promise sits with the tool, where it is the answer to an actual
question, rather than in the headline where it displaced the offer.

WHY THIS DESIGN AND NOT THE OTHER TWO

Three variants were drawn for this door. The Desk opens with six live tiles;
the Three Questions opens with the loudest threads verbatim; the Ledger opens
with one horizontal bar and the sub-totals marked. The Ledger won on a single
constraint: a large share of this traffic arrives on a phone, from a link
posted in a group, and one bar with the short requirement marked survives a 390px first
screen where six tiles do not. The other two are not discarded - the Desk's
detail is what the bar expands into, and the Questions sit directly beneath
it.

THE WORD "GATE" IS GONE, AND THE REASON IS NOT ONLY THE JARGON

This page used to call the four requirements "gates". Two things were wrong
with that. Nobody outside the person who wrote it knows what a gate is meant
to be. And it framed the 3,000 as the thing you are working toward, when the
3,000 is almost never what decides anybody's date - a caseload of adult
individuals closes the total long before it produces 500 relational hours, and
the 104 weeks bind anyone moving quickly.

So they are requirements, they are named that, and the page says plainly which
one usually runs out last rather than implying it is the big number at the
top.

NOTHING IS SENT ANYWHERE, AND THAT IS SAID IN THE HERO

Every figure is computed in the browser. There is no storage, no share hash,
no query string and no network call - which matters twice over, because the
site's analytics guard fails the build if tracking can read a typed value, and
because the promise is worth nothing if a reader has to find it in the footer.

THE SHELF IS BUILT FROM stage_note, NOT FROM TITLES

Each page below is annotated with what it tells THIS reader, at THIS stage,
read from the registry field written by _dev/stage_tags.py. That is the whole
difference between a stage hub and a re-listed topic hub, and a guard here
refuses to print a page that has no note.

REBUILT 15 AUG 2026 TO 3C "THE LEDGER", DECLUTTERED TO THE A2 VERDICT

The user's A2 ruling: the door CONCEPT is right, the execution was "messy,
cluttered, so much going on". So this page now renders P2's own
recommendation for door 3 - 3C The Ledger, with 3A's tiles as the EXPANDED
state after input and 3B's questions directly below the bar - held to the
A2 standard: ONE dark band (the hero), white cards on paper, one accent
(gold, on the requirement people miss), generous space, fewer simultaneous
elements per viewport. Concretely, against the first build:

  - the hero lost the four-figure stat grid (each figure survives in the
    body: the guide count heads the shelf, the 58 counties and 165,000
    licensees are on their shelf cards, free/no-account joined the privacy
    line). Per 3C, the privacy line sits IN the hero, not with the tool.
  - the ledger comes first - the bar is the page, per the mockup - and its
    four requirement tiles are hidden until a figure is typed, so the
    empty state is one quiet bar instead of four dashes (3A's own critique).
  - the requirements panel and the four start doors are white cards now,
    not extra dark blocks; the hero is the page's only dark band.
  - the shelf annotations (hand-written, per stage) kept, with room.

This page carries NO inline CSS of its own: body.bcf + css/house-for.css
own the whole design (_dev/family_for.py converts and guards it, running
LAST in ship.py). This page is the TEMPLATE the other three doors copy.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "for/associates.html"
# THE DONOR IS A ROOT PAGE, AND THE BUILDER MOVES ITS LINKS DOWN A LEVEL.
#
# Two things pull in opposite directions here. `pagekit.chrome_parts` only
# recognises stylesheet links written as `href="css/<hash>.css"`, so the donor
# has to be a page at the site root - borrowing from a topic hub yields no
# stylesheets at all and the page ships unstyled. But a root page's chrome
# links are bare, and `contact.html` resolves to `/for/contact.html` from
# here, which is dead.
#
# The first attempt at this borrowed from a root page and let a later pass
# correct the depth. It corrected some of them: the footer came out with
# `../affiliate-disclosure.html` beside a bare `terms.html`, which is worse
# than uniformly wrong because it looks fine. So the builder does it itself,
# to everything, in one place.
DONOR = "county-job-portals-california.html"
REG = os.path.join(SITE, "mock", "library", "registry.json")
STAGE = "associate"

# Everything on this page sits one directory down, so every internal link
# needs to climb. Getting this wrong produces a hub of dead links, which is
# the one thing a hub may not be - the guard below checks every one resolves
# to a file that exists.
UP = "../"

JUMPS = [("ledger", "Where you are"),
         ("asking", "What this room asks"),
         ("start", "Start here"),
         ("shelf", "All %d guides"),
         ("sources", "The rules behind it")]

# The four things most people arrive wanting. Ordered by how often the
# question turns up, not by how good the page is.
START = [
    ("amft-3000-hours-california.html", "When do I actually finish?",
     "Your date, from the hours you are really logging"),
    ("getting-hired-as-a-california-associate.html",
     "Why is nobody hiring me?",
     "It is a billing rule, and it is not about your hour count"),
    ("associate-therapist-pay-los-angeles-bay-area.html",
     "What should this job pay?",
     "Salary against per-session, and what counties actually pay"),
    ("associate-unpaid-hours-california.html", "Do I have to work unpaid?",
     "No, and there is a wage claim with a deadline"),
]

# The shelf, grouped. Twenty ungrouped cards is a wall; five headed groups is
# a table of contents, and a cold arrival can see the shape of the whole thing
# without reading any of it.
GROUPS = [
    ("Your hours, and what counts toward them",
     ["amft-3000-hours-california.html",
      "practicum-california-mft-trainee.html",
      "associate-hours-telehealth-out-of-state.html",
      "associate-hours-trackers-compared.html",
      "out-of-state-to-california-licensure.html"]),
    ("Getting hired, and what it pays",
     ["getting-hired-as-a-california-associate.html",
      "associate-mft-job-advisor.html",
      "associate-therapist-pay-los-angeles-bay-area.html",
      "county-therapist-pay-california.html",
      "county-job-portals-california.html",
      "medi-cal-safety-net-employers-california.html",
      "associate-unpaid-hours-california.html"]),
    ("Money back on your loans",
     ["loan-forgiveness-employers-california.html",
      "mbh-slrp-california.html"]),
    ("The Board: exams, fees and waiting",
     ["bbs-exam-pass-rates-california.html",
      "bbs-processing-times-california.html",
      "bbs-fees-california-2026.html",
      "continuing-education-california-lmft.html",
      "therapist-discipline-cases-california.html"]),
    ("The market you are qualifying into",
     ["therapists-by-county-california.html"]),
]

# The three loudest threads in the community analysis, de-identified - no
# name, no group, no quotable handle. The wording is the recurring shape of
# the question rather than any one person's post.
ASKING = [
    ("&ldquo;Hundreds of hours in, and nobody will hire me.&rdquo;",
     "It is a billing rule, not your hour count.",
     "Medi-Cal names registered associates as a billable staff type. Most "
     "commercial payers do not, which is why the jobs are concentrated where "
     "they are &mdash; and it has nothing to do with how far along you are.",
     "getting-hired-as-a-california-associate.html"),
    ("&ldquo;Am I supposed to be doing this unpaid?&rdquo;",
     "The wage claim is a real one, and the Board is not where you file it.",
     "Non-clinical time an employer requires is time worked. The claim goes to "
     "the Labor Commissioner, there is a form, and there is a deadline.",
     "associate-unpaid-hours-california.html"),
    ("&ldquo;Will hours from another state count?&rdquo;",
     "Yes, with conditions &mdash; and the Board has answered this five times.",
     "The answer sits in a PDF nobody links to. What travels, what does not, "
     "and what your supervisor has to be.",
     "associate-hours-telehealth-out-of-state.html"),
]

# NO PAGE CSS HERE, AND THAT IS THE POINT. The first build shipped a 60-rule
# inline block; the A2 verdict called the result cluttered and not the house
# style. The design now lives ONLY in css/house-for.css, gated on body.bcf
# and linked by _dev/family_for.py - one sheet, reviewable in one place, and
# the template the other three doors copy. (pagekit's shared block still
# rides along via pk.assemble; family_for strips it, running last.)

JS = """<script>/* the ledger. Everything here stays in this browser: no storage,
   no hash, no query string, no network. */
(function(){
 var $=function(i){return document.getElementById(i)};
 var F=["lgTotal","lgDirect","lgRel","lgWeeks","lgRate"];
 function num(id){var e=$(id);if(!e)return 0;var v=parseFloat(e.value);
   return (isNaN(v)||v<0)?0:v}
 function money(n){return n.toLocaleString("en-US")}
 function draw(){
  var tot=num("lgTotal"),dir=num("lgDirect"),rel=num("lgRel"),
      wk=num("lgWeeks"),rate=num("lgRate");
  /* 3A's tiles are the EXPANDED state: they appear once any figure is
     typed. Before that the ledger is one quiet bar (the 3C empty state). */
  var g=document.querySelector(".lg-g");
  if(g){g.classList[(tot+dir+rel+wk+rate)>0?"add":"remove"]("open")}
  var pct=Math.max(0,Math.min(100,tot/3000*100));
  $("lgFill").style.width=pct.toFixed(1)+"%";
  $("lgPct").textContent=Math.round(pct)+"%";
  $("lgTot").textContent=money(Math.round(tot))+" / 3,000";
  set("gDirect",dir,1750,"direct clinical hours");
  set("gRel",rel,500,"relational hours");
  set("gWeeks",wk,104,"weeks elapsed");
  var left=Math.max(0,3000-tot);
  var wks=rate>0?Math.ceil(left/rate):0;
  var need=Math.max(wks,Math.max(0,104-wk));
  var e=$("gWhen");
  if(rate>0&&tot>0){
    e.querySelector(".v").textContent=need+" wk";
    e.querySelector(".s").textContent=need>0
      ? "at "+rate+" h a week, and the 104-week floor"
      : "both the hours and the weeks are met";
    e.className=need>0?"":"done";
  }else{
    e.querySelector(".v").textContent="\\u2014";
    e.querySelector(".s").textContent="enter hours and a weekly rate";
    e.className="";
  }
 }
 function set(id,have,need,label){
  var e=$(id);
  e.querySelector(".v").textContent=money(Math.round(have))+" / "+money(need);
  var short=Math.max(0,need-have);
  e.querySelector(".s").textContent=short>0
    ? money(Math.round(short))+" still to find"
    : label+" met";
  e.className=short>0?(id==="gRel"?"hot":""):"done";
 }
 for(var i=0;i<F.length;i++){
  var el=$(F[i]);
  if(el){el.addEventListener("input",draw);el.addEventListener("change",draw)}
 }
 draw();
})();
</script>"""



def descend(html):
    """Move a root page's chrome down one directory.

    Rewrites every relative href and src to climb out of `/for/`. Absolute
    URLs, protocol-relative URLs, fragments, `mailto:`, `tel:` and `data:`
    URIs are left exactly as they are, and anything already climbing is left
    alone so this stays safe to apply twice.
    """
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if (url.startswith(("http://", "https://", "//", "#", "mailto:",
                            "tel:", "data:", "../", "/"))
                or not url.strip()):
            return m.group(0)
        return '%s="%s%s"' % (attr, UP, url)
    return re.sub(r'\b(href|src)="([^"]*)"', fix, html)


def note_esc(x):
    """pk.esc for registry text that already carries entities.

    Registry titles and stage notes are written WITH entities (&mdash;,
    &rsquo;). Plain pk.esc turns those into literal "&amp;mdash;" - the
    double-escape bug this repo has shipped twice before, and it was live
    on three shelf cards of the first build. Escape, then give the known
    named entities their ampersand back.
    """
    s = pk.esc(x)
    return re.sub(r"&amp;(#\d+|[a-zA-Z]+);", r"&\1;", s)


def body(shelf):
    o = ['<article class="fd-wrap">']

    # The hero: the page's ONE dark band. Kicker, headline, the offer in a
    # sentence, the privacy line (3C: in the hero, in every version), jumps.
    # The old four-figure stat grid is gone per the A2 declutter - each of
    # its figures survives in the body of the page.
    o.append('<section class="pk-hero">')
    o.append('<p class="hk">For California associates &middot; AMFT, ASW '
             "and APCC</p>")
    o.append("<h1>Everything a California associate needs, in one place.</h1>")
    o.append('<p class="hl">%d guides for the years between registration and '
             "your license &mdash; the hours and what counts toward them, why "
             "employers can or cannot hire you, what the work pays county by "
             "county, the loan repayment nobody mentions, and the "
             "Board&rsquo;s own numbers on exams and waiting times. Every "
             "figure comes from a named source, and the whole site is free."
             "</p>" % len(shelf))
    o.append('<p class="hpriv">Free, no account &middot; every figure you '
             "type is computed in this browser and never stored or sent</p>")
    o.append('<p class="hj">')
    for h, l in JUMPS:
        o.append('<a href="#%s">%s</a>' % (h, l % len(shelf)
                                           if "%d" in l else l))
    o.append("</p>")
    o.append("</section>")

    # ---------------------------------------------------------------- ledger
    # First, per 3C: the bar IS the page. The requirement tiles are its
    # expanded state - hidden until a figure is typed.
    o.append('<section class="pk-sec" id="ledger">')
    o.append('<p class="pk-k">Where you are</p>')
    o.append('<h2 class="pk-h">Which requirement is actually holding you up?</h2>')
    o.append('<p class="pk-d">Five numbers off your own log. The bar is the '
             "3,000; the sub-totals appear underneath it as you type, and one "
             "of them stops more people than the rest.</p>")

    o.append('<div class="lg">')
    o.append('<div class="lg-in">')
    for fid, lab, ph in [
        ("lgTotal", "Hours logged, total", "1284"),
        ("lgDirect", "Of those, direct clinical", "742"),
        ("lgRel", "Of those, relational", "228"),
        ("lgWeeks", "Weeks since you registered", "61"),
        ("lgRate", "Hours in a typical week", "18"),
    ]:
        o.append('<div><label for="%s">%s</label>'
                 '<input id="%s" type="number" min="0" step="1" '
                 'inputmode="numeric" placeholder="%s"></div>' % (fid, lab, fid, ph))
    o.append("</div>")

    o.append('<p class="lg-read"><b id="lgTot">&mdash;</b> '
             '<span id="lgPct">0%</span> of the way</p>')
    o.append('<div class="lg-bar"><i id="lgFill"></i></div>')
    o.append('<div class="lg-mk"><span style="left:58.3%">1,750 direct</span>'
             '<span style="left:99%">3,000</span></div>')
    o.append('<div class="lg-g req">')
    for gid, k in [("gDirect", "Direct clinical"), ("gRel", "Relational hours"),
                   ("gWeeks", "Weeks elapsed"), ("gWhen", "Weeks still to go")]:
        o.append('<div id="%s"><span class="k">%s</span>'
                 '<span class="v">&mdash;</span>'
                 '<span class="s">&nbsp;</span></div>' % (gid, k))
    o.append("</div>")
    o.append('<p class="lg-note">The relational requirement is '
             "marked because it is the one people reach 3,000 without: 500 "
             "hours with couples, families and children, inside the 1,750. "
             "Everything here is your arithmetic, not the Board&rsquo;s "
             "record.</p>")
    o.append("</div>")

    o.append(pk.callout(
        "The four requirements, and where they come from",
        ["<b>3,000</b> hours over at least <b>104 weeks</b>, of which at least "
         "<b>1,750</b> are direct clinical counseling and at least <b>500</b> "
         "of those are with couples, families and children. No more than 40 "
         "hours in any seven days, and no more than 1,250 of nonclinical time.",
         'All of it is &sect;&thinsp;4980.43(c). The full arithmetic, including '
         'what happens to hours gained before your degree, is on '
         '<a href="%samft-3000-hours-california.html">the calculator</a> and '
         '<a href="%spracticum-california-mft-trainee.html">the practicum '
         "page</a>." % (UP, UP)]))
    o.append("</section>")

    # --------------------------------------------------------------- asking
    # 3B's questions, directly below the bar - per the approved 3C scoping.
    o.append('<section class="pk-sec" id="asking">')
    o.append('<p class="pk-k">What this room asks</p>')
    o.append('<h2 class="pk-h">Three questions, and the pages that answer '
             "them.</h2>")
    o.append('<p class="pk-d">Taken from the shape of what actually gets '
             "posted in the pre-licensed groups, not from a taxonomy. Nobody "
             "is quoted and nobody is identified.</p>")
    for q, ans, expl, href in ASKING:
        o.append('<div class="ask"><q>%s</q><p class="an">%s</p><p>%s</p>'
                 '<a href="%s%s">Read it &rarr;</a></div>'
                 % (q, ans, expl, UP, href))
    o.append("</section>")

    # ----------------------------------------------------------------- start
    o.append('<section class="pk-sec" id="start">')
    o.append('<p class="pk-k">Start here</p>')
    o.append('<h2 class="pk-h">Four questions bring most people to this '
             "page.</h2>")
    o.append('<p class="pk-d">Written for AMFTs. Where a rule differs for an '
             "ASW or an APCC, the page says so and links to the difference.</p>")
    o.append('<div class="start">')
    for href, q, sub in START:
        o.append('<a href="%s%s"><span class="q">%s</span>'
                 '<span class="s">%s</span></a>' % (UP, href, q, sub))
    o.append("</div>")
    o.append("</section>")

    # ---------------------------------------------------------------- shelf
    o.append('<section class="pk-sec" id="shelf">')
    o.append('<p class="pk-k">All %d guides</p>' % len(shelf))
    o.append('<h2 class="pk-h">Everything on this site written for somebody '
             "counting hours.</h2>")
    o.append('<p class="pk-d">The line under each title is not the '
             "page&rsquo;s summary &mdash; it is what that page tells somebody "
             "at this stage specifically. The same page says something "
             "different to a student or to a licensed therapist.</p>")

    by_file = {f: (t, n) for f, t, n in shelf}
    printed = set()
    for heading, files in GROUPS:
        rows = [f for f in files if f in by_file]
        if not rows:
            continue
        o.append('<h3 class="pk-h3">%s</h3>' % heading)
        o.append('<div class="shelf">')
        for f in rows:
            title, note = by_file[f]
            printed.add(f)
            o.append('<a class="card" href="%s%s"><span class="t">%s</span>'
                     '<span class="n">%s</span></a>'
                     % (UP, f, note_esc(title), note_esc(note)))
        o.append("</div>")

    # Anything tagged but not placed in a group still has to appear, or the
    # tagging and the page silently disagree about what is on the shelf.
    left = [f for f, _, _ in shelf if f not in printed]
    if left:
        o.append('<h3 class="pk-h3">Also for this stage</h3>')
        o.append('<div class="shelf">')
        for f in left:
            title, note = by_file[f]
            o.append('<a class="card" href="%s%s"><span class="t">%s</span>'
                     '<span class="n">%s</span></a>'
                     % (UP, f, note_esc(title), note_esc(note)))
        o.append("</div>")
    o.append("</section>")

    src, nsrc = pk.sources([
        ("The rule behind the bar", [
            ("Business and Professions Code &sect;&thinsp;4980.43 &mdash; the "
             "3,000 hours, the 104 weeks, and every sub-total on this page",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?lawCode=BPC&sectionNum=4980.43."),
            ("&sect;&thinsp;4980.43.2 &mdash; the supervision each of those "
             "hours needs",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?lawCode=BPC&sectionNum=4980.43.2."),
        ]),
    ], note="This page is a door, not a record. <b>Every figure you enter is "
            "computed in your browser and nothing is stored or sent</b> "
            "&mdash; reload the page and it is gone. It is your arithmetic "
            "against the statute, and it is not the Board&rsquo;s count of "
            "your hours; only your supervisor&rsquo;s signed forms are that. "
            "Written for AMFTs, with the differences for ASWs and APCCs on the "
            "pages linked above. Nothing here is legal advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "For California associates: everything for counting your 3,000 hours",
    "One page for registered associates - where you are against the 3,000 "
    "hours and all four requirements inside them, the three questions the "
    "pre-licensed groups actually ask, and every page written for this stage.",
    "licensure", "reference",
    "What do I need while I am a registered associate in California?",
    "The whole requirement in one bar, and every page on this site written "
    "for somebody counting hours",
    "The 3,000 is almost never what decides your date",
    weight=5)


def main():
    print("the associates door")

    reg = json.load(open(REG, encoding="utf-8"))
    shelf = []
    for p in reg["pages"]:
        if STAGE not in p.get("stages", []):
            continue
        note = (p.get("stage_note") or {}).get(STAGE, "").strip()
        if not note:
            sys.exit("%s is tagged %r with no stage_note. A hub entry with "
                     "nothing to say at this stage is the thin duplicate this "
                     "whole design exists to avoid." % (p["file"], STAGE))
        shelf.append((p["file"], p["title"], note))
    shelf.sort(key=lambda r: r[1])

    if len(shelf) < 5:
        sys.exit("only %d page(s) tagged %r - a hub this thin fails the test "
                 "it was built to pass" % (len(shelf), STAGE))

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    head, header, footer = descend(head), descend(header), descend(footer)
    links = [descend(l) for l in links]
    html_body, nsrc = body(shelf)
    html = pk.assemble(head, META, header, html_body, footer, links, scripts,
                       extra=JS)

    os.makedirs(os.path.join(SITE, "for"), exist_ok=True)
    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d shelf pages, %d sources"
          % (PAGE, format(len(html), ",d"), len(shelf), nsrc))

    bad = pk.check_page(p, [
        ("a stylesheet link that climbs a level", 'href="../css/'),
        ("the offer in the headline", "in one place"),
        ("the start-here block", "bring most people to this page"),
        ("the relational finding", "almost never what decides your date"),
        ("the not-the-Board caveat", "not the Board&rsquo;s count"),
        ("the family wrapper family_for keys on", 'class="fd-wrap"'),
        ("the privacy line in the hero (the 3C rule)",
         "computed in this browser and never stored or sent"),
    ], [j[0] for j in JUMPS])

    s = open(p, encoding="utf-8").read()
    art = pk.article(s)

    # Every link must climb out of /for/ and land on a file that exists. A hub
    # of dead links is the one thing a hub may not be, and the depth prefix is
    # exactly the kind of thing that is wrong everywhere or nowhere.
    import re
    for href in set(re.findall(r'href="(\.\./[^"#]+)"', art)):
        target = os.path.normpath(os.path.join(SITE, "for", href))
        if not os.path.exists(target):
            print("GUARD: %s does not resolve to a file" % href)
            bad += 1
    if 'href="../' not in art:
        print("GUARD: no link climbs out of /for/ - the depth prefix is gone")
        bad += 1

    # The ledger must not persist or transmit anything. The site's promise is
    # the reason anybody types a number into it at all.
    for pat, why in ((r"localStorage", "browser storage"),
                     (r"sessionStorage", "browser storage"),
                     (r"location\.hash\s*=", "a share hash"),
                     (r"\bfetch\s*\(", "a network call"),
                     (r"XMLHttpRequest", "a network call"),
                     (r"navigator\.sendBeacon", "a network call")):
        if re.search(pat, JS):
            print("GUARD: the ledger uses %s, and the hero promises it does "
                  "not" % why)
            bad += 1

    # Registry notes arrive with entities already in them; a shelf card
    # showing a literal "&mdash;" is the double-escape bug, again.
    if re.search(r"&amp;(#\d+|[a-zA-Z]+);", art):
        print("GUARD: a double-escaped entity survived on the page")
        bad += 1

    for w in pk.spelling(s):
        print("GUARD: British spelling %r" % w)
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards ok - %d shelf entries, every link resolves" % len(shelf))


if __name__ == "__main__":
    main()
