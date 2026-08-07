#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fill in Kaiser Permanente School of Allied Health Sciences.

It was the thinnest row in the directory and the most interesting one: an MFT
programme run by an integrated health system, three Northern California
campuses, and a page that published none of the basics.

WHY IT WAS EMPTY, WHICH IS WORTH RECORDING. kpsahs.edu is a Nuxt single-page
app whose text never appears in the served HTML, so every fetch of the
programme page returned chrome and nothing else. The content is reachable three
other ways: the old Drupal site is still live on a subdomain, the site's Directus
CMS answers unauthenticated reads, and the current catalog is a PDF the catalog
page only loads through JavaScript. Nothing was behind a login or a bot wall -
the page was simply unreadable to anything that does not run scripts, which is
also true of every search engine that indexes it.

THE TUITION FIGURE IS TUITION, NOT THE TOTAL COST. Kaiser publishes both, which
most schools do not: $38,970 tuition, $1,265 fees, and a $43,779 estimated grand
total including books, screenings and licensure. The directory's `total` field
means published tuition everywhere else, and the cost chart compares those, so
using the grand total here would put Kaiser a notch high against every other bar
for being more forthcoming than its peers. The fuller figures go in the note,
where they inform without distorting the comparison.

THE FINANCING FACT IS THE ONE A PROSPECTIVE STUDENT NEEDS FIRST. The school
takes no federal aid at all - not Title IV, no FAFSA. On a $40,000 degree that
changes the entire funding conversation, and it appears nowhere on the
programme page.

WHAT IS DELIBERATELY NOT CARRIED OVER: the BPPE fact sheet's 0% job-placement
rate for 2023 and 2024. It is an artifact of BPPE's employment definition applied
to graduates who are still accruing associate hours, and printing it would be
publishing a number that is technically sourced and completely misleading. The
on-time completion figures - 85% and 79% - are the meaningful ones and are in
the note.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "programs.json")
DEPTH = os.path.join(HERE, "depth")
SRC = "/tmp/slices/kaiser.json"
NAME = "Kaiser Permanente School of Allied Health Sciences"
SLUG = "kaiser-permanente-school-of-allied-health-sciences-mft"

# Prose is written here rather than lifted from the research, which is written
# for me rather than for a reader. Every fact below is in kaiser.json.
NOTE = (
    "Run by an integrated health system rather than a university, which shapes "
    "almost everything about it. Clinical placements are assigned by the "
    "programme&rsquo;s own coordinator inside Kaiser&rsquo;s Northern California "
    "Mental Health Training Program &mdash; you are not competing for a site "
    "&mdash; but Kaiser says its training locations are &ldquo;currently limited "
    "geographically&rdquo; and warns that students &ldquo;may be required to "
    "travel long distances&rdquo;. A place in the programme is not a job offer "
    "either: the post-degree Kaiser fellowship is explicitly not guaranteed. "
    "The financing is the other thing to settle early &mdash; the school accepts "
    "no federal aid at all, no Title IV and no FAFSA, so a $40,000 degree is "
    "funded by private loan, an employer, or the Mental Health Scholars Academy "
    "scholarship of up to $19,485, which is itself contingent on completing "
    "practicum at a Kaiser site."
)

CHARACTER = [
    "One cohort a year, starting each July, of about twenty to twenty-five "
    "students, on a fixed 24-month full-time schedule of eight quarters. There "
    "is no part-time or extended track published anywhere in the catalog, which "
    "makes this one of the least flexible programmes on the Board&rsquo;s list "
    "and one of the most predictable.",
    "Teaching is hybrid and built around people who work: two afternoons or "
    "evenings a week, one in person and one online, with the in-person day at "
    "Richmond, San Mateo or Lathrop. Clinical hours are the exception and run "
    "in normal business hours, which is the scheduling conflict to think through "
    "before applying rather than after.",
    "The Lathrop site is inside a working clinic &mdash; the Board&rsquo;s own "
    "paperwork names it the Kaiser Permanente Lathrop Mental Health and Wellness "
    "Center &mdash; and opened to students in July 2026.",
]

GAPS = [
    "The catalog cites Business and Professions Code &ldquo;section 498.36&rdquo; "
    "where the programme page correctly says 4980.36. A typo in the catalog, not "
    "a different rule.",
    "The BPPE fact sheet reports a 0% job-placement rate for 2023 and 2024. That "
    "is BPPE&rsquo;s employment definition applied to graduates who are still "
    "accruing associate hours, not a finding about whether they found work, and "
    "it is not reproduced as an outcome here. On-time completion &mdash; 85% and "
    "79% &mdash; is the figure that means something.",
]


def _label(url):
    """A readable name for a bare URL, from its own last path segment."""
    tail = url.rstrip("/").rsplit("/", 1)[-1].split("?")[0]
    tail = tail.replace(".pdf", "").replace("-", " ").replace("_", " ").strip()
    if not tail or tail.startswith("http"):
        return "Kaiser Permanente School of Allied Health Sciences"
    return tail[:1].upper() + tail[1:]


