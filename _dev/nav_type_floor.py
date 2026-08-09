#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One label size, not nine. A 10.5px floor for the site's small-caps labels.

WHAT THE AUDIT FOUND

Asked to check the layout against good UI practice, a sweep of the rendered
pages measured the computed font size of every leaf element on eight
representative pages. The chrome and the labels came back like this:

    9.0px   the arrow captions in a flow graphic
    9.2px   .fchip, .chk
    9.4px   .tsk            "In short"
    9.5px   .np-col h5      "Calculators", "Money", "Licensure" - the
                            navigation panel's column headings, on 164 pages
    9.5px   .lkind          "Tool"
    9.6px   .pdr span (150 of them), .tsn, .pdfig, .pdyr, .np, .uk, .np-all
    9.8px   table <th>, .artnext b
    10.0px  .pdcity, .pdgo, .sitenav-sub, .tag, .rm, .tsall, .eap-rate-h
    10.2px  a <dt>
    10.5px  .rm span, h5, .ig-cap, .statcard-label, .ltag, .kick, .leyebrow …

**Nine different sizes for one thing.** Everything in that list is the same
kind of object: an uppercase, letter-spaced, mono or heavy small-caps label
naming the thing beside it. The 10.5px group is the largest and is clearly the
size the design intends. The rest are accidents - a value typed once in one
component and never reconciled.

The worst of them is not the smallest. It is `.np-col h5` at 9.5px, because
those are the only words telling a reader which group of navigation links they
are looking at, and they are on every page at every width.

WHAT THIS DOES

Raises everything in that scatter to **10.5px**, the size the design already
uses. It does not introduce a new size; it removes eight accidental ones.

`_dev/mobile_floor.py` already sets a 12px floor for sentence-carrying text at
phone widths only, and that reasoning - desktop typography is a design decision
and a blanket floor would flatten it - is right for prose. It is wrong for
chrome. A navigation label is functional text, it is the same size on a
27-inch display as on a phone, and no design intent is served by making it
unreadable on both.

WHAT IT DELIBERATELY LEAVES ALONE

Colour, weight, case, tracking and spacing. Single-letter class names like
`.l`, `.t`, `.c`, `.o` and `.n`, which are used for different things on
different pages and are not safe to target globally. And anything already at
10.5px or above.

Idempotent, guarded. The guard reads the site's stylesheets rather than the
CSS this file wrote, and says so when the override stops doing any work -
because a pass that overrides a rule which now agrees with it is dead weight
and should be retired rather than left in the pipeline looking busy.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/nav_type_floor.py */"
FLOOR = 10.5

# selector, measured size, what it is
# Every one of these was measured in a browser, not read out of a stylesheet.
RAISE = [
    (".navpanel .np-col h5", 9.5, "nav panel column headings, all 164 pages"),
    (".np-promo .np-all", 9.6, "'The hub' in the nav panel"),
    (".sitenav-sub", 10.0, "'Supporting California therapists'"),
    # Bare, not `.tsshort .tsk`. The In-short kicker also appears outside that
    # wrapper on five pages, and scoping the selector to the wrapper left those
    # five at 9.4px - which the re-measure caught.
    (".tsk", 9.4, "'In short'"),
    (".tsn", 9.6, "the numerals in an on-this-page rail"),
    (".pdr span", 9.6, "the PsyD row labels - 150 of them"),
    (".pdfig", 9.6, "PsyD figures"),
    (".pdyr", 9.6, "PsyD years"),
    (".pdcity", 10.0, "PsyD cities"),
    (".pdgo", 10.0, "PsyD links"),
    (".pdgone i", 9.6, "PsyD closed-programme notes"),
    (".fchip", 9.2, "filter chips"),
    (".chk", 9.2, "checklist marks"),
    (".lkind", 9.5, "'Tool' on the home page cards"),
    (".np", 9.6, "nav panel small text"),
    (".uk", 9.6, "uplink kickers"),
    (".tag", 10.0, "tags"),
    (".tsall", 10.0, "'see all' links"),
    (".eap-rate-h", 10.0, "EAP rate table headings"),
    (".artnext b", 9.8, "next-article labels"),
    (".arr em", 9.0, "the arrow captions in ig-flow"),
    (".soon", 10.0, "'coming soon' markers"),
    # `table th` is not a class, so `double()` leaves it alone and it loses to
    # every `.dc-t th` / `.tbl th` rule on the site. Named explicitly, at the
    # specificity those rules actually use.
    (".dc-t th", 9.8, "case-library table headings"),
    (".tbl th", 9.8, "article table headings"),
    (".eap-tbl th", 9.8, "the EAP rate table"),
    (".li-tbl th", 9.8, "the liability table"),
    (".pdtbl th", 9.8, "the PsyD table"),
]


