#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Attach the Board's own by-school exam results to each school page.

THE FINDING THAT STARTED THIS. I had this filed as "probably impossible - the
Board likely does not break exam statistics out by institution". It does, and it
has since 2018. The reason nobody uses it is that the files are called
`exam_stats_YYYY.pdf`, which reads like an aggregate report; every one of them is
actually headed "EXAM RESULTS BY SCHOOL". The better series - thirteen
semiannual reports with a real text layer - is not linked from any page on the
Board's site and is reachable only by guessing the URL.

So the data is public, official, free, and effectively invisible. Rendering it
legibly is a genuine public service. Rendering it as a league table is not, and
most of the design decisions below exist to keep the first from becoming the
second.

WHAT IS SHOWN, AND WHAT IS DELIBERATELY NOT.

  Shown: first-time pass rate, on the school's own page, with the number of
  candidates at the same visual weight as the percentage, beside the statewide
  figure for the same window.

  Not shown: any directory column, any sort, any rank, any badge, any "top".
  There is no way to line the schools up against each other on this site, and
  that is the point rather than an oversight.

WHY FIRST-TIME RATHER THAN ALL TAKERS. 80% against 70% statewide, so the choice
is material. All-takers double-counts the same candidate on every resit, which
means it measures how many attempts people needed rather than how many passed,
and it penalises schools whose graduates keep going. First-time is the fairer
denominator and the one the Board itself splits out.

WHY A FLOOR OF FORTY. Of 122 institutions in the pooled data, 46 have twenty-
eight candidates or fewer and several have exactly one - a school with N=1 and a
pass shows as "100%", which would sit at the top of any sorted column and mean
nothing at all. A floor of 40 suppresses 57 schools while suppressing only about
2% of all first-time candidates, because the tail is genuinely tiny. Forty
rather than thirty because both leave the same 65 real institutions standing, so
the higher floor is free.

A SUPPRESSED SCHOOL SAYS SO. "Fewer than 40 candidates in six and a half years,
so no rate is published here" is information - it usually means a small or new
programme - and it is much better than an absent section, which reads as though
nobody looked.

THE CAVEAT THAT MATTERS MOST, AND WHY IT IS PRINTED EVERY TIME. In 2022 the
Council on Social Work Education REMOVED licensing-exam pass rates from its
accreditation standards, on the stated grounds that the data "may not be an
equitable measure of program outcomes" - after ASWB's own disaggregation showed
first-time pass rates of 84% for white candidates and 45% for Black candidates
on a comparable exam. The accrediting body with the most reason to want this
metric looked at it and concluded it does not measure what a school-quality
metric has to measure.

That does not make the number worthless; it makes it a number about a cohort
rather than a verdict on teaching. A programme serving more career-changers and
more students of colour will post a lower rate while teaching at least as well,
and a site that printed the figure without saying so would be laundering a
composition effect into a quality signal. So the note ships with every figure
and is not collapsible.

WHAT THE FIGURE IS NOT ABOUT. These are people who sat an exam in a window,
often years after graduating and frequently after the programme changed. The
denominator is not "students at this school today".

NAME MATCHING IS BY THE BOARD'S SCHOOL CODE, never by string similarity. The
Board's names drift between reports, and a fuzzy matcher would happily collapse
the twenty-three CSU campuses. The map below is by hand, one line per code, and
the Board's own string is printed beside every figure so a reader always knows
whose number they are looking at.

CODES ARE POOLED ONLY ACROSS A RENAME, never across an acquisition. Azusa
Pacific and Alliant each appear under two codes and are the same school. Brandman
and UMass Global are the same school before and after 2021. But John F. Kennedy
University and Northcentral University are separate institutions that National
University later absorbed, and folding their candidates into National's rate
would attribute one school's results to another - so they are left out entirely
rather than merged.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DEPTH = os.path.join(HERE, "depth")
SRC = "/tmp/slices/bbsexam.json"
SLUGS = json.load(open(os.path.join(HERE, "school_slugs.json"), encoding="utf-8"))
PROGRAMS = json.load(open(os.path.join(HERE, "programs.json"), encoding="utf-8"))

