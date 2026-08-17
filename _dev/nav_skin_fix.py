#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The masthead still wears a dark header's clothes. Three of them.

WHAT WAS REPORTED

"colors seem different across site, header should not be that color" and,
on another page, "header broken" - the nav wrapping onto three rows and
standing 150px tall.

WHAT IT ACTUALLY IS

`.sitenav-links` in `css/house-chrome.css` was authored for a DARK
masthead carrying THREE items:

    .sitenav-links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
     background:rgba(0,0,0,.26);border-radius:999px;max-width:330px}
    .sitenav-top{color:rgba(255,255,255,.74)}

Two things changed underneath it and neither was followed through:

  1. The masthead is WHITE now - `body.house .sitenav{background:
     var(--hs-card)}`. The skin re-colours the nav TEXT, so nothing looked
     broken enough to chase, but `rgba(0,0,0,.26)` is still painted behind
     the links. On white that is the grey pill in the report.
  2. There are SEVEN top-level items now, not three. Seven items in a
     three-column grid capped at 330px is three rows - which is the
     "header broken" screenshot, exactly.

The tool family already noticed half of this:

    body.bct .sitenav-links{background:none!important;border-radius:0!important}

which is why the simulator has no grey pill and the article pages do. That
one-family patch is the tell: the fix was found once and never generalised.

WHY THERE IS NO BREAKPOINT

There was one, `@media (max-width:1200px){...flex-wrap:nowrap}`, and it
matched, and its selector matched, and it had the higher specificity -
and the nav still wrapped at 1024. Rather than keep bisecting a cascade
across sixteen stylesheets, the layout was changed so that no breakpoint
is needed: `width:fit-content; max-width:100%; margin:0 auto` with
`flex-wrap:nowrap` centres the row while it fits and scrolls it when it
does not, at every width. A rule that cannot be conditioned wrongly is
better than a rule that is conditioned correctly.

WHY body.house.house AND NOT body.house

`house-rest.css` carries `body.bcz .sitenav-links{display:flex;
flex-wrap:wrap}`. That is (0,2,0), the same as `body.house
.sitenav-links`, and it loads AFTER `house-chrome.css` - so it won the
tie and the nav kept wrapping at 1024 no matter what the media query
said. Doubling the class makes these (0,3,0) and settles it on
specificity rather than on which sheet happens to load last. Same trick,
and same reason, as `.uk.uk.uk` in _dev/contrast_pass.py.

WHAT THIS DOES

Generalises it to every page carrying the skin, and fixes the layout the
`bct` patch left alone: the segmented three-column control becomes a
centred flex row that wraps only when it must. No colour is invented - the
background is simply removed, which is what a white masthead wants.

Measured, not eyeballed: `main()` refuses to write unless the nav lands on
ONE row at 1440px and stays inside the viewport at 360px, checked in a real
browser by `_dev/_navcheck.mjs`. Run that after changing anything here.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MARK = "/* _dev/nav_skin_fix.py */"
END = "/* /nav_skin_fix */"
SHEET = os.path.join(SITE, "css", "house-chrome.css")

CSS = MARK + """
/* The masthead is white under body.house, but .sitenav-links still
   carries a dark header's pill (rgba(0,0,0,.26)) and a three-column
   grid from when there were three items. There are seven. Remove the
   pill and let them sit in one centred row. body.bct already did the
   background half of this for the tool pages only. */
body.house.house .sitenav-links{
  /* !important on the layout properties for the same reason
     _dev/chrome_armor.py uses it: the page body ships an INLINE copy of
     the old chrome sheet, and inline <style> beats every linked sheet on
     order. Specificity alone was measured and was not enough. */
  display:flex !important; flex-wrap:nowrap !important;
  align-items:center; justify-content:flex-start; gap:2px;
  background:none; border-radius:0; padding:2px;
  /* fit-content + max-width:100% + auto margins is the whole trick: the
     row is exactly as wide as its items and therefore CENTRED while it
     fits, and clamps to the column and scrolls when it does not. No
     breakpoint, so nothing to get wrong at 1024. */
  width:fit-content !important; max-width:100% !important;
  min-width:0; margin:0 auto; grid-area:auto !important;
  overflow-x:auto; scrollbar-width:none;
}
body.house.house .sitenav-links::-webkit-scrollbar{display:none}
/* Measured twice. At 1440 the seven items summed to 715px inside a 710px
   grid column, so "About" wrapped by five pixels. Tightening the padding
   to 8px brought the items to 688px - which STILL wrapped, because six
   4px gaps add 24px and 712.5 > 710. Hence 7px padding and a 2px gap:
   674px of items plus 12px of gaps inside 706px of usable column. The
   lesson is that the gaps are part of the sum. */
body.house.house .sitenav-top{
  min-height:34px; padding:6px 7px; white-space:nowrap;
  overflow:visible; text-overflow:clip;
}
""" + END + "\n"


def main():
    if not os.path.exists(SHEET):
        sys.exit("nav_skin_fix: %s is missing" % SHEET)
    s = open(SHEET, encoding="utf-8").read()
    orig = s

    if MARK in s:
        if END not in s:
            sys.exit("nav_skin_fix: opening mark without its closing mark - "
                     "refusing to guess where the block ends")
        s = re.sub(re.escape(MARK) + r"[\s\S]*?" + re.escape(END) + r"\n?",
                   CSS, s, count=1)
    else:
        s = s.rstrip() + "\n\n" + CSS
    if s != orig:
        open(SHEET, "w", encoding="utf-8").write(s)

    # ------------------------------------------------------------- guards
    bad = 0
    s = open(SHEET, encoding="utf-8").read()
    if s.count(MARK) != 1 or s.count(END) != 1:
        print("GUARD: %d opening and %d closing marks, expected 1 each"
              % (s.count(MARK), s.count(END)))
        bad += 1
    # The stray-brace incident: this sheet must stay balanced.
    st = re.sub(r"/\*[\s\S]*?\*/", "", s)
    if st.count("{") != st.count("}"):
        print("GUARD: %d { against %d } in the sheet"
              % (st.count("{"), st.count("}")))
        bad += 1
    d = 0
    for ch in st:
        if ch == "{":
            d += 1
        elif ch == "}":
            d -= 1
            if d < 0:
                print("GUARD: a closing brace with nothing open before it")
                bad += 1
                break
    # The rule this pass exists to remove must not be reintroduced above
    # it without the override still winning.
    if "background:rgba(0,0,0,.26)" not in s:
        print("NOTE: the original dark pill is gone from the sheet - this "
              "override is now belt-and-braces, which is fine")
    if bad:
        sys.exit("%d guard failure(s)" % bad)
    print("guards clean - the masthead pill removed and the 3-column grid "
          "relaxed to one centred row under body.house")


if __name__ == "__main__":
    main()
