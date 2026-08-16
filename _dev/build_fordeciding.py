#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/for/deciding - the third stage door, to the associates-door pattern.

WHO ARRIVES: someone weighing the whole thing - a career change, a
program choice, a move - almost always cold, from a search
for one specific question. The associates door established what a cold
arrival needs in the first screen (am I in the right place, is this the
whole thing, where do I start) and that template is followed exactly:
kicker, one-sentence offer with the count, jumps, then the four questions
that bring people here, then the shelf built from stage_note.

NO WIDGET. The associates door earns its ledger because the associate's
question is arithmetic. The student's question is a search, and the tool
for a search is the method page - so where the ledger sits on the other
door, this one places its four starting questions and gets out of the
way.

THE SHELF IS BUILT FROM stage_note, exactly as on /for/associates: each
card's second line is what that page tells a STUDENT specifically,
hand-written in _dev/stage_tags.py, and a tagged page with no note fails
the build. This build is the moment the student notes were written -
"a page is tagged when a hub that lists it is built."

Chrome borrowed from the same root donor; body.bcf + css/house-for.css
own the design; _dev/family_for.py converts and guards it, running LAST.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagekit as pk

SITE = pk.SITE
PAGE = "for/deciding.html"
STAGE = "deciding"
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
    o.append('<p class="hk">Thinking about it &middot; career change or '
             "program choice</p>")
    o.append("<h1>Deciding whether to become a California therapist, with "
             "the numbers in front of you.</h1>")
    o.append('<p class="hl">%d guides for the decision itself &mdash; what '
             "the whole route costs and how long it takes, what the work "
             "pays county by county at the end, how all 78 programs differ "
             "on the year that varies most, and how crowded the field "
             "actually is. Every figure comes from a named source, and the "
             "whole site is free.</p>" % len(shelf))
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
    o.append('<h2 class="pk-h">Four questions decide this for most '
             "people.</h2>")
    o.append('<p class="pk-d">Written for the MFT route. Where social work '
             "or counseling differs, the page says so and links the "
             "difference.</p>")
    o.append('<div class="start">')
    for href, q, s2 in [
        ("../becoming-a-therapist-california-career-change.html",
         "What does the whole route actually take?",
         "Every stage from another career, ordered by what you can start "
         "this month"),
        ("../county-therapist-pay-california.html",
         "What does the work pay at the end?",
         "Every county ranked from employers&rsquo; own returns &mdash; a "
         "2.8&times; spread"),
        ("../mft-programs-california.html",
         "Which program should I pick?",
         "All 78 compared on the year that varies most &mdash; who finds "
         "your practicum site"),
        ("../bbs-fees-california-2026.html",
         "What does the license itself cost?",
         "The Board&rsquo;s whole fee schedule, halved through 2030"),
    ]:
        o.append('<a href="%s"><span class="q">%s</span>'
                 '<span class="s">%s</span></a>' % (href, q, s2))
    o.append("</div></section>")

    # ------------------------------------------------------------- shelf
    o.append('<section class="pk-sec" id="shelf">')
    o.append('<p class="pk-k">All %d guides</p>' % len(shelf))
    o.append('<h2 class="pk-h">Everything on this site written for '
             "somebody still deciding.</h2>")
    o.append('<p class="pk-d">The line under each title is not the '
             "page&rsquo;s summary &mdash; it is what that page tells "
             "someone weighing the decision specifically. The same page "
             "says something different to a student or an associate.</p>")
    o.append('<div class="shelf">')
    for f, title, note in shelf:
        o.append('<a class="card" href="../%s"><span class="t">%s</span>'
                 '<span class="n">%s</span></a>'
                 % (f, note_esc(title), note_esc(note)))
    o.append("</div></section>")

    # ----------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("The statutes the decision runs on", [
            ("Business and Professions Code &sect;&thinsp;4980.36 &mdash; "
             "the degree the license requires, unit by unit",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?lawCode=BPC&sectionNum=4980.36."),
            ("&sect;&thinsp;4980.42 &mdash; the practicum year inside "
             "that degree, and whose job the site agreement is",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?lawCode=BPC&sectionNum=4980.42."),
            ("&sect;&thinsp;4980.43 &mdash; the 3,000 supervised hours "
             "that follow the degree",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?lawCode=BPC&sectionNum=4980.43."),
        ]),
    ], note="This page is a door, not advice. Every rule above is quoted "
            "and sourced in full on the pages it links; where this stage "
            "touches money or law, those pages link the statute rather "
            "than summarizing it. Nothing here is legal advice.")
    o.append(src)

    o.append("</article>")
    return "".join(o), nsrc


META = pk.meta_block(
    PAGE,
    "Deciding to become a California therapist: the numbers first",
    "One page for the decision itself - what the route costs and how long "
    "it takes, what the work pays at the end, and how the 78 programs "
    "differ on the year that varies most.",
    "licensure", "reference",
    "Should I become a therapist in California?",
    "The route and its cost, county pay at the end, all 78 programs on "
    "placement, and how crowded the field actually is",
    "The same clinical job pays 2.8x more in one county than another",
    weight=5)


def main():
    print("the deciding door")
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
        ("the career-change card", "becoming-a-therapist-california"),
        ("the county-pay card", "county-therapist-pay"),
        ("the programs card", "mft-programs-california"),
        ("the fd wrapper family_for converts on", 'class="fd-wrap"'),
        ("the 4980.36 source", "sectionNum=4980.36."),
        ("the 4980.42 source", "sectionNum=4980.42."),
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
