#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What a 390px phone gets wrong on 131 pages, found by looking at 390px.

The contrast sweep runs at 1440 and is structurally blind to this. A checkbox
that is a comfortable click is a 22px tap target; a 9.8px credit line is small
on a laptop and unreadable at arm's length; and a single URL quoted in a
sentence slides the entire page sideways under the reader's thumb. "Seems broke
iPhone" was reported once and fixed once, for the masthead. The other 130 pages
had never been looked at.

`mob_audit.mjs` checks five things at 390x844 with touch: document overflow and
its culprit, tap targets under 24x24, sub-12px text that carries a sentence
rather than a label, and sticky furniture eating the viewport. This pass fixes
what it found.

## 1. THREE PAGES SLIDE SIDEWAYS. IT IS A URL.

    hope-international-university-mft.html                     441px document
    psychedelic-training-psychedelic-coalition-for-health.html 450px
    simplepractice-california-therapists.html                  405px

Not a table, not a grid, not an image. A filename and two source URLs, quoted
inside ordinary paragraphs:

    (mft_student_faculty_demographics_summer_2025.pdf)
    (https://www.vistaequitypartners.com/news/vista-equity-partners-...
    https://www.psychedeliccoalitionforhealth.com/training.

`overflow-wrap` was `normal`, so a 50-character unbreakable token widens its
line box, its list item, its article, and the document.

**It took four passes to find, and the wrong answer was convincing at every
step.** The audit's own culprit-finder returned nothing, because it skipped any
element inside an `overflow-x:auto` ancestor and the only things sticking past
the viewport were masthead buttons in a deliberate scroller. Looking for the
widest element found `table.octbl` at 460px in a 338px column - which looks
exactly like the bug, and is not: `.octw` already scrolls it. Only asking
"whose `scrollWidth` exceeds its own `clientWidth`, with no scrolling ancestor"
walked down to an `<li>` with no overflowing child element at all - which is the
signature of a text node that cannot break.

So the fix is one property on running text, and it generalises: every page that
ever quotes a URL is now protected, rather than these three being patched.
`anywhere` rather than `break-word`, because `break-word` does not shrink the
element's min-content width and so still lets a flex or grid track widen.

## 2. TAP TARGETS: WCAG 2.5.8, AND WHERE IT DOES NOT APPLY

24x24 CSS px is the AA minimum. Failing, across the site:

    input[type=checkbox]   18-22px   132 pages - the consent boxes
    a.tsall                    11px   111 pages - "All updates"
    a.uall                     16px   117 pages - "All 12 pages on ..."
    summary                 11-15px    88 pages - every disclosure
    .az a                      17px             - the A-Z index letters
    a.perma                  7x15px             - the section anchors
    button.keep                21px

**Inline links inside running prose are exempt** - the spec exempts them, and
"make body-copy links 24px tall" is not advice anyone should follow. The audit
applies that exemption.

Every fix adds hit area with padding, not with type size. Nothing gets visually
bigger; the touch box does.

## 3. TEXT UNDER 12px THAT CARRIES A SENTENCE

The audit only counts runs of 25 characters or more, so labels, chips and units
- which are legitimately tiny - are not swept up.

    span in label.consent  11.8px  124 pages   "Yes, email me practice notes..."
    .nlmeta                11.0px  103 pages
    .vmeta                  9.8px   65 pages   figure credits
    .cun / .tm / .mods      9.8px
    .tsbadge                9.6px
    ...and eighteen more

All go to a 12px floor **at phone widths only**. Desktop typography is
untouched.

**Every selector is tripled** (`.nlmeta.nlmeta.nlmeta`). The first version of
this pass shipped them single-class and changed nothing on the pages that
mattered, because `.sec .nlmeta` and `.cform .nlmeta` are (0,2,0) and were
already winning. This project has now hit that exact trap four times; the rule
is that a late override of an existing class needs more class tokens, not more
faith.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "/* _dev/mobile_floor.py */"

# Sentence-carrying classes the sweep found under 12px, with the smallest size
# observed. Labels, chips and units are absent on purpose.
TINY = [
    ("label.consent span, label.lconsent span", 11.8),
    (".nlmeta", 11.0),
    (".vmeta", 9.8),
    (".cun", 9.8),
    (".tm", 9.8),
    (".mods", 9.8),
    (".ccode", 9.8),
    (".tsbadge", 9.6),
    (".np", 9.6),
    (".lhdph", 9.6),
    (".sub", 10.2),
    (".kick", 10.0),
    (".pr-kick", 10.0),
    (".city", 10.4),
    (".pdcity", 10.0),
    (".anote", 10.6),
    (".cx", 10.6),
    (".ocl", 10.6),
    (".leyebrow", 10.5),
    (".lname", 11.0),
    (".lab", 11.0),
    (".tck", 11.0),
    (".grouplab span", 11.0),
    (".fact i", 11.5),
    (".hwfact i", 11.5),
    (".cnum", 11.6),
    (".nx-f", 11.6),
    (".jobfoot", 11.9),
    (".mo", 11.6),
    (".cred", 10.4),
    (".ig-l", 10.4),
    # Containers whose text sits in classless spans, so the class cannot be
    # targeted directly - the breadcrumb's current page, the "Page updated"
    # strip, the affiliate note, the fee-table rows.
    (".bcr span", 10.4),
    (".pdmeta, .pdmeta span", 10.4),
    (".afmeta, .afmeta span", 10.4),
    (".tbl .r span, .tbl .r b .sub", 10.2),
    (".pdgone i", 9.6),
]

# Controls that are not inline prose links and are under 24px of hit area.
TAPS = ["a.tsall", "a.uall", "a.tcall", "a.srmore", "a.go", "a.pdgo",
        "button.keep"]

# Where a URL may legally be quoted. Everything a reader reads in SENTENCES.
#
# `td` and `th` were in this list and had to come out, because `anywhere` and
# `break-word` differ in exactly the way that matters to a table.
#
# `anywhere` is a soft wrap opportunity that IS counted when the browser
# computes min-content width. That is precisely why it was chosen - it lets a
# flex or grid track shrink past a long token instead of being widened by it.
# Inside a table it is a disaster: every column's min-content width collapses to
# roughly one character, so an auto-layout table at `width:100%` shrinks every
# column to its narrowest and breaks every word. On a phone the payer table
# rendered "Headway" as "Head / way", "Grow Therapy" as "Grow / Ther / apy" and
# the column header "MINIMUM" as "MIN / IMU / M".
#
# Table cells get `break-word` instead: it breaks a genuinely over-long token
# but leaves min-content width alone, so the columns keep their natural widths.
# The tables that can still overflow are inside scrollers.
#
# None of the three pages that actually slid sideways was a table - they were
# an <li> and two <p>s, each with a URL in it. `td, th` was never needed here.
PROSE = ("p, li, dd, dt, blockquote, figcaption, "
         "summary, .lco, .srn, .tcio, cite, q")
CELLS = "td, th"


REPEAT = 4


def triple(sel):
    """`.nlmeta` -> `.nlmeta.nlmeta.nlmeta.nlmeta`.

    Three was not enough. `.sub.sub.sub` is (0,3,0) and lost to
    `.bd .r b .sub`, which is (0,3,1) - the element selector in the descendant
    chain is the tie-breaker, and it wins. Four class tokens clears every
    descendant rule on this site by construction."""
    out = []
    for part in sel.split(","):
        part = part.strip()
        out.append(re.sub(r"\.([A-Za-z0-9_-]+)",
                          lambda m: "." + (".".join([m.group(1)] * REPEAT)),
                          part))
    return ",\n  ".join(out)


CSS = """<style>%(mark)s
/* A quoted URL is a single unbreakable token. Three pages were 15-60px wider
   than the viewport because of one, and every future page that cites a source
   inline would have joined them. `anywhere` and not `break-word`: break-word
   leaves the element's min-content width intact, so a flex or grid track can
   still be widened by the same string. */
%(prose)s{overflow-wrap:anywhere}
/* Cells break long tokens but keep their natural column widths. See PROSE. */
%(cells)s{overflow-wrap:break-word}
@media (max-width:640px){
  /* Hit area, not type size. Nothing here gets visually bigger. */
  %(taps)s{min-height:24px;display:inline-flex;align-items:center;padding-block:4px}
  summary{min-height:24px}
  /* The rest are ordinary links that happen to be the whole of their line:
     "The program's own page", a cost-chart bar label, "source" at the end of a
     table cell. They come in at 11-18px because that is what a line of 13px
     type is.
     Vertical padding on an INLINE element does not affect the line box - it
     grows the hit rectangle and moves nothing. That is the whole trick, and it
     is why this is padding rather than min-height: min-height on these would
     have pushed every line of every article apart to fix a touch target. */
  main a, .sitefoot a{padding-block:7px}
  .az a, a.perma{min-width:24px;min-height:24px;display:inline-flex;
    align-items:center;justify-content:center}
  input[type="checkbox"], input[type="radio"]{min-width:24px;min-height:24px}
  select{min-height:26px}
  /* A 12px floor for text that carries a sentence. Phone widths only: the
     desktop sizes were designed for reading distance and are left alone.
     Tripled because `.sec .nlmeta` and friends are (0,2,0) and were winning. */
%(tiny)s
}
</style>"""


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def build_css():
    tiny = "\n".join("  %s{font-size:12px}" % triple(sel) for sel, _w in TINY)
    return CSS % {"mark": MARK, "prose": PROSE, "cells": CELLS,
                  "taps": ",\n  ".join(TAPS), "tiny": tiny}


def main():
    smallest = min(w for _s, w in TINY)
    print("%d selector group(s) raised to a 12px floor (smallest observed %.1fpx)"
          % (len(TINY), smallest))
    print("%d control(s) given a 24px hit area" % (len(TAPS) + 5))
    print("overflow-wrap:anywhere on: %s" % PROSE)

    css = build_css()
    n = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        i = s.lower().rfind("</body>")
        if i < 0:
            continue
        s = s[:i] + css + "\n" + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("\n%d page(s) written" % n)

    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" in s and s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1
    # Every tiny selector must have come out with at least three class tokens,
    # or it will lose the same argument the first version lost.
    for sel, _w in TINY:
        t = triple(sel)
        for part in t.split(","):
            if "." in part and part.count(".") % REPEAT != 0:
                print("GUARD: %r did not triple cleanly -> %r" % (sel, part))
                bad += 1
    if "overflow-wrap:anywhere" not in css:
        print("GUARD: the wrap rule is missing - the three wide pages stay wide")
        bad += 1
    # The regression this pass shipped once: `anywhere` on a table cell
    # collapses every column and breaks every word. It must never come back.
    anywhere_sel = css.split("{overflow-wrap:anywhere}")[0].split("*/")[-1]
    for cell in ("td", "th", "table"):
        if re.search(r"(^|[\s,])" + cell + r"([\s,]|$)", anywhere_sel):
            print("GUARD: %r is in the `anywhere` list - that breaks tables" % cell)
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
