#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Four of the seven topics were unreachable on a phone.

WHAT WAS WRONG

Reported from a phone: "mobile nav not great". Measured, it is worse than it
looks. At 390px the topic row shows three of seven sections and cuts the
fourth mid-word:

    320px   3 of 7 visible      Getting paid, Practice, Training, About hidden
    390px   3 of 7 visible      the same four hidden
    430px   4 of 7 visible
    768px   5 of 7 visible

It is a horizontal scroller, so the other four are technically reachable - but
there is no scrollbar (`scrollbar-width:none`), the fade mask is 18px and
invisible against the masthead, and the cut lands mid-word. Nothing tells a
reader that more exists, so "Getting paid" and "Practice" - two of the site's
five topics - simply do not appear to be there.

THE PART THAT IS NOT A STYLE CHOICE

The nav is not merely overflowing; it is boxed. Its parent `.sitenav-in` is a
grid, and on a phone the nav gets **221px of a 390px viewport** - the wordmark
and the Updates button hold the rest - while the seven items need 608px. So
turning wrapping on alone does nothing: the row simply wraps inside a 221px
box and overflows the page. The fix has to give the nav the whole row first.

`body.house.house .sitenav-links{flex-wrap:nowrap !important;
width:fit-content !important}` from `nav_skin_fix.py` also has to be
outranked, hence the third `.house` here. That is a specificity fight, and it
is the honest way to win it without editing a pass that is right about the
desktop case.

`rates.html` carries `body.ratespage` and no `house` class, because it is
excluded from the house passes by decision - so the first version of this pass
shipped its stylesheet to that page and then matched nothing on it, leaving
four of seven topics cut there and nowhere else. Its own class is doubled for
the same specificity reason. This is chrome, not the page's editorial voice,
which is what the exclusion protects.

WHAT IT DOES, AND WHAT IT COSTS

Two breakpoints, because the header is not one layout.

**At 640px and below** the masthead is already a grid with the topic row on
its own line, so the row takes the full width, wraps, and its items go very
slightly tighter - seven fit in two lines rather than three.

**Between 641 and 900** the row still sits beside the wordmark and the Updates
button, and forcing it onto its own line there would take the header from 67px
to 161px for no reason: all seven already fit the width it has, they were
simply clipped by a `nowrap`. So that range gets wrapping and no repositioning.

    390px   7 of 7 visible   header 116px -> 150px   2 rows   items 34px tall
    430px   7 of 7 visible   header 116px -> 150px   2 rows
    320px   7 of 7 visible   header 158px -> 227px   3 rows
    768px   7 of 7 visible   header  67px ->  67px   1 row

The header is `position:sticky`, so this is a real cost: 34px more of a phone
screen, permanently. 18% of an 844px viewport rather than 14%. That is the
trade - four sections that were invisible become visible, and the sticky bar
gets taller. Above 900px, where all seven already fit on one line, nothing changes at all.

Item height stays at 34px, above the 24px pointer floor `mobile_reassert.py`
enforces, and no page gains horizontal overflow at any width.

Ships inline, in LAST, after the hoisting chain. Same reason as
`mobile_reassert.py`: rules that live in a shared sheet on this site have a
history of being unlinked by a later family pass, and a nav fix that silently
stops applying looks exactly like the bug it fixed.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

CSS_MARK = "/* _dev/nav_wrap.py */"
CSS_END = "/* /_dev/nav_wrap.py */"
STYLE_OPEN = "<style>" + CSS_MARK
STYLE_SHUT = CSS_END + "</style>"

# The third `.house` is deliberate - see the docstring. It outranks
# nav_skin_fix.py's own !important without editing that pass.
CSS = """
@media (max-width:640px){
body.house.house.house .sitenav-links,body.ratespage.ratespage .sitenav-links{
grid-column:1/-1 !important;width:100% !important;max-width:100% !important;
flex-wrap:wrap !important;overflow-x:visible !important;
-webkit-mask-image:none !important;mask-image:none !important;
background-image:none !important;justify-content:flex-start !important;
row-gap:1px !important;padding-right:0 !important}
body.house.house.house .sitenav-links .sitenav-top,
body.ratespage.ratespage .sitenav-links .sitenav-top{
font-size:11px !important;padding:5px 5px !important}}
@media (min-width:641px) and (max-width:900px){
body.house.house.house .sitenav-links,body.ratespage.ratespage .sitenav-links{
width:100% !important;max-width:100% !important;
flex-wrap:wrap !important;overflow-x:visible !important;
-webkit-mask-image:none !important;mask-image:none !important;
background-image:none !important;justify-content:flex-start !important;
row-gap:1px !important;padding-right:0 !important}}
"""


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f)
                    for f in sorted(os.listdir(p)) if f.endswith(".html")]
    return out


def strip(s):
    return re.sub(re.escape(STYLE_OPEN) + r"[\s\S]*?" + re.escape(STYLE_SHUT),
                  "", s)


def main(check_only=False):
    bad, done, skipped = [], 0, 0
    for page in pages():
        p = os.path.join(SITE, page)
        s = open(p, encoding="utf-8").read()
        out = strip(s)
        # Only pages that actually carry the topic row.
        if "sitenav-links" not in out:
            skipped += 1
            if out != s and not check_only:
                open(p, "w", encoding="utf-8").write(out)
            continue
        h = out.rfind("</head>")
        if h < 0:
            bad.append("%s has no head to put the nav rule in" % page)
            continue
        if not check_only:
            out = out[:h] + STYLE_OPEN + CSS + STYLE_SHUT + out[h:]
            if out != s:
                open(p, "w", encoding="utf-8").write(out)
        done += 1

    if not check_only:
        for page in pages():
            s = open(os.path.join(SITE, page), encoding="utf-8").read()
            if "sitenav-links" not in s:
                continue
            if s.count(CSS_MARK) != 1 or s.count(CSS_END) != 1:
                bad.append("%s has %d/%d nav-wrap marker(s)"
                           % (page, s.count(CSS_MARK), s.count(CSS_END)))

    if bad:
        for b in bad:
            print("GUARD: %s" % b)
        sys.exit("%d problem(s)" % len(bad))
    print("the topic row wraps on %d page(s) at 900px and below, so all seven "
          "sections are visible; %d page(s) carry no topic row."
          % (done, skipped))


if __name__ == "__main__":
    main("--check" in sys.argv)
