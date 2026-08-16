#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/for/students - the second stage door, to the associates-door pattern.

WHO ARRIVES: someone enrolled in a California MFT program with the
practicum ahead of them or underway - almost always cold, from a search
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
PAGE = "for/students.html"
STAGE = "student"
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
    o.append('<p class="hk">For California MFT students &middot; trainee '
             "stage</p>")
    o.append("<h1>Everything a California MFT student needs, in one "
             "place.</h1>")
    o.append('<p class="hl">%d guides for the years between enrolling and '
             "your associate number &mdash; how the practicum actually "
             "works and who finds your site, the seven rules that decide "
             "whether a placement counts, the Bay Area seats laid out by "
             "name, and the two pieces of paperwork that start before you "
             "graduate. Every figure comes from a named source, and the "
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
    o.append('<h2 class="pk-h">Four questions bring most students to this '
             "page.</h2>")
    o.append('<p class="pk-d">Written for MFT trainees. Where a rule '
             "differs for an MSW or counseling student, the page says so "
             "and links the difference.</p>")
    o.append('<div class="start">')
    for href, q, s2 in [
        ("../how-to-find-a-practicum-site-california.html",
         "How do I actually find a practicum site?",
         "The search in order, and the six questions that protect your "
         "hours"),
        ("../practicum-california-mft-trainee.html",
         "What am I allowed to do as a trainee?",
         "The seven rules, and which of the 78 programs finds your site"),
        ("../bbs-90-day-rule-california.html",
         "What paperwork starts before I graduate?",
         "The 90-day rule, and the Live Scan that has to come first"),
        ("../amft-3000-hours-california.html",
         "Do my practicum hours count later?",
         "Up to 1,300 can bank toward the 3,000 &mdash; see what yours "
         "are worth"),
    ]:
        o.append('<a href="%s"><span class="q">%s</span>'
                 '<span class="s">%s</span></a>' % (href, q, s2))
    o.append("</div></section>")

    # ------------------------------------------------------------- shelf
    o.append('<section class="pk-sec" id="shelf">')
    o.append('<p class="pk-k">All %d guides</p>' % len(shelf))
    o.append('<h2 class="pk-h">Everything on this site written for '
             "somebody still in the degree.</h2>")
    o.append('<p class="pk-d">The line under each title is not the '
             "page&rsquo;s summary &mdash; it is what that page tells a "
             "student specifically. The same page says something different "
             "to an associate counting hours.</p>")
    o.append('<div class="shelf">')
    for f, title, note in shelf:
        o.append('<a class="card" href="../%s"><span class="t">%s</span>'
                 '<span class="n">%s</span></a>'
                 % (f, note_esc(title), note_esc(note)))
    o.append("</div></section>")

    # ----------------------------------------------------------- sources
    src, nsrc = pk.sources([
        ("The statutes this stage runs on", [
            ("Business and Professions Code &sect;&thinsp;4980.42 &mdash; "
             "the practicum course, the site agreement your school must "
             "hold, and the under-90-day gap",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?lawCode=BPC&sectionNum=4980.42."),
            ("&sect;&thinsp;4980.43.3 &mdash; what a trainee may and may "
             "not do, and the settings that can never count",
             "https://leginfo.legislature.ca.gov/faces/codes_displaySection."
             "xhtml?lawCode=BPC&sectionNum=4980.43.3."),
            ("&sect;&thinsp;4980.43 &mdash; the 1,300 pre-degree hours "
             "that can bank, and the 750-hour inner cap",
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
    "For California MFT students: the practicum, and what comes after",
    "One page for MFT students - how the practicum works and who finds "
    "your site, the rules that decide whether a placement counts, and the "
    "paperwork that starts before you graduate.",
    "licensure", "reference",
    "What do I need while I am an MFT student in California?",
    "The practicum search, the trainee rules, the Bay Area seats by name, "
    "and the two deadlines that start before the degree",
    "Up to 1,300 pre-degree hours can bank toward the 3,000",
    weight=5)


def main():
    print("the students door")
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
        ("the practicum method card", "how-to-find-a-practicum-site"),
        ("the 90-day card", "bbs-90-day-rule"),
        ("the trainee rules card", "practicum-california-mft-trainee"),
        ("the fd wrapper family_for converts on", 'class="fd-wrap"'),
        ("the 4980.42 source", "sectionNum=4980.42."),
        ("the 4980.43.3 source", "sectionNum=4980.43.3."),
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
