#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Narrow the reading cards to the column they actually hold.

Why. `widen.py` grew centred containers to 1320px at >=1500 and 1560px at >=1900.
That was right for card grids, which fill the extra width with more columns. It
was wrong for cards that hold nothing but prose: they became 1,500px boxes around
a 464px paragraph, and `measure.py` (which caps the reading measure) makes that
gap visible rather than causing it. A text card should be as wide as the text.

The fix is the opposite of `widen.py`: cap the CARD, centre it. Not to widen the
text, which would undo the measure cap and put us back at 230-character lines.

A CORRECTION TO THE AUDIT THAT COMMISSIONED THIS. The first pass reported eight
under-filled containers. It measured **the widest single child** against the
container, which makes any multi-column grid look 1/n filled: `.lkitrows` is a
four-column grid whose cells are each 25% of a full row, and it was reported as
"25% filled" when it is 100% filled. Re-measured with the bounding box of ALL
children — the correct metric — index, tools, simulator, job advisor and
3,000-hours all pass, and only these four are real:

    .txb     tax strategy, 10 instances   32% at 1920   1,462px around 464px of prose
    .rwcard  working remotely, 3          40%           1,456px around 580px
    .clnote  cost of living, 2            23%           1,476px around 345px
    .clbig   cost of living, 1            66%           figures cluster left

Any future check must use the bounding box of all children. Measuring the widest
one produces confident, wrong answers about every grid on the site.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/fill.py */"
END = "/* end fill */"
SKIP = ("tycoon.html", "local.html", "concepts.html")

CSS = """
/* Reading cards. Width chosen so the capped prose inside fills ~90% of the
   card's inner box rather than ~30% of it.
   NOT centred. Centring was tried first and looked worse: the section <h2> above
   these cards is left-aligned in the same wrapper, so a centred card sat 400px to
   the right of its own heading. Left-aligned, the heading and the column share an
   edge, which is what makes it read as a document rather than as a mistake. */
.txb, .clnote{max-width:592px}
.rwcard{max-width:680px}

/* .clbig is a flex row: three small figures then a legend. Letting the legend
   absorb the slack does NOT work here and it is worth saying why — the legend is
   a <p>, so measure.py caps it at 62ch, and no amount of `flex-grow` makes a box
   exceed its own max-width. Correct behaviour: a legend should not run 1,000px.
   So cap the row instead, same as the reading cards above. */
.clbig{max-width:1040px;align-items:baseline}

/* Below the widen.py breakpoint these caps are wider than the container, so the
   rule is inert on laptops and phones. Stated so nobody adds a media query that
   duplicates it. */
"""


def main():
    changed = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in SKIP:
            continue
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()

        s2 = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?" + re.escape(END) + r"</style>\n?",
                    "", s, flags=re.S)
        if "</body>" not in s2:
            continue

        # only touch pages that actually contain one of these
        if not any(c in s2 for c in ("txb", "clnote", "rwcard", "clbig")):
            if s2 != s:
                open(path, "w", encoding="utf-8").write(s2)
            continue

        s2 = s2.replace("</body>", "\n<style>" + MARK + CSS + END + "</style>\n</body>", 1)
        if s2 != s:
            open(path, "w", encoding="utf-8").write(s2)
            changed += 1

    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in SKIP:
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        assert s.count(MARK) <= 1, "%s has %d fill blocks" % (f, s.count(MARK))

    print("%d page(s) filled" % changed)


if __name__ == "__main__":
    main()
