#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Touro's MFT track is accredited WITH SHOW CAUSE, and the page said "accredited".

WHERE THIS CAME FROM

A member of a 12,500-strong California MFT Facebook group posted that they were
enrolled at Touro University Worldwide, felt they were not getting what they
needed, and were "concerned about them losing accreditation, as they are
currently under show cause". Thirteen comments.

Checked rather than repeated, because a claim about a named school's
accreditation is the most damaging thing this site could get wrong in either
direction:

  - **WSCUC (institutional): Accredited.** Most recent Commission action
    27 June 2025, no sanction of any kind. The member's fear that the *school*
    is losing accreditation is not supported.
  - **COAMFTE (programmatic): accredited with show cause.** Confirmed from
    Touro's own student-and-consumer-information page, which states it plainly:
    the MFT track "is the only track accredited with show cause" by COAMFTE.

So the member was right about the programme and wrong about the school, and the
distinction is exactly the one this site already draws for PsyD programmes -
institutional accreditation is what a licensing board looks at, programmatic
accreditation is what decides whether the degree travels.

WHY THE PAGE HAD TO CHANGE

`touro-university-worldwide-mft.html` carried `coamfte: true` and therefore
rendered the green **"COAMFTE accredited"** verdict block - the strongest
positive claim the builder can make - directly under a headline question reading
*"Is Touro's cheap online MFT accredited?"*, on the cheapest published programme
in the state. True, and materially incomplete. Somebody choosing on price was
being told the reassuring half.

WHAT THIS ADDS

1. A `notice`, using the machinery the Sentio Notice-to-Students already uses:
   a "Read this first" block above everything else, with the source and the date
   it was checked. The builder already fails the build if a notice in the data
   does not reach the page.
2. A `coamfte_note` field, mirroring the existing `lpcc_note`, and builder
   support so that a qualified accreditation renders as a **caution** rather
   than as a green tick. `coamfte` stays `true` because it is true - the
   programme is accredited - but "accredited" is no longer allowed to appear
   unqualified anywhere on the page.

WHAT IT DELIBERATELY DOES NOT SAY

That the degree will not qualify you in California. It will: the Board lists the
institution, and California licensure does not require COAMFTE accreditation at
all. This is not the Sentio situation, where the Board itself published a notice
saying graduates cannot sit the clinical exam. Saying so is part of the notice,
because the risk here is real but specific - portability, some federal and VA
employment, and the possibility that the programme loses accreditation while a
student is enrolled.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DATA = os.path.join(SITE, "mock", "mftguide", "programs.json")
BUILDER = os.path.join(SITE, "mock", "mftguide", "build_schools.py")

NOTICE = {
    "kind": "warning",
    "title": "This programme's COAMFTE accreditation is on show cause",
    "body": (
        "Touro&rsquo;s own student-and-consumer-information page states that the "
        "Marriage and Family Therapy track &ldquo;is the only track accredited "
        "with show cause&rdquo; by COAMFTE. Show cause is the most serious "
        "status short of withdrawal: the programme keeps its accreditation "
        "while it is required to demonstrate why it should not lose it. "
        "<b>Two things this does not mean.</b> The institution is not in "
        "trouble &mdash; WSCUC lists Touro University Worldwide as accredited "
        "with no sanction, most recent Commission action 27 June 2025. And it "
        "does not stop you licensing in California: the Board lists this "
        "institution, and California licensure does not require COAMFTE "
        "accreditation at all. <b>What it does affect</b> is portability to "
        "states and employers that require a COAMFTE degree, and the risk that "
        "the programme&rsquo;s status changes while you are enrolled. If you "
        "are considering this programme, or are in it, ask the programme "
        "directly what the show-cause findings were and when the Commission "
        "next reviews them."),
    "url": "https://www.tuw.edu/about/consumer-information/",
    "as_of": "10 August 2026",
}

COAM_NOTE = ("on <b>show cause</b> &mdash; see the notice at the top of this "
             "page before you read this as a clean tick")


def main():
    # ------------------------------------------------------------ the data
    progs = json.load(open(DATA, encoding="utf-8"))
    hit = [p for p in progs if p.get("institution") == "Touro University Worldwide"]
    if len(hit) != 1:
        sys.exit("patch_touro: %d Touro records, expected 1" % len(hit))
    p = hit[0]
    if not p.get("coamfte"):
        sys.exit("patch_touro: the record no longer claims COAMFTE, so this "
                 "patch would be qualifying a claim the page does not make")
    p["notice"] = NOTICE
    p["coamfte_note"] = COAM_NOTE
    json.dump(progs, open(DATA, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    print("  ok  programs.json: notice + coamfte_note set on Touro")

    # --------------------------------------------------------- the builder
    s = open(BUILDER, encoding="utf-8").read()

    # The whole `if coam:` header is replaced, rather than a substring inside
    # it, because the block is one parenthesised concatenation and swapping a
    # fragment inside it is how the first attempt produced `verdict = ((`.
    #
    # A qualified accreditation is not a green tick. `coamfte_note` mirrors the
    # existing `lpcc_note`: when set, the verdict renders as a caution and the
    # qualifier goes in the heading, so "accredited" cannot appear unqualified
    # anywhere on the page.
    OLD = ('        verdict = (\'<div class="verd ok"><h3>COAMFTE accredited'
           '</h3>\'\n')
    NEW = ('        cnote = p.get("coamfte_note")\n'
           '        verdict = (\'<div class="verd %s"><h3>COAMFTE accredited%s'
           '</h3>\'\n'
           '                   % ("warn" if cnote else "ok",\n'
           '                      (", " + cnote) if cnote else "") +\n')

    if s.count(OLD) != 1:
        sys.exit("patch_touro: the COAMFTE verdict header matched %d times, "
                 "expected 1. Do not guess - open build_schools.py and look."
                 % s.count(OLD))
    if "coamfte_note" not in s:
        s = s.replace(OLD, NEW, 1)

    # A qualifier in the data that does not reach the page is the same failure
    # the notice guard already covers.
    GOLD = '        if p.get("notice") and p["notice"]["url"] not in doc:\n'
    GNEW = ('        if p.get("coamfte_note") and "show cause" not in doc:\n'
            '            bad.append("%s: the coamfte_note did not render" % sl)\n')
    if GOLD in s and "coamfte_note did not render" not in s:
        s = s.replace(GOLD, GNEW + GOLD, 1)

    open(BUILDER, "w", encoding="utf-8").write(s)
    print("  ok  build_schools.py: coamfte_note qualifies the verdict")


if __name__ == "__main__":
    main()
