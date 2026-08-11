#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Counts derived from HRSA bulk downloads. WRITTEN BY _dev/hrsa_sites.py.

Do not edit by hand - rerun the ETL. Every figure here is a count of
facilities or designations, never of people, and the raw files are left
out of the repository because they are large and regenerable.

CA_MH_HPSA_DESIGNATED counts only rows whose HPSA Status is "Designated".
The file also carries withdrawn and proposed-for-withdrawal rows, which
outnumber the live ones five to one in California.
"""

CHECKED = '11 August 2026'

# every California mental-health HPSA row, by status
CA_MH_HPSA_BY_STATUS = {'Withdrawn': 2084, 'Designated': 820, 'Proposed For Withdrawal': 2113}

CA_MH_HPSA_DESIGNATED = 820
CA_MH_HPSA_TOTAL_ROWS = 5017

CA_MH_HPSA_BY_TYPE = {'Federally Qualified Health Center': 170, 'Federally Qualified Health Center Look A Like': 46, 'Indian Health Service, Tribal Health, and Urban Indian Health Organizations': 119, 'Rural Health Clinic': 108, 'Correctional Facility': 31, 'Geographic HPSA': 16, 'HPSA Population': 213, 'High Needs Geographic HPSA': 115, 'Other Facility': 2}

CA_MH_HPSA_BY_RURAL = {'Non-Rural': 505, 'Rural': 242, 'Partially Rural': 53, 'Unknown': 20}

CA_MH_HPSA_BY_COUNTY = {'Los Angeles': 116, 'Tulare': 17, 'Riverside': 19, 'Alameda': 13, 'Sonoma': 7, 'Sacramento': 8, 'Fresno': 59, 'Placer': 10, 'Marin': 3, 'Mendocino': 14, 'Tehama': 13, 'Siskiyou': 11, 'Shasta': 11, 'Merced': 6, 'Santa Clara': 13, 'Colusa': 3, 'San Diego': 28, 'Napa': 1, 'Trinity': 5, 'Santa Barbara': 8, 'Solano': 2, 'Santa Cruz': 3, 'Kings': 13, 'San Bernardino': 72, 'Modoc': 5, 'Imperial': 7, 'Kern': 184, 'San Francisco': 8, 'Stanislaus': 4, 'Orange': 18, 'Yolo': 5, 'Yuba': 4, 'Humboldt': 7, 'El Dorado': 5, 'Lassen': 6, 'San Benito': 16, 'Contra Costa': 2, 'Nevada': 3, 'Madera': 5, 'Ventura': 2, 'Butte': 7, 'Lake': 13, 'San Mateo': 3, 'Monterey': 8, 'Sutter': 3, 'San Joaquin': 4, 'San Luis Obispo': 1, 'Glenn': 2, 'Mariposa': 4, 'Inyo': 3, 'Plumas': 7, 'Sierra': 2, 'Del Norte': 6, 'Calaveras': 4, 'Tuolumne': 12, 'Mono': 2, 'Amador': 3}

# the shortage score, 0 to 25 - NHSC funds highest score first
HPSA_SCORE_MIN = 3
HPSA_SCORE_MAX = 24
HPSA_SCORE_MEAN = 16.6

COUNTIES_WITH_NONE = ['Alpine']

CA_HEALTH_CENTER_SITES = 3038

CA_HEALTH_CENTER_BY_TYPE = {'Service Delivery Site': 2542, 'Administrative': 293, 'Administrative/Service Delivery Site': 203}

CA_HEALTH_CENTER_BY_COUNTY = {'Ventura': 59, 'Los Angeles': 831, 'San Diego': 286, 'Santa Clara': 100, 'Santa Barbara': 57, 'Orange': 182, 'Riverside': 126, 'Kern': 78, 'Kings': 23, 'Fresno': 110, 'Sacramento': 96, 'Tulare': 74, 'Placer': 8, 'Marin': 34, 'San Bernardino': 87, 'Monterey': 31, 'Alameda': 168, 'Humboldt': 33, 'San Francisco': 86, 'Solano': 30, 'Contra Costa': 53, 'Mendocino': 24, 'Napa': 8, 'Nevada': 8, 'San Mateo': 44, 'Siskiyou': 15, 'San Joaquin': 47, 'Santa Cruz': 42, 'San Luis Obispo': 15, 'Imperial': 9, 'Stanislaus': 49, 'Yuba': 13, 'Yolo': 20, 'Merced': 28, 'Madera': 25, 'Sutter': 12, 'Colusa': 2, 'Shasta': 28, 'Butte': 9, 'Sonoma': 54, 'Del Norte': 4, 'San Benito': 2, 'Mariposa': 2, 'El Dorado': 7, 'Tehama': 5, 'Inyo': 2, 'Lake': 1, 'Glenn': 2, 'Sierra': 1, 'Trinity': 2, 'Lassen': 4, 'Amador': 1}

CA_COUNTIES = ['Alameda', 'Alpine', 'Amador', 'Butte', 'Calaveras', 'Colusa', 'Contra Costa', 'Del Norte', 'El Dorado', 'Fresno', 'Glenn', 'Humboldt', 'Imperial', 'Inyo', 'Kern', 'Kings', 'Lake', 'Lassen', 'Los Angeles', 'Madera', 'Marin', 'Mariposa', 'Mendocino', 'Merced', 'Modoc', 'Mono', 'Monterey', 'Napa', 'Nevada', 'Orange', 'Placer', 'Plumas', 'Riverside', 'Sacramento', 'San Benito', 'San Bernardino', 'San Diego', 'San Francisco', 'San Joaquin', 'San Luis Obispo', 'San Mateo', 'Santa Barbara', 'Santa Clara', 'Santa Cruz', 'Shasta', 'Sierra', 'Siskiyou', 'Solano', 'Sonoma', 'Stanislaus', 'Sutter', 'Tehama', 'Trinity', 'Tulare', 'Tuolumne', 'Ventura', 'Yolo', 'Yuba']
