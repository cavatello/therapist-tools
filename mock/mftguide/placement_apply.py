#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge the practicum-placement and GRE research into programs.json and depth/.

WHY THESE TWO FIELDS. Practicum is the highest-consequence variable in a
California MFT degree that is not the price. It is what most often turns a
two-year programme into a three-year one, and until now this directory carried
several thousand words of practicum prose on 65 individual pages and nothing
comparable across them. The GRE is the other one: a hard application gate that
previously cost a reader seventy-eight site visits to discover.

THE TAXONOMY, AND WHY IT HAD TO BE REBUILT.

Six researchers worked a slice each and split on one question: what to call a
school that runs its own training clinic. Some called it "in-house". Others
called the same shape "assisted", reasoning that the clinic is one of several
sites a student still has to compete for and that the external placement is
where the hours - and the risk - actually are.

The second reading is right, and the disagreement exposed that "in-house" was
never a placement model at all. It is a fact about the school's facilities.
Whether the school owns a clinic and whether a seat in it is yours are
different questions, and a reader asking "could this add a year to my degree?"
is asking the second one. So the field splits in two:

  placement  - WHO SECURES YOUR SEAT. The thing that can cost you a year.
  own_clinic - does the school run a training clinic. A separate boolean,
               already collected, now no longer competing with the above.

`placement` values, in descending order of how much certainty they give a
student:

  guaranteed      the school states every student in good standing gets a seat
  placed          the school finds or assigns the site for you
  assisted        approved-site list and real support, but YOU apply and
                  compete. Most schools are here.
  student-sourced you find your own site; the school approves it
  not published   the site does not say. Thirty of seventy-eight, which is a
                  finding about the sector rather than about the research.

The gap between `assisted` and `student-sourced` is the one that must never be
guessed, so where a researcher could not tell, the answer stayed unpublished.

