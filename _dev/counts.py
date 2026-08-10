#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The site's counts, derived once, for every pass that wants to print one.

WHY THIS EXISTS

The navigation panel on all 185 pages described the case library as "30 real
BBS decisions" for as long as the library had 48, and the school directory as
"65 California schools" when there were 66. Both numbers were typed into a
blurb by hand, in two different files, and neither had any connection to the
data they described.

This is the third time the same bug has been fixed on this site. `build_cases.py`
had "thirty" written into nine strings. `infographics.py` drew a bar chart from
literal group counts authored when there were thirty cases. Each was fixed in
place, and each fix left the next copy of the number somewhere else.

So the numbers live here now, computed from the files that define them, and the
passes interpolate. A count printed to a reader should be readable off the thing
it counts.

WHAT IT DELIBERATELY DOES NOT DO

It does not try to be a general "count anything" helper. Every entry is a number
the site actually prints in prose somewhere; if a pass wants a count that is not
here, add it here rather than counting inline, because counting inline is how
all of this started.
"""
import os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)


def _root(pattern):
    return len([f for f in os.listdir(SITE)
                if f.endswith(".html") and re.match(pattern, f)])


def cases():
    """Written-up discipline cases. Read from case_data, not from the disk, so
    it matches what the library renders rather than what happens to be lying
    in the directory."""
    sys.path.insert(0, HERE)
    from case_data import CASES
    return len(CASES)


def schools():
    return _root(r".+-mft\.html$")


def psychedelic():
    return _root(r"psychedelic-training-.+\.html$")


def registry():
    p = os.path.join(SITE, "mock", "library", "registry.json")
    return json.load(open(p, encoding="utf-8"))


def calculators():
    return len([p for p in registry()["pages"] if p.get("format") == "calculator"])


def pages():
    return len([p for p in registry()["pages"] if not p.get("skip")])


ALL = {"cases": cases, "schools": schools, "psychedelic": psychedelic,
       "calculators": calculators, "pages": pages}


if __name__ == "__main__":
    for k in sorted(ALL):
        print("%-14s %d" % (k, ALL[k]()))