FLOOR = 40
STATS_PAGE = "https://www.bbs.ca.gov/exams/exam_stats.html"

# BBS school code -> our institution. Hand-built; see the module docstring on
# why this is not fuzzy-matched. A code absent here is a school we do not list
# (closed, or never in the directory) and is simply not used.
MAP = {
    "135": "Pepperdine University (GSEP)",
    "236": "University of Phoenix",
    "241": "Antioch University Los Angeles",
    "129": "National University (absorbed Northcentral University and "
           "John F. Kennedy University)",
    "253": "University of Massachusetts Global (formerly Brandman)",
    "272": "University of Massachusetts Global (formerly Brandman)",
    "107": "California Institute of Integral Studies",
    "105": "California Baptist University",
    "139": "Alliant International University (CSPP)",
    "112": "Alliant International University (CSPP)",
    "143": "University of San Francisco",
    "103": "Azusa Pacific University",
    "020": "Azusa Pacific University",
    "20":  "Azusa Pacific University",
    "144": "Santa Clara University",
    "006": "California State University, Fullerton (University Extension)",
    "106": "Campbellsville University — Los Angeles Education Center "
           "(formerly Phillips Graduate University/Institute)",
    "154": "Pacifica Graduate Institute",
    "133": "Pacific Oaks College",
    "010": "California State University, Northridge",
    "258": "Palo Alto University",
    "005": "California State University, Fresno (Fresno State)",
    "150": "The Wright Institute",
    "251": "The Chicago School",
    "145": "University of Southern California (Rossier)",
    "116": "Notre Dame de Namur University",
    "131": "Hope International University",
    "128": "Mount Saint Mary's University",
    "243": "Antioch University Santa Barbara",
    "119": "Fuller Theological Seminary",
    "108": "California Lutheran University",
    "007": "California State University, East Bay",     # "CSU Hayward" until 2005
    "008": "California State University, Long Beach",
    "004": "California State University, Dominguez Hills",
    "262": "Touro University Worldwide",
    "142": "University of San Diego (SOLES)",
    "015": "San Diego State University",
    "113": "Chapman University",
    "016": "San Francisco State University",
    "136": "Saint Mary's College of California",
    "232": "Western Seminary",
    "011": "California State University, Sacramento",
    "009": "California State University, Los Angeles",
    "126": "Loyola Marymount University",
    "156": "Vanguard University",
    "246": "California Southern University",
    "140": "University of La Verne",
    "018": "Sonoma State University",
    "003": "California State University, Chico",
    "125": "Loma Linda University",
    "001": "Cal Poly San Luis Obispo",
    "117": "Dominican University of California",
    "002": "California State University, Bakersfield",
    "254": "Simpson University",
    "019": "Cal Poly Pomona",
    "261": "Point Loma Nazarene University",
    "151": "Golden Gate University",
    "013": "California State University, Stanislaus",
    "012": "California State University, San Bernardino",
    "155": "Sofia University",
    "017": "San Jose State University",
    "014": "Cal Poly Humboldt",                         # "Humboldt State" until 2022
    "127": "Fresno Pacific University",
    "266": "Jessup University",

    # Below the floor, and mapped anyway. A school in this directory that the
    # Board has recorded fewer than forty candidates for should say exactly
    # that on its page - "too few to publish" is a fact about a small or new
    # programme, and it is a much better answer than a missing section.
    "237": "Southern California Seminary",
    "153": "Fresno Pacific University",          # second code; pools with 127
    "238": "University of Phoenix",              # second code; pools with 236
    "255": "University of the West",
    "231": "Meridian University",
    "247": "HIS University",
    "252": "La Sierra University",
    "220": "Western Institute for Social Research",
    "268": "Concordia University Irvine (Townsend Institute)",
    "146": "University of the Pacific (Benerd College)",
    "269": "Daybreak University",
    "270": "Rhombus University",
    "271": "Weimar University",
    "273": "Kaiser Permanente School of Allied Health Sciences",
}

