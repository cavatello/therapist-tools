#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/for/licensed - the fourth and last stage door, to the associates-door
pattern.

WHO ARRIVES: somebody whose license number is real - building or running
a practice - almost always cold, from a search for one money question.
The associates door established what a cold arrival needs in the first
screen (am I in the right place, is this the whole thing, where do I
start) and that template is followed exactly: kicker, one-sentence offer
with the count, jumps, then the four questions that bring people here,
then the shelf built from stage_note.

NO WIDGET. The associates door earns its ledger because the associate's
question is arithmetic. The licensed clinician's arithmetic already has
a whole tool - the practice simulator - so where the ledger sits on the
other door, this one places its four starting questions and gets out of
the way.

THE SHELF IS BUILT FROM stage_note, exactly as on the other doors: each
card's second line is what that page tells a LICENSED clinician
specifically, hand-written in _dev/stage_tags.py, and a tagged page with
no note fails the build. This build is the moment the licensed notes
were written - "a page is tagged when a hub that lists it is built."

Chrome borrowed from the same root donor; body.bcf + css/house-for.css
own the design; _dev/family_for.py converts and guards it, running LAST.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "for/licensed.html"
STAGE = "licensed"
DONOR = "county-job-portals-california.html"
REG = os.path.join(SITE, "mock", "library", "registry.json")
UP = "../"

JUMPS = [("start", "Where to start"), ("shelf", "Every guide for this stage"),
         ("sources", "Sources")]


def descend(html):
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if (url.startswith(("http://", "https://", "//", "#", "mailto:",
                            "tel:", "data:", "../", "/"))
                or not url.strip()):
            return m.group(0)
        return '%s="%s%s"' % (attr, UP, url)
    return re.sub(r'\b(href|src)="([^"]*)"', fix, html)


def note_esc(x):
    s = pk.esc(x)
    return re.sub(r"&amp;(#\d+|[a-zA-Z]+);", r"&\1;", s)


def body(shelf):
    o = ['<article class="fd-wrap">']

    o.append('<section class="pk-hero">')
    o.append('<p class="hk">For licensed California therapists &middot; '
             "the practice years</p>")
    o.append("<h1>Everything after the license number, in one place.</h1>")
    o.append('<p class="hl">%d guides for the years the license actually '
             "pays &mdash; what your rate and caseload put in your bank "
             "account after expenses and tax, what each insurance panel "
             "actually reimburses per code, whether the professional "
             "corporation beats the sole proprietorship on your numbers, "
             "and the 36 CE hours every renewal demands. Every figure "
             "comes from a named source, and the whole site is "
             "free.</p>" % len(shelf))
    o.append('<p class="hpriv">Free, no account &middot; nothing you read '
             "or type here is stored or sent anywhere</p>")
    o.append('<p class="hj">')
    for h, l in JUMPS:
        o.append('<a href="#%s">%s</a>' % (h, l))
    o.append("</p>")
    o.append("</section>")

    # ------------------------------------------------------------- start
    o.append('<section class="pk-sec" id="start">')
    o.append('<p class="pk-k">Start here</p>')
    o.append('<h2 class="pk-h">Four questions bring most licensed '
             "therapists to this page.</h2>")
    o.append('<p class="pk-d">Written for the solo LMFT in private '
             "practice. Where a rule differs for a group practice or "
             "another license, the page says so and links the "
             "difference.</p>")
    o.append('<div class="start">')
    for href, q, s2 in [
        ("../practice-simulator.html",
         "What will my practice actually pay me?",
         "Your rate and caseload run live &mdash; gross to net, after "
         "expenses and tax"),
        ("../insurance-reimbursement-rates-california-therapist.html",
         "Are insurance panels worth joining?",
         "What each payer actually reimburses per code, against your "
         "private-pay rate"),
        ("../therapist-tax-strategy-california.html",
         "Sole proprietorship or professional corporation?",
         "The whole decision worked on your numbers, with the payroll "
         "gap most comparisons skip"),
        ("../therapy-liability-insurance-california.html",
         "What insurance does the practice itself need?",
         "Eight malpractice programs compared on what they publish and "
         "what people actually pay"),
    ]:
        o.append('<a href="%s"><span class="q">%s</span>'
                 '<span class="s">%s</span></a>' % (href, q, s2))
    o.append("</div></section>")

    # ------------------------------------------------------------- shelf
    o.append('<section class="pk-sec" id="shelf">')
    o.append('<p class="pk-k">All %d guides</p>' % len(shelf))
    o.append('<h2 class="pk-h">Everything on this site written for '
             "somebody already licensed.</h2>")
    o.append('<p class="pk-d">The line under each title is not the '
             "page&rsquo;s summary &mdash; it is what that page tells a "
             "licensed clinician specifically. The same page says "
             "something different to a student or an associate counting "
             "hours.</p>")
    o.append('<div class="shelf">')
    for f, title, note in shelf:
        o.append('<a class="card" href="../%s"><span class="t">%s</span>'
                 '<span class="n">%s</span></a>'
                 % (f, note_esc(title), note_esc(note)))
    o.append("</div></section>")

    # ----------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("The statutes the practice runs on", [
            ("Corporations Code &sect;&thinsp;17701.04 &mdash; why a "
             "licensed therapist cannot form an LLC for clinical work, "
             "and what the real entity choice is",
             "https://leginfo.legislature.ca.gov/faces/codes_display"
             "Section.xhtml?sectionNum=17701.04.&lawCode=CORP"),
            ("&sect;&thinsp;13401.5 &mdash; who may own shares in a "
             "marriage and family therapy corporation",
             "https://leginfo.legislature.ca.gov/faces/codes_display"
             "Section.xhtml?sectionNum=13401.5.&lawCode=CORP"),
            ("Business and Professions Code &sect;&thinsp;4980.54 "
             "&mdash; the 36 hours of continuing education every "
             "renewal requires",
             "https://leginfo.legislature.ca.gov/faces/codes_display"
             "Section.xhtml?sectionNum=4980.54.&lawCode=BPC"),
        ]),
    ], note="This page is a door, not advice. Every rule above is quoted "
            "and sourced in full on the pages it links; where this stage "
            "touches money or law, those pages link the statute rather "
            "than summarizing it. Nothing here is legal or tax advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "For licensed California therapists: the practice, in numbers",
    "One page for the licensed years - what your practice pays you after "
    "expenses and tax, what insurance panels actually reimburse, the "
    "entity decision worked on your numbers, and the 36 CE hours each "
    "renewal requires.",
    "licensure", "reference",
    "What do I need now that I am licensed in California?",
    "Take-home at your rate and caseload, panel arithmetic per payer, "
    "the entity decision, and the CE clock",
    "36 CE hours per renewal, and an audit most fail on paperwork",
    weight=5)


