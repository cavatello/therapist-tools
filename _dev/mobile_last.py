#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The mobile rules, re-asserted after the passes that were dropping them.

WHAT WAS HAPPENING

`mobile_floor.py` gives every small control a 24px hit area and sets a 12px
floor on text that carries a sentence. It runs in the FLOORS stage, writes
an inline `<style>` block, and its own guard passes on the file it just
wrote. Then:

  `extract_css.py` hoists that block into `css/<hash>.css`, because four or
  more pages share it - correct, and the whole point of the CSS chain.

  the five `family_*.py` passes rewrite each page's stylesheet list to a
  FIXED set - `house`, `house-chrome`, `house-<family>` and the page's own
  CSS - which is how rollout step 5 retires the legacy sheets. The hoisted
  sheet is not on that list.

So the rules were hoisted into a file that 240 of 242 pages stopped
loading. Measured in a browser rather than inferred: the newsletter consent
checkbox computes `min-width: auto` and renders **22x22** on a phone, and
the rule that should have clamped it to 24 is in a sheet the page does not
link. The only two survivors are `rates.html` and one other - the pages
excluded from `house_swap` by decision, which is exactly the tell.

This is the third instance of one shape in this repository: **a pass does
its work, its guard passes on the file it wrote, and a later pass removes
the result.** The first was `css/house-skin.css` being re-attached to a
redirect stub; the second was `build_redirect.py` asserting a clean
`tools.html` that `house_swap.py` then re-skinned. A guard that only looks
at the moment of writing cannot see any of them. The check has to run at
the END of the pipeline, against the page as it ships.

WHY A SEPARATE PASS RATHER THAN MOVING mobile_floor

`mobile_floor.py` does four things and only the hit-area half was lost -
its `overflow-wrap:anywhere` reaches 240 of 242 pages, because the family
passes ported that rule into the family sheets. Moving the whole pass would
duplicate the three-quarters that already work. This re-asserts the part
that does not, in the one position where nothing can take it away again:
after the families, inline, so there is no sheet to drop.

WHAT IT ADDS

  24x24 on checkboxes, radios and small controls   the WCAG 2.5.8 minimum,
                                                   and the reason the
                                                   consent box was 22x22
  16.5px on inputs, selects and textareas          form controls had NO
                                                   authored size at all and
                                                   inherited the browser
                                                   default of 13.3333px.
                                                   Below 16px, iOS Safari
                                                   zooms the page on focus
                                                   and does not zoom back -
                                                   so every newsletter
                                                   sign-up on a phone left
                                                   the reader stranded at
                                                   1.3x. 16.5px is the
                                                   house body step and it
                                                   is over the threshold.

Idempotent: the block carries a marker and is replaced, not appended.
Guarded: every published page must end up with the block, and the checkbox
must compute at least 24x24 - which is checked in a browser by
`_dev/_viewports.mjs`, not asserted here.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")
MARK = "/* _dev/mobile_last.py */"
SKIP = {"tycoon.html", "concepts.html"}

BLOCK = """<style>%s
/* Form controls had no authored font-size, so they took the browser default
   of 13.3333px. Under 16px, iOS Safari zooms on focus and never zooms back.
   16.5px is the house body step. */
input,select,textarea,button{font-size:16.5px}
@media (max-width:900px){
  /* WCAG 2.5.8: 24x24 minimum. mobile_floor.py sets this too, and its rule
     is hoisted into a stylesheet that the family passes stop the page
     loading - see this pass's docstring. Class-doubled so it outranks the
     explicit `width:22px` in house-chrome.css's (pointer:coarse) block. */
  input[type="checkbox"],input[type="radio"],
  .consent input,.consent input[type="checkbox"]{
    min-width:24px;min-height:24px;width:24px;height:24px}
  select,button[type="submit"]{min-height:24px}
}
</style>
""" % MARK

EXISTING = re.compile(r"<style>\s*" + re.escape(MARK) + r"[\s\S]*?</style>\n?")


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    n = 0
    for rel in pages():
        if os.path.basename(rel) in SKIP:
            continue
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s
        s = EXISTING.sub("", s)
        i = s.rfind("</body>")
        if i < 0:
            print("  SKIP %s has no </body>" % rel)
            continue
        s = s[:i] + BLOCK + s[i:]
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("the mobile control rules re-asserted on %d page(s)" % n)

    bad = 0
    for rel in pages():
        if os.path.basename(rel) in SKIP:
            continue
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if s.count(MARK) != 1:
            print("GUARD %s carries the block %d time(s)"
                  % (rel, s.count(MARK)))
            bad += 1
        # it has to be the LAST thing before </body>, or a family sheet
        # linked after it wins the tie on source order
        tail = s[s.rfind(MARK):]
        if 'rel="stylesheet"' in tail:
            print("GUARD %s: a stylesheet is linked after the block" % rel)
            bad += 1
    if bad:
        sys.exit("%d problem(s)" % bad)
    print("guard clean - the block is on every published page and nothing "
          "is linked after it")


if __name__ == "__main__":
    main()
