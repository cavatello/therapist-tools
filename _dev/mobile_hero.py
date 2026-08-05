#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make the heroes fit a phone.

Measured at 390x844 before this pass, with every child of the hero over 24px
tall listed (node _dev/... see claude/hero-design-rules.md):

  grow    hero 850px   h1 87 · lede 195 · CTA row 150 · proof panel 226 · pad 84
  advisor hero 844px   h1 87 · lede  98 · CTA row  97 · art SVG 180 · panel 134
  amft    hero 760px   same shape

A hero that is 100% of the screen is not a hero, it is a page. The reader
arrives, reads, scrolls, and only then finds out the thing is interactive.

Three costs, and what each is worth on a phone:

1. THE ART. 180px of decorative SVG. It is illustration - the four-gates drawing
   on the associate pages restates a concept the page then explains in words. On
   a desktop it sits beside the text and costs nothing; on a phone it stacks and
   costs a fifth of the screen. Hidden below 560px.

2. THE JUMP LINKS. Three pills at 13.5px with 11x18 padding wrap onto three
   rows. They are navigation and they are MORE useful on a phone than on a
   desktop, because the scroll is longer - so they are kept, not hidden, and
   made small enough to sit on two rows. The primary keeps its size; only the
   secondary ghosts shrink, so the thing you are meant to press stays the thing
   that looks pressable.

3. THE PROOF PANEL. The two live figures are the hook and they stay. What goes
   is the air around them: 20/22 padding and 11px row gaps were drawn for a
   desktop column.

What is deliberately NOT done here: nothing is truncated, no sentence is
clamped, and no figure is dropped. A phone gets the same information; it gets
it in less vertical space.

Idempotent. Run last, after breadcrumbs.py and hero_notes.py, so this stylesheet
sits after every other rule in the document - at equal specificity the last rule
wins, and this codebase has shipped that bug three times.
newsletter.html was the worst on the site at 159% of a phone screen - 1346px
of hero, in this order: headline, a 240px deck, a 323px list of what you get,
THEN the form, then a 354px illustration. The reader had to scroll past
everything the page was arguing for before reaching the box it wanted them to
type in, and the email field sat at y=872, just below the fold. Same treatment:
the illustration goes, the form comes up under the deck, and the list of what
you get sits underneath it - where it reads as reassurance after the decision
rather than a sales pitch before it.

Note that these stylesheets are written PER PAGE, so a rule here only ever
applies to the page it is attached to. That is why the newsletter block can use
selectors as plain as `.lede` without scoping them.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/mobile_hero.py */"

PAGES = [
    "grow-your-therapy-practice.html",
    "therapist-tax-strategy-california.html",
    "associate-mft-job-advisor.html",
    "amft-3000-hours-california.html",
    "newsletter.html",
]

CSS = """
@media (max-width:560px){
  /* 0. the hero's own padding was drawn for a desktop band: 44px top and 40px
     bottom on a 844px screen is 10% of everything the reader gets. */
  .ghero,.thero,.ahero{padding:28px 0 24px}

  /* 1. decorative hero art */
  .ahero .aart,
  .ahero .apanel > svg,
  .ghero .gpanel > svg{display:none}

  /* 2. secondary jump links: kept, shrunk. The primary is untouched. */
  .gherocta,.aherocta,.therocta{gap:7px}
  .gherocta .ghost,.aherocta .ghost,.therocta .ghost{
    padding:8px 12px;font-size:12.4px;min-height:38px}

  /* 3. ORDER. On grow and tax the deck is four sentences - 195px and 220px of
     type on a phone - and it sat between the headline and everything the page
     can actually do. Nothing is cut: the deck moves below the figures and the
     buttons, so the first screen reads headline, hook, live numbers, action,
     and the explanation is there for the reader who wants it.

     display:contents lifts the text column's children into the hero grid so
     the deck and the panel can be ordered against each other; they are in
     different containers otherwise. The plain <div> it dissolves carries no
     box of its own - no background, border or padding - so there is nothing
     to lose. Desktop is untouched. */
  /* the hero grid's row gap was drawn for TWO rows; dissolving the text
     column turns it into six, so 24px of gap became 120px and the hero got
     taller than it was before the reorder. Measured, not guessed. */
  .ghero .in,.thero .in{gap:11px}
  .ghero .in > div:first-child,
  .thero .in > div:first-child{display:contents}
  /* Every one of these carries the SAME specificity (0,3,0 - two classes and
     one more class/element) on purpose. The first draft wrote the default as
     `.ghero .in > div:first-child > *` (0,3,1) and the exceptions as bare
     `.glede` (0,1,0); the default outranked all of them and the order never
     changed. That is the third time this codebase has been bitten by a rule
     losing to a more specific neighbour - see claude/design-audit-and-global-fixes.md.
     Keep these level with each other. */
  .ghero .in .bcr,   .thero .in .bcr     {order:1}
  .ghero .in h1,     .thero .in h1       {order:2}
  .ghero .in .gtag,  .thero .in .ttag    {order:3}
  .ghero .in .gpanel,.thero .in .tpanel  {order:4}
  .ghero .in .gherocta,.thero .in .therocta{order:5}
  .ghero .in .glede, .thero .in .tlede   {order:6;margin-bottom:0}

  /* 3b. the proof panel: same figures, less air */
  .gpanel,.apanel,.tpanel{padding:13px 15px}
  .gpanel .pr,.tpanel .pr{padding:7px 0}
  .apanel .arow{padding:6px 0}
  .gpanel .pr b,.tpanel .pr b{font-size:26px}
  .gpanel .pn,.tpanel .pn,.apanel .anote{margin-top:8px}
}
"""


# Per-page additions, appended after the shared block on that page only.
EXTRA = {
    "newsletter.html": """
@media (max-width:560px){
  .band .bandart{display:none}
  .band .pw > div:first-child{display:flex;flex-direction:column}
  .band .bcr    {order:1}
  .band h1      {order:2}
  .band .lede   {order:3}
  .band .nlform {order:4;margin-bottom:18px}
  .band .getlist{order:5;margin-top:0}
  .band{padding:28px 0 24px}
}
""",
}


def main():
    n = 0
    for slug in PAGES:
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            print("%-44s MISSING" % slug)
            continue
        s = open(path, encoding="utf-8").read()
        s = re.sub(r"\n?<style>" + re.escape(MARK) + r".*?/\* end mh \*/</style>\n?",
                   "", s, flags=re.S)
        if "</body>" not in s:
            print("%-44s no </body>" % slug)
            continue
        block = CSS + EXTRA.get(slug, "")
        s = s.replace("</body>", "\n<style>" + MARK + block + "/* end mh */</style>\n</body>", 1)
        open(path, "w", encoding="utf-8").write(s)
        n += 1

    bad = 0
    for slug in PAGES:
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            continue
        s = open(path, encoding="utf-8").read()
        if s.count(MARK) != 1:
            print("GUARD %s: %d stylesheets" % (slug, s.count(MARK))); bad += 1
        # our block must be the LAST <style> in the document
        last = s.rfind("<style>")
        if s.find(MARK) < last:
            print("GUARD %s: another stylesheet follows ours" % slug); bad += 1
    if bad:
        sys.exit("mobile_hero: %d guard failure(s)" % bad)
    print("%d page(s) given a mobile hero" % n)


if __name__ == "__main__":
    main()