def main():
    print("the licensed door")
    reg = json.load(open(REG, encoding="utf-8"))
    shelf = []
    for p in reg["pages"]:
        if STAGE not in p.get("stages", []):
            continue
        note = (p.get("stage_note") or {}).get(STAGE, "").strip()
        if not note:
            sys.exit("%s is tagged %r with no stage_note." % (p["file"],
                                                              STAGE))
        shelf.append((p["file"], p["title"], note))
    shelf.sort(key=lambda r: r[1])
    if len(shelf) < 8:
        sys.exit("only %d page(s) tagged %r - a hub this thin fails the "
                 "test it was built to pass" % (len(shelf), STAGE))

    head, header, footer, links, scripts = pk.chrome_parts(DONOR)
    head, header, footer = descend(head), descend(header), descend(footer)
    links = [descend(l) for l in links]
    html_body, nsrc = body(shelf)
    html = pk.assemble(head, META, header, html_body, footer, links, scripts)

    os.makedirs(os.path.join(SITE, "for"), exist_ok=True)
    p = os.path.join(SITE, PAGE)
    open(p, "w", encoding="utf-8").write(html)
    print("  wrote %s, %s bytes, %d shelf pages, %d sources"
          % (PAGE, format(len(html), ",d"), len(shelf), nsrc))

    n = pk.check_page(p, [
        ("a stylesheet link that climbs a level", 'href="../css/'),
        ("the simulator card", "practice-simulator"),
        ("the reimbursement card", "insurance-reimbursement-rates"),
        ("the tax-strategy card", "therapist-tax-strategy"),
        ("the fd wrapper family_for converts on", 'class="fd-wrap"'),
        ("the 17701.04 source", "sectionNum=17701.04."),
        ("the 13401.5 source", "sectionNum=13401.5."),
    ], [h for h, _ in JUMPS])
    s = open(p, encoding="utf-8").read()
    for phrase in ("is hiring", "has openings", "takes trainees",
                   "accepting trainees"):
        if phrase in re.sub(r"<[^>]+>", " ", s).lower():
            sys.exit("availability language: %r" % phrase)
    if s.count('class="card"') != len(shelf):
        sys.exit("shelf card count %d != %d"
                 % (s.count('class="card"'), len(shelf)))
    if n:
        sys.exit("%d check failure(s)" % n)
    print("  checks passed, guards clean")


if __name__ == "__main__":
    main()
