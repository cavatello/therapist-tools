#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Attach COAMFTE Student Achievement Data to the twelve accredited schools.

COAMFTE requires its accredited programmes to publish graduation, licensure and
job-placement rates by cohort on a publicly accessible page. All twelve publish
something and all twelve give cohort sizes, which is unusually clean.

AND YET THE ONE THING THIS PASS REFUSES TO BUILD IS THE COMPARISON TABLE.

Not because the definitions differ. Because they are nearly IDENTICAL and the
numbers still are not comparable - which is worse, since a shared table would
look defensible.

  1. "Licensure rate" does not mean licensed. Nine schools use COAMFTE's
     boilerplate - graduates "who have achieved ANY level of MFT licensure".
     Three break rank and say what that means in California: CSUN spells it out
     as "achieving the Associate Level of licensure", SDSU as "an associate
     title that leads to an LMFT", Alliant as "associate, provisional, or
     registered". So a 98% licensure rate largely means 98% of RESPONDING
     graduates filed an Associate registration - a form, not an outcome.

  2. Identical wording, half the number. National University uses the same
     boilerplate as Chapman and Alliant and reports 51-59%, against peers at
     90-100%. A two-fold spread on identical wording is a difference in alumni
     survey practice, not in outcomes.

  3. Two columns that are secretly one. At USD, licensure equals job placement
     in every row from 2017-18 onward (97/97, 95/95, 90/90, 86/86, 91/91,
     94/94, 97/97); the same at Northwestern. One set of survey respondents
     reported twice, not two independent facts.

  4. Graduation rate runs on different clocks. It is measured against each
     school's "advertised length", which varies from two years to four and a
     half. Hope International proves it: it publishes an extra maximum-time
     column nobody else has, showing 48.84% in advertised time against 100% at
     maximum, because 40-50% of its students choose a three-year track. Putting
     Hope's 48% beside CSUN's 87% would libel a programme for offering a
     scheduling option.

  5. Survivorship. Touro's 2020-21 full-time cohort is 274 students at 62.04%
     graduation and 98.64% licensure - but that 98.64% is a share of the ~170
     who finished. About 61% of enrollers got any credential.

So: per-school only, every figure printed beside its cohort size and the
school's own verbatim wording for what the figure counts. No cross-school view
exists anywhere on this site.

WHAT IS SHOWN. The most recent five cohorts, because the older ones drift out
of relevance and a fifty-row table on a school page is not read by anyone. Where
a school reports several campuses or tracks separately, they stay separate -
merging them would be the same averaging mistake at a smaller scale.

TWO ACCESS FINDINGS worth recording. Loma Linda publishes its required
disclosure only as JPG images - not text, not reachable by a screen reader.
USD hosts its on a Google Drive share link, and its actual "Learning and Career
Outcomes" page carries no rates at all. Both are noted on their pages, because a
required public disclosure that a blind applicant cannot read is a fact about
the school worth knowing.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DEPTH = os.path.join(HERE, "depth")
SRC = "/tmp/slices/coamfte.json"
SLUGS = json.load(open(os.path.join(HERE, "school_slugs.json"), encoding="utf-8"))
PROGRAMS = json.load(open(os.path.join(HERE, "programs.json"), encoding="utf-8"))

SHOW = 5      # most recent cohorts per school/campus/track

ALIAS = {
    "National University":
        "National University (absorbed Northcentral University and "
        "John F. Kennedy University)",
}

ACCESS = {
    "Loma Linda University":
        "Loma Linda publishes this disclosure only as JPG images. The figures "
        "below were read off those images; nothing on that page is selectable "
        "text, which means a screen reader cannot read a disclosure the "
        "accreditor requires to be public.",
    "University of San Diego (SOLES)":
        "USD&rsquo;s own &ldquo;Learning and Career Outcomes&rdquo; page carries "
        "no rates. The required disclosure is on a Google Drive share link "
        "instead, which is public but will not survive a broken share setting.",
    "Daybreak University":
        "Daybreak was accredited on 1 May 2024, so seven of its cohorts predate "
        "accreditation and the three since have no completers yet. It also "
        "published the COAMFTE template with the placeholder brackets still in "
        "the title. There is nothing to report here yet, which is what a newly "
        "accredited programme should look like.",
}


