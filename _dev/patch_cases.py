#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fold the second collection into the case library.

Run once, from _dev/. Every edit asserts on its anchor before making it, so a
partial application is not possible: either every anchor matched and the file
is rewritten, or nothing is touched and you get a message saying which anchor
moved.
"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def sub_once(s, old, new, what):
    n = s.count(old)
    if n != 1:
        sys.exit("patch_cases: the anchor for %r matched %d times, expected 1.\n"
                 "  Nothing has been written. Re-read the file and update the "
                 "anchor rather than loosening it." % (what, n))
    print("  ok  %s" % what)
    return s.replace(old, new, 1)


# =============================================================== case_data.py
s = open("case_data.py", encoding="utf-8").read()
orig = s

# ---- 1. the ninth group -----------------------------------------------------
APPLYING = '''    {
        "key": "applying",
        "short": "Applying with a record",
        "n": "Applying with a record",
        # A Statement of Issues is not an Accusation, and readers conflate them
        # constantly. Nobody here did anything as a therapist: they applied, and
        # the Board looked at what was already on the record. The reason this
        # group earns its own heading is the outcomes - most of these end with
        # the registration being ISSUED, on probation, rather than refused.
        "lede": "The Board is not deciding what somebody did in a session. It "
                "is deciding whether to let them start at all. &sect;480 lets "
                "it look back seven years &mdash; except for a serious felony "
                "under Penal Code &sect;1192.7, where there is no time limit at "
                "all, and where &sect;1192.7(c)(23) sweeps in any felony "
                "involving a weapon. What the statute will not let the Board do "
                "is refuse on the conviction type alone: &sect;493 requires the "
                "rehabilitation analysis in 16 CCR &sect;1813 every time. Read "
                "these for what that analysis actually accepts.",
    },
'''
anchor = '''    {
        "key": "probation",
        "short": "After discipline",'''
s = sub_once(s, anchor, APPLYING + anchor, "the ninth group, `applying`")

# ---- 2. counts out of the ledes ---------------------------------------------
# build_cases.py already prints the count beside the group heading. A number
# written into the prose as well is a number that goes stale in two places.
LEDES = [
    ("Six cases. One went to a full hearing; the rest settled. The ",
     "One went to a full hearing; the rest settled. The "),
    ("Five cases where nobody touched anybody. Texting",
     "Nobody touched anybody. Texting"),
    ("Three cases about paper. A letter", "All about paper. A letter"),
    ("Four cases under &sect;4982.25. If any other board",
     "All under &sect;4982.25. If any other board"),
    ("One page, three cases, one lesson: an order",
     "One lesson: an order"),
    ("Three cases about the part nobody plans for. Probation runs ",
     "The part nobody plans for. Probation runs "),
]
for old, new in LEDES:
    s = sub_once(s, old, new, "count out of a lede: %r" % old[:34])

# The money group's lede opens with a count too, and the conviction group's
# says "Three are written up in full", which is now wrong in the other
# direction - there are more.
s = sub_once(s, '"lede": "Three cases. One involves no clients at all',
             '"lede": "One of these involves no clients at all',
             "the money lede")
s = sub_once(s,
             '"those are a DUI arriving through the Department of Justice "\n'
             '                "notification feed rather than through a client. Three are "\n'
             '                "written up in full, because past the first one they repeat: the "\n'
             '                "case that shows what the typical one looks like, the case about "\n'
             '                "reporting it, and the case that shows the Board does not need a "\n'
             '                "conviction at all. The remaining two are listed at the end of "\n'
             '                "the group for completeness rather than because they teach "\n'
             '                "anything the first three do not.",',
             '"those are a DUI arriving through the Department of Justice "\n'
             '                "notification feed rather than through a client. Only a few "\n'
             '                "DUIs are written up in full, because past the first they "\n'
             '                "repeat. What is here instead is the range: the modal case, "\n'
             '                "the duty to report a conviction inside thirty days, the "\n'
             '                "convictions that have nothing to do with a client at all, and "\n'
             '                "the cases the Board decided on its own evidence packet because "\n'
             '                "nobody filed a notice of defense.",',
             "the conviction lede")

# ---- 3. the duplicated afternoon --------------------------------------------
# `discipline-case-drinking-at-lunch` and decision 031 are the same afternoon:
# same date, same $5,190, same three causes. The thin entry is replaced in
# place by the fuller one, keeping the slug so the URL and every link to it
# survive.
lunch = json.load(open("lunch_replacement.json", encoding="utf-8"))
FIELDS = ["slug", "group", "t", "dek", "role", "eff", "case", "hear", "facts",
          "charges", "outcome", "cost", "rule", "ins", "prevent"]


def lit(v, ind):
    return json.dumps(v, ensure_ascii=False, indent=1).replace("\n", "\n" + " " * ind)


start = s.index('        "slug": "discipline-case-drinking-at-lunch",')
start = s.rindex("    {\n", 0, start)
end = s.index("\n    {\n", start) + 1
block = ["    {"]
block.append('        # The same afternoon as decision 2002023002307 in the '
             'second collection.')
block.append('        # The thin entry written from the newsletter summary was '
             'replaced by the')
block.append('        # full account from the decision itself. The slug is '
             'deliberately unchanged:')
block.append('        # the page is already indexed and linked.')
for k in FIELDS:
    v = lunch["slug"] if k == "slug" else lunch[k]
    if k == "slug":
        v = "discipline-case-drinking-at-lunch"
    block.append('        %s: %s,' % (json.dumps(k), lit(v, 8)))
block.append("    },\n")
s = s[:start] + "\n".join(block) + s[end:]
print("  ok  the drinking-at-lunch entry rewritten from the decision")

# ---- 4. the second collection -----------------------------------------------
TAIL = '''

# --------------------------------------------------- the second collection
# Eighteen more, from a separate download of 105 decisions. Kept in their own
# module so that where a case came from stays visible: everything above was
# read from the Board's newsletters, everything in `case_data_more.py` came
# through the redaction pipeline documented in that file's header.
from case_data_more import MORE  # noqa: E402

CASES = CASES + MORE
'''
if "from case_data_more import MORE" not in s:
    s = s.rstrip() + "\n" + TAIL
    print("  ok  case_data_more folded in")

open("case_data.py", "w", encoding="utf-8").write(s)

# ============================================================== case_depth.py
d = open("case_depth.py", encoding="utf-8").read()
DTAIL = '''

# --------------------------------------------------- the second collection
from case_depth_more import MORE_DEPTH  # noqa: E402

DEPTH.update(MORE_DEPTH)
'''
if "from case_depth_more import MORE_DEPTH" not in d:
    d = d.rstrip() + "\n" + DTAIL
    open("case_depth.py", "w", encoding="utf-8").write(d)
    print("  ok  case_depth_more folded in")

print("\ndone. Now run:  python3 build_cases.py")
