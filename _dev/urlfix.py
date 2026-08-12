#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repoint citations whose sources have moved, and name the ones that died.

WHY THIS MATTERS MORE HERE THAN ON AN ORDINARY SITE. Every claim on this site is
supposed to be traceable to a real source. A dead citation does not merely
annoy - it silently converts a sourced claim into an unsourced one, and the
reader has no way to tell the difference. A full outbound sweep of 1,665
distinct external URLs across 130 pages found 10 dead and 68 moved.

THREE CATEGORIES, AND THE DIFFERENCE IS THE WHOLE POINT.

  SWAP - the source moved to a specific equivalent page. Safe and mechanical.
  Whole-site reorganisations dominate: St Mary's moved its counselling
  programme under the Kalmanovitz School, USC Rossier folded its admissions
  subdomain into the main site, CSULB's catalog moved to a vendor domain,
  Kaiser reorganised everything this session's research had just cited.

  LEAVE - the redirect is cosmetic (a www prefix, a trailing slash, a port) or
  it lands somewhere generic. A 301 from a specific course page to a catalog
  home page is not a move, it is a deletion with a soft landing, and rewriting
  the citation to point at the index would make it look like we cite index
  pages for course facts.

  DEAD - no equivalent exists. These are NOT rewritten. They are listed at the
  bottom of this file so the next pass starts from a decision rather than a
  rediscovery, and the pages that carry them need their claims re-sourced or
  reworded by hand.

WHAT MUST NEVER BE SWAPPED, and this pass would have got it wrong. The affiliate
links are HTTP redirectors - partners.simplepractice.com and
share.findheadway.com both 301 to the merchant with tracking attached. They
appear in a redirect report looking exactly like a moved page. Rewriting either
one to its destination would strip the tracking and cost the site its only
revenue, silently, while every link still worked. They are refused explicitly
below and the guard fails if either destination ever appears in the markup.

Idempotent: a second run finds nothing to change.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

