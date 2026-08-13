#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A fourth door on the home page, for the people who have not started yet.

WHAT WAS MISSING

"Who this is for" offered three cards - registered associates, solo private
practice, practices with room to grow. All three assume the reader is already
in the profession. Somebody deciding whether to become an MFT at all had no
entry point on the home page.

That is the largest single body of work on the site sitting behind no door:
sixty-six school pages, the MFT program directory, the PsyD directory, the
route guide and the cost-of-living comparison. And `_dev/stage_router.py` has
had a matching stage - "Choosing a program / You have not started yet" - the
whole time. The tab existed; the card did not.

It also happens to be the top of the funnel for everything else on the site. A
reader who arrives while choosing a program is the same reader who needs the
hours calculator in two years and the tax pages in six.

WHY A PASS RATHER THAN AN EDIT

The three existing cards are hand-written in `index.html` and no pass owns
them, which is how the section stayed three-wide through two years of the site
growing. A pass makes the fourth card survive the next person who regenerates
the home page, and its guard makes the omission loud if the block is ever
rewritten.

THE GRID

Four cards in a three-column grid leaves one alone on a second row. The section
moves to `auto-fit` with a floor of 235px, so it lays out four across on a wide
screen, two-by-two on a tablet and one per row on a phone - and, unlike a fixed
`repeat(4, ...)`, it does not have to be edited again if a fifth audience is
ever added.

Runs BEFORE `_dev/stage_router.py`, which wraps each card in a `.srpair` and
adds the "Everything for this situation" link beneath it. Inserting after that
would produce a card with no link under it.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
HOME = os.path.join(SITE, "index.html")
MARK = "<!-- _dev/home_doorway.py -->"
END = "<!-- /home_doorway -->"
CSSMARK = "/* _dev/home_doorway.py */"

LABEL = "Considering the path"
TARGET = "mft-programs-california.html"

CARD = (MARK + '<a class="laud" href="' + TARGET + '">'
        "<b>" + LABEL + "</b>"
        "<span>Weighing an MFT against a doctorate, comparing programs, and "
        "working out whether the California arithmetic adds up.</span>"
        "<em>Start with the programs &rarr;</em></a>" + END)

CSS = ("<style>" + CSSMARK + """
/* Four cards, not three. auto-fit rather than repeat(4,...) so a fifth
   audience would not need this rule edited again. Doubled selector because the
   3-column rule lives in the home page's own inline stylesheet and a single
   class would tie on specificity and lose on source order. */
.lgrid.lg3.lg3{grid-template-columns:repeat(auto-fit,minmax(235px,1fr))}
@media (max-width:760px){.lgrid.lg3.lg3{grid-template-columns:minmax(0,1fr)}}
</style>""")


def main():
    if not os.path.exists(HOME):
        sys.exit("home_doorway: index.html is missing")
    s = open(HOME, encoding="utf-8").read()
    # Rollout step 4 (Aug 2026): the landing was rebuilt to option A by
    # _dev/build_home.py and the audience cards this pass decorated no
    # longer exist. The six claim rows carry the doorway's job now. No-op
    # rather than retire, so an old index restored from a snapshot still
    # gets its doorway back.
    if 'class="bc2 home"' in s:
        print("home_doorway: option-A home present - nothing to do")
        return
    orig = s

    # our own output out first, in both possible shapes: bare, and already
    # wrapped in a .srpair by stage_router on a previous full run
    s = re.sub(r'<div class="srpair">\s*' + re.escape(MARK) + r"[\s\S]*?</div>",
               "", s)
    s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), "", s)
    s = re.sub(r"<style>" + re.escape(CSSMARK) + r"[\s\S]*?</style>", "", s)

    if LABEL in s:
        sys.exit("home_doorway: %r is already on the page outside this pass's "
                 "markers. Two cards with the same label would both be wrapped "
                 "by stage_router and the reader would see it twice." % LABEL)

    # First child of the audience grid: this audience comes before the others
    # in time, so it comes before them on the page.
    # `<div class="lgrid lg3">` appears more than once on the home page - the
    # promise block uses the same grid - and anchoring on the first match put
    # the card in the wrong section entirely. Anchored on the heading that
    # names the section, then the first grid after it.
    head = re.search(r"Who this is for", s)
    m = re.search(r'<div class="lgrid lg3">', s[head.end():]) if head else None
    if not head or not m:
        sys.exit("home_doorway: could not find the audience grid - the "
                 "\"Who this is for\" heading or the grid after it has been "
                 "renamed. Do not guess a new anchor, look at the page.")
    at = head.end() + re.search(r'<div class="lgrid lg3">',
                                s[head.end():]).end()
    s = s[:at] + CARD + s[at:]

    e = s.lower().rfind("</body>")
    s = s[:e] + CSS + "\n" + s[e:]

    if s != orig:
        open(HOME, "w", encoding="utf-8").write(s)
    print("home page: the fourth door added, pointing at %s" % TARGET)

    # --------------------------------------------------------------- guards
    bad = 0
    s = open(HOME, encoding="utf-8").read()

    if s.count(MARK) != 1:
        print("GUARD: %d copies of the card" % s.count(MARK)); bad += 1
    if s.count(CSSMARK) != 1:
        print("GUARD: %d stylesheets" % s.count(CSSMARK)); bad += 1
    if not os.path.exists(os.path.join(SITE, TARGET)):
        print("GUARD: the card points at %s, which is not on the site" % TARGET)
        bad += 1

    h2 = s.find("Who this is for")
    seg = s[h2:s.find("</section>", h2)] if h2 >= 0 else ""
    n = len(re.findall(r'<a class="laud"', seg))
    if n != 4:
        print("GUARD: %d audience card(s) in the grid, expected 4" % n)
        bad += 1

    # The router has to have a stage for it, or the "Everything for this
    # situation" link stage_router adds would point at a tab that does not
    # exist. Checked against the router's source, not against a memory of it.
    router = open(os.path.join(HERE, "stage_router.py"), encoding="utf-8").read()
    if '("%s", "program")' % LABEL not in router:
        print("GUARD: stage_router.py has no HOME_ROUTES entry for %r, so this "
              "card would get no situation link" % LABEL)
        bad += 1
    if '("program", "Choosing a programme"' not in router \
            and '("program", "Choosing a program"' not in router:
        print("GUARD: stage_router.py has no `program` stage to route into")
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - four cards, one stylesheet, and a router stage "
          "behind the new one")


if __name__ == "__main__":
    main()
