#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""County behavioral health plans. WRITTEN BY _dev/county_bh.py.

Transcribed from DHCS's county mental health plan page, then every
link fetched. `url` is the address that actually answered, after
redirects; `listed` is what the state page prints; `moved` is True
where those differ. A plan with url None is shipped without a link.
"""

CHECKED = '11 August 2026'
SOURCE = 'https://www.dhcs.ca.gov/CMHP'

PLANS = [
    {'county': 'Alameda, and the City of Berkeley', 'url': 'https://health.alamedacountyca.gov/department/behavioral-health-department/', 'listed': 'http://www.acbhcs.org/', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Alpine', 'url': 'http://www.alpinecountyca.gov/192/Behavioral-Health-Services', 'listed': 'http://www.alpinecountyca.gov/Index.aspx?NID=192', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Amador', 'url': 'http://www.co.amador.ca.us/services/behavioral-health/mental-health', 'listed': 'http://www.co.amador.ca.us/services/behavioral-health/mental-health', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Butte', 'url': 'https://www.buttecounty.net/159/Behavioral-Health', 'listed': 'https://www.buttecounty.net/159/Behavioral-Health', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'Calaveras', 'url': 'https://mentalhealth.calaverasgov.us/', 'listed': 'https://mentalhealth.calaverasgov.us/', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'Colusa', 'url': 'https://www.countyofcolusaca.gov/325/Behavioral-Health', 'listed': 'http://www.countyofcolusa.org/index.aspx?nid=325', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Contra Costa', 'url': 'http://cchealth.org/mentalhealth/', 'listed': 'http://cchealth.org/mentalhealth/', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Del Norte', 'url': 'https://www.co.del-norte.ca.us/departments/health-human-services/Behavioral-Health-Branch', 'listed': 'http://www.co.del-norte.ca.us/departments/health-human-services/Behavioral-Health-Branch', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'El Dorado', 'url': 'https://www.eldoradocounty.ca.gov/Health-Well-Being/Behavioral-Health', 'listed': 'https://www.eldoradocounty.ca.gov/Health-Well-Being/Behavioral-Health', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Fresno', 'url': 'https://www.co.fresno.ca.us/departments/behavioral-health', 'listed': 'https://www.co.fresno.ca.us/departments/behavioral-health', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Glenn', 'url': 'http://www.countyofglenn.net/dept/health-human-services/behavioral-health/welcome', 'listed': 'http://www.countyofglenn.net/dept/health-human-services/behavioral-health/welcome', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Humboldt', 'url': 'https://www.humboldtgov.org/329/Behavioral-Health', 'listed': 'http://www.humboldtgov.org/329/Mental-Health', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Imperial', 'url': 'https://bhs.imperialcounty.org/', 'listed': 'https://bhs.imperialcounty.org/', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'Inyo', 'url': 'https://www.inyocounty.us/behavioral-health-division', 'listed': 'https://www.inyocounty.us/services/health-human-services/behavioral-health-division', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Kern', 'url': 'https://www.kernbhrs.org/', 'listed': 'https://www.kernbhrs.org/', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Kings', 'url': 'http://www.kcbh.org/', 'listed': 'http://www.kcbh.org/', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Lake', 'url': 'https://lcbh.lakecountyca.gov/173/Behavioral-Health-Services', 'listed': 'http://lcbh.lakecountyca.gov/', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Lassen', 'url': 'https://www.lassencounty.gov/', 'listed': 'http://www.lassencounty.org/node/142', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Los Angeles', 'url': 'https://dmh.lacounty.gov/', 'listed': 'https://dmh.lacounty.gov/', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'Madera', 'url': 'https://www.maderacounty.com/government/behavioral-health-services', 'listed': 'https://www.maderacounty.com/government/behavioral-health-services', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Marin', 'url': 'https://www.marinhhs.org/mental-health-services', 'listed': 'https://www.marinhhs.org/mental-health-services', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Mariposa', 'url': 'http://www.mariposacounty.gov/250/Behavioral-Health-Recovery-Services', 'listed': 'http://www.mariposacounty.org/index.aspx?nid=250', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Mendocino', 'url': 'https://www.co.mendocino.ca.us/hhsa/mentalhealth.htm', 'listed': 'https://www.co.mendocino.ca.us/hhsa/mentalhealth.htm', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Merced', 'url': 'https://www.countyofmerced.com/78/Behavioral-Health-Recovery-Services', 'listed': 'http://www.co.merced.ca.us/index.aspx?nid=78', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Modoc', 'url': None, 'listed': 'http://www.co.modoc.ca.us/departments/health-services', 'moved': False, 'blocked': False, 'note': 'did not answer'},
    {'county': 'Mono', 'url': None, 'listed': 'http://www.monocounty.ca.gov/behavioral-health/page/about-us', 'moved': False, 'blocked': False, 'note': 'did not answer'},
    {'county': 'Monterey', 'url': 'http://www.co.monterey.ca.us/government/departments-a-h/health/behavioral-health', 'listed': 'http://www.co.monterey.ca.us/government/departments-a-h/health/behavioral-health', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Napa', 'url': 'https://www.napacounty.gov/3730/Behavioral-Health-Services-BHS', 'listed': 'https://www.countyofnapa.org/3730/Behavioral-Health-Services-BHS', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Nevada', 'url': 'https://www.nevadacountyca.gov/430/Behavioral-Health', 'listed': 'https://www.mynevadacounty.com/430/Behavioral-Health', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Orange', 'url': 'https://www.ochealthinfo.com/services-programs/mental-health-crisis-recovery/mental-health', 'listed': 'http://www.ochealthinfo.com/bhs/', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Placer', 'url': 'https://www.placer.ca.gov/2166/Mental-Health-Services', 'listed': 'https://www.placer.ca.gov/2166/Mental-Health-Services', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'Plumas', 'url': 'https://www.plumascounty.us/87/Behavioral-Health', 'listed': 'http://www.countyofplumas.com/mentalhealth/', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Riverside', 'url': 'https://www.ruhealth.org/behavioral-health', 'listed': 'http://www.rcdmh.org/', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Sacramento', 'url': None, 'listed': 'http://www.dhs.saccounty.net/BHS/Pages/BHS-Home.aspx', 'moved': False, 'blocked': False, 'note': 'did not answer'},
    {'county': 'San Benito', 'url': 'https://www.cosb.us/departments/behavioral-health', 'listed': 'https://www.cosb.us/departments/behavioral-health', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'San Bernardino', 'url': 'https://wp.sbcounty.gov/dbh/', 'listed': 'http://wp.sbcounty.gov/dbh/', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'San Diego', 'url': 'https://www.sandiegocounty.gov/hhsa/programs/bhs/', 'listed': 'http://www.sandiegocounty.gov/hhsa/programs/bhs/', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'San Francisco', 'url': 'https://www.sf.gov/information--get-help-mental-health-or-substance-use', 'listed': 'https://www.sf.gov/information/mental-health-and-substance-use-resources', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'San Joaquin', 'url': 'https://www.sjcbhs.org/index.aspx', 'listed': 'https://www.sjcbhs.org/index.aspx', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'San Luis Obispo', 'url': 'https://www.slocounty.ca.gov/departments/slo-health/behavioral-health', 'listed': 'https://www.slocounty.ca.gov/departments/health-agency/behavioral-health', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'San Mateo', 'url': 'https://www.smchealth.org/mental-health-services', 'listed': 'http://www.smchealth.org/mentalhealth', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Santa Barbara', 'url': 'https://www.countyofsb.org/bw-behavioral-wellness', 'listed': 'https://www.countyofsb.org/behavioral-wellness', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Santa Clara', 'url': 'https://bhsd.sccgov.org/home', 'listed': 'https://bhsd.sccgov.org/home', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Santa Cruz', 'url': 'https://www.santacruzhealth.org/login.aspx?ReturnUrl=%2fHSAHome%2fHSADivisions%2fBehavioralHealth.aspx', 'listed': 'http://www.santacruzhealth.org/HSAHome/HSADivisions/BehavioralHealth.aspx', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Shasta', 'url': 'http://www.co.shasta.ca.us/index/hhsa_index/mental_wellness.aspx', 'listed': 'http://www.co.shasta.ca.us/index/hhsa_index/mental_wellness.aspx', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Sierra', 'url': 'https://www.sierracounty.ca.gov/181/Behavioral-Health', 'listed': 'http://www.sierracounty.ca.gov/index.aspx?NID=181', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Siskiyou', 'url': 'https://www.siskiyoucounty.gov/behavioralhealth', 'listed': 'https://www.co.siskiyou.ca.us/behavioralhealth', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Solano', 'url': 'https://www.solanocounty.gov/government/health-social-services-hss/behavioral-health', 'listed': 'https://www.solanocounty.gov/government/health-social-services-hss/behavioral-health', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'Sonoma', 'url': 'https://sonomacounty.gov/health-and-human-services/health-services/divisions/behavioral-health/services', 'listed': 'https://sonomacounty.ca.gov/health-and-human-services/health-services/divisions/behavioral-health/services', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Stanislaus', 'url': 'https://www.stancounty.com/bhrs/', 'listed': 'http://www.stancounty.com/bhrs/', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'Sutter and Yuba', 'url': 'https://www.co.sutter.ca.us/doc/government/depts/hs/mh/hs_behavioral_health', 'listed': 'https://www.co.sutter.ca.us/doc/government/depts/hs/mh/hs_behavioral_health', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Tehama', 'url': 'https://www.tehamacohealthservices.net/', 'listed': 'https://www.tehamacohealthservices.net/', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'Trinity', 'url': 'https://www.trinitycounty.org/Behavioral-Health', 'listed': 'https://www.trinitycounty.org/Behavioral-Health', 'moved': False, 'blocked': False, 'note': None},
    {'county': 'Tulare', 'url': None, 'listed': None, 'moved': False, 'blocked': False, 'note': 'not listed by DHCS'},
    {'county': 'Tuolumne', 'url': 'http://www.co.tuolumne.ca.us/Index.aspx?NID=220', 'listed': 'http://www.co.tuolumne.ca.us/Index.aspx?NID=220', 'moved': False, 'blocked': True, 'note': None},
    {'county': 'Ventura', 'url': 'https://hca.venturacounty.gov/behavioral-health/en/', 'listed': 'https://vcbh.org/en/', 'moved': True, 'blocked': False, 'note': None},
    {'county': 'Yolo', 'url': 'https://www.yolocounty.org/government/general-government-departments/health-human-services/mental-health/mental-health-services', 'listed': 'https://www.yolocounty.org/government/general-government-departments/health-human-services/mental-health/mental-health-services', 'moved': False, 'blocked': True, 'note': None},
]

TOTAL = 57
LINKED = 53
DEAD = 4
MOVED = 23
BLOCKED = 17
