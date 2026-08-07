#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconcile programs.json against the Board of Behavioral Sciences' own list.

THE SOURCE. https://www.bbs.ca.gov/applicants/education_resources.html - an
HTML table of 87 institutions, three columns (School Name / Degree Type / Link),
of which 77 rows carry LMFT. It is the only authority that exists for the
question this directory is built around, and until now our sixty-five records
had never been checked against it end to end.

FOUR THINGS THIS PASS CHANGES, IN ORDER OF HOW MUCH THEY MATTER.

1. THIRTEEN INSTITUTIONS WERE MISSING. The arithmetic closes exactly: 77 Board
   LMFT rows minus these 13 leaves 64, which is our 65 minus Northwestern (an
   Illinois school that qualifies through the out-of-state certification route
   and is not on the Board's table at all - kept, with that route named). One
   of the thirteen, Western Institute for Social Research at $9,600 a year, is
   by a wide margin the cheapest LMFT-qualifying degree in the state, so its
   absence was not a rounding error for a cost-sensitive reader.

2. THE LPCC COLUMN WAS MOSTLY UNKNOWN, AND SOMETIMES WRONG. Eighteen records
   said nothing; several said "BBS lists X for LMFT and LPCC", which is a note
   about the source rather than an answer. Thirty-three are corrected here from
   the Board's own row, and - this is the part that was actually wrong rather
   than merely absent - six of them resolve to NO: Chico, Cal Poly Humboldt,
   Cal Poly San Luis Obispo, USC, Fresno Pacific, La Verne and Campbellsville
   are listed for LMFT and not for LPCC.

   `lpcc` is now strictly true / false / null, and it means three different
   things: the Board lists this school for LPCC, the Board does not, and the
   Board's row was not checked. A qualifier that carries information the
   boolean cannot - Fuller's Pasadena-campus-only endorsement, CIIS's
   format-dependence, SFSU's extra emphasis requirement - moves to `lpcc_note`
   and is still printed. A qualifier that only restated the source is dropped.

3. SENTIO CARRIES A BOARD WARNING AND OUR ROW DID NOT MENTION IT. The Board has
   published a Notice to Students: Sentio holds provisional BPPE approval only,
   expiring July 2028, and its graduates may register as Associates and sit the
   Law and Ethics exam but CANNOT sit the Clinical Exam - so they cannot be
   licensed - until Sentio is fully accredited. If it is not accredited by July
   2028, existing Associates are disqualified on that degree and their
   supervised hours do not count. A directory that lists Sentio beside sixty-four
   ordinary programmes without saying that is not neutral, it is misleading.

4. NAMES. The Board writes "California State Polytechnic University, Humboldt"
   and "Wright Institute, The". Adopting those would move live URLs for no
   reader benefit, so the display name stays ours and the Board's string is
   stored in `alias`, which is what future reconciliations should match on.
   One "mismatch" is not cosmetic: the Board lists UMass Global as "California
   campus only", an eligibility limit, and that goes into the note.

WHAT THE BOARD'S LIST IS NOT. It hedges twice - degrees "may qualify", and
applicants are told to verify with the school - and it lists INSTITUTIONS, not
programmes, so a school listed for LMFT may offer several master's degrees of
which only one qualifies. Absence from it is not a finding of ineligibility
either: Bus. & Prof. Code 4980.36/4980.37 admit an unlisted or out-of-state
degree through the Board's Out-of-State Degree Program Certification. Every
degree name, city and unit count below therefore comes from the school's own
site; the Board corroborates only that the institution is listed, and for what.

Idempotent. Guarded. Run from mftguide/, then rebuild.
"""
import os, sys, json, copy

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "programs.json")
BOARD = "https://www.bbs.ca.gov/applicants/education_resources.html"

# --------------------------------------------------------------- the thirteen
# Degree, units, length and format are from each school's own page. The Board's
# table has none of those columns; it corroborates the listing and nothing else.
NEW = [
 {"institution": "America Evangelical University / Kairos Pacific University",
  "city": "Tustin",
  "degree": "M.A. in Counseling Psychology, emphasis in Marriage and Family Therapy",
  "units": "66 units", "length": "About 2.5 years",
  "format": "In person, with evening and part-time options",
  "url": "https://kairos.aeu.edu/master-marriage-and-family-therapy",
  "lpcc": True,
  "note": "The Board lists this under a double-barrelled name, “America "
          "Evangelical University, Kairos Pacific University” — AEU runs the "
          "Kairos Pacific campus on Walnut Avenue in Tustin. It is not the same "
          "institution as Kairos University in Sioux Falls, which is separately "
          "COAMFTE-accredited. The school’s own page says the programme meets "
          "the educational standards set by the Board."},

 {"institution": "California Southern University",
  "city": "Online (Chandler, AZ; incorporated in California in 1978)",
  "degree": "M.A. in Psychology, emphasis in Marriage and Family Therapy",
  "units": "60 credits", "length": None, "format": "Fully online",
  "url": "https://calsouthern.smartcatalogiq.com/en/2025-2026/general-catalog/"
         "school-of-behavioral-sciences/master-of-arts-in-psychology-with-an-"
         "emphasis-in-marriage-and-family-therapy",
  "lpcc": True,
  "other_accreditation": "Higher Learning Commission",
  "note": "One thing to settle before applying: CalSouthern’s own catalog says "
          "the Board considers it an out-of-state institution, and the Board’s "
          "table lists it for both LMFT and LPCC anyway. Those two statements are "
          "hard to reconcile from outside, and this is a question for the Board "
          "rather than for either page."},

 {"institution": "HIS University",
  "city": "Brea",
  "degree": "M.A. in Marriage and Family Therapy",
  "units": "67 units", "length": None, "format": None,
  "url": "https://hisuniversity.edu/eng/academics_01",
  "lpcc": False,
  "note": "A small Korean-American Christian institution on East Lambert Road in "
          "Brea. There is no page for the programme on its own — the link goes "
          "to the whole programme list. Its page states the 67-unit degree "
          "qualifies graduates for California LMFT licensure. Accreditation is "
          "not stated on the site, which is the first thing to ask."},

 {"institution": "Jessup University",
  "city": "Rocklin",
  "degree": "M.A. in Counseling Psychology (MACP)",
  "units": "63 units", "length": "26 months",
  "format": "In person at Rocklin and San Jose, with a fully remote option for "
            "California residents",
  "url": "https://jessup.edu/academics/majors-programs/graduate/"
         "master-of-arts-counseling-psychology/",
  "lpcc": True,
  "note": "Formerly William Jessup University. The programme requires 280 direct "
          "client-contact hours and 20 hours of personal psychotherapy, and its "
          "page states it is designed to meet the Board’s qualifying-degree "
          "requirements for both LMFT and LPCC."},

 {"institution": "Kaiser Permanente School of Allied Health Sciences",
  "city": "Richmond",
  "degree": "M.S. in Counseling, Marriage and Family Therapy",
  "units": None, "length": None, "format": None,
  "url": "https://kpsahs.edu/master-science-counseling/",
  "lpcc": False,
  "note": "An MFT programme run by an integrated health system — campuses in "
          "Richmond and San Mateo, and a third opening in Lathrop in July 2026 "
          "with applications from September. Units, length, format and tuition "
          "are not published on the programme page, so this row is thinner than "
          "the rest until someone reads the academic catalog or asks admissions."},

 {"institution": "Life Pacific University",
  "city": "San Dimas",
  "degree": "M.A. in Counseling (MAC)",
  "units": "63 units",
  "length": "21 courses plus a 12-month practicum",
  "format": "Online, synchronous and asynchronous, in 8-week terms",
  "url": "https://lifepacific.edu/academics/online/master-of-arts-in-counseling/",
  "lpcc": True,
  "note": "Life Pacific announced Board approval for both LMFT and LPCC on 26 "
          "September 2025, and the Board’s table lists both. The programme page "
          "itself still mentions only LPCC — the announcement and the table are "
          "the newer sources."},

 {"institution": "Rhombus University",
  "city": "La Mesa",
  "degree": "M.A. in Counseling Psychology",
  "units": "60 units", "length": "2–3 years",
  "format": "Online and self-paced",
  "url": "https://rhombusuniversity.edu/degree/",
  "lpcc": True,
  "note": "The Board lists Rhombus for LMFT and LPCC. Its own programme page "
          "states neither licensure eligibility nor accreditation, and markets "
          "“professional Christian counselors” — confirm its accreditation "
          "with the school before treating this row as equivalent to the rest of "
          "the list."},

 {"institution": "Simpson University",
  "city": "Redding",
  "degree": "M.A. in Counseling Psychology (MACP)",
  "units": "67.5 units", "length": "2 years",
  "format": "In class two nights a week, in 7-week terms",
  "url": "https://simpsonu.edu/academics/graduate-studies/"
         "m-a-in-counseling-psychology/",
  "lpcc": True,
  "note": "The programme page states it meets Board requirements for both LMFT "
          "and LPCC. With Cal Poly Humboldt it is one of only two options on the "
          "Board’s list sited in far northern California, which is most of the "
          "reason to know about it."},

 {"institution": "Southern California Seminary",
  "city": "El Cajon",
  "degree": "M.A. in Marriage and Family Therapy (MAMFT)",
  "units": "72 units", "length": None,
  "format": "On campus, with online options",
  "url": "https://www.socalsem.edu/master-of-arts-marriage-family-therapy/",
  "lpcc": True,
  "note": "The Board lists it for LMFT and LPCC. The programme page describes the "
          "Board-required training components but does not itself name the LPCC "
          "pathway."},

 {"institution": "University of Phoenix",
  "city": "Online (Phoenix, AZ; enrolment restricted to California residents)",
  "degree": "M.S. in Counseling, Marriage, Family and Child Therapy",
  "units": "60 credits", "length": None,
  "format": "Fully online and asynchronous, in 5–6 week courses",
  "url": "https://www.phoenix.edu/online-behavioral-sciences-degrees/"
         "marriage-family-child-counseling-masters-degree.html",
  "lpcc": True,
  "note": "California residents only, by design — the programme exists to satisfy "
          "the California Board. Read it as an out-of-state institution "
          "delivering a California-specific degree, not as a California campus."},

 {"institution": "Weimar University",
  "city": "Weimar",
  "degree": "M.A. in Counseling Psychology and Wellness",
  "units": "60 units", "length": "2 years full time", "format": "Online only",
  "url": "https://weimar.edu/academics/graduate-departments/"
         "ma-counseling-psychology-and-wellness/",
  "lpcc": True,
  "note": "One of the few schools on the Board’s list that says it in its own "
          "words: the programme page states it is “approved by the state of "
          "California’s Board of Behavioral Sciences (BBS) for both LPCC and "
          "LMFT licensure requirements.”"},

 {"institution": "Western Institute for Social Research",
  "city": "Berkeley",
  "degree": "M.S. in Psychology, Marriage and Family Therapy",
  "units": None, "length": "2–6 years", "format": "Online",
  "url": "https://wisr.edu/home/degree-programs/mft-program/",
  "lpcc": True,
  "other_accreditation": "DEAC",
  "note": "Tuition is $9,600 a year, charged as an annual subscription rather "
          "than per unit — on any ordinary completion timeline that makes it by "
          "a wide margin the cheapest LMFT-qualifying degree on the Board’s "
          "list. Two things to weigh against that. It is accredited by DEAC, a "
          "national rather than a regional accreditor, which is the distinction "
          "that decides whether a degree travels. And the unit count is not on "
          "the website; it is in the June 2026 catalog PDF. Non-profit, founded "
          "1975."},

 {"institution": "Western Seminary",
  "city": "San Jose",
  "degree": "M.A. in Counseling, Marriage, Couple and Family Counseling "
            "specialization",
  "units": "71 credits", "length": "About 3 years (minimum 2 years 8 months)",
  "format": "Primarily in person, with 10 credits available online",
  "url": "https://www.westernseminary.edu/academics/masters-degrees/"
         "ma-in-counseling-california",
  "lpcc": True,
  "note": "Board-approved since 1992, and the page states it satisfies both the "
          "AMFT/LMFT and APCC/LPCC registration paths. The seminary is "
          "Oregon-based; the California counseling degree is delivered from the "
          "San Jose campus, which is what the Board lists."},
]

# ------------------------------------------------------------ the Board's LPCC
# institution -> what the Board's row says. True = listed for LPCC, False = the
# row carries LMFT and not LPCC. Read off the table, one row at a time.
LPCC = {
 "San Diego State University": True,
 "California State University, Dominguez Hills": True,
 "California State University, Chico": False,
 "California State University, Stanislaus": True,
 "San Jose State University": True,
 "California State University, Long Beach": True,
 "California State University, San Bernardino": True,
 "Cal Poly Humboldt": False,
 "Cal Poly San Luis Obispo": False,
 "University of Southern California (Rossier)": False,
 "University of San Francisco": True,
 "Loyola Marymount University": True,
 "Antioch University Los Angeles": True,
 "Fresno Pacific University": False,
 "University of La Verne": False,
 "Campbellsville University — Los Angeles Education Center": False,
 "The Wright Institute": True,
 "Notre Dame de Namur University": True,
 "The Chicago School": True,
 "Touro University Worldwide": True,
 "Loma Linda University": True,
 "University of San Diego (SOLES)": True,
 "Daybreak University": True,
 "University of the Pacific (Benerd College)": True,
 "Concordia University Irvine (Townsend Institute)": True,
 "National University": True,
 "University of Massachusetts Global (formerly Brandman)": True,
 "Pacific Oaks College": True,
 "Sofia University": True,
 "Palo Alto University": True,
 "Fuller Theological Seminary": True,
 "San Francisco State University": True,
 "California Institute of Integral Studies": True,
}

# A string qualifier survives only if it says something the boolean cannot.
# "BBS lists X for LMFT and LPCC" is a note about where the answer came from,
# not an answer, and it goes.
DROP_QUALIFIER_PREFIX = ("BBS lists",)

# ------------------------------------------------------------------- the names
# Board string -> stored as `alias`, matched on by the next reconciliation.
# The display name stays ours in every case: adopting the Board's would move
# eight live URLs and none of the eight would read better for it.
ALIAS = {
 "Cal Poly Humboldt": "California State Polytechnic University, Humboldt",
 "Cal Poly Pomona": "California State Polytechnic University, Pomona",
 "Cal Poly San Luis Obispo": "California State Polytechnic University, San Luis Obispo",
 "Alliant International University (CSPP)": "Alliant University",
 "The Wright Institute": "Wright Institute, The",
 "The Chicago School": "Chicago School, The",
 "Biola University (Talbot School of Theology)": "Biola University, Talbot School of Theology",
 "Concordia University Irvine (Townsend Institute)": "Concordia University, Townsend Institute",
 "University of Massachusetts Global (formerly Brandman)":
     "University of Massachusetts Global – California campus only",
 "California State University, Fresno (Fresno State)": "California State University, Fresno",
 "California State University, Fullerton (University Extension)":
     "California State University, Fullerton",
 "University of Southern California (Rossier)": "University of Southern California",
 "Pepperdine University (GSEP)": "Pepperdine University",
 "University of San Diego (SOLES)": "University of San Diego",
 "University of the Pacific (Benerd College)": "University of the Pacific",
 "National University (absorbed Northcentral University and John F. Kennedy University)":
     "National University",
 "Antioch University Santa Barbara": "Antioch University, Santa Barbara",
 "Antioch University Los Angeles": "Antioch University, Los Angeles",
 "Campbellsville University — Los Angeles Education Center "
 "(formerly Phillips Graduate University/Institute)":
     "Campbellsville University – Los Angeles Education Center",
}

# ----------------------------------------------------------- Board-issued flags
# A `notice` is the Board speaking about a school in its own publication, not a
# fact gathered about it. It renders as a warning block, above everything else.
NOTICE = {
 "Sentio University": {
   "kind": "warning",
   "title": "The Board has issued a Notice to Students about this school",
   "body": "Sentio holds provisional approval from the Bureau for Private "
           "Postsecondary Education, and that approval expires in July 2028. "
           "Per the Board’s notice, a Sentio graduate may register as an "
           "Associate and may sit the California Law and Ethics exam — but "
           "may not sit the Clinical Exam, and therefore cannot be licensed, "
           "until Sentio is fully accredited. If accreditation is not achieved "
           "by July 2028, Associates registered on this degree are disqualified "
           "and their supervised hours will not be accepted. That is the whole "
           "pathway, so read the notice itself before applying — and note "
           "that the school appears on the Board’s qualifying-degree list at "
           "the same time.",
   "url": "https://www.bbs.ca.gov/pdf/publications/sentio_uni_nts_status.pdf",
   "as_of": "27 May 2026"},
}

# The one school not on the Board's table at all.
OFF_LIST = {
 "Northwestern University, The Family Institute":
   "This is the only school here that does not appear on the Board’s list, "
   "under any spelling — it is an Illinois institution and the list is "
   "overwhelmingly California-sited. That is not a finding of ineligibility. Its "
   "MSMFT is COAMFTE-accredited, and a COAMFTE-accredited out-of-state degree can "
   "qualify in California through Bus. & Prof. Code §§4980.36/4980.37 and the "
   "Board’s Out-of-State Degree Program Certification — but through that route, "
   "on application, rather than automatically.",
}

UMASS = ("University of Massachusetts Global (formerly Brandman)",
         "The Board’s listing is qualified: it reads “University of "
         "Massachusetts Global – California campus only”. UMass Global is a "
         "national institution and the Board’s approval does not extend past "
         "the California campus, so confirm which campus a given cohort is "
         "enrolled through before assuming the degree qualifies.")

DEFAULTS = {"coamfte": False, "notable": None, "note": None,
            "other_accreditation": None, "per_unit": None, "total": None,
            "tyear": None, "turl": None, "units": None, "length": None,
            "format": None, "lpcc": None}


def find(P, name):
    """Ours may carry a parenthetical the Board's string does not."""
    for r in P:
        if r["institution"] == name:
            return r
    for r in P:
        if r["institution"].startswith(name):
            return r
    return None


def main():
    P = json.load(open(DATA, encoding="utf-8"))
    before = copy.deepcopy(P)
    have = {r["institution"] for r in P}

    added = []
    for rec in NEW:
        if rec["institution"] in have:
            continue
        full = dict(DEFAULTS)
        full.update(rec)
        full.setdefault("bbs_alias", None)
        full["turl"] = full.get("turl") or full["url"]
        P.append(full)
        added.append(rec["institution"])

    lpcc_set, quals, unmatched = 0, 0, []
    for name, want in LPCC.items():
        r = find(P, name)
        if r is None:
            unmatched.append(name)
            continue
        cur = r.get("lpcc")
        if isinstance(cur, str):
            if not cur.startswith(DROP_QUALIFIER_PREFIX):
                r["lpcc_note"] = cur
                quals += 1
        if cur is not want:
            lpcc_set += 1
        r["lpcc"] = want
        r["lpcc_src"] = BOARD

    aliased = 0
    for name, board in ALIAS.items():
        r = find(P, name)
        if r is None:
            unmatched.append("alias:" + name)
            continue
        if r.get("bbs_alias") != board:
            aliased += 1
        r["bbs_alias"] = board

    for name, n in NOTICE.items():
        r = find(P, name)
        if r is None:
            unmatched.append("notice:" + name)
            continue
        r["notice"] = n

    for name, txt in OFF_LIST.items():
        r = find(P, name)
        if r is None:
            unmatched.append("offlist:" + name)
            continue
        r["bbs_listed"] = False
        r["bbs_note"] = txt

    r = find(P, UMASS[0])
    if r is not None and not (r.get("note") or "").startswith("The Board’s listing"):
        r["note"] = UMASS[1] + ((" " + r["note"]) if r.get("note") else "")

    # Everything else IS on the Board's table; say so explicitly rather than by
    # the absence of a flag, so a future record cannot inherit "listed" for free.
    for rec in P:
        rec.setdefault("bbs_listed", True)
        rec.setdefault("bbs_alias", None)
        rec.setdefault("lpcc_note", None)
        rec.setdefault("notice", None)

    # stable order: keep the existing sequence, append the new ones sorted
    json.dump(P, open(DATA, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print("institutions %d -> %d" % (len(before), len(P)))
    if added:
        print("  added %d:" % len(added))
        for a in added:
            print("    " + a)
    print("  lpcc set from the Board's row: %d (qualifiers kept: %d)"
          % (lpcc_set, quals))
    print("  Board aliases stored: %d" % aliased)
    if unmatched:
        print("  UNMATCHED: %s" % ", ".join(unmatched))

    # ---------------------------------------------------------------- guards
    bad = 0
    if unmatched:
        print("GUARD: %d name(s) in this pass match no record" % len(unmatched))
        bad += 1
    names = [r["institution"] for r in P]
    if len(names) != len(set(names)):
        print("GUARD: duplicate institution after the merge")
        bad += 1
    for r in P:
        if not isinstance(r.get("lpcc"), (bool, type(None))):
            print("GUARD %s: lpcc is still a string %r"
                  % (r["institution"], r["lpcc"]))
            bad += 1
        if r.get("lpcc") is None and r.get("bbs_listed"):
            # Not fatal - it means the Board's row for this school was not read.
            print("  note: %s has no LPCC answer" % r["institution"])
        for k in ("institution", "city", "url"):
            if not r.get(k):
                print("GUARD %s: missing %s" % (r.get("institution"), k))
                bad += 1
        if r.get("url") and not r["url"].startswith("http"):
            print("GUARD %s: url is not absolute" % r["institution"])
            bad += 1
    # The count the whole reconciliation rests on.
    listed = sum(1 for r in P if r.get("bbs_listed"))
    if listed != 77:
        print("GUARD: %d records claim to be on the Board's list; the table has "
              "77 LMFT rows" % listed)
        bad += 1
    # Nothing that was already correct may have been disturbed.
    b = {r["institution"]: r for r in before}
    for r in P:
        o = b.get(r["institution"])
        if not o:
            continue
        for k in ("degree", "units", "length", "format", "url", "coamfte",
                  "per_unit", "total"):
            if o.get(k) != r.get(k):
                print("GUARD %s: %s changed, and this pass does not touch it"
                      % (r["institution"], k))
                bad += 1
    if find(P, "Sentio University").get("notice") is None:
        print("GUARD: the Sentio notice did not attach")
        bad += 1
    if bad:
        sys.exit("bbs_apply: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
