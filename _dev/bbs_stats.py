#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seven quarters of the Board's own numbers, transcribed once.

WHERE THIS COMES FROM

Every figure in this file was read out of a Board of Behavioral Sciences board
meeting packet, listed in PACKETS below with the URL it was read from. Nothing
here is derived, estimated, adjusted or filled in. Where the Board did not
publish a figure the value is None and the pages render an em dash, because a
gap in the Board's reporting is information and a plausible interpolation is
not.

TWO THINGS THAT WILL TRIP UP THE NEXT PERSON

1. **The filename pattern is not stable.** `20250227_28_item_11.pdf`,
   `20251120-21_item_21.pdf`, `20260507_item20.pdf` - underscore, hyphen, and
   no separator at all, in three consecutive years. Guessing a URL will 404.
   Scrape the hrefs off https://bbs.ca.gov/about/board_meetings.html instead.

2. **The Board changed how it measures processing time at Q2 FY 2025/26.**
   Before that it published one number per application type covering every
   application processed. From Q2 FY 2025/26 it splits approved from deficient.
   These are not one series. The Feb 2026 packet backfills Q2 FY 2024/25 on the
   new basis and gets AMFT 29 where the 2025 packets published 45 for the same
   quarter on the old basis. Both are correct; they measure different things.
   Splicing them produces a dramatic and completely fictional improvement.

