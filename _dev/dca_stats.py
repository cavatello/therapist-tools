#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Counts derived from the DCA licensee file. GENERATED - do not edit.

Written by `_dev/dca_licensees.py`, which downloads the state's own
monthly file of every BBS licensee and counts it. Nothing here is
estimated and nothing here identifies anybody: this file holds totals,
and the raw file it came from is never committed.

Source: https://www.dca.ca.gov/consumers/public_info/index.shtml
File as at: August 2026

The raw file also carries an `Original Issue Date` field. It does NOT
mean the date the licence was issued, and no series here is built from
it - see the docstring in `_dev/dca_licensees.py` for the two checks
that refute it.
"""

SOURCE = 'https://www.dca.ca.gov/consumers/public_info/index.shtml'
AS_AT = 'August 2026'
TOTAL = 165235
CITIES = 1290
OUT_OF_STATE = 14710

BY_TYPE = {
    'Licensed Marriage and Family Therapist': 59706,
    'Licensed Clinical Social Worker': 45129,
    'Associate Clinical Social Worker': 21217,
    'Associate Marriage & Family Therapist': 19403,
    'Assoc. Professional Clinical Counselor': 8736,
    'Licensed Professional Clinical Counselor': 6969,
    'Licensed Educational Psychologist': 2486,
    'Temp 30Day Practice Allow(OOS Lic Only)': 1560,
    'MRF': 25,
    'Temp MSP Assoc. Clinical Social Worker': 4,
}

BY_STATUS = {
    'Current': 144473,
    'Delinquent': 14949,
    'CurrentInactive': 5813,
}

# short -> {total, delinquent, pct}
DELINQUENCY = {
    'AMFT': {"total": 19403, "delinquent": 1818, "pct": 9.4},
    'APCC': {"total": 8736, "delinquent": 2329, "pct": 26.7},
    'ASW': {"total": 21217, "delinquent": 2831, "pct": 13.3},
    'LCSW': {"total": 45129, "delinquent": 2352, "pct": 5.2},
    'LEP': {"total": 2486, "delinquent": 450, "pct": 18.1},
    'LMFT': {"total": 59706, "delinquent": 3823, "pct": 6.4},
    'LPCC': {"total": 6969, "delinquent": 197, "pct": 2.8},
}

# county -> {assoc, lic, ratio}. California addresses only.
COUNTIES = {
    'Los Angeles': {"assoc": 14325, "lic": 28438, "ratio": 0.504},
    'San Diego': {"assoc": 3879, "lic": 9162, "ratio": 0.423},
    'Orange': {"assoc": 3825, "lic": 8353, "ratio": 0.458},
    'Alameda': {"assoc": 2282, "lic": 5775, "ratio": 0.395},
    'Riverside': {"assoc": 2885, "lic": 4531, "ratio": 0.637},
    'San Bernardino': {"assoc": 2619, "lic": 4042, "ratio": 0.648},
    'Santa Clara': {"assoc": 2035, "lic": 4128, "ratio": 0.493},
    'Sacramento': {"assoc": 1775, "lic": 4184, "ratio": 0.424},
    'San Francisco': {"assoc": 1383, "lic": 3491, "ratio": 0.396},
    'Contra Costa': {"assoc": 1204, "lic": 3068, "ratio": 0.392},
    'Ventura': {"assoc": 1011, "lic": 2619, "ratio": 0.386},
    'Fresno': {"assoc": 1194, "lic": 1946, "ratio": 0.614},
    'Sonoma': {"assoc": 589, "lic": 2116, "ratio": 0.278},
    'San Mateo': {"assoc": 739, "lic": 1871, "ratio": 0.395},
    'Marin': {"assoc": 396, "lic": 1662, "ratio": 0.238},
    'Kern': {"assoc": 767, "lic": 1252, "ratio": 0.613},
    'Santa Barbara': {"assoc": 553, "lic": 1424, "ratio": 0.388},
    'Placer': {"assoc": 502, "lic": 1346, "ratio": 0.373},
    'Santa Cruz': {"assoc": 414, "lic": 1360, "ratio": 0.304},
    'San Joaquin': {"assoc": 649, "lic": 906, "ratio": 0.716},
    'Solano': {"assoc": 512, "lic": 955, "ratio": 0.536},
    'Monterey': {"assoc": 495, "lic": 931, "ratio": 0.532},
    'San Luis Obispo': {"assoc": 316, "lic": 1107, "ratio": 0.285},
    'Stanislaus': {"assoc": 520, "lic": 855, "ratio": 0.608},
    'Tulare': {"assoc": 499, "lic": 669, "ratio": 0.746},
    'Butte': {"assoc": 299, "lic": 648, "ratio": 0.461},
    'Humboldt': {"assoc": 251, "lic": 557, "ratio": 0.451},
    'Shasta': {"assoc": 248, "lic": 517, "ratio": 0.48},
    'Yolo': {"assoc": 216, "lic": 490, "ratio": 0.441},
    'El Dorado': {"assoc": 174, "lic": 505, "ratio": 0.345},
    'Nevada': {"assoc": 126, "lic": 451, "ratio": 0.279},
    'Napa': {"assoc": 151, "lic": 421, "ratio": 0.359},
    'Merced': {"assoc": 217, "lic": 264, "ratio": 0.822},
    'Mendocino': {"assoc": 86, "lic": 268, "ratio": 0.321},
    'Imperial': {"assoc": 173, "lic": 164, "ratio": 1.055},
    'Madera': {"assoc": 121, "lic": 187, "ratio": 0.647},
    'Kings': {"assoc": 130, "lic": 162, "ratio": 0.802},
    'Sutter': {"assoc": 88, "lic": 147, "ratio": 0.599},
    'Yuba': {"assoc": 77, "lic": 76, "ratio": 1.013},
    'San Benito': {"assoc": 62, "lic": 86, "ratio": 0.721},
    'Tehama': {"assoc": 56, "lic": 81, "ratio": 0.691},
    'Tuolumne': {"assoc": 37, "lic": 99, "ratio": 0.374},
    'Siskiyou': {"assoc": 30, "lic": 95, "ratio": 0.316},
    'Calaveras': {"assoc": 30, "lic": 92, "ratio": 0.326},
    'Lake': {"assoc": 25, "lic": 85, "ratio": 0.294},
    'Amador': {"assoc": 19, "lic": 52, "ratio": 0.365},
    'Del Norte': {"assoc": 17, "lic": 43, "ratio": 0.395},
    'Glenn': {"assoc": 19, "lic": 38, "ratio": 0.5},
    'Inyo': {"assoc": 13, "lic": 37, "ratio": 0.351},
    'Mariposa': {"assoc": 15, "lic": 33, "ratio": 0.455},
    'Plumas': {"assoc": 7, "lic": 36, "ratio": 0.194},
    'Lassen': {"assoc": 14, "lic": 27, "ratio": 0.519},
    'Trinity': {"assoc": 9, "lic": 25, "ratio": 0.36},
    'Colusa': {"assoc": 12, "lic": 21, "ratio": 0.571},
    'Mono': {"assoc": 12, "lic": 19, "ratio": 0.632},
    'Modoc': {"assoc": 3, "lic": 17, "ratio": 0.176},
    'Alpine': {"assoc": 1, "lic": 3, "ratio": 0.333},
    'Sierra': {"assoc": 1, "lic": 2, "ratio": 0.5},
}

