#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cap the reading measure. One rule, every page, idempotent.

Why. Prose on this site had no maximum width, so line length was whatever the
container happened to be. Measured with the real fonts at 1280/1512/1920:
`therapist-working-remotely` ran 81 characters a line at 1280 and **186 at 1920**
— it more than doubled. Tax strategy, the job advisor and grow all carried
outliers over 230. Comfortable reading is 45-75 characters; 80 is the outer edge.
Nobody reads a 230-character line, because the eye loses the return sweep.

This is the other half of `widen.py`. That pass grew centred containers to 1320px
at >=1500 and 1560px at >=1900, which was right for card grids, but it is a
container-level pass and cannot know what is inside. Everything it widened that
held plain prose simply got longer lines.

THE `ch` TRAP, which cost a round trip. **The CSS `ch` unit is the advance width
of the digit 0, not the average character.** In Fraunces and Inter the 0 is about
28% wider than the average lowercase letter, so `max-width:76ch` renders roughly
**97** real characters. The audit document that recommended this fix failed its
own check for exactly this reason. Multiply the target by 0.78: for a 75-character
line, write 58ch. Never trust the declared value — measure the rendered text.

Safety. `max-width` can only ever make a box narrower, so a blanket rule cannot
overflow anything or push content off-screen. The two real risks are (a) a <p>
used as a layout row (a centred CTA), which is excluded by class below, and (b) a
<p> inside a container that centres its children, which is handled by giving
centred blocks `margin-inline:auto` so the cap does not shove them left.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/measure.py */"
END = "/* end measure */"

SKIP = ("tycoon.html", "local.html", "concepts.html")

# 58ch ~= 75 rendered characters at these fonts (the 0.78 factor above).
# 62ch ~= 80 for the small print, which is set smaller and reads in shorter bursts.
CSS = """
/* Reading measure. See the module docstring: `ch` is the width of "0", NOT the
   average character, so these numbers are ~0.78 of the character count wanted.
   58ch renders ~75 characters; 62ch renders ~80. */
.pw p, .pw li, section p, section li, main p, main li,
article p, article li, .slab p, .slab li, .card p, .card li{
  max-width:58ch}

/* Small print and captions: set smaller, read in short bursts, so a slightly
   longer line is fine and a very short one looks broken. */
.pw p.fine, .pw p.disc, .pw p.pay-note, .pw p.clfine, .pw p.rwfine,
.pw p.jobfoot, .pw p.waitnote, .pw p.cf-fine, .pw p.lnote, .pw p.cleg,
p.fine, p.disc, p.pay-note, p.clfine, p.rwfine, p.jobfoot, p.waitnote,
p.cf-fine, p.lnote, p.cleg, p.sub, p.pn{
  max-width:62ch}

/* Layout rows that happen to be <p>. These are not prose and must keep their
   full width or the button inside them jumps left. */
.pw p.ctarow, p.ctarow, p.btnrow, p.actions, p[class*="cta"]{
  max-width:none}

/* A centred block that gets a max-width would otherwise pin to the left edge of
   its container, which reads as a mistake. Re-centre it. */
.pw p[align="center"], .tac p, .center p, .hero p.deck, .band p.deck{
  margin-left:auto;margin-right:auto}

/* Table cells and stat labels are sized by their own grid; a measure cap on
   them fights the column. */
td p, th p, .fig p, .stat p, .kpi p{max-width:none}

/* Phones are already far below the cap, so the rule is inert there. Stated so
   nobody adds a redundant media query later. */
"""


def main():
    changed, skipped = 0, 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in SKIP:
            continue
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()

        # idempotent: drop any previous block before adding this one
        s2 = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?" + re.escape(END) + r"</style>\n?",
                    "", s, flags=re.S)

        if "</body>" not in s2:
            print("%-44s no </body>, skipped" % f)
            skipped += 1
            continue

        s2 = s2.replace("</body>",
                        "\n<style>" + MARK + CSS + END + "</style>\n</body>", 1)
        if s2 != s:
            open(path, "w", encoding="utf-8").write(s2)
            changed += 1

    # ---- guards. One block per page, and never two.
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in SKIP:
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        n = s.count(MARK)
        assert n == 1, "%s has %d measure blocks" % (f, n)

    print("%d page(s) capped, %d skipped" % (changed, skipped))


if __name__ == "__main__":
    main()
