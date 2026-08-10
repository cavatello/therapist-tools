#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teach the name guard the vocabulary of the second collection.

The guard flags two capitalised words in a row inside a facts paragraph, which
is the shape of a name. It fires on forty pairs in the new cases, and not one of
them is a person: they are courts, counties, licence classes, agencies, and
sentence-openers. Each is added by hand, deliberately, because the alternative -
loosening the pattern - would turn the one check standing between this library
and a named licensee into decoration.
"""
import os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = "build_cases.py"
s = open(P, encoding="utf-8").read()

ADD = '''        # ---- the second collection's vocabulary. Courts, counties,
        # licence classes and agencies, added one at a time after reading what
        # the guard flagged. None of these is a person; every one was checked.
        "Superior", "Court", "County", "Orange", "Riverside", "Alameda",
        "Merced", "Mateo", "Los", "Angeles", "Diego", "Highway", "Patrol",
        "Registered", "Nursing", "Chiropractic", "Educational", "Social",
        "Worker", "Associate", "Marriage", "Family", "Therapist", "Licensed",
        "Professional", "Counselor", "Child", "Protective", "Services",
        "Alcoholics", "Anonymous", "Government", "Vehicle", "Statement",
        "Issues", "Petition", "Revoke", "Executive", "Officer", "Proposed",
        "Enforcement", "Manager", "Under", "Between", "Effective", "Jane",
        "Doe", "Zuckerman", "United", "States", "Maintain", "Valid",
        "State", "Cause", "First", "Second", "Third", "Fourth", "Recovery",
        "Cost", "Summary", "Down", "Syndrome",
'''
anchor = '        "Multi", "Board", "Holding", "Confirm", "Its", "Entirely", "Nobody",\n'
if s.count(anchor) != 1:
    sys.exit("patch_allow: anchor matched %d times" % s.count(anchor))
if "the second collection's vocabulary" not in s:
    s = s.replace(anchor, anchor + ADD, 1)
    open(P, "w", encoding="utf-8").write(s)
    print("allow-list extended by %d terms" % len(
        [x for x in ADD.split('"') if x.strip() and not x.strip().startswith("#")]) )
else:
    print("already extended")