# Deliberately unmapped, recorded so the next pass does not re-litigate them.
NOT_MAPPED = {
    "124": "John F. Kennedy University - a separate institution National later "
           "absorbed, not National's own graduates",
    "256": "Northcentral University - same reasoning as JFK",
    "204": "Argosy University - closed 2019, not in the directory",
    "122": "Holy Names University - closed 2023, not in the directory",
    "152": "Bethel Theological Seminary - not in the directory",
    "300": "the Board's 'Out-of-State' bucket, not an institution",
    "400": "the Board's 'Out-of-Country' bucket, not an institution",
    "104": "Biola University's row names the Rosemead School of Psychology, a "
           "different unit from the Talbot MFT degree this directory lists. One "
           "candidate, and attributing another school's result to Talbot would "
           "be wrong at exactly the level this figure is already weakest.",
    "100": "a Board placeholder row - 'Changed to school code 241'",
    "102": "a Board placeholder row - 'Changed to school code 243'",
}

# Every remaining Board code is an institution this directory does not list -
# closed, never Californian, or never an MFT programme. Named individually so a
# future pass can tell "decided against" from "never looked at".
NOT_LISTED = """130 New College of California · 265 Cambridge University ·
157 Bethany College · 250 Eisner Institute · 137 Saybrook University ·
149 Pacific Graduate School of Psychology · 216 Ryokan College ·
244 San Diego University for Integrative Studies · 203 California Graduate
Institute · 245 Santa Barbara Graduate Institute · 201 Trinity College of
Graduate Studies · 240 University of Santa Monica · 242 Antioch San Francisco ·
257 California Institute of Human Science · 110 CSPP Fresno · 260 Capella ·
248 Webster · 235 American Behavioral Studies Institute · 109 CSPP Berkeley ·
214 Professional School of Psychology · 267 Bastyr · 205 Cambridge Graduate
School · 208 Human Relations Center · 134 Pacific Union College ·
249 Pentecostal Theological Seminary · 239 Remington College · 217 Sierra
University · 054 UC San Diego · 055 UC San Francisco · 056 UC Santa Barbara ·
218 University for Humanistic Studies · 202 California Coast University ·
121 Graduate Theological Union · 210 International College · 213 Professional
School of Psychological Studies · 215 Rosebridge · 138 Southern California
School of Theology · 263 Walden · 226 World University of America"""
for _c in NOT_LISTED.replace("\n", " ").split("·"):
    _c = _c.strip().split(" ")[0]
    if _c:
        NOT_MAPPED.setdefault(_c, "not listed in this directory")


def pct(a, b):
    return round(100.0 * a / b) if b else None


