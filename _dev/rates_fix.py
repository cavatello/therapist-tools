#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Correct the two published-fee-schedule rows on rates.html.

rates.html is hand-written and has no builder, so this exists to make the edit
reproducible and to record why it was made.

WHAT WAS WRONG, both verified from the primary documents rather than taken from
a secondary read:

MEDICARE. The row said ~$125. That is the national unadjusted amount ($125.25)
with no California GPCI applied, and every California practice-expense GPCI is
at or above 1.096, so it understated the rate everywhere in the state. Computed
from CMS's own CY2026 RVU release: 90837 carries 5.00 total non-facility RVUs
(work 3.78, PE 1.20, MP 0.02); the CY2026 non-qualifying-APM conversion factor
is $33.4009; apply the final California GPCIs and then the 75% reduction under
42 U.S.C. 1395l(a)(1)(FF). Rest of California is $129.52, Santa Clara $148.66.
The arithmetic checks against the published $167.00 national non-facility
amount.

The page's existing wording - "75% of the psychologist rate" - is left alone. It
is what the statute literally says, and since psychologists are paid the full
schedule amount it resolves to the same number. It is more precise than "75% of
the physician fee schedule", not less.

MEDI-CAL. The row said $98 in both columns. $98.02 is real but it is the
"MD, NP, PA" column; the "LP, LCSW, LPCC, LMFT" column pays $38.01. So the row
was quoting the wrong column.

BUT THIS IS NOT A NUMBER SWAP, and that is the point of this file. Two things
make a straight substitution the wrong fix:

  1. As published, 90837 (60 min, $38.01) pays LESS than 90834 (45 min, $67.16)
     in the therapist column. That looks like a defect in the DHCS document -
     $38.01 is also the crisis-code rate printed one row below in both columns -
     rather than policy. Printing it alone, without the 90834 comparison, would
     hand a reader a number that is technically sourced and practically
     misleading.

  2. More decisively, only 5.8% of Medi-Cal is fee-for-service. Outpatient
     psychotherapy for the other 94.2% is a managed care plan or county mental
     health plan responsibility at negotiated rates nobody publishes. So the
     published schedule is a floor reference, not what a contracted Medi-Cal
     therapist is paid - and a table headed "verifiable fee schedules" has to
     say so or the heading is doing work the row cannot support.

The associate column changes regardless: it said $98, and there is no associate
rate at all. An associate cannot be the billing provider; the supervising
clinician is.

CalVCB was checked and is correct - $105 and $97, effective 15 December 2022 and
carried forward in the 2024 revision. Left untouched.

Idempotent: re-running finds the old rows gone and does nothing.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PAGE = os.path.join(SITE, "rates.html")

OLD_MEDICARE = ("<tr><td>Medicare, 2026 (90837)</td><td>&asymp;$125</td>"
                "<td>n/a</td></tr>")
NEW_MEDICARE = ('<tr><td>Medicare, CY2026 (90837)</td>'
                "<td>$130&ndash;$149<br><span class=\"mono\" style=\"font-size:11.5px\">"
                "Rest of CA $129.52 &middot; LA $134.47 &middot; SF $146.29 "
                "&middot; Santa Clara $148.66</span></td><td>n/a</td></tr>")

OLD_MEDICAL = ("<tr><td>Medi-Cal, 2026 (90837)</td><td>$98</td><td>$98</td></tr>")
NEW_MEDICAL = ('<tr><td>Medi-Cal fee-for-service (90837)</td>'
               "<td>$38.01<br><span class=\"mono\" style=\"font-size:11.5px\">"
               "90834, 45 min: $67.16</span></td>"
               "<td>n/a</td></tr>")

OLD_NOTE = ('<p style="font-size:13.5px; color:var(--muted);">Medicare pays LMFTs '
            "and LPCCs at 75% of the psychologist rate. LMFTs became independently "
            "billable to Medicare in January 2024.<sup>[1]</sup></p>")
NEW_NOTE = (
    '<p style="font-size:13.5px; color:var(--muted);">Medicare pays LMFTs and '
    "LPCCs at 75% of the psychologist rate, and LMFTs became independently "
    "billable in January 2024.<sup>[1]</sup> The range above is that 75% applied "
    "to each California locality &mdash; 5.00 non-facility RVUs for 90837 "
    "&times; the CY2026 conversion factor of $33.4009 &times; the local GPCIs. "
    "It is the allowed amount: Medicare pays 80% and the client owes the other "
    "20%.</p>"
    '<div class="note"><b>The Medi-Cal row is a floor, not a going rate.</b> '
    "Two things about it. Its own published table pays <b>less for the 60-minute "
    "code than for the 45-minute one</b> &mdash; $38.01 against $67.16 &mdash; "
    "which reads as a defect in the document rather than policy, and the $98 "
    "figure quoted almost everywhere is the physician column, not the therapist "
    "one. More importantly, <b>only about 6% of Medi-Cal is fee-for-service</b>. "
    "Outpatient psychotherapy for the rest runs through managed care plans and "
    "county mental health plans at negotiated rates nobody publishes, so this "
    "schedule tells you what the floor looks like and nothing about what a "
    "contracted Medi-Cal therapist actually receives. Associates have no rate "
    "here at all &mdash; the supervising clinician is the billing provider.</div>")


def main():
    s = open(PAGE, encoding="utf-8").read()
    before = s
    done = []
    for old, new, name in ((OLD_MEDICARE, NEW_MEDICARE, "Medicare row"),
                           (OLD_MEDICAL, NEW_MEDICAL, "Medi-Cal row"),
                           (OLD_NOTE, NEW_NOTE, "footnote and caveat")):
        if old in s:
            s = s.replace(old, new, 1)
            done.append(name)
    if s == before:
        print("rates_fix: nothing to change (already applied)")
    else:
        open(PAGE, "w", encoding="utf-8").write(s)
        print("rates_fix: %s" % ", ".join(done))

    # ---- guards
    bad = 0
    s = open(PAGE, encoding="utf-8").read()
    # The two wrong figures must not survive in the fee-schedule table.
    i = s.find("Published, verifiable fee schedules")
    table = s[i:i + 1400] if i >= 0 else ""
    if "&asymp;$125" in table:
        print("GUARD: the unadjusted national Medicare figure survives")
        bad += 1
    if re.search(r"<td>\$98</td>", table):
        print("GUARD: the physician-column Medi-Cal figure survives")
        bad += 1
    # A number this page publishes must be accompanied by what it is.
    for must, why in (("$129.52", "the low end of the Medicare range"),
                      ("$148.66", "the high end of the Medicare range"),
                      ("$67.16", "the 90834 comparison that makes $38.01 readable"),
                      ("only about 6% of Medi-Cal is fee-for-service",
                       "the caveat that makes the row honest")):
        if must not in s:
            print("GUARD: missing %s (%s)" % (must, why))
            bad += 1
    # CalVCB was verified correct and must be left alone.
    if "<tr><td>CalVCB (per hour)</td><td>$105</td><td>$97</td></tr>" not in s:
        print("GUARD: the CalVCB row was altered - it was verified correct")
        bad += 1
    if s.count("<h1") != 1:
        print("GUARD: %d h1" % s.count("<h1"))
        bad += 1
    if bad:
        sys.exit("rates_fix: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
