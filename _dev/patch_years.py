#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two claims on the hub that the second collection made untrue.

  1. The kicker says "2024-2026". Four of the new cases took effect in 2023,
     and one of the older ones in January 2024, so the range is wider than the
     label. It is now read off the cases.
  2. "Sixty-two of the 103 decisions read for this library" was true when the
     library had one source collection. There are two now, and that sentence
     silently reattributes a statistic computed on the first to the whole
     thing. The count is unchanged; the sentence now says which collection it
     came from.
"""
import os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = "build_cases.py"
s = open(P, encoding="utf-8").read()


def once(old, new, what):
    global s
    if s.count(old) != 1:
        sys.exit("patch_years: %r matched %d times" % (what, s.count(old)))
    s = s.replace(old, new, 1)
    print("  ok  %s" % what)


once('''def money_max():''',
     '''def years():
    """The span the library actually covers, off the effective dates.

    The kicker said 2024-2026 because that was true of the first collection.
    A label that describes the corpus rather than the cases is a label that
    goes wrong the first time the corpus grows."""
    ys = sorted({int(y) for c in CASES for y in
                 re.findall(r"\\b(20\\d\\d)\\b", c.get("eff") or "")})
    if not ys:
        return ""
    return str(ys[0]) if ys[0] == ys[-1] else "%d&ndash;%d" % (ys[0], ys[-1])


def money_max():''', "years()")

once("""o.append('<p class="hk">Case library &middot; California &middot; 2024&ndash;2026</p>')""",
     """o.append('<p class="hk">Case library &middot; California &middot; %s</p>'
             % years())""", "the kicker")

once("'<b>Sixty-two of the 103 decisions read for this library cite '",
     "'<b>Sixty-two of the 103 decisions in the first collection cite '",
     "the 62-of-103 attribution")
once("o.append('<p class=\"dc-d\">Counted from the text of the 103 decisions. A '",
     "o.append('<p class=\"dc-d\">Counted from the text of those 103 decisions. A '",
     "the subdivision-table caption")

open(P, "w", encoding="utf-8").write(s)
print("done")