def double(sel):
    """`.a .b` -> `.a.a .b.b`. The sizes being overridden live in hoisted
    files whose names are content hashes, and `extract_css.py` renames them on
    every run - so an edit at source survives until the next build and a late
    doubled selector does not care."""
    return " ".join((p + p) if p.startswith(".") else p for p in sel.split())


def sheet():
    o = ["<style>%s" % MARK,
         "/* One label size. Eight accidental sizes between 9.0 and 10.2px,",
         "   all naming the thing beside them, all raised to the 10.5px the",
         "   design already uses everywhere else. Size only - colour, weight,",
         "   case, tracking and spacing are left exactly as they were. */"]
    for sel, was, what in RAISE:
        o.append("%s{font-size:%spx}  /* was %spx - %s */"
                 % (double(sel), FLOOR, was, what))
    o.append("</style>")
    return "\n".join(o)


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in ("money", "licensure", "getting-paid", "practice", "training"):
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    css = sheet()
    print("one label size: %d selector(s) raised to %spx" % (len(RAISE), FLOOR))
    for sel, was, what in RAISE[:6]:
        print("  %-24s %4spx -> %s   %s" % (sel, was, FLOOR, what))
    print("  ... and %d more" % (len(RAISE) - 6))

    n = 0
    for rel in pages():
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
    corpus = []
    cssdir = os.path.join(SITE, "css")
    if os.path.isdir(cssdir):
        for f in sorted(os.listdir(cssdir)):
            if f.endswith(".css"):
                corpus.append(open(os.path.join(cssdir, f), encoding="utf-8",
                                   errors="ignore").read())
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" not in s:
            continue
        corpus.append("".join(re.findall(r"<style>([\s\S]*?)</style>", s)))
        if s.count(MARK) != 1:
            print("GUARD %s: %d stylesheets" % (rel, s.count(MARK)))
            bad += 1
    blob = "\n".join(corpus)

    # A selector that no longer appears anywhere is styling nothing, and a
    # list of dead selectors is how a floor quietly stops being a floor.
    missing = [sel for sel, _w, _x in RAISE
               if sel.split()[-1].lstrip(".") not in blob
               and sel.split()[-1] not in ("th",)]
    if missing:
        print("  note: %d selector(s) no longer appear in the site's CSS and "
              "may be styling nothing: %s" % (len(missing), ", ".join(missing)))

    # And if every upstream size is already at or above the floor, this pass
    # is redundant. Say so rather than sit in the pipeline looking busy.
    still = []
    for sel, was, _x in RAISE:
        leaf = re.escape(sel.split()[-1])
        for m in re.finditer(leaf + r"\s*\{[^}]*font-size:\s*([\d.]+)px", blob):
            if float(m.group(1)) < FLOOR:
                still.append(sel)
                break
    if not still:
        print("  note: nothing upstream is under %spx any more. If the sizes "
              "were fixed at source, retire this pass." % FLOOR)
    else:
        print("  %d of %d selector(s) still set below the floor upstream, so "
              "the override is doing real work" % (len(still), len(RAISE)))

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - one stylesheet per page, and the floor still has "
          "something to raise")


if __name__ == "__main__":
    main()
