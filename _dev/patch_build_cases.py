#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fold the second collection into build_cases.py: counts, figures, and a date
that is not in the document.

Every number this file printed about the library was written by hand when there
were thirty cases. There are now forty-eight, and there will be more, so the
numbers are computed from `CASES` rather than typed.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
P = "build_cases.py"
s = open(P, encoding="utf-8").read()


def once(old, new, what):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("patch_build_cases: %r matched %d times, expected 1" % (what, n))
    s = s.replace(old, new, 1)
    print("  ok  %s" % what)


# --------------------------------------------------------------- the helpers
HELPERS = '''
# ------------------------------------------------------------------ counting
# Every figure the hub prints about itself is computed. The first version of
# this file wrote "thirty" into nine strings, and the library is now
# forty-eight; a number typed into prose is a number that goes stale silently.
WORD = ("no", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen", "twenty")
TENS = {30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy",
        80: "eighty", 90: "ninety"}


def word(n):
    """Spelled out, because "Forty-eight cases" reads better than "48 cases"."""
    if n <= 20:
        return WORD[n]
    t, u = divmod(n, 10)
    base = TENS.get(t * 10)
    if not base:
        return str(n)
    return base if not u else "%s-%s" % (base, WORD[u])


def money_max():
    """The largest cost recovery in the library, read off the cases.

    It was $15,883 when this was typed by hand, then $32,956, then $33,704.
    Nobody was going to remember to update it a third time."""
    best, txt = 0, None
    for c in CASES:
        v = c.get("cost")
        if not v:
            continue
        for m in re.findall(r"\\$([\\d,]+(?:\\.\\d\\d)?)", v):
            f = float(m.replace(",", ""))
            if f > best:
                best, txt = f, "$" + m.split(".")[0]
    return txt or "&mdash;"


NUM = len(CASES)
'''
once("HUB = \"therapist-discipline-cases-california.html\"",
     HELPERS + "\nHUB = \"therapist-discipline-cases-california.html\"",
     "the counting helpers")

# ---------------------------------------------------- a date that is missing
# One decision in the second collection has an effective date that the scan
# rendered as "~~1s_,____,,---___". Guessing it would put an invented fact on a
# page whose whole claim is that it does not invent facts.
once('def esc(x):',
     '''def eff_of(c):
    """The effective date, or an honest gap.

    One decision's effective date is illegible in the scan. The page says so
    rather than carrying a date nobody can read off the document - and this
    function exists so that the four places that print a date all say the same
    thing when there is not one."""
    return (c.get("eff") or "date not legible").split(";")[0]


def esc(x):''', "eff_of()")

for old in ('c["eff"].split(";")[0]',):
    n = s.count(old)
    s = s.replace(old, "eff_of(c)")
    print("  ok  %d call site(s) moved to eff_of()" % n)
once('% c["eff"])', '% eff_of(c))', "the remaining eff call site")

# ------------------------------------------------------------- hero and copy
once('''    for n, l in (("103", "decisions read"),
                 ("30", "written up"),
                 ("$15,883", "largest cost recovery")):''',
     '''    for n, l in ((str(NUM), "written up in full"),
                 (money_max(), "largest cost recovery"),
                 (str(len(GROUPS)), "ways it goes wrong")):''',
     "the three hero figures")

once("o.append('<a href=\"#cases\">The thirty cases</a>')",
     "o.append('<a href=\"#cases\">The %s cases</a>' % word(NUM))",
     "the hero jump link")
once("o.append('<h2 class=\"dc-h\">Thirty cases, grouped by what went wrong.</h2>')",
     "o.append('<h2 class=\"dc-h\">%s cases, grouped by what went wrong.</h2>'\n"
     "             % word(NUM).capitalize())",
     "the section heading")
once("'aria-pressed=\"true\">All thirty</button>')",
     "'aria-pressed=\"true\">All %s</button>' % word(NUM))",
     "the all-cases chip")
once("o.append('<p class=\"dc-count\" id=\"dc-count\">Showing all 30 cases</p>')",
     "o.append('<p class=\"dc-count\" id=\"dc-count\">Showing all %d cases</p>'\n"
     "             % NUM)", "the count line")
once("""'<span class="t">All thirty cases</span></a>' % HUB)""",
     """'<span class="t">All %s cases</span></a>' % (HUB, word(NUM)))""",
     "the back-link label")
once('o.append("<p>Read the thirty cases and the pattern is hard to miss: almost "',
     'o.append("<p>Read them and the pattern is hard to miss: almost "',
     "the pattern sentence")

# --------------------------------------------------------------- the metadata
once('''        "Thirty real California BBS disciplinary decisions for LMFTs and AMFTs, "
        "de-identified: what happened, which subdivision of B&amp;P &sect;4982 it "
        "was charged under, how it resolved, and what the cost recovery was. Read "
        "from 103 signed decisions.",''',
     '''        "%d real California BBS disciplinary decisions, de-identified: what "
        "happened, which subdivision it was charged under, how it resolved, and "
        "what the cost recovery was. Read from two collections of signed "
        "decisions." % NUM,''', "the hub description")
once('''        "Thirty real cases, the exact code section each was charged under, and "
        "what each one cost",
        "103 decisions read, 30 written up",''',
     '''        "%s real cases, the exact code section each was charged under, and "
        "what each one cost" % word(NUM).capitalize(),
        "%d written up in full" % NUM,''', "the hub outcome and number")

open(P, "w", encoding="utf-8").write(s)
print("\ndone")
