#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One content frame, because the site had six and they disagreed.

WHAT WAS REPORTED, IN THE USER'S WORDS

  "See how close breadcrumbs are to header and h1, the H1 does not seem to use
   the entire width and is truncated... too many different layouts and styles"

  "LOOKS LIKE A BUG WITH CONTENT BLOCK WIDER THAN REST OF SITE, FIX GLOBALLY,
   FIND ANY SIMILAR AND FIX"

Both are the same underlying thing and both are measurable, so both are fixed
by measurement rather than by taste.

MEASURED, BEFORE                              article page      case page
  breadcrumb -> H1 gap                            37px             14px
  H1 max-width                                  528.8px          514.9px
  the column the H1 sits in                       740px           1040px
  content container                              1180px          1040px

So on an article the headline is capped at 71% of its own column and wraps to
three lines at 40px - about thirteen characters a line. That is the "does not
use the entire width and is truncated" report, exactly. And the gap above it
is 37px on one template and 14px on another, which is the "too many different
layouts" report, exactly.

THE TABLE

  <table class="tbl">   801px  - its own content demands this
  <div class="tw">      713px  - overflow-x:auto
  <div class="artbody"> 713px

The table is 88px wider than its scroller. It IS scrollable - but macOS uses
overlay scrollbars, so there is no scrollbar, no fade, no affordance of any
kind. It renders as a table with its last column sliced off. Every reader will
read that as a bug, and they are right to.

Two things fix it, and this pass does both:

1. At >=900px the cells are allowed to break anywhere, which lets the table's
   min-content width collapse to its container. `overflow-wrap:anywhere` is
   counted in min-content width; `break-word` is not - that difference is the
   whole mechanism.

   It is applied ONLY at >=900px. Below that it stays `break-word`, because
   `anywhere` on a narrow table is the regression this project already shipped
   once: it rendered "Headway" as "Head/way" and "MINIMUM" as "MIN/IMU/M" on a
   phone. The guard at the bottom refuses to let `anywhere` reach a narrow
   viewport.

2. Any scroller that still overflows gets a real affordance - a right-edge fade
   and a visible scrollbar - so overflow looks like overflow.

Idempotent, guarded. Run in the FLOORS stage of _dev/ship.py, after the markup
exists and before extract_css hoists it.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "/* _dev/content_frame.py */"

INK = "#16211B"
PAPER = "#F4F0E6"
CREAM = "#FBF9F3"

# Every scroller class on the site. A new one that is not listed here gets no
# affordance, which is why the guard counts them.
SCROLLERS = (".tw", ".li-tw", ".dc-tw", ".octw", ".srn-w", ".tblw")
# Every headline that carries its own cap.
HEADLINES = (".dc-title", ".art h1", ".artband h1", ".li-h", "main h1")

