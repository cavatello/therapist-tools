#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two hand-edits in house-chrome.css are the whole reason no page scrolls
sideways at 320px. Both have been reverted once already, silently.

WHAT THIS IS

The narrow-viewport floor is 320px - an iPhone SE in portrait, and the
narrowest width any real reader arrives on. At that width two rules decide
whether the page fits:

    .ftnl-t{flex:1;min-width:min(300px,100%)}

      The footer newsletter block. Written as a bare `min-width:300px` it is
      wider than the content column at 320 minus padding, so it pushes the
      document to 326px on EVERY page that carries a footer - which is all of
      them. The min() form keeps the 300px intention on wide screens and lets
      it collapse on narrow ones.

    @media (max-width:360px){ .pdgrid ... .thl a{min-width:0 !important} ... }

      Grid children default to min-width:auto, so a wide child refuses to
      shrink below its content and blows the track out. Three pages carry
      these grids.

WHY IT IS A PASS AND NOT JUST AN EDIT

Because it was an edit, and the edit did not survive. `css/house-chrome.css`
is hand-authored - no pass generates it - so when a working copy based on an
older revision is written back wholesale, the fix disappears with no error
anywhere. It happened on 18 August 2026: the site went from zero pages
overflowing at 320 to 189, and nothing failed. The only tell was a browser
sweep.

So this pass asserts both rules on every build, and --check fails loudly if
either has gone missing again. Repairing is cheap; noticing was not.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSS = os.path.join(SITE, "css", "house-chrome.css")

BARE = ".ftnl-t{flex:1;min-width:300px}"
WANT = ".ftnl-t{flex:1;min-width:min(300px,100%)}"
GRID_MARK = "/* _dev/narrow_floor.py - grid children may shrink at 360 */"
GRID = (GRID_MARK + "\n"
        "@media (max-width:360px){\n"
        ".pdgrid>*,.crsl>*,.thl>*,.pdgrid article,.crsl article,.thl a"
        "{min-width:0 !important}\n"
        ".pdgrid,.crsl,.thl{grid-template-columns:1fr !important}}\n")


def read():
    with open(CSS, encoding="utf-8") as fh:
        return fh.read()


def state(t):
    return (WANT in t, GRID_MARK in t)


def main():
    check = "--check" in sys.argv
    t = read()
    has_ftnl, has_grid = state(t)

    if check:
        missing = []
        if not has_ftnl:
            missing.append("the .ftnl-t min() rule - every footer overflows 320px without it")
        if not has_grid:
            missing.append("the 360px grid-child rule - pdgrid/crsl/thl blow out without it")
        if missing:
            print("  narrow_floor.py: house-chrome.css is missing " + str(len(missing))
                  + " rule(s) the 320px floor depends on:")
            for m in missing:
                print("    - " + m)
            print("    Run _dev/narrow_floor.py to put them back.")
            return 1
        print("  guards clean - both 320px floor rules present in house-chrome.css")
        return 0

    fixed = []
    if not has_ftnl:
        if BARE in t:
            t = t.replace(BARE, WANT)
        else:
            t = t.rstrip("\n") + "\n" + WANT + "\n"
        fixed.append(".ftnl-t")
    if not has_grid:
        t = t.rstrip("\n") + "\n" + GRID
        fixed.append("360px grid children")

    if fixed:
        with open(CSS, "w", encoding="utf-8") as fh:
            fh.write(t)
        print("  restored " + ", ".join(fixed) + " in house-chrome.css")
    else:
        print("  both 320px floor rules already present - nothing to restore")
    return 0


if __name__ == "__main__":
    sys.exit(main())
