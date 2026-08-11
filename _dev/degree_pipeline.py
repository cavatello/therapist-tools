#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""California master's degrees in the therapy pipeline, by year.

WRITTEN BY _dev/ipeds_degrees.py, which needs the network. Do not
edit. `WIDE` is the set of CIP codes a California LMFT or LPCC
degree actually files under; 51.1505 alone undercounts because the
Board approves a degree by content rather than by CIP. 2020 is absent
because this mirror returns it byte-identical to 2015 for every
California institution, which is not a real year.
"""

CHECKED = '11 August 2026'
SOURCE = 'https://educationdata.urban.org/documentation/colleges.html'
NCES = 'https://nces.ed.gov/ipeds/use-the-data'
YEARS = [2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023]
EXCLUDED_YEAR = 2020
CIP = [('511505', 'Marriage and family therapy', True), ('422803', 'Counseling psychology', True), ('511508', 'Mental health counseling', True), ('422801', 'Clinical psychology', True), ('440701', 'Social work', False), ('131101', 'Counselor education and school counseling', False), ('420101', 'Psychology, general', False), ('511501', 'Substance abuse and addiction counseling', False), ('511503', 'Clinical and medical social work', False), ('511599', 'Mental and social health services, other', False)]
WIDE = ['511505', '422803', '511508', '422801']
SERIES = {2015: {'511505': 1232, '422803': 1143, '511508': 20, '422801': 810, '440701': 3380, '131101': 1191, '420101': 1171, '511501': 0, '511503': 0, '511599': 0}, 2016: {'511505': 1303, '422803': 1246, '511508': 30, '422801': 758, '440701': 3476, '131101': 1225, '420101': 1240, '511501': 0, '511503': 0, '511599': 0}, 2017: {'511505': 1193, '422803': 1186, '511508': 25, '422801': 779, '440701': 3538, '131101': 1476, '420101': 1369, '511501': 0, '511503': 0, '511599': 0}, 2018: {'511505': 1155, '422803': 1209, '511508': 25, '422801': 900, '440701': 3500, '131101': 1538, '420101': 1289, '511501': 0, '511503': 0, '511599': 0}, 2019: {'511505': 1165, '422803': 1302, '511508': 31, '422801': 808, '440701': 3290, '131101': 1589, '420101': 1315, '511501': 0, '511503': 42, '511599': 0}, 2021: {'511505': 1186, '422803': 1319, '511508': 41, '422801': 974, '440701': 3073, '131101': 1877, '420101': 1293, '511501': 0, '511503': 37, '511599': 0}, 2022: {'511505': 1293, '422803': 1466, '511508': 32, '422801': 1112, '440701': 3003, '131101': 1870, '420101': 1313, '511501': 0, '511503': 64, '511599': 0}, 2023: {'511505': 1802, '422803': 1737, '511508': 256, '422801': 1514, '440701': 3049, '131101': 1791, '420101': 1223, '511501': 1, '511503': 56, '511599': 0}}
STATE_TOTAL = {2015: 79619, 2016: 80925, 2017: 82644, 2018: 85051, 2019: 85440, 2021: 86304, 2022: 87280, 2023: 90511}
WIDE_LATEST = 5309
WIDE_FIRST = 3205