CSS = """<style>%(mark)s
/* ============================================================ THE FRAME
   One rhythm, one measure, one headline width. Measured before this pass:
   the breadcrumb-to-H1 gap was 37px on an article and 14px on a case page,
   and the H1 was capped at 529px inside a 740px column. */

:root{
  --ts-crumb-gap:34px;      /* one value, both templates */
  --ts-headline:30ch;       /* was 20ch, which is ~13 characters at 40px */
  --ts-prose:72ch;
}

/* --- breadcrumb to headline ------------------------------------------- */
.bcr.bcr.bcr, .dc-crumb.dc-crumb.dc-crumb{margin-bottom:var(--ts-crumb-gap)}
.bcr.bcr.bcr + h1, .dc-crumb.dc-crumb.dc-crumb + h1,
.dc-crumb.dc-crumb.dc-crumb + .dc-title{margin-top:0}

/* --- the headline uses its column ------------------------------------- */
/* A display face at 37-41px needs about 30 characters a line, not 13. The cap
   stays - an unbounded headline on a 2560px screen is its own problem - it is
   just set to a width a headline can actually use. */
.dc-title.dc-title.dc-title{max-width:var(--ts-headline)}
.artband.artband h1, .art.art h1{max-width:var(--ts-headline)}

/* ============================================== WIDE BLOCKS IN A COLUMN
   A table whose content is wider than its column used to sit in a scroller
   with no scrollbar, no fade and no affordance, and read as a bug. */

/* 1. Let it fit. `anywhere` is counted in min-content width, `break-word` is
      not, so this is what actually collapses an over-wide table into its
      column. Wide viewports only - see the note in the pass. */
@media (min-width:900px){
  %(cells)s{overflow-wrap:anywhere}
  %(tables)s{width:100%%;min-width:0}
}

/* 2. Where it still cannot fit, make the overflow visible. */
%(scrollers)s{
  position:relative;
  scrollbar-width:thin;
  scrollbar-color:#C9C0AA transparent;
  background:
    linear-gradient(to right, %(cream)s 30%%, rgba(251,249,243,0)) left center,
    linear-gradient(to right, rgba(251,249,243,0), %(cream)s 70%%) right center,
    radial-gradient(farthest-side at 0 50%%, rgba(22,33,27,.16), rgba(22,33,27,0)) left center,
    radial-gradient(farthest-side at 100%% 50%%, rgba(22,33,27,.16), rgba(22,33,27,0)) right center;
  background-repeat:no-repeat;
  background-size:36px 100%%, 36px 100%%, 14px 100%%, 14px 100%%;
  background-attachment:local, local, scroll, scroll;
}
%(scrollbars)s
</style>"""


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def triple(sel):
    parts = sel.strip().split(" ")
    head = parts[0]
    if head.startswith("."):
        head = "." + ".".join([head.lstrip(".")] * 3)
    return " ".join([head] + parts[1:])


def build():
    cells = ", ".join("%s td, %s th" % (triple(s), triple(s)) for s in SCROLLERS)
    tables = ", ".join("%s table" % triple(s) for s in SCROLLERS)
    scr = ", ".join(triple(s) for s in SCROLLERS)
    bars = "\n".join(
        "%s::-webkit-scrollbar{height:9px}\n"
        "%s::-webkit-scrollbar-thumb{background:#C9C0AA;border-radius:9px}\n"
        "%s::-webkit-scrollbar-track{background:transparent}"
        % (triple(s), triple(s), triple(s)) for s in SCROLLERS)
    return CSS % {"mark": MARK, "cells": cells, "tables": tables,
                  "scrollers": scr, "scrollbars": bars, "cream": CREAM}


def main():
    css = build()
    print("one frame, applied to:")
    print("  breadcrumb gap    34px, both templates (was 37 and 14)")
    print("  headline measure  30ch (was 20ch = ~13 characters at 40px)")
    print("  wide tables       collapse into their column at >=900px")
    print("  scrollers         %s" % ", ".join(SCROLLERS))

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

    # ------------------------------------------------------------- guards
    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" in s and s.count(MARK) != 1:
            print("GUARD %s: %d copies" % (rel, s.count(MARK)))
            bad += 1

    # THE ONE THAT MATTERS. `overflow-wrap:anywhere` on a table cell at a phone
    # width is a regression this project has already shipped: it broke "Headway"
    # into "Head/way". It is allowed here ONLY inside a min-width:900px block.
    m = re.search(r"@media \(min-width:900px\)\{([\s\S]*?)\n\}", css)
    if not m:
        print("GUARD: the >=900px block is missing - `anywhere` would be global")
        bad += 1
    elif "anywhere" not in m.group(1):
        print("GUARD: `anywhere` is not inside the >=900px block")
        bad += 1
    # Strip CSS comments before looking. The first version of this guard fired
    # on its own explanatory comment - "`anywhere` is counted in min-content
    # width" - which is the guard checking the wrong thing, the exact failure
    # mode it exists to prevent.
    outside = css.replace(m.group(0), "") if m else css
    outside = re.sub(r"/\*[\s\S]*?\*/", "", outside)
    if "anywhere" in outside:
        print("GUARD: `anywhere` also appears OUTSIDE the >=900px block. That is "
              "the regression that rendered 'MINIMUM' as 'MIN/IMU/M' on a phone.")
        bad += 1

    for s_ in SCROLLERS:
        if triple(s_) not in css:
            print("GUARD: %s did not triple" % s_)
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - `anywhere` is confined to >=900px, every scroller "
          "carries an affordance")


if __name__ == "__main__":
    main()
