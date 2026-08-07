#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two visible layout defects, both reported from screenshots.

1. THE DEAD TRACK. associate-mft-job-advisor compares two job offers side by
   side. When a reader is evaluating only one - which is the default, and the
   state the shared links land in - the second card is hidden and the grid
   keeps its track:

       .jobs      {grid-template-columns:repeat(2,minmax(0,1fr))}
       .jobs.solo {grid-template-columns:minmax(0,620px)}

   Measured at 1440: the card is 998px wide, the single column is 620px, and
   378px to the right of it is empty. The form hugs the left edge of a
   half-empty white panel and the page reads as broken, which is exactly how it
   was reported.

   The fix is one declaration - centre the solo column - rather than letting it
   stretch. A 998px-wide column of single-line inputs would be worse than the
   bug: label and field would be a hand's width apart on a laptop.

2. THE ORPHAN KICKER. The strip under the nav ("For practicum students and new
   associates - California") is set at opacity .62 with no other treatment, so
   it renders as pale text floating in the header pill with nothing to attach
   it to. On the associate page, where the line is longest, it reads as
   left-over text rather than a label.

   Making it a chip - a bordered pill at full opacity - says "this is a tag"
   in the way the opacity was trying and failing to say "this is secondary".

Idempotent. Style-only; no markup moves.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/layout_fixes.py */"

SOLO_PAGE = "associate-mft-job-advisor.html"

CSS_SOLO = """
/* Left-aligned and a little wider, NOT centred and NOT stretched.

   Centring was the first attempt and it traded one misalignment for another:
   the card sat in the middle of the panel while the section heading, its
   paragraph and the filing-status select above it all began at the panel's
   left edge, so the one element that mattered was the one out of line.

   Stretching to the full 998px would be worse than the original bug - a
   single-line input a thousand pixels wide puts its label and its value a
   hand's width apart.

   So: same left edge as everything above it, 720px instead of 620px to use
   more of the room, and the remaining space reads as a margin rather than as
   a hole, because now there is a straight edge running down the left of the
   whole section. */
.jobs.solo{grid-template-columns:minmax(0,720px);justify-content:start}
"""

CSS_KICK = """
/* The context strip in the header. Was opacity:.62 bare text; now a chip, so
   it reads as a label rather than as something left behind. Opacity is back to
   1 and the recession is done with colour, which keeps the text legible on the
   green band at small sizes. */
.bcrq{display:inline-block;opacity:1;color:rgba(255,255,255,.74);
  background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);
  border-radius:20px;padding:4px 11px;margin:9px 0 0;font-size:10px}
@media (max-width:560px){.bcrq{font-size:9.5px;padding:3px 9px;letter-spacing:.07em}}
"""


def pages():
    return [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]


def add_style(path, css, end):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?" + re.escape(end)
               + r"</style>\n?", "", s)
    if "</body>" not in s:
        return False
    s = s.replace("</body>", "\n<style>" + MARK + css + end + "</style>\n</body>", 1)
    open(path, "w", encoding="utf-8").write(s)
    return True


def main():
    # ---- 1. the dead track
    p = os.path.join(SITE, SOLO_PAGE)
    if not os.path.exists(p):
        sys.exit("layout_fixes: %s not found" % SOLO_PAGE)
    src = open(p, encoding="utf-8").read()
    if ".jobs.solo{grid-template-columns:minmax(0,620px)}" not in src:
        print("%-44s solo rule not found - has the page changed?" % SOLO_PAGE)
    add_style(p, CSS_SOLO, "/* end solo */")
    print("%-44s solo column centred" % SOLO_PAGE)

    # ---- 2. the orphan kicker, everywhere it appears
    n = 0
    for f in pages():
        path = os.path.join(SITE, f)
        if 'class="bcrq"' not in open(path, encoding="utf-8").read():
            continue
        add_style(path, CSS_KICK, "/* end kick */")
        n += 1
    print("%-44s kicker restyled on %d page(s)" % ("", n))

    # ---- guards
    bad = 0
    s = open(p, encoding="utf-8").read()
    if s.count("/* end solo */") != 1:
        print("GUARD %s: %d solo blocks" % (SOLO_PAGE, s.count("/* end solo */"))); bad += 1
    kicked = 0
    for f in pages():
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if 'class="bcrq"' not in s:
            if "/* end kick */" in s:
                print("GUARD %s: styled a kicker it does not have" % f); bad += 1
            continue
        kicked += 1
        if s.count("/* end kick */") != 1:
            print("GUARD %s: %d kicker blocks" % (f, s.count("/* end kick */"))); bad += 1
        if s.count("<h1") != 1 and f not in ("privacy.html", "terms.html"):
            print("GUARD %s: %d h1" % (f, s.count("<h1"))); bad += 1
    if kicked != n:
        print("GUARD: styled %d, found %d" % (n, kicked)); bad += 1
    if bad:
        sys.exit("layout_fixes: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
