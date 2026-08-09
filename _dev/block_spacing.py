#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give the injected blocks a relationship to whatever ends up next to them.

THE DEFECT

On the insurance page the "In short" card sat with **zero** pixels between its
bottom border and the paragraph underneath - close enough that the paragraph
overlapped the card's own 4px offset shadow. It read as broken, and it was
reported as "the fonts too close, this looks defective".

THE CAUSE IS STRUCTURAL, NOT COSMETIC

`.tsshort` is emitted with `margin-bottom:0`. That is survivable everywhere it
had been used before, because the element that happened to follow it brought its
own top margin - 17px on the directory pages. It is not survivable anywhere the
next element has `margin-top:0`, which is every hand-built page with a reset.

So the card was never spaced. It was **relying on its neighbour to space it**,
and the day it landed next to a neighbour that did not, it collapsed. A block
that is injected into pages it has never seen cannot depend on what follows it.

Two things follow from that, and this pass does both:

1. Every injected block owns the space beneath it, rather than borrowing it.
2. A block with a solid offset shadow needs clearance for the shadow as well as
   for the type. `.tsshort` casts 4px down; margin that ignores it leaves text
   sitting on the shadow, which is exactly the overlap that looked defective.

Deliberately narrow: it sets bottom margins on the blocks the passes inject and
touches nothing else. It is not a spacing system.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "/* _dev/block_spacing.py */"

# (selector, margin, why)
BLOCKS = [
    (".tsshort", "26px", "the In short card - 4px of shadow plus real air"),
    (".tsmeta", "22px", "the provenance strip"),
    (".tsfoot", "0", "sits directly on the signup band, which footer_order owns"),
    (".tsupd", "22px", "the what-changed disclosure"),
    (".uplink", "26px", "the More on this block"),
    (".fixrow", "22px", "the correction row"),
]

CSS = """<style>%(mark)s
/* Every block below is injected by a pass into pages it has never seen, so it
   owns the space beneath it instead of borrowing it from whatever follows.
   `.tsshort` shipped with margin-bottom:0 and a 4px offset shadow, and landed
   next to a paragraph with margin-top:0 - the text sat on the shadow. */
%(rules)s
/* Nothing may butt straight up against the card either. */
.tsshort + *, .tsmeta + *, .uplink + *{margin-top:0}
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
    # Tripled, for the reason this project has now hit five times: a late
    # override of an existing class needs more class tokens than the longest
    # descendant chain that could match it.
    rules = "\n".join(
        "%s{margin-bottom:%s}   /* %s */"
        % ("." + ".".join([sel.lstrip(".")] * 3), mb, why)
        for sel, mb, why in BLOCKS)
    return CSS % {"mark": MARK, "rules": rules}


def main():
    css = build_css()
    print("blocks given their own bottom margin:")
    for sel, mb, why in BLOCKS:
        print("  %-10s %-6s %s" % (sel, mb, why))

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
    for sel, _mb, _w in BLOCKS:
        tripled = "." + ".".join([sel.lstrip(".")] * 3)
        if tripled not in css:
            print("GUARD: %s did not triple" % sel)
            bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
