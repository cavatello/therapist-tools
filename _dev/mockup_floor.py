#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The two mockups are noindex. They are not unpublished.

WHAT THIS IS FOR

After the design audit closed, every contrast and overflow finding left on
therapistsupport.org sat on two files:

    tycoon.html     26 text/background pairs under 4.5:1, at all five widths
    concepts.html   a 3-column table 416px wide in a 390px viewport

Both are visual-direction sketches. Both carry `noindex` and are linked only
from `mock/`. Neither is a page the site sends a reader to - and both are
SERVED, at a stable URL, over the same certificate as everything else. A sketch
nobody links is still a page somebody can open, and "it is only a mockup" is
the argument that leaves 26 unreadable labels on the internet.

So they are fixed rather than excused. What is NOT done here is any change to
what the mockups are FOR: the purple stays purple, the coin stays gold, the
park-map aesthetic is untouched. Only the light end of each pair moves, and
only far enough to clear 4.5:1 - measured against the surface the colour
actually lands on, in a browser, not estimated from the stylesheet.

THE SEVENTH COLLISION, AGAIN, ON A PAGE WITH NO BODY CLASS

`.stat .n` computes `#8A6516` on tycoon's `#1F1440` card: 3.21:1. The page's
own rule says `color:var(--dim)` and loses, because a site-wide pass emits

    .src.src.src, .n.n.n{color:#8A6516}

in `css/314849add915.css` - a class-tripled amber written for a LIGHT surface,
which is correct everywhere it was aimed and wrong on a dark card. One class,
two surfaces, for the eighth time in this repository.

`surface_fix.py` is the tool for exactly this and could not be used: it scopes
each rule to a body class, and **tycoon.html has no class on its body at all**.
Adding one would pull the whole `body.house` cascade onto a page that is
deliberately outside it. So the override is written here, into the page, at a
specificity that beats a tripled class (four tokens), and this pass runs after
the palette passes and after `surface_fix.py` so nothing downstream re-darkens
what it sets.

WHY THE COLOURS ARE THE ONES THEY ARE

  --dimmer  #7C6BA8 -> #A093C1   one muted purple, not four. It lands on four
                                 different dark surfaces (#3A1E5C, #2B1B4D,
                                 #241640, #1F1440); this value clears 4.5 on
                                 the LIGHTEST of them (4.89) and has more
                                 margin on the rest (up to 6.04).
  .n        #8A6516 -> #F6C560   the house gold, already used on this site for
                                 `.hh-chip`. 10.6:1 on the card, and it is
                                 what the coin motif wanted in the first place.
  mint      #CDEBD8 -> #F6F8F6   the house `--paper`. 4.73:1 on the schedule
            #DFF3E6 -> #F6F8F6   green, and two fewer off-palette colours on a
                                 page that holds most of the site's remaining
                                 123.

THE TABLE

`concepts.html`'s comparison table has three columns of sentences and a
min-content width the viewport cannot meet. `mobile_floor.py` already gives
cells `overflow-wrap:break-word` rather than `anywhere`, deliberately - see its
docstring for the phone rendering of "Head / way" that `anywhere` produced - so
the columns keep their natural widths and the table stays 416px. The house
answer for a table that cannot shrink is a scroller, and that is what this
adds: a wrapper element, so the table keeps its table formatting context
instead of being made `display:block`.

Idempotent: the style block carries a marker and is replaced; the wrapper is
added only when it is absent.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/mockup_floor.py */"

# fg -> replacement, with the surface it was measured against and the ratio
# BEFORE and AFTER. Kept here so the next reader does not have to re-measure
# to know whether a change is safe.
TYCOON_CSS = """<style>%s
/* One muted purple for every dark surface on the page, replacing a value that
   ran 2.98-3.67:1 depending on which card it landed on. Declared on :root
   after the page's own :root, which is the whole override. */
:root{--dimmer:#A093C1}
/* `.n.n.n` in a site stylesheet paints this the light-surface amber. Four
   tokens to outrank three. See this pass's docstring. */
.n.n.n.n{color:#F6C560}
/* The schedule strip: pale mint on #2E7D4F was 3.96 and 4.35. --paper is
   4.73 and is a colour the site already owns. */
.sc-time.sc-time{color:#F6F8F6}
.sched-legend.sched-legend{color:#F6F8F6}
/* The standing note under the board. 2.98:1 on #3A1E5C. */
.footnote.footnote{color:#A093C1}
</style>
""" % MARK

CONCEPTS_CSS = """<style>%s
/* Three columns of sentences whose min-content width exceeds a phone. The
   house answer is a scroller, not a narrower table - see the docstring. */
.tblscroll{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%%}
.tblscroll>table{min-width:100%%}
</style>
""" % MARK

EXISTING = re.compile(r"\n?<style>" + re.escape(MARK) + r"[\s\S]*?</style>\n?")


def put(rel, css):
    p = os.path.join(SITE, rel)
    if not os.path.exists(p):
        print("  SKIP %s is not on disk" % rel)
        return False
    s = open(p, encoding="utf-8").read()
    orig = s
    s = EXISTING.sub("\n", s)
    i = s.lower().rfind("</body>")
    if i < 0:
        print("  SKIP %s has no closing body" % rel)
        return False
    s = s[:i] + css + s[i:]
    if s != orig:
        open(p, "w", encoding="utf-8").write(s)
        return True
    return False


def wrap_tables(rel):
    """Put every bare table in a horizontal scroller. Idempotent."""
    p = os.path.join(SITE, rel)
    if not os.path.exists(p):
        return 0
    s = open(p, encoding="utf-8").read()
    n = 0
    out = []
    i = 0
    while True:
        j = s.find("<table", i)
        if j < 0:
            out.append(s[i:])
            break
        k = s.find("</table>", j)
        if k < 0:
            out.append(s[i:])
            break
        k += len("</table>")
        before = s[:j]
        # already wrapped?
        if re.search(r'<div class="tblscroll">\s*$', before):
            out.append(s[i:k])
            i = k
            continue
        out.append(s[i:j])
        out.append('<div class="tblscroll">' + s[j:k] + "</div>")
        n += 1
        i = k
    if n:
        open(p, "w", encoding="utf-8").write("".join(out))
    return n


def main():
    a = put("tycoon.html", TYCOON_CSS)
    b = put("concepts.html", CONCEPTS_CSS)
    w = wrap_tables("concepts.html")
    print("tycoon.html %s, concepts.html %s, %d table(s) wrapped"
          % ("written" if a else "unchanged",
             "written" if b else "unchanged", w))

    bad = 0
    for rel in ("tycoon.html", "concepts.html"):
        p = os.path.join(SITE, rel)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        if s.count(MARK) != 1:
            print("GUARD %s carries the block %d time(s)" % (rel, s.count(MARK)))
            bad += 1
        if 'rel="stylesheet"' in s[s.rfind(MARK):]:
            print("GUARD %s: a stylesheet is linked after the block" % rel)
            bad += 1
        if s.count("<div") != s.count("</div>"):
            print("GUARD %s: %d open div against %d close"
                  % (rel, s.count("<div"), s.count("</div>")))
            bad += 1
    s = open(os.path.join(SITE, "concepts.html"), encoding="utf-8").read()
    if s.count("<table") != s.count('<div class="tblscroll">'):
        print("GUARD concepts.html: %d table(s), %d scroller(s)"
              % (s.count("<table"), s.count('<div class="tblscroll">')))
        bad += 1
    if bad:
        sys.exit("%d problem(s)" % bad)
    print("guard clean - one block on each mockup, every table in a scroller")


if __name__ == "__main__":
    main()
