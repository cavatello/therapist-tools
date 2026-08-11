#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""How many people a year California graduates into the therapy pipeline.

WHERE THIS COMES FROM

IPEDS Completions - the federal survey every accredited institution must
file - read through the Urban Institute's Education Data API, which mirrors
it with a stable query interface. One call per year, filtered to California
(fips 6) and to master's degrees, grouped by six-digit CIP code.

  https://educationdata.urban.org/documentation/colleges.html

Unlike most passes in `_dev/` this one needs the network, so it is run when a
new IPEDS year lands and the file it writes - `degree_pipeline.py` - is what
gets committed. The builder reads that, never this.

THREE THINGS THAT WILL TRIP UP THE NEXT PERSON

1. AWARD LEVEL 9 IS THE MASTER'S DEGREE, NOT 7. Level 7 is the bachelor's.
   Getting this wrong is silent: you get plausible numbers that are simply a
   different degree. The check is the state total - California awards roughly
   90,000 master's degrees and roughly 220,000 bachelor's degrees a year, and
   the pass asserts the first of those below.

2. 2020 IS A COPY OF 2019 IN THIS MIRROR. Every California institution
   returns byte-identical counts for the two years across all ten CIP codes,
   which is not what a pandemic year looks like. It is excluded, and the
   exclusion is printed on the page rather than smoothed away.

3. CIP 51.1505 IS NOT THE WHOLE MFT PIPELINE. California MFT programs file
   under at least four codes - Marriage and Family Therapy, Counseling
   Psychology, Mental Health Counseling and Clinical Psychology - because the
   Board approves the degree by content, not by CIP. A number from 51.1505
   alone undercounts badly. Both the narrow and the wide figure are computed,
   and the page prints both with the reason.
"""
import json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "degree_pipeline.py")
CHECKED = "11 August 2026"
API = "https://educationdata.urban.org/api/v1/college-university/ipeds"
DOC = "https://educationdata.urban.org/documentation/colleges.html"
NCES = "https://nces.ed.gov/ipeds/use-the-data"

YEARS = tuple(y for y in range(2015, 2024) if y != 2020)
EXCLUDED = 2020
MASTERS = 9          # award_level. 7 is the bachelor's; see the docstring.
CA = 6               # fips

# Six-digit CIP, label, and whether it feeds the clinical licensure pipeline
# in California. "wide" is the set a California LMFT or LPCC degree actually
# files under; school counseling is listed and deliberately excluded from it,
# because a PPS credential is not a BBS license.
CIP = [
    ("511505", "Marriage and family therapy", True),
    ("422803", "Counseling psychology", True),
    ("511508", "Mental health counseling", True),
    ("422801", "Clinical psychology", True),
    ("440701", "Social work", False),
    ("131101", "Counselor education and school counseling", False),
    ("420101", "Psychology, general", False),
    ("511501", "Substance abuse and addiction counseling", False),
    ("511503", "Clinical and medical social work", False),
    ("511599", "Mental and social health services, other", False),
]


def get(url, tries=4):
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(url, timeout=120))
        except Exception as e:                       # network, not logic
            print("  retry %d: %s" % (i + 1, e))
            time.sleep(3 * (i + 1))
    sys.exit("the Education Data API did not answer after %d tries. This pass "
             "needs the network; %s is the committed artifact and the builder "
             "reads that." % (tries, os.path.basename(OUT)))


def year(y):
    u = ("%s/completions-cip-6/summaries?stat=sum&var=awards_6digit"
         "&by=cipcode_6digit&fips=%d&award_level=%d&year=%d"
         "&race=99&sex=99&majornum=1" % (API, CA, MASTERS, y))
    rows = get(u)["results"]
    return {str(r["cipcode_6digit"]): r["awards_6digit"] for r in rows}


def main():
    print("IPEDS completions, California master's degrees")
    series, totals = {}, {}
    for y in YEARS:
        m = year(y)
        allm = m.get("99")
        if not allm or not 40000 < allm < 200000:
            sys.exit("California reported %r master's degrees in %d. That is "
                     "not a master's total - award_level %d is probably not "
                     "the master's degree in this release."
                     % (allm, y, MASTERS))
        series[y] = {c: m.get(c, 0) for c, _, _ in CIP}
        totals[y] = allm
        print("  %d  %s master's statewide; MFT %s, counseling psych %s, "
              "social work %s"
              % (y, format(allm, ",d"), format(series[y]["511505"], ",d"),
                 format(series[y]["422803"], ",d"),
                 format(series[y]["440701"], ",d")))

    first, last = YEARS[0], YEARS[-1]
    wide = [c for c, _, w in CIP if w]
    wide_last = sum(series[last][c] for c in wide)
    wide_first = sum(series[first][c] for c in wide)

    b = ['#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n',
         '"""California master\'s degrees in the therapy pipeline, by year.\n\n',
         "WRITTEN BY _dev/ipeds_degrees.py, which needs the network. Do not\n",
         "edit. `WIDE` is the set of CIP codes a California LMFT or LPCC\n",
         "degree actually files under; 51.1505 alone undercounts because the\n",
         "Board approves a degree by content rather than by CIP. %d is absent\n"
         % EXCLUDED,
         "because this mirror returns it byte-identical to %d for every\n"
         % (EXCLUDED - 1),
         'California institution, which is not a real year.\n"""\n\n']
    b.append("CHECKED = %r\n" % CHECKED)
    b.append("SOURCE = %r\n" % DOC)
    b.append("NCES = %r\n" % NCES)
    b.append("YEARS = %r\n" % list(YEARS))
    b.append("EXCLUDED_YEAR = %d\n" % EXCLUDED)
    b.append("CIP = %r\n" % [(c, l, w) for c, l, w in CIP])
    b.append("WIDE = %r\n" % wide)
    b.append("SERIES = %r\n" % series)
    b.append("STATE_TOTAL = %r\n" % totals)
    b.append("WIDE_LATEST = %d\nWIDE_FIRST = %d\n" % (wide_last, wide_first))
    open(OUT, "w", encoding="utf-8").write("".join(b))

    print("  the wide clinical pipeline: %s in %d, %s in %d (%+.0f%%)"
          % (format(wide_first, ",d"), first, format(wide_last, ",d"), last,
             100.0 * (wide_last - wide_first) / wide_first))
    print("  wrote %s" % os.path.basename(OUT))


if __name__ == "__main__":
    main()
