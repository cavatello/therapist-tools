#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for the three parsers that turn prose into numbers.

WHY THIS FILE EXISTS. Three separate bugs have now been found in this code, all
of the same shape and all silent:

  units_of   took the first number in the sentence, so "4.5 quarter units per
             course" read as a 4.5-unit degree and "43 units base MS; 60 with
             the MFT concentration" read as the wrong degree.
  years_of   could not match "2-year or 2.5-year tracks", and turned
             "8 quarters (24 months)" into 2.67 years by assuming three
             quarters a year when the school had already said 24 months.
  format_of  matched "in-person" but not "in person", so a school that said
             exactly what it does read as saying nothing.

None of them crashed. Two of them made the site state something false about a
school - that it publishes no length, or no format - and one fed the cost
chart. On a site whose entire proposition is that every figure is real, a
silently wrong parser is the most expensive kind of bug there is, and none of
these was found by a guard. Two were found by eye, and the third by a derived
sentence on a card that happened to print the raw string.

So: every case that has ever been wrong is pinned here, alongside the cases that
were always right, because the fix for one of them is exactly the kind of change
that breaks another.

THE SHARED PRINCIPLE THESE TEST. A parser reading prose should fail to an honest
"not published" rather than to a confident absurdity. Hence MIN_UNITS and the
one-to-six-year clamp: not to be clever, but so that the failure mode is a gap
a reader can see rather than a number they cannot check.

Run: python3 test_charts.py
"""
import sys

import charts

# (length string, expected years or None, why this case is here)
YEARS = [
    ("2 years", 2.0, "the ordinary case"),
    ("3 years (7 semesters)", 3.0, "years wins over a parenthetical term count"),
    ("2.5-3 years", 2.5, "a range takes the low end"),
    ("5 semesters", 2.5, "term counts convert where nothing else is stated"),
    ("24 months", 2.0, "months convert"),
    ("26 months", 26 / 12.0, "months that are not a whole year"),
    ("2-year or 2.5-year tracks", 2.0,
     "BUG: the hyphen after the number was not allowed before 'year'"),
    ("2-year or 2.5-year plans", 2.0, "the same shape, second school"),
    ("Three-year or four-year pathway", 3.0,
     "BUG: word-numbers were not matched at all"),
    ("Two-year full-time track (14-16 units per quarter) or three-year track",
     2.0, "word-number, with a digit range earlier in the sentence to distract"),
    ("8 quarters (24 months) minimum full-time, one-day-per-week schedule", 2.0,
     "BUG: read as 2.67 by assuming 3 quarters a year, when the school said 24 "
     "months. An explicit duration must beat an inference."),
    ("21 courses plus a 12-month practicum", None,
     "the 12 months are the PRACTICUM, not the degree - must stay unparsed"),
    ("90 quarter units in 6 quarters", None,
     "a unit count in the length field would read as 30 years without the clamp"),
    ("", None, "empty"),
    (None, None, "absent"),
    ("Varies", None, "prose with no number"),
]

# (record, expected (count, system), why)
UNITS = [
    ({"units": "60 semester units"}, (60.0, "semester"), "the ordinary case"),
    ({"units": "90 quarter units"}, (90.0, "quarter"), "quarter calendar"),
    ({"units": "63-90 units"}, (63.0, "semester"), "a range takes the low end"),
    ({"units": "60 credits (LPCC specialization adds 5)"}, (60.0, "semester"),
     "the base requirement, not the specialisation"),
    ({"units": "Quarter system; 4.5 quarter units per course; total not stated"},
     (None, None),
     "BUG: units PER COURSE read as the degree total. The string says the "
     "total is not stated and the parser must agree with it."),
    ({"units": "25 Northwestern quarter units (26 courses)"}, (None, None),
     "BUG: a non-standard unit, not comparable with anyone else's"),
    ({"units": "43 units base MS; 60 units with MFT and/or PCC concentration",
      "units_n": 60, "units_sys": "semester"}, (60.0, "semester"),
     "BUG: the first number is the NON-qualifying degree. units_n overrides "
     "the prose without rewriting prose for a parser's benefit."),
    ({"units": None}, (None, None), "absent"),
]

# (format string, expected bucket, why)
FORMAT = [
    ("On-campus", "In person", "the ordinary case"),
    ("Fully online", "Fully online", "online"),
    ("Hybrid — online coursework plus in-person practicum",
     "Hybrid or low-residency", "explicit hybrid"),
    ("On-campus and fully online (synchronous + asynchronous)",
     "Hybrid or low-residency", "both modes named makes it hybrid"),
    ("In person, with evening and part-time options", "In person",
     "BUG: 'in person' without the hyphen matched nothing"),
    ("On-ground; morning, afternoon and evening courses", "In person",
     "BUG: 'on-ground' is unambiguous and was unmatched"),
    ("In class two nights a week, in 7-week terms", "In person",
     "BUG: 'in class' is unambiguous and was unmatched"),
    ("In person at Rocklin and San Jose, with a fully remote option",
     "Hybrid or low-residency", "'remote' counts as online"),
    ("Evening and daytime cohorts", None,
     "a TIMETABLE, not a delivery mode - must stay unparsed. Guessing 'in "
     "person' here would invent the one fact the field exists to carry."),
    ("Cohort model; daytime and weekend schedules", None, "same reasoning"),
    ("", None, "empty"),
]


def main():
    fails = []

    for L, want, why in YEARS:
        got = charts.years_of({"length": L})
        ok = (got is None and want is None) or (
            got is not None and want is not None and abs(got - want) < 0.005)
        if not ok:
            fails.append("years_of(%r) -> %r, expected %r  [%s]"
                         % (L, got, want, why))

    for rec, want, why in UNITS:
        got = charts.units_of(rec)
        if got != want:
            fails.append("units_of(%r) -> %r, expected %r  [%s]"
                         % (rec.get("units"), got, want, why))

    for F, want, why in FORMAT:
        got = charts.format_of({"format": F})
        if got != want:
            fails.append("format_of(%r) -> %r, expected %r  [%s]"
                         % (F, got, want, why))

    # A cost is only computed where the units survived. This is the path the
    # unit bugs would have travelled down if any of the three schools had
    # published a per-unit rate, which none happened to.
    if charts.cost_of({"per_unit": 1000,
                       "units": "Quarter system; 4.5 quarter units per course"
                       }) != (None, None):
        fails.append("cost_of computed a total from a per-course unit count")
    if charts.cost_of({"per_unit": 1000, "units": "60 semester units"}) \
            != (60000, "computed"):
        fails.append("cost_of stopped computing a legitimate total")
    if charts.cost_of({"total": 50000, "per_unit": 1000,
                       "units": "60 semester units"}) != (50000, "published"):
        fails.append("a published total no longer beats a computed one")

    n = len(YEARS) + len(UNITS) + len(FORMAT) + 3
    if fails:
        print("%d of %d FAILED:" % (len(fails), n))
        for f in fails:
            print("  - " + f)
        sys.exit(1)
    print("%d cases pass" % n)


if __name__ == "__main__":
    main()
