#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The federal shortage-area and health-center files, reduced to counts.

WHAT THIS IS FOR

Two loan repayment programs for California therapists turn on WHERE a job is
rather than who the employer is:

  * NHSC Loan Repayment - the site must be NHSC-approved and in a mental health
    Health Professional Shortage Area.
  * California SLRP - the site must be in a federally designated HPSA, be a
    public or private not-for-profit outpatient facility, and put up matching
    funds dollar for dollar.

HRSA publishes both underlying layers as bulk downloads with no usage
limitations. This pass turns them into the counts the page prints, and writes
`_dev/hrsa_stats.py`. Nothing personal is in either file - these are facilities
and geographic designations, not people - so unlike `_dev/dca_licensees.py`
there is no privacy gate here. The raw files are still left out of the repo
because they are 38MB and regenerable.

THE TRAP THIS PASS EXISTS TO AVOID

The HPSA file contains every designation the program has ever recorded, and
in California most of them are dead: of 5,017 California mental-health rows,
2,084 are Withdrawn and 2,113 are Proposed For Withdrawal. Only 820 are
Designated. Reading the file without filtering on status overstates California
shortage areas by a factor of six, and would put a confidently wrong number on
a page people use to make employment decisions.

WHAT THE COUNTS DO NOT MEAN

