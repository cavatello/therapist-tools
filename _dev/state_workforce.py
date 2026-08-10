#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The mental health workforce of every state, from BLS and the Census.

WHERE THIS COMES FROM

Employment: the Bureau of Labor Statistics **Occupational Employment and Wage
Statistics**, May 2025 estimates, released 15 May 2026. State file:
https://www.bls.gov/oes/special-requests/oesm25st.zip

Population: Census Bureau **Vintage 2025** resident population, 1 July 2025
(NST-EST2025-POP), released January 2026.

OEWS is the only source that counts the same way in all fifty states, which is
the entire reason this comparison is possible. Every other route - fifty
licensing boards, each with its own titles and its own definition of "active" -
produces a table that looks comparable and is not.

THE THREE THINGS THAT WILL MISLEAD SOMEBODY WHO USES THIS FILE

1. **OEWS does not count the self-employed.** It is an employer survey. BLS:
   "The survey does not include the self-employed, owners and partners in
   unincorporated firms." A therapist in solo practice as a sole proprietor is
   invisible to it; one who incorporated and pays herself a salary is counted.
   That is a large, uneven omission in exactly this profession.

2. **The MFT figure is a licensure-title map, not a supply map.** SOC 21-1013
   counts people employed *as* marriage and family therapists. States that
   license the same clinicians under LPC or LMHC titles put them in 21-1018
   instead. Texas showing 4.4 MFTs per 100,000 against California's 88.9 is
   mostly a fact about statutes, not about how many therapists live there. The
   four-occupation total is the honest supply comparison; the MFT column is a
   story about California's own professional history.

3. **Suppression is not zero.** BLS withholds an estimate when it fails quality
   standards or would identify a respondent. Those are `None` here, printed as
   "not published", and never imputed. Washington's MFT count in particular is
   a hole, not an absence of therapists.

WHY THE TOTALS ARE MARKED