def main():
    if not os.path.exists(SRC):
        sys.exit("kaiser_apply: %s missing" % SRC)
    K = json.load(open(SRC, encoding="utf-8"))
    P = json.load(open(DATA, encoding="utf-8"))
    rec = next((p for p in P if p["institution"] == NAME), None)
    if rec is None:
        sys.exit("kaiser_apply: %r is not in programs.json" % NAME)

    rec.update({
        "city": "Richmond (also San Mateo and Lathrop)",
        "degree": "M.S. in Counseling, Marriage and Family Therapy",
        "units": "90 quarter credits",
        "length": "24 months, eight quarters, full time",
        "format": "Hybrid — two afternoons or evenings a week, one in person "
                  "and one online; clinical hours in business hours",
        # Tuition only, to stay comparable with every other bar on the chart.
        "total": 38970,
        "per_unit": 433,
        "tyear": "2026",
        "turl": K.get("turl"),
        "other_accreditation": "WSCUC",
        "coamfte": False,
        "note": NOTE,
        "placement": "placed",
        "placement_evidence":
            "Clinical assignments for all programs are made by the clinical "
            "coordinator in collaboration with the program director. Students "
            "may be required to travel long distances to receive full clinical "
            "education.",
        "placement_url": "https://kpsahs.edu/student-resources/academic-catalog",
        "placement_why": None,
        "own_clinic": True,
        "clinic_names": ["Kaiser Permanente Northern California Mental Health "
                         "Training Program clinics"],
        "practicum_hours": "600 supervised hours, of which 225 direct patient care",
        "practicum_hours_url": "https://kpsahs.edu/student-resources/academic-catalog",
        "practicum_length": "Observation from quarter three; 16–24 hours a week "
                            "of direct practice from quarter five",
        "gre": "not required",
        "gre_evidence": "No admission test of any kind is required for the "
                        "counseling programme; the Wonderlic applies only to "
                        "Medical Assisting and Phlebotomy.",
        "gre_url": "https://kpsahs.edu/programs/master-science-counseling",
        "min_gpa": "3.0",
        "fields_checked": "2026-08-07",
    })
    json.dump(P, open(DATA, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # A depth record, so the page has its practicum and admissions sections
    # rather than only a table. Everything here is from the catalog.
    f = os.path.join(DEPTH, SLUG + ".json")
    d = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
    d.update({
        "slug": SLUG,
        "institution": NAME,
        "city": "Richmond, San Mateo and Lathrop",
        "degree": "M.S. in Counseling, Marriage and Family Therapy",
        "url": "https://kpsahs.edu/programs/master-science-counseling",
        "orientation": "Integrated-health-system training, inside Kaiser "
                       "Permanente's own mental health clinics",
        "character": CHARACTER,
        "practicum": {
            "model": "placed",
            "model_evidence": rec["placement_evidence"],
            "model_url": rec["placement_url"],
            "own_clinic": True,
            "clinic_names": rec["clinic_names"],
            "hours": "600 supervised hours minimum, of which 225 must be direct "
                     "patient care. Eight hours a week of observation in quarters "
                     "three and four — which the school states do not count "
                     "towards licensure — then 16 to 24 hours a week of direct "
                     "practice from quarter five.",
            "starts": "Observation in quarter three; direct practice from "
                      "quarter five.",
            "detail": "Clinical training is hybrid, with at least half the time "
                      "in person at one of the Kaiser training clinics across "
                      "Northern California.",
        },
        "admissions": {
            "gre": "not required",
            "gre_evidence": rec["gre_evidence"],
            "gre_url": rec["gre_url"],
            "min_gpa": "3.0 over the last 60 semester or 90 quarter units; a "
                       "lower GPA can be addressed in the essay",
            "cohort_size": "About 20–25, one cohort a year starting in July",
            "prereqs": "Any undergraduate discipline, with no recency "
                       "requirement. Essay, résumé and two references, applied "
                       "through PsychologyCAS.",
            "src": "https://kpsahs.edu/programs/master-science-counseling",
        },
        "cost": {
            "total": 38970,
            "note": "Tuition for the July 2026 cohort is $38,970, plus $1,265 in "
                    "fees, and the school publishes an estimated grand total of "
                    "$43,779 once books, screenings and licensure fees are "
                    "included. The figure compared on the directory is tuition, "
                    "so that it sits beside other schools' tuition rather than "
                    "against their unstated extras.",
            "src": "https://kpsahs.edu/tuition-and-financial-aid/tuition-and-fees",
        },
        "gaps": GAPS,
        # The depth schema wants {label, url}; the research returns bare URLs.
        # Converting here rather than loosening the renderer: one caller with a
        # different shape is a caller's problem, and a renderer that accepts
        # both shapes stops telling you when a source lost its label.
        "sources": [{"label": _label(u), "url": u}
                    for u in (K.get("sources") or []) if u],
    })
    json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # ---- guards
    bad = 0
    for k in ("degree", "units", "length", "format", "total", "placement",
              "gre", "note"):
        if not rec.get(k):
            print("GUARD: %s is still empty" % k)
            bad += 1
    if rec["total"] >= 43779:
        print("GUARD: the grand total was used where tuition belongs - it would "
              "sit a notch high against every other bar on the cost chart")
        bad += 1
    # Scoped to everything EXCEPT `gaps`. The first version checked the whole
    # record and fired on the gaps entry that exists precisely to explain why
    # the 0% is not used - a guard cannot tell a claim from its refutation by
    # substring, so it has to be pointed at the fields that make claims.
    claims = {k: v for k, v in d.items() if k != "gaps"}
    if "0%" in json.dumps(claims):
        print("GUARD: the BPPE 0% placement artifact reached a field that "
              "presents it as a fact rather than disowns it")
        bad += 1
    if not any("0%" in g for g in d.get("gaps") or []):
        print("GUARD: the 0% artifact is no longer explained anywhere - if it "
              "is dropped silently, the next researcher will re-find it")
        bad += 1
    if not d["practicum"]["model_evidence"]:
        print("GUARD: a placement model with no quote")
        bad += 1
    print("Kaiser Permanente filled in: %s, %s, $%s tuition, practicum %s, GRE %s"
          % (rec["units"], rec["length"], "{:,}".format(rec["total"]),
             rec["placement"], rec["gre"]))
    if bad:
        sys.exit("kaiser_apply: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