THE TEN RECLASSIFICATIONS below are recorded individually with the evidence
that moved each one, because a reclassification with no stated reason is
indistinguishable from a mistake, and CIIS - the school this site features most
prominently - is one of the ones that moved DOWN.
"""
import os, sys, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "programs.json")
DEPTH = os.path.join(HERE, "depth")
SLUGS = json.load(open(os.path.join(HERE, "school_slugs.json"), encoding="utf-8"))
RESEARCH = "/tmp/slices/all.json"

# institution -> (new placement, why it moved). Applied over the researchers'
# raw `model`, which used the retired "in-house" value.
RECLASS = {
    "California Lutheran University": ("guaranteed",
        "Its own words: a 12-month placement in the on-site Community Counseling "
        "Center, described as providing the clinical training itself. There is no "
        "external site search in the published model at all."),
    "Chapman University": ("guaranteed",
        "“All students in our program” complete the practicum year in the "
        "on-site Frances Smith Center. “All” is the load-bearing word."),
    "Sentio University": ("guaranteed",
        "The only school on the list that states the guarantee explicitly and "
        "draws the contrast itself: students in good standing “receive "
        "guaranteed clinical training placement”, unlike “programs that "
        "offer 'practicum support' but leave students to find their own field "
        "placements”."),
    "Cal Poly Humboldt": ("placed",
        "“You will be placed in CAPS or a community agency”, and the "
        "handbook has placements arranged by the student's faculty supervisor. "
        "The programme drives it, so this is placed rather than in-house even "
        "though year one is in its own clinic."),
    "Cal Poly San Luis Obispo": ("placed",
        "“Interviews are then arranged and, eventually, trainees are selected "
        "and placed.” The on-campus clinic is stage one; the programme "
        "places the community traineeship."),
    "California Institute of Integral Studies": ("assisted",
        "Owning three clinics is not the same as holding a seat in one. CIIS's "
        "own Field Placement Office says practicums are competitive and advises "
        "applying to at least six sites. This is the reclassification that moved "
        "a featured school down, and it is the honest reading."),
    "San Diego State University": ("not published",
        "Genuinely two-stage. The first practicum is in-house at the Dede Alpert "
        "Center; the external traineeship, where SDSU says the majority of hours "
        "accrue, does not say who secures the seat. Classified on the stage that "
        "carries the risk."),
    "Daybreak University": ("not published",
        "Has an on-site counseling center and says time there counts towards the "
        "requirement, but never says every student trains there or that a seat is "
        "assured. Owning a clinic is not a placement model."),
}

# The research is per-school prose about a two-branch school; the row is one row.
BRANCH_NOTE = {
    "Northwestern University, The Family Institute":
        "Two branches, two models. The Evanston on-campus branch trains students "
        "in The Family Institute's own clinic. The online branch — the one "
        "Californians enrol in — is placed: “Do I secure my own "
        "placements? No.” Published constraints on that branch: no placement "
        "at your current employer, up to 75 miles of travel, unpaid, and no "
        "guarantee without a car.",
    "Pepperdine University (GSEP)":
        "The GRE answer depends on format, and the marketing pages contradict the "
        "catalog: the Daytime programme requires the GRE or a completed waiver "
        "form, while the Evening programme advertises no standardised tests.",
}

# Conflicts a school publishes against itself. These are printed, not resolved -
# the point is that the reader knows to ask.
CONFLICTS = {
    "California State University, East Bay":
        "The programme page says the GRE is not required; the department's own "
        "FAQ PDF says it is required regardless of any prior postgraduate degree. "
        "Both are live. Worth a phone call before you rely on either.",
    "HIS University":
        "Two different practicum-hour figures: the academics page says 300 "
        "supervised direct hours, the February 2025 practicum manual says 250, in "
        "two modules of 125.",
    "University of La Verne":
        "The programme page says 225 fieldwork hours; the catalog says 280 direct "
        "face-to-face hours.",
    "Western Seminary":
        "The programme page says 280 direct hours; the practicum manual, dated "
        "2019, says 225 for the LMFT track.",
    "California State University, Long Beach":
        "The practicum page and the fieldwork course descriptions give different "
        "hour figures (175 against 150).",
    "Campbellsville University — Los Angeles Education Center "
    "(formerly Phillips Graduate University/Institute)":
        "Two different totals appear on the school's own pages: 375 hours in one "
        "place, 350 plus 100 in another.",
}

# Corrections the research turned up against figures already on the site.
FIX = {
    "Cal Poly Pomona": {"min_gpa": "3.0"},          # was 3.2 in our notes
    "California Baptist University": {"min_gpa": "2.75"},   # was 3.0
}

ORDER = ["guaranteed", "placed", "assisted", "student-sourced", "not published"]


def main():
    if not os.path.exists(RESEARCH):
        sys.exit("placement_apply: %s missing" % RESEARCH)
    R = {r["institution"]: r for r in json.load(open(RESEARCH, encoding="utf-8"))}
    P = json.load(open(DATA, encoding="utf-8"))

    moved, applied, missing = [], 0, []
    for p in P:
        name = p["institution"]
        r = R.get(name)
        if not r:
            missing.append(name)
            continue
        pr, gre = r["practicum"], r["gre"]

        model = pr.get("model")
        if name in RECLASS:
            new, why = RECLASS[name]
            moved.append((name, model, new))
            model = new
            pr["reclass_note"] = why
        elif model == "in-house":
            # The value is retired. Anything still carrying it was not
            # individually adjudicated, and guessing is how the taxonomy broke
            # in the first place.
            sys.exit("placement_apply: %s is still 'in-house' and has no "
                     "reclassification entry - adjudicate it by hand" % name)
        if model not in ORDER:
            sys.exit("placement_apply: %s has unknown placement %r" % (name, model))

        p["placement"] = model
        p["placement_evidence"] = pr.get("evidence") or None
        p["placement_url"] = pr.get("url") or None
        p["placement_why"] = pr.get("reclass_note")
        p["own_clinic"] = bool(pr.get("own_clinic"))
        p["clinic_names"] = pr.get("clinic_names") or None
        p["practicum_hours"] = pr.get("hours_direct") or None
        p["practicum_hours_url"] = pr.get("hours_url") or None
        p["practicum_length"] = pr.get("how_long") or None

        p["gre"] = gre.get("status")
        p["gre_evidence"] = gre.get("evidence") or None
        p["gre_url"] = gre.get("url") or None
        p["min_gpa"] = gre.get("min_gpa") or None
        p.update(FIX.get(name, {}))

        p["admissions_conflict"] = CONFLICTS.get(name)
        p["placement_branches"] = BRANCH_NOTE.get(name)
        p["fields_checked"] = r.get("checked") or "2026-08-07"
        applied += 1

    json.dump(P, open(DATA, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # Push the same facts into each school's depth record, so the page and the
    # directory row cannot drift apart.
    wrote = 0
    for p in P:
        sl = SLUGS.get(p["institution"], "").replace(".html", "")
        f = os.path.join(DEPTH, sl + ".json")
        if not sl or not os.path.exists(f):
            continue
        d = json.load(open(f, encoding="utf-8"))
        pr = d.setdefault("practicum", {})
        pr["model"] = p["placement"]
        pr["model_evidence"] = p["placement_evidence"]
        pr["model_url"] = p["placement_url"]
        pr["model_why"] = p.get("placement_why")
        pr["branches"] = p.get("placement_branches")
        pr["own_clinic"] = p["own_clinic"]
        pr["clinic_names"] = p.get("clinic_names")
        ad = d.setdefault("admissions", {}) or {}
        if isinstance(ad, dict):
            ad["gre"] = p["gre"]
            ad["gre_evidence"] = p.get("gre_evidence")
            ad["gre_url"] = p.get("gre_url")
            ad["min_gpa"] = p.get("min_gpa")
            ad["conflict"] = p.get("admissions_conflict")
            d["admissions"] = ad
        json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        wrote += 1

    from collections import Counter
    print("merged %d/%d institutions; %d depth records updated"
          % (applied, len(P), wrote))
    if missing:
        print("  NO RESEARCH for: %s" % ", ".join(missing))
    print("\n  placement")
    c = Counter(p.get("placement") for p in P)
    for k in ORDER:
        print("    %-16s %d" % (k, c.get(k, 0)))
    print("  gre")
    for k, v in Counter(p.get("gre") for p in P).most_common():
        print("    %-16s %d" % (k, v))
    print("  own clinic       %d" % sum(1 for p in P if p.get("own_clinic")))
    print("  publishes hours  %d" % sum(1 for p in P if p.get("practicum_hours")))
    print("  publishes a GPA  %d" % sum(1 for p in P if p.get("min_gpa")))
    if moved:
        print("\n  reclassified %d:" % len(moved))
        for n, a, b in moved:
            print("    %-46s %s -> %s" % (n[:46], a, b))

    # ---- guards
    bad = 0
    if missing:
        print("GUARD: %d institutions have no research" % len(missing))
        bad += 1
    for p in P:
        if p.get("placement") in ("guaranteed", "placed", "assisted",
                                  "student-sourced") and not p.get("placement_evidence"):
            print("GUARD %s: a placement claim with no quote behind it"
                  % p["institution"])
            bad += 1
        if p.get("placement_evidence") and not p.get("placement_url"):
            print("GUARD %s: quote with no source URL" % p["institution"])
            bad += 1
        if p.get("gre") not in ("required", "not required", "waivable",
                                "not published"):
            print("GUARD %s: unknown gre %r" % (p["institution"], p.get("gre")))
            bad += 1
        if "in-house" == p.get("placement"):
            print("GUARD %s: retired value survived" % p["institution"])
            bad += 1
    # Every reclassification must carry its reason onto the page.
    for n in RECLASS:
        rec = next((x for x in P if x["institution"] == n), None)
        if not rec or not rec.get("placement_why"):
            print("GUARD: %s was reclassified with no reason recorded" % n)
            bad += 1
    if bad:
        sys.exit("placement_apply: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