A designated HPSA is a shortage AREA. It is not a list of employers, it is not
a list of NHSC-approved sites, and it does not mean any particular job at that
location qualifies for anything. The page has to say that in terms, because the
gap between "this county has designated shortage areas" and "this job qualifies"
is where somebody could lose four years of payments.
"""
import csv, collections, os, sys, io, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
OUT = os.path.join(HERE, "hrsa_stats.py")

HPSA_URL = ("https://data.hrsa.gov/DataDownload/DD_Files/"
            "BCD_HPSA_FCT_DET_MH.csv")
HC_URL = ("https://data.hrsa.gov/DataDownload/DD_Files/"
          "Health_Center_Service_Delivery_and_LookAlike_Sites.csv")

# The real 58, pinned rather than derived, for the same reason
# `_dev/dca_licensees.py` pins them: a county list read out of a data file is a
# county list that changes when the data file does.
CA_COUNTIES = [
    "Alameda", "Alpine", "Amador", "Butte", "Calaveras", "Colusa",
    "Contra Costa", "Del Norte", "El Dorado", "Fresno", "Glenn", "Humboldt",
    "Imperial", "Inyo", "Kern", "Kings", "Lake", "Lassen", "Los Angeles",
    "Madera", "Marin", "Mariposa", "Mendocino", "Merced", "Modoc", "Mono",
    "Monterey", "Napa", "Nevada", "Orange", "Placer", "Plumas", "Riverside",
    "Sacramento", "San Benito", "San Bernardino", "San Diego", "San Francisco",
    "San Joaquin", "San Luis Obispo", "San Mateo", "Santa Barbara",
    "Santa Clara", "Santa Cruz", "Shasta", "Sierra", "Siskiyou", "Solano",
    "Sonoma", "Stanislaus", "Sutter", "Tehama", "Trinity", "Tulare",
    "Tuolumne", "Ventura", "Yolo", "Yuba",
]


def fetch(url, name):
    path = os.path.join(CACHE, name)
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print("  cached  %s" % name)
        return path
    if not os.path.isdir(CACHE):
        os.makedirs(CACHE)
    print("  fetching %s" % name)
    req = urllib.request.Request(url, headers={"User-Agent": "therapistsupport.org"})
    with urllib.request.urlopen(req, timeout=180) as r, open(path, "wb") as f:
        f.write(r.read())
    print("  %s bytes" % format(os.path.getsize(path), ",d"))
    return path


def read(path):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        return list(csv.DictReader(f))


def county_of(row, key):
    v = (row.get(key) or "").replace(" County, CA", "").strip()
    return v


def main():
    print("HRSA shortage areas and health centers")

    hpsa = read(fetch(HPSA_URL, "hpsa_mh.csv"))
    ca = [r for r in hpsa
          if (r.get("Common State Abbreviation")
              or r.get("Primary State Abbreviation")) == "CA"]
    status = collections.Counter(r["HPSA Status"] for r in ca)
    des = [r for r in ca if r["HPSA Status"] == "Designated"]
    print("  California mental-health rows %s, of which Designated %d"
          % (format(len(ca), ",d"), len(des)))

    if not des:
        sys.exit("no designated California mental-health HPSAs - the file "
                 "layout has changed and every count below would be zero")

    by_type = collections.Counter(r["Designation Type"] for r in des)
    by_rural = collections.Counter(r["Rural Status"] for r in des)
    by_county = collections.Counter()
    for r in des:
        c = county_of(r, "Common County Name")
        if c in CA_COUNTIES:
            by_county[c] += 1

    scores = []
    for r in des:
        try:
            scores.append(float(r["HPSA Score"]))
        except (TypeError, ValueError):
            pass

    missing = [c for c in CA_COUNTIES if not by_county.get(c)]

    hc = read(fetch(HC_URL, "hc_sites.csv"))
    cahc = [r for r in hc if r.get("Site State Abbreviation") == "CA"
            and (r.get("Site Status Description") or "") == "Active"]
    hc_type = collections.Counter(
        (r.get("Health Center Type Description") or "").strip() for r in cahc)
    hc_county = collections.Counter()
    for r in cahc:
        c = county_of(r, "County Equivalent Name")
        if c in CA_COUNTIES:
            hc_county[c] += 1
    print("  California active health-center sites %s" % format(len(cahc), ",d"))
    if not hc_county:
        sys.exit("no California health-center sites mapped to a county - the\n                 column name has changed. This produced an empty dict rather\n                 than an error the first time and the page would have shipped\n                 a blank table.")

    body = io.StringIO()
    body.write('#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n')
    body.write('"""Counts derived from HRSA bulk downloads. WRITTEN BY '
               '_dev/hrsa_sites.py.\n\n'
               'Do not edit by hand - rerun the ETL. Every figure here is a '
               'count of\nfacilities or designations, never of people, and the '
               'raw files are left\nout of the repository because they are '
               'large and regenerable.\n\n'
               'CA_MH_HPSA_DESIGNATED counts only rows whose HPSA Status is '
               '"Designated".\nThe file also carries withdrawn and '
               'proposed-for-withdrawal rows, which\noutnumber the live ones '
               'five to one in California.\n"""\n\n')
    body.write("CHECKED = %r\n\n" % "11 August 2026")
    body.write("# every California mental-health HPSA row, by status\n")
    body.write("CA_MH_HPSA_BY_STATUS = %r\n\n" % dict(status))
    body.write("CA_MH_HPSA_DESIGNATED = %d\n" % len(des))
    body.write("CA_MH_HPSA_TOTAL_ROWS = %d\n\n" % len(ca))
    body.write("CA_MH_HPSA_BY_TYPE = %r\n\n" % dict(by_type))
    body.write("CA_MH_HPSA_BY_RURAL = %r\n\n" % dict(by_rural))
    body.write("CA_MH_HPSA_BY_COUNTY = %r\n\n" % dict(by_county))
    body.write("# the shortage score, 0 to 25 - NHSC funds highest score first\n")
    body.write("HPSA_SCORE_MIN = %g\nHPSA_SCORE_MAX = %g\n"
               "HPSA_SCORE_MEAN = %.1f\n\n"
               % (min(scores), max(scores), sum(scores) / len(scores)))
    body.write("COUNTIES_WITH_NONE = %r\n\n" % missing)
    body.write("CA_HEALTH_CENTER_SITES = %d\n\n" % len(cahc))
    body.write("CA_HEALTH_CENTER_BY_TYPE = %r\n\n" % dict(hc_type))
    body.write("CA_HEALTH_CENTER_BY_COUNTY = %r\n\n" % dict(hc_county))
    body.write("CA_COUNTIES = %r\n" % CA_COUNTIES)

    open(OUT, "w", encoding="utf-8").write(body.getvalue())
    print("  wrote %s" % os.path.basename(OUT))
    print("  %d of %d counties have at least one designated mental-health "
          "HPSA; without: %s"
          % (len(CA_COUNTIES) - len(missing), len(CA_COUNTIES),
             ", ".join(missing) or "none"))


if __name__ == "__main__":
    main()
