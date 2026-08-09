#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One grid. Every page's content starts where the logo starts.

THE REPORT

  "too many different layouts and styles"

which had been read, until now, as a typography problem. It is not, or not
mainly. Measured across the families, the type is close: h1 runs 38-44px,
section headings 26-28px, deks 15.2-17px. Nobody would call that "too many
styles" from four points of difference in a headline.

What a reader actually sees is this. The masthead and the footer are 1180px
wide with 26px of side padding on every page, so the logo sits at x=156 at a
1440px viewport, always. The content underneath does not:

    scband, artband, pxband, pdband, mgband, hwband   1180   x=156   aligned
    libband, afband, lwrap                            1120   x=186   +30
    ghero, adv, tax, li-wrap, and a bare `.in`        1060   x=216   +60
    dc-wrap                                           1040   x=220   +64
    rwwrap                                            1020   x=226   +70
    clwrap                                            1000   x=230   +74
    lgwrap, drwrap                                    1240   x=126   -30

Every one of those containers is centred, so a narrower max-width does not
indent the content - it moves the whole column inward from both sides. Click
between two pages and the headline jumps sideways by up to 74px while the logo
above it stays put. That is the "different layouts" complaint, and it is a
geometry bug rather than a design decision: nothing in this site's design
system ever asked for eight content widths.

WHAT THIS CHANGES, AND WHAT IT DELIBERATELY DOES NOT

It sets one page grid - 1180px, 26px of side padding, centred - to match
`.sitenav-in` and `.ftin`, which are already the canon and are on every page.

It does not touch the reading measure. A narrow column of prose is right, and
this site already gets it from `max-width` in `ch` on the text itself, set by
`content_frame.py` and `wide_measure.py`. Those are two different jobs that
were being done by one number, which is why widening the container here does
not widen a paragraph: the paragraph was never the width of its container.

The design statement, said plainly: THE PAGE HAS ONE GRID, AND COLUMNS SIT
INSIDE IT. A column that wants to be narrower says so on itself; it does not
shrink and re-centre everything around it.

WHY A STYLESHEET RATHER THAN EDITING THE RULES

The widths live in nineteen different places - hoisted files under `css/`, and
inline `<style>` blocks in pages whose builders no longer run. Rewriting each
in place would mean nineteen edits that a later pass could undo, in files that
`extract_css.py` rewrites by content hash. One late stylesheet with doubled
selectors survives all of that and is one thing to read.

Idempotent. Guarded on the thing that actually matters: every selector it
overrides must still exist in the site's CSS, so a renamed container fails the
build instead of quietly opting out of the grid.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/one_grid.py */"

CANON = 1180        # matches .sitenav-in and .ftin, on every page
PAD = 26            # matches the masthead's side padding

# The grid is not one number. `_dev/widen.py` steps the masthead and the footer
# out on large displays, and a flat override here would have pinned the
# containers this pass touches at 1180 while the logo above them moved to 1560
# on a 27-inch 5K - the same misalignment, only visible to fewer people. These
# MUST stay equal to widen.py's STEP1 and STEP2, and the guard checks it.
STEPS = [(1500, 1320), (1900, 1560)]

# selector, the width it currently declares, what it is
# Ordered widest-to-narrowest so the diff reads as a range being closed.
TARGETS = [
    (".lgbody > .lgwrap", 1240, "privacy and terms"),
    (".drwrap", 1240, "the doc rails body"),
    (".libband .in", 1120, "the calculators and changes heroes"),
    (".libwrap", 1120, "their bodies"),
    (".afband .in", 1120, "affiliate disclosure, simplepractice"),
    (".afwrap", 1120, "their bodies"),
    (".lwrap", 1120, "the home page"),
    (".tax .in", 1060, "the tax strategy hero"),
    (".adv .in", 1060, "the job advisor hero"),
    (".gro .in", 1060, "grow-your-practice"),
    (".li-wrap", 1060, "liability insurance"),
    (".dc-wrap", 1040, "the case library and all 30 case pages"),
    (".rwwrap", 1020, "working remotely"),
    (".clwrap", 1000, "cost of living"),
    # Both are already 1180. What is wrong with them is the PADDING - 30px
    # against the masthead's 26 - which put the footer, and the about and
    # contact pages, exactly 4px inboard of every other block on the site.
    # Four pixels is not visible on its own page and is very visible in the
    # vertical line running down the left edge of a scroll.
    (".ftin", 1180, "the footer, on all 158 pages - padding only"),
    (".pw", 1180, "the about and contact bands - padding only"),
]

# These already sit on the grid. Listed so the guard can prove the canon is
# what this pass claims it is, rather than a number somebody picked.
ALREADY = [".sitenav-in", ".artband .in", ".artwrap",
           ".pxband .in", ".pxwrap", ".scband .in", ".scwrap",
           ".mgband .in", ".mgwrap", ".pdband .in", ".pdwrap",
           ".hwband .in", ".hwwrap"]