def main():
    if not os.path.exists(SRC):
        sys.exit("bbsexam_apply: %s missing" % SRC)
    B = json.load(open(SRC, encoding="utf-8"))
    NAMES = {p["institution"] for p in PROGRAMS}

    bad = [c for c, n in MAP.items() if n not in NAMES]
    if bad:
        sys.exit("bbsexam_apply: map points at institutions that do not exist: %s"
                 % ", ".join("%s->%s" % (c, MAP[c]) for c in bad))

    sw = B["statewide"]["clinical"]
    swl = B["statewide"].get("law_ethics") or {}
    # Both halves of every fraction, not just the rate and the denominator. The
    # first version stored the percentage and the number of candidates, and the
    # renderer had no numerator to print - so the statewide card read
    # "17,698 of 17,698 candidates", which is a claim of a 100% pass rate sitting
    # directly beside the words "80% passed". Store what you intend to show.
    state = {"first_time": pct(sw["first_time_passed"], sw["first_time_taking"]),
             "first_time_n": sw["first_time_taking"],
             "first_time_passed": sw["first_time_passed"],
             "all": pct(sw["all_passed"], sw["all_taking"]),
             "all_n": sw["all_taking"],
             "all_passed": sw["all_passed"],
             "law_ethics_first_time": pct(swl.get("first_time_passed", 0),
                                          swl.get("first_time_taking", 0))}

    # ---- pool by our institution
    pool = {}
    unmapped = []
    for s in B["schools"]:
        code = str(s.get("bbs_code") or "").strip()
        name = MAP.get(code) or MAP.get(code.zfill(3))
        if not name:
            keys = {code, code.zfill(3), code.lstrip("0") or code}
            if not (keys & set(NOT_MAPPED)):
                unmapped.append("%s %s" % (code, s["bbs_name"][:44]))
            continue
        r = pool.setdefault(name, {"ft_t": 0, "ft_p": 0, "all_t": 0, "all_p": 0,
                                   "le_t": 0, "le_p": 0, "as": [], "periods": 0})
        c, le = s["clinical"], s.get("law_ethics") or {}
        r["ft_t"] += c["first_time_taking"]
        r["ft_p"] += c["first_time_passed"]
        r["all_t"] += c["all_taking"]
        r["all_p"] += c["all_passed"]
        r["le_t"] += le.get("first_time_taking", 0)
        r["le_p"] += le.get("first_time_passed", 0)
        r["as"].append(s["bbs_name"])
        r["periods"] = max(r["periods"], s.get("periods", 0))

    wrote = shown = suppressed = 0
    for name, r in sorted(pool.items()):
        sl = SLUGS.get(name, "").replace(".html", "")
        f = os.path.join(DEPTH, sl + ".json")
        if not sl or not os.path.exists(f):
            continue
        d = json.load(open(f, encoding="utf-8"))
        enough = r["ft_t"] >= FLOOR
        d["exam"] = {
            "period": B["period_label"],
            "source": STATS_PAGE,
            "as_recorded": sorted(set(r["as"])),
            "floor": FLOOR,
            "enough": enough,
            "first_time_taking": r["ft_t"],
            "first_time_passed": r["ft_p"],
            "first_time_pct": pct(r["ft_p"], r["ft_t"]) if enough else None,
            "all_taking": r["all_t"],
            "all_passed": r["all_p"],
            "all_pct": pct(r["all_p"], r["all_t"]) if enough else None,
            "law_ethics_taking": r["le_t"],
            "law_ethics_pct": (pct(r["le_p"], r["le_t"])
                               if r["le_t"] >= FLOOR else None),
            "statewide": state,
        }
        json.dump(d, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        wrote += 1
        shown += 1 if enough else 0
        suppressed += 0 if enough else 1

    print("statewide first-time clinical %d%% of %d candidates; all takers %d%% of %d"
          % (state["first_time"], state["first_time_n"], state["all"], state["all_n"]))
    print("attached to %d school pages: %d publish a rate, %d suppressed under N=%d"
          % (wrote, shown, suppressed, FLOOR))
    matched = {n for n in pool if n in SLUGS}
    print("in the directory with no Board data at all: %d"
          % len([p for p in PROGRAMS
                 if p["institution"] in SLUGS and p["institution"] not in matched]))
    if unmapped:
        print("UNMAPPED Board codes with data:")
        for u in unmapped:
            print("   " + u)

    # ---- guards
    bad = 0
    if unmapped:
        print("GUARD: %d Board code(s) neither mapped nor explicitly excluded"
              % len(unmapped))
        bad += 1
    for name, r in pool.items():
        if r["ft_p"] > r["ft_t"] or r["all_p"] > r["all_t"]:
            print("GUARD %s: more passes than candidates" % name)
            bad += 1
        if r["ft_t"] > r["all_t"]:
            print("GUARD %s: more first-timers than total takers" % name)
            bad += 1
    # A statewide card that prints "N of N" is a 100% pass rate next to the
    # words "80% passed". Cheap to assert, and it was live for one build.
    if state["first_time_passed"] >= state["first_time_n"]:
        print("GUARD: statewide numerator equals or exceeds its denominator")
        bad += 1
    # The pooled total must not exceed the Board's own statewide total - if it
    # does, a code has been counted twice by the rename-merging above.
    tot = sum(r["ft_t"] for r in pool.values())
    if tot > sw["first_time_taking"]:
        print("GUARD: pooled first-timers (%d) exceed the statewide total (%d) "
              "- a code is double-counted" % (tot, sw["first_time_taking"]))
        bad += 1
    if bad:
        sys.exit("bbsexam_apply: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