A state missing one of the four occupations cannot have its four-occupation
total compared with a state that has all four. `complete()` is the only
accessor that returns states safe to rank, and `TOTAL_IS_FLOOR` marks the rest
so a partial total can never be silently ranked against a whole one.
"""

# (state, population, MFT 21-1013, counselors 21-1018, MH social workers
#  21-1023, psychologists 19-3033). None = BLS did not publish it.
STATES = [
    ("Alabama", 5193088, 190, None, 740, 260),
    ("Alaska", 737270, 60, 1290, 250, 40),
    ("Arizona", 7623818, None, 9990, 3690, 730),
    ("Arkansas", 3114791, 80, 2570, 1040, 370),
    ("California", 39355309, 34970, 75610, 19860, 12840),
    ("Colorado", 6012561, 900, 14920, 1640, 1170),
    ("Connecticut", 3688496, 260, 7540, 1540, 660),
    ("Delaware", 1059952, 400, 1700, 510, 280),
    ("District of Columbia", 693645, None, 1260, 510, 220),
    ("Florida", 23462518, 930, 29750, 5150, 3040),
    ("Georgia", 11302748, None, 9600, 1330, 1120),
    ("Hawaii", 1432820, 220, 2110, None, 250),
    ("Idaho", 2029733, 140, 2990, 510, 300),
    ("Illinois", 12719141, 860, 20250, 3460, 5810),
    ("Indiana", 6973333, 510, 11890, 2490, 1850),
    ("Iowa", 3238387, 240, 3530, 1200, 440),
    ("Kansas", 2977220, 190, 2600, 1620, 400),
    ("Kentucky", 4606864, 330, 7690, 1360, 710),
    ("Louisiana", 4618189, None, 6420, 970, 320),
    ("Maine", 1414874, 180, 1930, 1860, None),
    ("Maryland", 6265347, 460, 9730, 2250, 2140),
    ("Massachusetts", 7154084, 600, 18190, 7440, 2860),
    ("Michigan", 10127884, 590, 10100, 4620, 2170),
    ("Minnesota", 5830405, 4870, 7110, 3590, 1290),
    ("Mississippi", 2954160, 140, 2090, 920, 210),
    ("Missouri", 6270541, 390, 8130, 1640, 840),
    ("Montana", 1144694, 100, 1820, 740, 150),
    ("Nebraska", 2018006, 260, 2170, 900, 770),
    ("Nevada", 3282188, None, 1810, 1100, 680),
    ("New Hampshire", 1415342, 70, 3690, 320, 330),
    ("New Jersey", 9548215, 4040, 14210, 2420, 2700),
    ("New Mexico", 2125498, 160, 2420, 800, None),
    ("New York", 20002427, 770, 26770, 14820, 8420),
    ("North Carolina", 11197968, 1400, 10300, 3690, 2770),
    ("North Dakota", 799358, None, 1290, 240, 170),
    ("Ohio", 11900510, 460, 18020, 6050, 2080),
    ("Oklahoma", 4123288, None, 5150, 1780, 950),
    ("Oregon", 4273586, 850, 8160, 2230, 540),
    ("Pennsylvania", 13059432, 2350, 30620, 3500, 3140),
    ("Rhode Island", 1114521, None, 2170, 800, 420),
    ("South Carolina", 5570274, 380, 6300, 720, None),
    ("South Dakota", 935094, 80, 1710, 230, 120),
    ("Tennessee", 7315076, 1440, 9040, 2220, 1180),
    ("Texas", 31709821, 1380, 21400, 8220, 3640),
    ("Utah", 3538904, 2390, 6320, 1240, 1020),
    ("Vermont", 644663, None, 1120, 320, 190),
    ("Virginia", 8880107, 930, 17940, 3670, 2140),
    ("Washington", 8001020, None, 14250, 3490, 1270),
    ("West Virginia", 1766147, 90, 2100, 420, 920),
    ("Wisconsin", 5972787, 180, 8340, 1880, 1150),
    ("Wyoming", 588753, None, 910, 200, 50),
]

# BLS national totals, May 2025, and the Census national population.
US_POP = 341784857
US = {"mft": 66740, "couns": 491930, "msw": 132810, "psych": 75990}

OCCUPATIONS = [
    ("mft", "21-1013", "Marriage and family therapists", "#00704A"),
    ("couns", "21-1018", "Mental health and substance abuse counselors",
     "#C2761B"),
    ("msw", "21-1023", "Mental health and substance abuse social workers",
     "#A6332B"),
    ("psych", "19-3033", "Clinical and counseling psychologists", "#2E5AA8"),
]

# The location quotient BLS publishes for MFT employment - how concentrated an
# occupation is in a state against the national average, where 1.00 is average.
MFT_LQ = {"California": 4.47, "Minnesota": 3.85, "Utah": 3.21,
          "New Jersey": 2.20, "Delaware": 1.92, "Tennessee": 1.02,
          "Oregon": 1.00, "Texas": 0.23, "Florida": 0.22, "New York": 0.18}

RELEASE = "May 2025 estimates, released 15 May 2026"
POP_VINTAGE = "Census Vintage 2025, resident population 1 July 2025"

OEWS_URL = "https://www.bls.gov/oes/tables.htm"
OEWS_TECH = "https://www.bls.gov/oes/2025/may/oes_tec.htm"
OEWS_FAQ = "https://www.bls.gov/oes/oes_ques.htm"
CENSUS_URL = ("https://www.census.gov/data/tables/time-series/demo/popest/"
              "2020s-state-total.html")
MATRIX_URL = ("https://www.bls.gov/emp/tables/"
              "industry-occupation-matrix-occupation.htm")

# Unincorporated self-employed share, BLS Employment Projections 2024-34.
# A floor, not the whole picture: an incorporated solo practitioner counts as
# wage-and-salary in both this and OEWS.
SELF_EMPLOYED = {"mft": 12.8, "couns": 5.9, "msw": 4.8, "psych": 2.4}


# ---------------------------------------------------------------- the titles
#
# The reason a per-capita MFT map misleads. Every state below licenses MFTs;
# what differs is which credential the profession actually grew into. Verified
# against each state's own board or statute, August 2026.
#
# (state, MFT title, counseling title, clinical social work title,
#  pre-licensed tier)
TITLES = [
    ("California", "LMFT", "LPCC", "LCSW", "AMFT / ASW / APCC"),
    ("Massachusetts", "LMFT", "LMHC", "LICSW", "tiered: LSW to LCSW to LICSW"),
    ("New Hampshire", "LMFT", "LCMHC", "LICSW", "candidate status"),
    ("Utah", "LMFT", "CMHC", "LCSW", "ACMHC / AMFT / CSW"),
    ("Colorado", "LMFT", "LPC", "LCSW", "PCC / MFTC / SWC candidate"),
    ("Pennsylvania", "LMFT", "LPC", "LCSW", "Licensed Associate MFT / LAPC"),
    ("Minnesota", "LMFT", "LPCC", "LICSW", "LPC is the pre-LPCC tier"),
    ("Virginia", "LMFT", "LPC", "LCSW", "Resident in Counseling / in MFT"),
    ("Oregon", "LMFT", "LPC", "LCSW", "Registered Associate / CSWA"),
    ("Connecticut", "LMFT", "LPC", "LCSW", "Professional Counselor Associate"),
    ("Illinois", "LMFT", "LCPC", "LCSW", "LPC and LSW are the supervised tier"),
    ("Ohio", "IMFT", "LPCC", "LISW", "CT / SWT / MFTT trainee"),
    ("Washington", "LMFT", "LMHC", "LICSW", "LMHCA / LMFTA / LICSWA"),
    ("New Jersey", "LMFT", "LPC", "LCSW", "Licensed Associate Counselor"),
    ("Texas", "LMFT", "LPC", "LCSW", "LPC-Associate / LMFT-Associate"),
    ("New York", "LMFT", "LMHC", "LCSW", "limited permit"),
    ("Florida", "LMFT", "LMHC", "LCSW", "Registered Intern"),
]

# Counts of ACTIVE LICENSEES published by each state's own board or oversight
# body - a different thing from BLS employment, and the contrast is the point.
# (state, MFT licensees, counseling licensees, as-at, source url)
LICENSEES = [
    ("California", 55002, 4862, "2025 sunset review",
     "https://sbp.senate.ca.gov/system/files/2025-03/"
     "1-board-of-behavioral-sciences-background-paper-2025.pdf"),
    ("Texas", 5274, 38350, "1 January 2025",
     "https://capitol.texas.gov/tlodocs/89R/handouts/C3102025030408001/"
     "33835667-fad8-4918-8778-d376d99f0954.PDF"),
    ("Florida", 3713, 20871, "FY 2024-25",
     "https://www.floridahealth.gov/wp-content/uploads/2026/01/"
     "2025.10.31.FY24-25MQAAR-FINAL1-1.pdf"),
    ("New York", 2172, 14545, "1 January 2026",
     "https://www.op.nysed.gov/professions/marriage-and-family-therapists/"
     "license-statistics-marriage-and-family-therapy"),
    ("Ohio", 829, 14170, "1 January 2025",
     "https://dam.assets.ohio.gov/image/upload/cswmft.ohio.gov/"
     "executive-board-update/2025-01-Board_Update.pdf"),
]

# California's own register, for the licensed-against-employed comparison.
CA_LMFT_LICENSED = 59706


def titles(state):
    for t in TITLES:
        if t[0] == state:
            return t
    return None


def per100k(n, pop):
    return None if n is None else 100000.0 * n / pop


def row(state):
    for r in STATES:
        if r[0] == state:
            return r
    raise KeyError(state)


def total(r):
    """(total, is_floor). A floor means one occupation was not published."""
    vals = r[2:6]
    return sum(v for v in vals if v is not None), any(v is None for v in vals)


def complete():
    """Only the states with all four occupations published - the rankable set."""
    return [r for r in STATES if all(v is not None for v in r[2:6])]


def us_per100k(key):
    return 100000.0 * US[key] / US_POP


def us_total_per100k():
    return 100000.0 * sum(US.values()) / US_POP


def check():
    problems = []
    if len(STATES) != 51:
        problems.append("%d states, expected 50 + DC" % len(STATES))
    names = [r[0] for r in STATES]
    if len(set(names)) != len(names):
        problems.append("a state is listed twice")
    for r in STATES:
        if r[1] < 500000 or r[1] > 45000000:
            problems.append("%s population %d is outside any plausible range"
                            % (r[0], r[1]))
        for v in r[2:6]:
            if v is not None and (v < 0 or v > 200000):
                problems.append("%s has an employment value of %s" % (r[0], v))
    # The state values should sum to somewhere near the national total. They
    # will not match exactly - suppressed cells are missing from the sum - but
    # a wild gap means a column was mistyped.
    for i, (k, _c, _l, _col) in enumerate(OCCUPATIONS):
        s = sum(r[2 + i] for r in STATES if r[2 + i] is not None)
        if not (0.75 * US[k] <= s <= 1.02 * US[k]):
            problems.append("%s sums to %d against a national total of %d"
                            % (k, s, US[k]))
    if len(complete()) < 35:
        problems.append("only %d states have all four occupations published"
                        % len(complete()))
    return problems


if __name__ == "__main__":
    import sys
    p = check()
    for x in p:
        print("GUARD:", x)
    if p:
        sys.exit("%d problem(s)" % len(p))
    print("state_workforce: %d states, %d rankable, US total %.1f per 100k"
          % (len(STATES), len(complete()), us_total_per100k()))