def double(sel):
    """`.a .b` -> `.a.a .b.b`, so a late rule outranks a hoisted one.

    Doubling the whole string would produce `.a .b.a .b`, which matches
    nothing. Each simple selector is doubled on its own and the combinators
    are left alone."""
    return " ".join(
        (p + p) if p.startswith(".") else p for p in sel.split())


def sheet():
    o = ["<style>%s" % MARK,
         "/* One page grid: %dpx, %dpx of side padding, centred - the same box",
         "   as .sitenav-in and .ftin, so a headline starts where the logo",
         "   starts on every page. Doubled selectors because several of these",
         "   are already set from a hoisted file and a bare class would lose.",
         "   The reading measure is NOT set here; it lives in ch on the text.",
         "*/"]
    o[1] = o[1] % (CANON, PAD)
    for sel, was, _what in TARGETS:
        o.append("%s{max-width:%dpx;padding-left:%dpx;padding-right:%dpx;"
                 "margin-left:auto;margin-right:auto}  /* was %dpx */"
                 % (double(sel), CANON, PAD, PAD, was))
    # the same steps widen.py gives the masthead and the footer
    for at, w in STEPS:
        o.append("@media (min-width:%dpx){" % at)
        for sel, _w, _x in TARGETS:
            o.append("  %s{max-width:%dpx}" % (double(sel), w))
        o.append("}")
    o.append("@media (max-width:640px){")
    for sel, _w, _x in TARGETS:
        o.append("  %s{padding-left:18px;padding-right:18px}" % double(sel))
    o.append("}")
    o.append("</style>")
    return "\n".join(o)


def css_corpus():
    """Every stylesheet the site actually serves, hoisted and inline."""
    blob = []
    cssdir = os.path.join(SITE, "css")
    if os.path.isdir(cssdir):
        for f in sorted(os.listdir(cssdir)):
            if f.endswith(".css"):
                blob.append(open(os.path.join(cssdir, f),
                                 encoding="utf-8", errors="ignore").read())
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html"):
            s = open(os.path.join(SITE, f), encoding="utf-8",
                     errors="ignore").read()
            blob.extend(re.findall(r"<style>([\s\S]*?)</style>", s))
    return "\n".join(blob)


def main():
    css = sheet()
    print("one grid: %dpx + %dpx padding, the same box as the masthead" % (CANON, PAD))
    print("containers brought onto it:")
    for sel, was, what in TARGETS:
        print("  %-20s %4dpx -> %4d   %s" % (sel, was, CANON, what))

    n = 0
    for rel in sorted(os.listdir(SITE)):
        if not rel.endswith(".html"):
            continue
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        orig = s
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?", "", s)
        e = s.lower().rfind("</body>")
        if e < 0:
            print("  MISSING  %s has no </body>" % rel)
            continue
        s = s[:e] + css + "\n" + s[e:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
        n += 1
    print("\napplied on %d page(s)" % n)

    # --------------------------------------------------------------- guards
    bad = 0
    corpus = css_corpus()

    # 1. Every selector this pass overrides must still exist. A container that
    #    gets renamed would otherwise drop off the grid silently, and the only
    #    symptom would be a headline that moves - which is exactly the bug this
    #    pass exists to fix.
    for sel, was, _what in TARGETS:
        needle = sel.split()[-1]
        if needle not in corpus:
            print("GUARD: %s is no longer in the site's CSS. Either it was "
                  "renamed - in which case update TARGETS - or the container "
                  "is gone and the entry should be removed." % sel)
            bad += 1

    # 2. The canon has to be the canon. If the masthead or the footer ever
    #    stops being 1180, this pass is aligning the page to the wrong number
    #    and every content block would move together, away from the logo.
    # The masthead is set at three widths, not one - the base and two steps
    # from widen.py. All three have to be in the set this pass mirrors, or the
    # content aligns with the logo at one viewport and not at another.
    expect = {CANON} | {w for _at, w in STEPS}
    for sel in (".sitenav-in", ".ftin"):
        got = set()
        for m in re.finditer(r"([^{}]*)\{([^{}]*)\}", corpus):
            if not re.search(r"(^|,)\s*" + re.escape(sel) + r"\s*(,|$)",
                             m.group(1).replace("\n", " ")):
                continue
            w = re.search(r"max-width\s*:\s*(\d+)px", m.group(2))
            if w:
                got.add(int(w.group(1)))
        if not got:
            print("GUARD: cannot find a max-width for %s - the canon is "
                  "unverifiable" % sel)
            bad += 1
        elif got != expect:
            print("GUARD: %s is set at %s but this pass mirrors %s. Content "
                  "would line up with the masthead at some viewports and not "
                  "others - update STEPS to match _dev/widen.py."
                  % (sel, sorted(got), sorted(expect)))
            bad += 1

    # 3. One stylesheet per page, never two.
    for rel in sorted(os.listdir(SITE)):
        if not rel.endswith(".html"):
            continue
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" in s and s.count(MARK) != 1:
            print("GUARD %s: %d grid stylesheets" % (rel, s.count(MARK)))
            bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - every overridden container still exists, and the "
          "masthead and footer confirm %dpx is the canon" % CANON)


if __name__ == "__main__":
    main()
