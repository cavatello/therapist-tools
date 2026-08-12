#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""San Francisco clinical pay. WRITTEN BY _dev/sf_pay.py.

San Francisco is absent from the State Controller's COUNTY file - it
is a consolidated city and county and files in the cities dataset -
so `_dev/county_pay.py` cannot see it. These figures come from the
city's own compensation file over DataSF, and are ACTUAL BASE SALARY
for full-time staff, not a published salary range. They are not
comparable with `county_pay_data.COUNTIES` and must never be put in
the same table.
"""

CHECKED = '12 August 2026'
SOURCE = 'https://data.sfgov.org/resource/88g8-5mnd.json'
PAGE = 'https://data.sfgov.org/City-Management-and-Ethics/Employee-Compensation/88g8-5mnd'
YEARS = ['2023', '2024', '2025']
FT_HOURS = 1800
TITLES = ['Behavioral Health Clinician', 'Sr Behavioral Health Clinicn', 'Clinical Psychologist', 'Behavioral Health Team Leader', 'Marriage, Family & Child Cnslr']
EXCLUDED = [('Counselor, Juvenile Hall', 'custody staff in the juvenile justice system, not a clinical classification'), ('Counselor, Family Court Svc', 'court mediation, under the Superior Court'), ('Environmental Health Inspector', 'matches on &ldquo;health&rdquo; and is an inspector'), ('Sr Employee Asst Counselor', 'internal employee assistance, two people'), ('Rehabilitation Counselor', 'vocational rehabilitation, one person')]
YEAR_TOTALS = {'2023': {'n_all': 396, 'n_ft': 278, 'median': 124311, 'p10': 104464, 'p90': 129724, 'top': 143899}, '2024': {'n_all': 424, 'n_ft': 297, 'median': 136180, 'p10': 113531, 'p90': 142728, 'top': 157940}, '2025': {'n_all': 441, 'n_ft': 305, 'median': 137650, 'p10': 113258, 'p90': 144788, 'top': 155048}}
BY_TITLE = [{'job': 'Behavioral Health Clinician', 'n': 183, 'median': 133875, 'p10': 113159, 'p90': 137918}, {'job': 'Sr Behavioral Health Clinicn', 'n': 71, 'median': 144788, 'p10': 140483, 'p90': 144788}, {'job': 'Clinical Psychologist', 'n': 18, 'median': 153390, 'p10': 139541, 'p90': 155048}, {'job': 'Behavioral Health Team Leader', 'n': 17, 'median': 111991, 'p10': 102297, 'p90': 114184}, {'job': 'Marriage, Family & Child Cnslr', 'n': 16, 'median': 133932, 'p10': 120527, 'p90': 133932}]
TOP_DEPARTMENT = ('Public Health', 298)
