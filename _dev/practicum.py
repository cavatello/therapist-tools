#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""How each of California's MFT programs handles the practicum placement.

WHERE THIS COMES FROM

`mock/mftguide/programs.json` - the research file behind the 78 program
pages already published here. Every record carries a `placement` code and a
`placement_evidence` field holding a verbatim passage from that program's
own handbook, catalogue or fieldwork page. Both were read by hand when the
program pages were built; this pass only reduces them.

WHY IT IS WORTH A PAGE OF ITS OWN

The placement is the single largest uncontrolled risk in a California
master's. Two students in the same cohort can have completely different
years: one is handed a seat at the program's own clinic, the other cold
emails forty agencies in a county where every seat is taken. Nothing in a
program's marketing tells you which one you are, and no comparison of the
78 exists anywhere.

THE FIVE-VALUE TAXONOMY, AND WHAT IT COSTS TO GET WRONG

  guaranteed      the program states every student gets a seat
  placed          the program assigns the site
  assisted        an approved-site list, contracts already signed, student applies
  student-sourced the student finds the site; the school approves it
  not published   nothing on the public site or handbook says

`not published` is a statement about the program's disclosure, NOT about
what the program does. Several will in practice place students well. The
finding is that a prospective student cannot tell before enrolling, and that
is worth reporting exactly as what it is.

Where a program runs two stages - an in-house clinic first, an external
traineeship second - it is classified on the stage that carries the risk,
because that is the one that can go wrong. Eight records carry a
`placement_why` note explaining the call; those are printed on the page.

THE DIRECT-CLIENT-CONTACT NUMBER IS CURATED, NOT PARSED

`practicum_hours` is prose, and prose does not reduce cleanly. "600 Hours
Fieldwork Requirement = Minimum of 500 Clinical Hours and 100 Supervision
Hours" and "300 client contact hours, 100 of which are relational" both
contain several numbers and only one of them is the direct-client-contact
minimum. A regular expression got roughly two thirds of them right, which is
the worst possible outcome - wrong numbers that look right.

