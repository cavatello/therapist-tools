#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BBS fees halved on 1 July 2026. The associate pages still show the old ones.

Both associate pages carried the fee schedule "effective 1 January 2021":
registration $150, annual renewal $150, law and ethics exam $150, application
for licensure $250, clinical exam $250, licence renewal $200 - and the job
advisor added them into a $1,750 total for the whole route to licensure.

Every one of those halved on 1 July 2026 under a temporary BBS fee reduction
running to 30 June 2030. Verified line by line against the Board's own FAQ
(bbs.ca.gov/pdf/publications/fee_reduction_faqs.pdf) on 5 August 2026:

    Registration Application AMFT, ASW, APCC        $150 -> $75
    Annual Renewal AMFT, ASW, APCC                  $150 -> $75
    California Law & Ethics Exam LMFT, LCSW, LPCC   $150 -> $75
    License Application LMFT, LCSW, LPCC, LEP       $250 -> $125
    LMFT Clinical Exam                              $250 -> $125
    Biennial Active Renewal LMFT, LCSW, LPCC; LEP   $200 -> $100

New total: 75 + (75 x 5) + 75 + 125 + 125 + 100 = $875.

Two things deliberately NOT folded into that total:

  - The $20 Mental Health Practitioner Education Fund fee, which the FAQ says
    "is not reduced as part of the temporary fee reduction". It applies to
    "license renewal-related applications", and the FAQ does not enumerate
    which ones, so adding it to a headline total would be a guess. It is
    stated in the note instead.
  - The reversion. This is a temporary reduction with a published end date, so
    the note carries the window rather than presenting $875 as permanent.

NOTE ON THE BOARD'S OWN PAGES: bbs.ca.gov/licensees/manage.html still displays
the pre-reduction table. The FAQ is the more specific and more recent document
and it is the one cited here, but if a reader lands on manage.html they will
see different numbers - which is exactly why the citation links the FAQ.

Idempotent: every replacement asserts it matches exactly once, so a second run
fails loudly rather than half-applying.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

OLD_CITE_URL = "https://www.bbs.ca.gov/pdf/bbs_fee_increase_2021.pdf"
NEW_CITE_URL = "https://www.bbs.ca.gov/pdf/publications/fee_reduction_faqs.pdf"

REPLACEMENTS = [
    # the citation, on both pages
    (OLD_CITE_URL, NEW_CITE_URL),
    ("BBS fee schedule, effective 1 January 2021",
     "BBS temporary fee reduction, effective 1 July 2026"),
    ("Registration $150, annual renewal $150, law and ethics exam $150, "
     "application for licensure $250, clinical exam $250, licence renewal $200.",
     "Registration $75, annual renewal $75, law and ethics exam $75, "
     "application for licensure $125, clinical exam $125, licence renewal $100. "
     "Halved from 1 July 2026 until 30 June 2030; a separate $20 Mental Health "
     "Practitioner Education Fund fee is not reduced."),
]

TABLE = [
    ("<tr><td>Associate registration</td><td>$150</td></tr>",
     "<tr><td>Associate registration</td><td>$75</td></tr>"),
    ("<tr><td>Associate renewal, each year</td><td>$150</td></tr>",
     "<tr><td>Associate renewal, each year</td><td>$75</td></tr>"),
    ("<tr><td>California Law and Ethics exam</td><td>$150</td></tr>",
     "<tr><td>California Law and Ethics exam</td><td>$75</td></tr>"),
    ("<tr><td>Application for licensure</td><td>$250</td></tr>",
     "<tr><td>Application for licensure</td><td>$125</td></tr>"),
    ("<tr><td>Clinical exam</td><td>$250</td></tr>",
     "<tr><td>Clinical exam</td><td>$125</td></tr>"),
    ("<tr><td>Licence renewal, every two years</td><td>$200</td></tr>",
     "<tr><td>Licence renewal, every two years</td><td>$100</td></tr>"),
    ("<td><b>$1750</b></td>", "<td><b>$875</b></td>"),
    ("Fees effective 1 January 2021. The law and ethics exam has to be taken "
     "during each renewal cycle until you pass it, so the $150 can recur.",
     "Fees are the BBS temporary reduction in force from 1 July 2026 to "
     "30 June 2030; they revert after that. The law and ethics exam has to be "
     "taken during each renewal cycle until you pass it, so the $75 can recur. "
     "A separate $20 Mental Health Practitioner Education Fund fee applies to "
     "licence renewal-related applications and is not reduced, so it is not in "
     "the total above."),
]

PAGES = {
    "associate-mft-job-advisor.html": REPLACEMENTS + TABLE,
    "amft-3000-hours-california.html": REPLACEMENTS,
}


def main():
    changed = 0
    for slug, pairs in sorted(PAGES.items()):
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            print("%-38s MISSING" % slug)
            continue
        s = open(path, encoding="utf-8").read()
        for old, new in pairs:
            n = s.count(old)
            if n != 1:
                sys.exit("%s: expected 1 match for %r, found %d" % (slug, old[:52], n))
            s = s.replace(old, new, 1)
        open(path, "w", encoding="utf-8").write(s)
        changed += 1
        print("%-38s %d replacement(s)" % (slug, len(pairs)))

    bad = 0
    for slug in PAGES:
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            continue
        s = open(path, encoding="utf-8").read()
        for stale in ("effective 1 January 2021", "bbs_fee_increase_2021",
                      "$1750", "annual renewal $150"):
            if stale in s:
                print("GUARD %s: stale %r survives" % (slug, stale)); bad += 1
    if bad:
        sys.exit("feepatch: %d guard failure(s)" % bad)
    print("%d page(s) repriced" % changed)


if __name__ == "__main__":
    main()