Every quarter except the two endpoints appears in two packets - each one prints
the prior quarter alongside the current one - and the overlapping values agree.
That is the reason to transcribe seven quarters rather than one: the series
checks itself.
"""

# ------------------------------------------------------------------- packets
# (label, what it reports, url). Every one of these was fetched and read.
PACKETS = [
    ("February 27-28, 2025, item 11",
     "Executive Officer Report - Q2 FY 2024/25 licensing and examination",
     "https://www.bbs.ca.gov/pdf/agen_notice/2025/20250227_28_item_11.pdf"),
    ("May 8-9, 2025, item 18",
     "Executive Officer Report - Q3 FY 2024/25",
     "https://www.bbs.ca.gov/pdf/agen_notice/2025/20250508_09_item_18.pdf"),
    ("August 21-22, 2025, item 15",
     "Executive Officer Report - Q4 FY 2024/25",
     "https://www.bbs.ca.gov/pdf/agen_notice/2025/20250821_22_item_15.pdf"),
    ("November 20-21, 2025, item 21",
     "Licensing Report - Q1 FY 2025/26",
     "https://www.bbs.ca.gov/pdf/agen_notice/2025/20251120-21_item_21.pdf"),
    ("November 20-21, 2025, item 22",
     "Examination Report - Q1 FY 2025/26",
     "https://www.bbs.ca.gov/pdf/agen_notice/2025/20251120-21_item_22.pdf"),
    ("February 19-20, 2026, item 14",
     "Registration and Licensing Report - Q2 FY 2025/26",
     "https://www.bbs.ca.gov/pdf/agen_notice/2026/20260219_20_item_14.pdf"),
    ("February 19-20, 2026, item 15",
     "Examination Report - Q2 FY 2025/26",
     "https://www.bbs.ca.gov/pdf/agen_notice/2026/20260219_20_item_15.pdf"),
    ("May 7-8, 2026, item 20",
     "Licensing Update - Q3 FY 2025/26, the most recent published",
     "https://www.bbs.ca.gov/pdf/agen_notice/2026/20260507_item20.pdf"),
    ("May 7-8, 2026, item 21",
     "Examination Report - Q3 FY 2025/26, the most recent published",
     "https://www.bbs.ca.gov/pdf/agen_notice/2026/20260507_item21.pdf"),
]

MEETINGS_INDEX = "https://bbs.ca.gov/about/board_meetings.html"

# Oldest first. LATEST is the one the pages lead with.
QUARTERS = ["Q1 FY 24/25", "Q2 FY 24/25", "Q3 FY 24/25", "Q4 FY 24/25",
            "Q1 FY 25/26", "Q2 FY 25/26", "Q3 FY 25/26"]
LATEST = QUARTERS[-1]
LATEST_LONG = "the third quarter of fiscal year 2025/26"
LATEST_PACKET = "https://www.bbs.ca.gov/pdf/agen_notice/2026/20260507_item21.pdf"

# --------------------------------------------------------------------- exams
# key -> (label, who sits it, [(total, overall%, first_time_n, first_time%)])
# in QUARTERS order.
EXAMS = [
    ("lmft_le", "LMFT Law &amp; Ethics",
     "Every AMFT, within their first registration renewal period", [
         (1359, 72, 1037, 79), (1627, 74, 1282, 79), (1462, 75, 1126, 80),
         (1444, 77, 1136, 83), (1586, 73, 1251, 77), (1443, 74, 1036, 83),
         (1451, 71, 1089, 78)]),
    ("lmft_cl", "LMFT Clinical",
     "The last exam before licensure, after the 3,000 hours", [
         (1028, 71, 741, 85), (1180, 76, 870, 88), (1071, 68, 803, 81),
         (1040, 73, 764, 86), (1133, 71, 853, 81), (1087, 70, 767, 84),
         (1057, 65, 742, 80)]),
    ("lcsw_le", "LCSW Law &amp; Ethics", "Every ASW", [
        (1465, 69, 1084, 74), (1427, 63, 1001, 68), (1346, 81, 982, 85),
        (1706, 77, 1364, 80), (1686, 58, 1276, 62), (1302, 76, 813, 84),
        (1256, 73, 893, 79)]),
    ("lcsw_cl", "ASWB Clinical",
     "The national social work exam, written by ASWB and not by California", [
         (1264, 54, 758, 73), (1169, 51, 702, 70), (1174, 53, 722, 70),
         (1205, 59, 696, 76), (1446, 49, 742, 69), (1217, 52, 653, 73),
         (1389, 55, 816, 72)]),
    ("lpcc_le", "LPCC Law &amp; Ethics", "Every APCC", [
        (574, 63, 416, 71), (563, 72, 427, 77), (651, 67, 491, 71),
        (646, 52, 498, 58), (729, 66, 551, 69), (619, 82, 425, 86),
        (693, 75, 480, 81)]),
    ("lpcc_cl", "NCMHCE",
     "The national clinical counselor exam, written by the NBCC", [
         (256, 68, 186, 77), (237, 69, 178, 81), (212, 67, 150, 78),
         (264, 70, 182, 79), (307, 67, 206, 76), (260, 61, 189, 75),
         (300, 68, 217, 77)]),
    ("lep", "LEP", "Licensed Educational Psychologists", [
        (55, 58, 38, 68), (51, 57, 36, 69), (54, 80, 38, 84),
        (62, 69, 48, 79), (73, 73, 51, 82), (70, 74, 50, 82),
        (59, 86, 49, 90)]),
]

TOTAL_ADMINISTERED = [6001, 6254, 5970, 6367, 6960, 5998, 6205]

# The Board's own five-year study of the LPCC Law & Ethics pass rate, from the
# February 2026 packet. Quoted rather than summarised, because the finding is
# that there is no finding and a paraphrase would soften it.
OPES_LPCC = ("no statistically significant or specific factors were "
             "identified that could explain the observed lower pass rates")

# The documented Pearson VUE incident. The May 2025 packet, item 18.
SCORING_INCIDENT = {
    "exam": "LPCC Law &amp; Ethics",
    "effective": "1 February 2025",
    "window": "1 February to 19 February 2025",
    "taken": 77,
    "still_fail": 44,
    "changed": 33,
    "url": "https://www.bbs.ca.gov/pdf/agen_notice/2025/20250508_09_item_18.pdf",
}

# --------------------------------------------------- processing, OLD series
# All processed applications, one figure per type. Q1 FY 24/25 to Q1 FY 25/26.
OLD_QUARTERS = QUARTERS[:5]
OLD_TIMES = [
    ("AMFT registration", [22, 45, 28, 12, 31]),
    ("ASW registration", [14, 17, 17, 12, 17]),
    ("APCC registration", [49, 65, 44, 17, 31]),
    ("LMFT license", [82, 72, 69, 69, 85]),
    ("LCSW license", [78, 67, 56, 58, 82]),
    ("LPCC license", [7, 10, 8, 7, 7]),
    ("LEP license", [12, 14, 18, 18, 12]),
]

# --------------------------------------------------- processing, NEW series
# Approved applications with no deficiencies, in calendar days, with the
# year-ago comparator each packet prints beside it.
# (label, Q2 24/25, Q2 25/26, Q3 24/25, Q3 25/26)
NEW_APPROVED = [
    ("AMFT registration", 29, 27, 18, 15),
    ("ASW registration", 15, 14, 29, 10),
    ("APCC registration", 39, 21, 46, 25),
    ("LMFT license", 64, 69, 54, 96),
    ("LCSW license", 55, 86, 48, 88),
    ("LPCC license", 17, 19, 17, 22),
    ("LEP license", 12, 13, 19, 11),
]

# Deficient applications. Published for Q2 FY 25/26 only - the May 2026 report
# dropped the table, so there is no Q3 figure and the pages say so.
DEFICIENT = [
    ("AMFT registration", 74, 72),
    ("ASW registration", 52, 65),
    ("APCC registration", 177, 64),
    ("LMFT license", 134, 123),
    ("LCSW license", 108, 144),
    ("LPCC license", 77, 68),
    ("LEP license", 26, 186),
]

# The Board's own explanation of the LEP outlier, so the page does not have to
# guess at it: a single application that stayed deficient and expired at 365
# days.
LEP_OUTLIER = ("one application that remained deficient until it expired at "
               "365 days")

# ------------------------------------------------------------------ volumes
# Q3 FY 2025/26, from the May 2026 licensing update.
VOLUMES = {
    "reg_received": 2256, "reg_received_prior": 2321,
    "reg_processed": 2235, "reg_processed_prior": 2408,
    "lic_received": 2295, "lic_received_prior": 2279,
    "lic_processed": 2391, "lic_processed_prior": 2168,
}

# Population, Q3 FY 2025/26 against Q3 FY 2024/25.
POPULATION = [
    ("LMFT", 58933, 3.55), ("LCSW", 44056, 6.41), ("LPCC", 6602, 18.89),
    ("LEP", 2445, 4.44), ("AMFT", 19106, None), ("ASW", 20760, None),
    ("APCC", 8522, None),
]
POPULATION_TOTAL = 160424
POPULATION_GROWTH = 5.64

# Q1 FY 2025/26 deficiency rates, from the November 2025 licensing report.
DEFICIENCY_RATE = 29.74
DEFICIENCY_RATE_PRIOR = 23.0


# ------------------------------------------------------------------- helpers
def exam(key):
    for k, label, who, series in EXAMS:
        if k == key:
            return label, who, series
    raise KeyError(key)


def latest(key):
    """(total, overall, first_time_n, first_time) for the most recent quarter."""
    return exam(key)[2][-1]


def spread(key, idx=1):
    """(low, high) across the seven quarters for one column of one exam.

    idx 1 is the overall pass rate, 3 the first-time rate. Used to say how
    much a single quarter's headline actually moves, which is the point of
    printing seven of them.
    """
    vals = [q[idx] for q in exam(key)[2]]
    return min(vals), max(vals)


def check():
    """Every series has to be the same length as the quarter list.

    A transcription that drops one quarter from one exam shifts that row by a
    quarter against every other row, and the result is a chart that looks
    fine. This is the only kind of error in this file that cannot be seen by
    reading it.
    """
    problems = []
    n = len(QUARTERS)
    for k, label, who, series in EXAMS:
        if len(series) != n:
            problems.append("%s has %d quarters, expected %d"
                            % (k, len(series), n))
        for q in series:
            if len(q) != 4:
                problems.append("%s has a row of %d values, expected 4"
                                % (k, len(q)))
            if not (0 <= q[1] <= 100) or not (0 <= q[3] <= 100):
                problems.append("%s has a pass rate outside 0-100" % k)
            if q[2] > q[0]:
                problems.append("%s has more first-time sitters than sitters"
                                % k)
    if len(TOTAL_ADMINISTERED) != n:
        problems.append("TOTAL_ADMINISTERED has %d quarters, expected %d"
                        % (len(TOTAL_ADMINISTERED), n))
    # The per-exam totals should come close to the Board's own total. They are
    # not required to match exactly - the Board counts endorsed and
    # out-of-state candidates separately in the FY 25/26 packets - but a gap
    # of more than a few per cent means a row was mistyped.
    for i, total in enumerate(TOTAL_ADMINISTERED):
        s = sum(e[3][i][0] for e in EXAMS)
        if abs(s - total) / float(total) > 0.06:
            problems.append("%s: the exam rows sum to %d against a published "
                            "total of %d" % (QUARTERS[i], s, total))
    for label, series in OLD_TIMES:
        if len(series) != len(OLD_QUARTERS):
            problems.append("%s old series has %d quarters, expected %d"
                            % (label, len(series), len(OLD_QUARTERS)))
    return problems


if __name__ == "__main__":
    import sys
    p = check()
    for x in p:
        print("GUARD:", x)
    if p:
        sys.exit("%d problem(s)" % len(p))
    print("bbs_stats: %d quarters, %d exams, %d packets, internally consistent"
          % (len(QUARTERS), len(EXAMS), len(PACKETS)))
