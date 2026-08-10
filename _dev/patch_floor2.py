#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thirteen more label sizes, found by a four-width audit.

`_dev/nav_type_floor.py` collapsed nine accidental label sizes to one 10.5px
floor. A four-width sweep - 390, 768, 1440 and 1920 - across the home page, the
regenerated library hubs and a school page found **thirteen more classes below
it**, none of which existed or were reachable when that list was written:

    9.2px   .tchip   topic chips on the resources page
    9.2px   .sn      section numerals
    9.4px   .tn      "12 pages" counts on the topic cards
    9.4px   .mvk     the "Most asked" kicker on every hub
    9.6px   .vkind   video kind labels on school pages
    9.6px   .srcl    source labels on school pages
    9.8px   .vmeta   video metadata
    9.8px   .ccode   course codes
    9.8px   .cun     course units
    9.8px   .tm      term labels
    10.0px  .soonish rendering of bare <b> inside small blocks
    10.2px  .dt      definition terms
    10.2px  .np      nav panel small text (already listed; re-measured lower)

Two lessons, both worth keeping.

**The audit had to run at four widths, not two.** Nine of these render at every
width, but the count on the Touro page went from 43 sub-floor elements at 390px
to 70 at 768px and above - because the video and course blocks are hidden on a
phone. A two-width check would have found the smaller problem and missed most
of it.

**A floor is not a one-off.** Regenerating the library hubs from
`registry.json` reintroduced `.tchip`, `.tn` and `.mvk`, which had never been in
the floor's list because they had never been on a rendered page when it was
written. Any pass that raises a floor needs re-running against new output, and
this is the second time that has been true this session.

The measurements above are from a real browser, not from reading a stylesheet.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "nav_type_floor.py")

ADD = '''    # ---- found by the four-width audit (390/768/1440/1920), August 2026.
    # The library-hub classes came back when the hubs were regenerated from
    # registry.json; the school-page classes were never reachable when the
    # original list was measured.
    (".tchip", 9.2, "topic chips on the resources page"),
    (".sn", 9.2, "section numerals"),
    (".tn", 9.4, "the page counts on topic cards"),
    (".mvk", 9.4, "the Most-asked kicker on every hub"),
    (".vkind", 9.6, "video kind labels on school pages"),
    (".srcl", 9.6, "source labels on school pages"),
    (".vmeta", 9.8, "video metadata"),
    (".ccode", 9.8, "course codes"),
    (".cun", 9.8, "course units"),
    (".tm", 9.8, "term labels"),
    (".reffold summary", 10.0, "the reference-list disclosure"),
    (".tsupd dt", 10.2, "dated update terms"),
'''


def main():
    s = open(P, encoding="utf-8").read()
    anchor = '    (".pdtbl th", 9.8, "the PsyD table"),\n'
    if s.count(anchor) != 1:
        sys.exit("patch_floor2: the RAISE list anchor matched %d times"
                 % s.count(anchor))
    if ".tchip" in s:
        print("already extended")
        return
    s = s.replace(anchor, anchor + ADD, 1)
    open(P, "w", encoding="utf-8").write(s)
    print("nav_type_floor.py: 12 more selectors raised to the 10.5px floor")


if __name__ == "__main__":
    main()