# COAMFTE's template is filled in with words as well as numbers: "NOT
# ACCREDITED" for cohorts predating accreditation, "IP" for in-progress. Those
# are the form's way of saying there is no figure, and treating them as figures
# put five rows of the word "NOT ACCREDITED" on Daybreak's page with no cohort
# size beside them - which the cohort-size guard then correctly refused. A value
# is a figure only if it contains a digit.
def rate(x):
    x = (x or "").strip()
    return x if any(ch.isdigit() for ch in x) else None


def main():
    if not os.path.exists(SRC):
        sys.exit("coamfte_apply: %s missing" % SRC)
    C = json.load(open(SRC, encoding="utf-8"))
    NAMES = {p["institution"] for p in PROGRAMS}
    COAM = {p["institution"] for p in PROGRAMS if p.get("coamfte")}

    wrote, skipped = 0, []
    for rec in C:
        name = ALIAS.get(rec["institution"], rec["institution"])
        if name not in NAMES:
            sys.exit("coamfte_apply: %r is not an institution" % name)
        if name not in COAM:
            sys.exit("coamfte_apply: %r is not marked COAMFTE-accredited in "
                     "programs.json - one of the two is wrong" % name)
        sl = SLUGS.get(name, "").replace(".html", "")
        f = os.path.join(DEPTH, sl + ".json")
        if not sl or not os.path.exists(f):
            skipped.append(name)
            continue

        # Group by campus/track so nothing is averaged across them, then keep
        # the most recent few of each.
        groups = {}
        for c in (rec.get("cohorts") or []):
            if not any(rate(c.get(k)) for k in
                       ("graduation_rate", "licensure_rate", "job_placement_rate")):
                continue                      # a row with no figures at all
            # An empty cohort still prints rates - Loma Linda's online part-time
            # 2021-22 row reads "0" graduation, "No Students" licensure, n "No
            # Students". A 0% on nobody is not a result, and it is exactly the
            # kind of cell that becomes a damning-looking number once it is
            # separated from its own denominator.
            if not rate(c.get("n")):
                continue
            k = " / ".join(x for x in (c.get("program"), c.get("campus"),
                                       c.get("track")) if x)
            groups.setdefault(k, []).append(c)
        out = []
        for k in sorted(groups):
            rows = sorted(groups[k], key=lambda c: str(c.get("year")))[-SHOW:]
            out.append({"label": k or None,
                        "rows": [{"year": c.get("year"),
                                  "graduation": rate(c.get("graduation_rate")),
                                  "licensure": rate(c.get("licensure_rate")),
                                  "placement": rate(c.get("job_placement_rate")),
                                  "n": rate(c.get("n"))} for c in rows]})

        d = json.load(open(f, encoding="utf-8"))
        d["outcomes"] = {
            "url": rec.get("url"),
            "as_published": rec.get("as_published"),
            "groups": out,
            "access_note": ACCESS.get(name),
            "school_note": rec.get("notes"),
            "shown": SHOW,
        }
        json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        wrote += 1

    print("COAMFTE outcomes attached to %d of %d accredited schools" % (wrote, len(C)))
    if skipped:
        print("  no page for: %s" % ", ".join(skipped))

    # ---- guards
    bad = 0
    n_rows = 0
    for name in COAM:
        sl = SLUGS.get(name, "").replace(".html", "")
        f = os.path.join(DEPTH, sl + ".json")
        if not sl or not os.path.exists(f):
            continue
        o = (json.load(open(f, encoding="utf-8")) or {}).get("outcomes")
        if not o:
            print("GUARD %s: COAMFTE-accredited with no outcomes record" % name)
            bad += 1
            continue
        for g in o["groups"]:
            for r in g["rows"]:
                n_rows += 1
                # A rate with no cohort size is the single way this data
                # misleads, and it is the whole reason the table is per-school.
                if not r.get("n"):
                    print("GUARD %s: a %s figure with no cohort size"
                          % (name, r.get("year")))
                    bad += 1
        if o["groups"] and not o.get("as_published"):
            print("GUARD %s: figures with no verbatim definition beside them"
                  % name)
            bad += 1
        if not o.get("url"):
            print("GUARD %s: no source URL" % name)
            bad += 1
    print("%d cohort rows across %d schools" % (n_rows, wrote))
    if bad:
        sys.exit("coamfte_apply: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
