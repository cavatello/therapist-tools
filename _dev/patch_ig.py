#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Point the discipline-hub bar chart at the data instead of at a memory of it.

The figure was authored when the library had thirty cases and eight groups. It
carried the counts as literals, and the group names as a second, hand-kept copy
of the taxonomy. The library is now forty-eight cases in nine groups, so both
copies were wrong and the anchor no longer matched the heading it was looking
for - which is how the pass announced the problem, and the only reason it was
caught.

It now reads `case_data.py`. There is one taxonomy, one set of counts, and the
next expansion moves the chart without anybody remembering to.
"""
import os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = "infographics.py"
s = open(P, encoding="utf-8").read()

start = s.index('        "therapist-discipline-cases-california.html",')
start = s.rindex("    (\n", 0, start)
end = s.index("\n    (", start + 5)

NEW = '''    # ---------------------------------------------------- discipline cases
    # Counts and labels come from case_data.py. They used to be literals here,
    # authored when the library held thirty cases in eight groups; the library
    # grew and this figure kept confidently drawing the old numbers until the
    # anchor stopped matching and the guard caught it.
    (
        "therapist-discipline-cases-california.html",
        r'<h2 class="dc-h">[A-Za-z-]+ cases, grouped by what went wrong[\\s\\S]{0,600}?</p>',
        lambda: bars(
            "%d cases, by what went wrong" % len(CASES),
            [(g["short"], "", _n(g["key"]), str(_n(g["key"])))
             for g in sorted(GROUPS, key=lambda g: -_n(g["key"]))],
            "Boundaries &mdash; sexual contact and the drift short of it "
            "&mdash; and criminal convictions are the two halves of this "
            "library. Only a handful began as a complaint about clinical "
            "work. <b>The pattern to take from this is that discipline "
            "usually arrives from outside the therapy room</b>, through a "
            "conviction feed, an employer, another licensing board, or an "
            "application form."),
    ),
'''
s = s[:start] + NEW + s[end + 1:]

HELP = '''
# The taxonomy and the counts have exactly one home.
import sys as _sys  # noqa: E402
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from case_data import CASES, GROUPS  # noqa: E402


def _n(key):
    return sum(1 for c in CASES if c["group"] == key)

'''
anchor = "\nHERE = os.path.dirname(os.path.abspath(__file__))"
if s.count(anchor) != 1:
    sys.exit("patch_ig: HERE anchor matched %d times" % s.count(anchor))
if "from case_data import CASES, GROUPS" not in s:
    i = s.index("\n", s.index(anchor) + 1)
    i = s.index("\n", i + 1)
    s = s[:i] + "\n" + HELP + s[i:]

open(P, "w", encoding="utf-8").write(s)
print("infographics.py now reads case_data.py")