# --------------------------------------------------------------------- swaps
SWAP = {
    # ---- confirmed 404, replacement verified 200
    "https://pointloma-public.courseleaf.com/grad-catalog/colleges-schools-departments/chs/grad-health-sciences/clinical-counseling-ma-online/":
        "https://pointloma-public.courseleaf.com/grad-catalog/colleges-schools-departments/chs/kin/clinical-counseling-ma-online/",
    "https://kpsahs.edu/programs/master-science-counseling":
        "https://kpsahs.edu/academics/all-programs/counseling-ms",
    "https://kpsahs.edu/master-science-counseling/":
        "https://kpsahs.edu/academics/all-programs/counseling-ms",
    "https://kpsahs.edu/student-resources/academic-catalog":
        "https://kpsahs.edu/academics/academic-catalog",
    "https://www.sondermind.com/for-providers/":
        "https://www.sondermind.com/providers/",
    "https://ensorahealth.com/mental-health/":
        "https://ensorahealth.com/who-we-serve/mental-health-solo-practice/",

    # ---- 301 to a specific equivalent: regulatory and reimbursement first,
    # because those sit under claims about what the law and the payers do.
    "https://www.cms.gov/medicare/payment/fee-schedules/physician/lookup-tool":
        "https://www.cms.gov/medicare/physician-fee-schedule/search/overview",
    "https://www.ecfr.gov/current/title-21/section-1308.11":
        "https://www.ecfr.gov/current/title-21/chapter-II/part-1308/subject-group-ECFRf62f8e189108c4d/section-1308.11",
    "https://www.ecfr.gov/current/title-21/section-1308.13":
        "https://www.ecfr.gov/current/title-21/chapter-II/part-1308/subject-group-ECFRf62f8e189108c4d/section-1308.13",
    # The subpart CHANGED, E to G. The old link still lands correctly today,
    # which is exactly why this one needs fixing now: any citation text naming
    # subpart E is already wrong even though the link works.
    "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-B/part-149/subpart-E/section-149.610":
        "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-B/part-149/subpart-G/section-149.610",
    "https://www.ecfr.gov/current/title-20/chapter-III/part-404/subpart-C/section-404.211":
        "https://www.ecfr.gov/current/title-20/chapter-III/part-404/subpart-C/subject-group-ECFR7fa0e3667334188/section-404.211",
    "http://aamft.informz.net/AAMFT/data/images/COAMFTE/COAMFTE%20Complaint%20Action%20Letter%202024%20-%20Touro%20University%20Worldwide.pdf":
        "https://assets.informz.net/AAMFT/data/images/COAMFTE/COAMFTE%20Complaint%20Action%20Letter%202024%20-%20Touro%20University%20Worldwide.pdf",

    # ---- school reorganisations
    "https://sentio.org/mft-program-overview":
        "https://sentio.org/sentio-mft-program-overview",
    "https://www.stmarys-ca.edu/graduate-professional-studies/ma-counseling/frequently-asked-questions":
        "https://www.stmarys-ca.edu/kalmanovitz-school-of-education/counseling/masters-counseling-program/frequently-asked-questions",
    "https://www.stmarys-ca.edu/graduate-professional-studies/ma-counseling/learning-outcomes":
        "https://www.stmarys-ca.edu/kalmanovitz-school-of-education/counseling/masters-counseling-program/learning-outcomes",
    "https://www.stmarys-ca.edu/graduate-professional-studies/ma-counseling/program-details":
        "https://www.stmarys-ca.edu/kalmanovitz-school-of-education/counseling/program-details",
    "https://www.stmarys-ca.edu/graduate-professional-studies/ma-counseling/specializations/mft-pcc":
        "https://www.stmarys-ca.edu/kalmanovitz-school-of-education/counseling/masters-counseling-program/mft-pcc",
    "https://www.stmarys-ca.edu/kalmanovitz-school-of-education/counseling/masters-counseling-program":
        "https://www.stmarys-ca.edu/kalmanovitz-school-of-education/masters-counseling-program",
    "https://admissions.rossier.usc.edu/how-to-apply/ms-in-marriage-and-family-therapy-application-instructions/":
        "https://rossier.usc.edu/programs/masters/mft/mft-application-instructions/",
    "https://admissions.rossier.usc.edu/how-to-apply/ms-in-marriage-and-family-therapy-mft-courses/":
        "https://rossier.usc.edu/programs/masters/mft/mft-course-schedule/",
    "https://rossier.usc.edu/news-insights/news/2024/july/usc-launches-master-science-marriage-and-family-therapy-online-program":
        "https://rossier.usc.edu/news/usc-launches-master-of-science-in-marriage-and-family-therapy-online-program/",
    "https://www.alliant.edu/admissions/graduate-application-requirements/":
        "https://www.alliant.edu/admissions/graduate",
    "https://www.alliant.edu/admissions/tuition/":
        "https://www.alliant.edu/admissions/tuition-and-fees",
    "https://www.alliant.edu/psychology/marital-and-family-therapy/ma/curriculum":
        "https://www.alliant.edu/marital-and-family-therapy/ma",
    "https://www.thechicagoschool.edu/los-angeles/":
        "https://www.thechicagoschool.edu/in-the-community/locations/los-angeles/",
    "https://lasierra.edu/education/psychology-counseling/course-descriptions/":
        "https://lasierra.edu/schools/education/psychology-counseling/course-descriptions/",
    "https://www.csub.edu/psychology/university-counselor-training-clinic-uctc-0":
        "https://www.csub.edu/psychology/uctc.shtml",
    "https://www.redlands.edu/meet-redlands/regional-campus-locations/":
        "https://www.redlands.edu/about/campus-locations",
    "https://soundmind.center/team": "https://www.soundmind.institute/team",
    "https://www.mind-foundation.org/molecules":
        "https://www.mind-foundation.org/en/molecules",
    "https://mind-foundation.org/apt/faculty":
        "https://www.mind-foundation.org/augmented-psychotherapy-training/faculty",
    "https://dnm.colorado.gov/": "https://nmd.colorado.gov/",
    "https://www.atcb.org/credentials/atr/":
        "https://atcb.org/atcb-pathways/atr-bridge-plan/",
    "https://www.gradreports.com/colleges/fresno-pacific-university":
        "https://www.onlineu.com/online-reviews/fresno-pacific-university",
}
# CSULB moved its whole catalog to a vendor domain, seven links, all the same
# host swap with the query string intact. Expressed as a rule rather than
# seven lines, because the next catalog page cited will need it too.
HOST_SWAP = [("https://catalog.csulb.edu/", "https://csulb.catalog.acalog.com/")]