So DCC below is written out by hand, one line per program, read off the
quoted passage that ships beside it on the page. Where the program states
an LMFT figure and an LPCC figure, the LMFT figure is used and the quote
shows both. Where the passage gives a total that is not direct client contact
- "500 hours of practicum", "400+ clinical hours" - the value is None and the
page prints the program's own words instead of a number it cannot support.
A guard below fails the build if a key here does not match an institution in
the source file, which is what catches a renamed school.
"""
import collections, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DATA = os.path.join(SITE, "mock", "mftguide", "programs.json")
OUT = os.path.join(HERE, "practicum_data.py")
CHECKED = "11 August 2026"

ORDER = ["guaranteed", "placed", "assisted", "student-sourced", "not published"]

# Direct client contact hours the program requires before it will graduate
# you, read off the passage quoted beside it on the page.
DCC = {
    "Alliant International University (CSPP)": 300,
    "America Evangelical University / Kairos Pacific University": 300,
    "Antioch University Santa Barbara": 225,
    "Azusa Pacific University": 300,
    "Biola University (Talbot School of Theology)": 225,
    "Cal Poly Humboldt": 150,
    "California Southern University": 285,
    "California State University, Bakersfield": 150,
    "California State University, Chico": 225,
    "California State University, Dominguez Hills": 300,
    "California State University, Fresno (Fresno State)": 300,
    "California State University, Fullerton (University Extension)": 280,
    "California State University, Northridge": 500,
    "Concordia University Irvine (Townsend Institute)": 280,
    "Dominican University of California": 280,
    "HIS University": 250,
    "Hope International University": 300,
    "Jessup University": 280,
    "Kaiser Permanente School of Allied Health Sciences": 225,
    "La Sierra University": 280,
    "Loma Linda University": 300,
    "Mount Saint Mary's University": 250,
    "Pacific Oaks College": 225,
    "Pacifica Graduate Institute": 280,
    "Palo Alto University": 280,
    "Pepperdine University (GSEP)": 225,
    "Point Loma Nazarene University": 290,
    "San Diego State University": 300,
    "San Francisco State University": 280,
    "San Jose State University": 225,
    "Santa Clara University": 225,
    "Sofia University": 225,
    "The Chicago School": 300,
    "The Wright Institute": 280,
    "Touro University Worldwide": 300,
    "University of La Verne": 280,
    "University of Massachusetts Global (formerly Brandman)": 300,
    "University of Phoenix": 300,
    "University of San Diego (SOLES)": 400,
    "Weimar University": 280,
    "Western Institute for Social Research": 150,
    "Western Seminary": 280,
}

# Programmes whose practicum wording WAS read and states no direct client
# contact minimum - a total that mixes counseling with supervision or
# observation, a weekly rate, or a bare "400+ clinical hours". Listing them
# explicitly rather than letting them fall through a .get() is what makes the
# guard below able to tell "no number published" from "nobody looked".
NO_DCC = (
    "California State University, Sacramento",
    "California State University, Long Beach",
    "Sonoma State University",
    "Cal Poly San Luis Obispo",
    "Loyola Marymount University",
    "Fresno Pacific University",
    "Campbellsville University — Los Angeles Education Center "
    "(formerly Phillips Graduate University/Institute)",
    "Notre Dame de Namur University",
    "Sentio University",
    "Golden Gate University",
    "Northwestern University, The Family Institute",
    "Rhombus University",
)


def slug(name):
    """The rule build_schools.py uses, kept identical so links do not rot."""
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"\(.*?\)", " ", s.lower())
    s = re.sub(r"^the\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s[:64].strip("-") + "-mft.html"


def trim(s, n):
    if not s:
        return None
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def main():
    print("practicum placement, from the program research file")
    if not os.path.exists(DATA):
        sys.exit("%s is missing" % DATA)
    raw = json.load(open(DATA, encoding="utf-8"))

    names = {r["institution"] for r in raw}
    stray = [k for k in list(DCC) + list(NO_DCC) if k not in names]
    if stray:
        sys.exit("%d curated key(s) match no institution - a school was "
                 "renamed:\n  %s" % (len(stray), "\n  ".join(sorted(stray))))

    # Anything that publishes practicum hours must have been read: it is
    # either in DCC with a number or in NO_DCC with a reason. A new program
    # arriving in the source file stops the build rather than appearing on the
    # page with a silent blank.
    unread = sorted(r["institution"] for r in raw
                    if r.get("practicum_hours")
                    and r["institution"] not in DCC
                    and r["institution"] not in NO_DCC)
    if unread:
        sys.exit("%d program(s) publish practicum hours that nobody has read:"
                 "\n  %s\nAdd each to DCC with a number or to NO_DCC with the "
                 "reason." % (len(unread), "\n  ".join(unread)))

    rows, seen = [], set()
    for r in raw:
        inst = r["institution"]
        p = (r.get("placement") or "not published").strip()
        if p not in ORDER:
            sys.exit("unknown placement code %r for %s" % (p, inst))
        sl = slug(inst)
        page = sl if os.path.exists(os.path.join(SITE, sl)) else None
        rows.append({
            "inst": inst,
            "degree": r.get("degree") or "",
            "city": r.get("city") or "",
            "page": page,
            "placement": p,
            "why": r.get("placement_why"),
            "evidence": trim(r.get("placement_evidence"), 420),
            "url": r.get("placement_url") or r.get("url"),
            "own_clinic": bool(r.get("own_clinic")),
            "clinics": r.get("clinic_names") or None,
            "dcc": DCC.get(inst),
            "hours_text": trim(r.get("practicum_hours"), 300),
            "hours_url": r.get("practicum_hours_url"),
            "length": trim(r.get("practicum_length"), 260),
            "lpcc": r.get("lpcc"),
            "coamfte": bool(r.get("coamfte")),
        })
        seen.add(inst)

    # What the degree costs, for the ones that publish enough to compute it.
    # A per-unit price times the published unit count, or a stated total where
    # there is one. The public campuses are largely absent because they
    # publish a per-semester full-time rate rather than a per-unit one, so
    # this is a range across the programs that publish, NOT the range across
    # California - and the page has to say so beside the number.
    tuition = []
    for r in raw:
        u = re.search(r"(\d{2,3})", r.get("units") or "")
        u = int(u.group(1)) if u else None
        per, tot = r.get("per_unit"), r.get("total")
        cost = tot if tot else (u * per if (u and per) else None)
        if cost:
            tuition.append({"inst": r["institution"], "cost": int(round(cost)),
                            "units": u, "per_unit": per,
                            "stated": bool(tot)})
    tuition.sort(key=lambda t: t["cost"])

    counts = collections.Counter(r["placement"] for r in rows)
    for k in ORDER:
        counts.setdefault(k, 0)

    dccs = [r["dcc"] for r in rows if r["dcc"]]
    buckets = collections.Counter(dccs)
    clinics = sum(1 for r in rows if r["own_clinic"])
    linked = sum(1 for r in rows if r["page"])
    with_hours = sum(1 for r in rows if r["hours_text"])
    with_len = sum(1 for r in rows if r["length"])

    # Sort: risk first. A prospective student is looking for the bad news.
    rank = {k: i for i, k in enumerate(
        ["not published", "student-sourced", "assisted", "placed", "guaranteed"])}
    rows.sort(key=lambda r: (rank[r["placement"]], r["inst"]))

    b = ['#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n',
         '"""Practicum placement across California\'s MFT programs.\n\n',
         "WRITTEN BY _dev/practicum.py. Do not edit.\n\n",
         "Reduced from mock/mftguide/programs.json. `placement` is a five-value\n",
         "code; `not published` describes the program's disclosure and not its\n",
         "practice. `dcc` is curated by hand in the pass, not parsed, and is None\n",
         "wherever the program's own wording does not state a direct client\n",
         'contact minimum.\n"""\n\n']
    b.append("CHECKED = %r\n" % CHECKED)
    b.append("SOURCE = %r\n" % "https://therapistsupport.org/mft-programs-california.html")
    b.append("ORDER = %r\n" % ORDER)
    b.append("N = %d\n" % len(rows))
    b.append("COUNTS = %r\n" % dict(counts))
    b.append("OWN_CLINIC = %d\n" % clinics)
    b.append("LINKED = %d\n" % linked)
    b.append("WITH_HOURS = %d\n" % with_hours)
    b.append("WITH_LENGTH = %d\n" % with_len)
    b.append("DCC_N = %d\n" % len(dccs))
    b.append("DCC_BUCKETS = %r\n" % sorted(buckets.items()))
    b.append("DCC_MIN = %r\nDCC_MAX = %r\n" % (min(dccs), max(dccs)))
    b.append("TUITION_N = %d\n" % len(tuition))
    b.append("TUITION = %r\n" % tuition)
    b.append("PROGRAMS = %r\n" % rows)
    open(OUT, "w", encoding="utf-8").write("".join(b))

    print("  %d programs; placement: %s"
          % (len(rows), ", ".join("%s %d" % (k, counts[k]) for k in ORDER)))
    print("  %d have their own training clinic, %d link to a published page"
          % (clinics, linked))
    print("  %d state a direct-client-contact minimum, %d to %d; commonest: %s"
          % (len(dccs), min(dccs), max(dccs),
             ", ".join("%d h (%d)" % kv for kv in buckets.most_common(4))))
    print("  %d publish enough to compute a tuition figure, %s to %s"
          % (len(tuition), "$%s" % format(tuition[0]["cost"], ",d"),
             "$%s" % format(tuition[-1]["cost"], ",d")))
    print("  wrote %s" % os.path.basename(OUT))


if __name__ == "__main__":
    main()