# --------------------------------------------------------------------- refuse
# An HTTP redirector is not a moved page. Both of these 301 to the merchant
# with tracking attached, and both appear in a redirect report looking exactly
# like a source that moved.
NEVER = [
    "partners.simplepractice.com",
    "share.findheadway.com",
]
NEVER_DEST = [
    "simplepractice.com/partners/affiliate-ps",
    "headway.co/share-link",
]

# --------------------------------------------------------------------- dead
# No equivalent found. Left in place deliberately: a citation pointing at a
# 404 is at least honest about where the claim came from, whereas repointing it
# at a plausible neighbour would be fabricating a source. The pages carrying
# these need the claim re-sourced or reworded, which is editorial work.
DEAD = {
    "https://www.cpp.edu/class/psychology/ms-psy-program/faq.shtml":
        "Cal Poly Pomona deleted the whole ms-psy-program tree. cal-poly-pomona-mft.html "
        "QUOTES this page directly, so the quotes are now unsourced. The live "
        "department index is https://www.cpp.edu/class/psychology/index.shtml.",
    "https://www.cpp.edu/class/psychology/ms-psy-program/index.shtml":
        "Same tree, same problem.",
    "https://phillips.campbellsville.edu/counseling-center/pre-masters-traineeship/":
        "Campbellsville's regional-centers tree moved and this page did not "
        "survive it; the redirect target 404s as well.",
    "https://ms.cp.mft.ndnu.edu/":
        "NXDOMAIN. Notre Dame de Namur is in teach-out and the programme "
        "subdomain is gone. The page should say the programme site no longer "
        "exists rather than link to it.",
    "https://www.rula.com/for-providers/":
        "Rula has no live provider page: /providers/ redirects in a loop and "
        "every plausible alternative 404s. Only /careers/ is up.",
}


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    for old in SWAP:
        if any(n in old for n in NEVER):
            sys.exit("urlfix: %s is an affiliate redirector and must not be "
                     "rewritten" % old)

    hits, changed = {}, 0
    for f in pages():
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        before = s
        for old, new in SWAP.items():
            n = s.count(old)
            if n:
                s = s.replace(old, new)
                hits[old] = hits.get(old, 0) + n
        for oldh, newh in HOST_SWAP:
            n = s.count(oldh)
            if n:
                s = s.replace(oldh, newh)
                hits[oldh] = hits.get(oldh, 0) + n
        if s != before:
            open(path, "w", encoding="utf-8").write(s)
            changed += 1

    for k in sorted(hits, key=lambda x: -hits[x]):
        print("%4d  %s" % (hits[k], k[:96]))
    print("%d citation(s) repointed across %d page(s)" % (sum(hits.values()), changed))

    # ---- guards
    bad = 0
    for f in pages():
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        for old in SWAP:
            if old in s:
                print("GUARD %s: a swapped URL survives - %s" % (f, old[:70]))
                bad += 1
                break
        # The affiliate redirectors must still be the redirectors.
        for d in NEVER_DEST:
            if d in s:
                print("GUARD %s: an affiliate link was rewritten to its "
                      "destination, which strips the tracking" % f)
                bad += 1
        for n in NEVER:
            pass
    # Both redirectors must still be present somewhere, or something upstream
    # rewrote them.
    allmarkup = "".join(open(os.path.join(SITE, f), encoding="utf-8").read()
                        for f in pages())
    for n in NEVER:
        if n not in allmarkup:
            print("GUARD: %s has disappeared from the site entirely" % n)
            bad += 1
    if DEAD:
        print("\nSTILL DEAD, needing an editorial decision rather than a swap:")
        for u, why in DEAD.items():
            print("  %s\n     %s" % (u[:92], why))
    if bad:
        sys.exit("urlfix: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
