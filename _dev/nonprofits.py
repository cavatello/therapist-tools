#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""California nonprofit mental-health organizations, from the IRS master file.

WHAT THIS IS FOR

The P3 Bay Area directories (see ops/bay-area-directories.html, approved
13 Aug 2026) need the universe of nonprofit clinical mental-health
organizations - the set that can lawfully employ a trainee or an associate
under BPC 4980.43.3(b)(1)(B). No state agency keeps that list. The IRS
Exempt Organizations Business Master File does, indirectly: every active
exempt organization, with an NTEE activity code, a ZIP, and reported
revenue. This pass reduces the California extract to a committed data
module, statewide, so the Bay Area pages are a filter rather than a
special case (the proposal's rule: build the data statewide, publish the
Bay Area first).

THE CLASSIFICATION, STATED SO IT CAN BE ARGUED WITH

NTEE F is "Mental Health & Crisis Intervention". Three buckets:

  clinical    F30-F79 and F99: treatment facilities, community mental
              health centers, residential care, hot lines and crisis
              services, addictive-disorder treatment, counseling,
              specific-disorder services, and not-elsewhere-classified.
              These are the organizations that plausibly employ clinicians.
  substance   F20-F29: alcohol and drug prevention and treatment. Real
              clinical employers too, but a different service system with
              its own funding - kept separate, as the proposal did.
  support     F01-F19 and F80-F98: alliances, management support,
              professional societies, research, single-organization
              support and fundraising, and associations. They advocate and
              fund; they mostly do not employ trainees to see clients.

NTEE is self-reported and the page says so. The split rule lives HERE and
nowhere else, so when somebody disagrees with where F99 belongs, there is
one line to change and one place to re-run.

COUNTY MAPPING. ZIP to county via the Census 2020 ZCTA-to-county
relationship file, assigning each ZCTA to the county holding the largest
land-area share of it. ZIPs with no ZCTA (PO-box-only ZIPs) fall back to
none and the organization keeps county=None rather than a guess.

USAGE
    python3 _dev/nonprofits.py            refresh - needs the network
    python3 _dev/nonprofits.py --check    reconcile committed counts, offline

Downloads (cached under _dev/_cache, gitignored):
  https://www.irs.gov/pub/irs-soi/eo_ca.csv                      (~35 MB)
  https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/
      tab20_zcta520_county20_natl.txt                            (~7 MB)

The committed artifact is _dev/nonprofit_data.py: name, city, ZIP-derived
county, NTEE code, bucket, and reported revenue. No people, no donors -
the BMF is organizations only, published by the IRS for exactly this use.
"""
import csv, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
OUT = os.path.join(HERE, "nonprofit_data.py")

EO_URL = "https://www.irs.gov/pub/irs-soi/eo_ca.csv"
ZCTA_URL = ("https://www2.census.gov/geo/docs/maps-data/data/rel2020/"
            "zcta520/tab20_zcta520_county20_natl.txt")

CA_FIPS_COUNTY = {
    "06001": "Alameda", "06003": "Alpine", "06005": "Amador", "06007": "Butte",
    "06009": "Calaveras", "06011": "Colusa", "06013": "Contra Costa",
    "06015": "Del Norte", "06017": "El Dorado", "06019": "Fresno",
    "06021": "Glenn", "06023": "Humboldt", "06025": "Imperial",
    "06027": "Inyo", "06029": "Kern", "06031": "Kings", "06033": "Lake",
    "06035": "Lassen", "06037": "Los Angeles", "06039": "Madera",
    "06041": "Marin", "06043": "Mariposa", "06045": "Mendocino",
    "06047": "Merced", "06049": "Modoc", "06051": "Mono", "06053": "Monterey",
    "06055": "Napa", "06057": "Nevada", "06059": "Orange", "06061": "Placer",
    "06063": "Plumas", "06065": "Riverside", "06067": "Sacramento",
    "06069": "San Benito", "06071": "San Bernardino", "06073": "San Diego",
    "06075": "San Francisco", "06077": "San Joaquin",
    "06079": "San Luis Obispo", "06081": "San Mateo", "06083": "Santa Barbara",
    "06085": "Santa Clara", "06087": "Santa Cruz", "06089": "Shasta",
    "06091": "Sierra", "06093": "Siskiyou", "06095": "Solano",
    "06097": "Sonoma", "06099": "Stanislaus", "06101": "Sutter",
    "06103": "Tehama", "06105": "Trinity", "06107": "Tulare",
    "06109": "Tuolumne", "06111": "Ventura", "06113": "Yolo", "06115": "Yuba",
}

BAY = ["Alameda", "Contra Costa", "Marin", "Napa", "San Francisco",
       "San Mateo", "Santa Clara", "Solano", "Sonoma"]

SMALLCAPS = {"of", "for", "the", "and", "in", "at", "on", "de", "la", "del",
             "a", "an", "to"}
KEEPCAPS = {"LLC", "II", "III", "IV", "USA", "SF", "AACI", "YMCA", "YWCA",
            "AIDS", "LGBTQ", "CA", "MFT", "PTSD", "OCD", "NAMI", "JFCS"}


def pretty(name):
    words = []
    for i, w in enumerate(re.split(r"\s+", (name or "").strip())):
        u = w.upper().strip(",")
        if u in KEEPCAPS:
            words.append(u + ("," if w.endswith(",") else ""))
        elif i and w.lower() in SMALLCAPS:
            words.append(w.lower())
        else:
            words.append(w[:1].upper() + w[1:].lower())
    return " ".join(words)


def bucket(ntee):
    nt = (ntee or "").strip().upper()
    if not nt.startswith("F"):
        return None
    code = nt[1:3]
    n = int(code) if code.isdigit() else -1
    if 20 <= n <= 29:
        return "substance"
    if 1 <= n <= 19 or 80 <= n <= 98:
        return "support"
    return "clinical"



# Hand-curated candidate websites for the largest organizations, each FETCHED
# during refresh before it may ship as a link (the hc_orgs.py rule: a wrong
# link is worse than no link). An org absent from this map publishes as plain
# text. Verified 13 August 2026.
CURATED_URLS = {
 'Momentum for Health': 'momentumforhealth.org',
 'John Muir Behavioral Health': 'johnmuirhealth.com',
 'Caminar': 'caminar.org',
 'Fred Finch Youth Center': 'fredfinch.org',
 'Richmond Area Multi-services Inc': 'ramsinc.org',
 'Asian Americans for Community Involvement of Santa Clara Co Inc': 'aaci.org',
 'Progress Foundation': 'progressfoundation.org',
 'Edgewood Center for Children and Families': 'edgewood.org',
 'Lincoln': 'lincolnfamilies.org',
 'East Bay Agency for Children': 'ebac.org',
 'Westcoast Childrens Clinic': 'westcoastcc.org',
 'Baker Places Inc': 'prcsf.org',
 'Buckelew Programs': 'buckelew.org',
 'Westside Community Mental Health Center': 'westside-health.org',
 'Jewish Family and Community Services East Bay': 'jfcs-eastbay.org',
 'Side By Side': 'sidebysideyouth.org',
 'Eden Housing Resident Services Inc': 'edenhousing.org',
 'Crisis Support Services of Alameda County': 'crisissupport.org',
 'One Life Counseling Center': 'onelifecounselingcenter.org',
 'Family Paths Inc': 'familypaths.org',
 'Peninsula Healthcare Connection Inc': 'peninsulahcc.org',
 'Center for Mindful Psychotherapy Inc': 'mindfulpsychotherapy.org',
 'Contra Costa Crisis Center': 'crisis-center.org',
 'Translifeline': 'translifeline.org',
}

import ssl
_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE
_UA = {"User-Agent":
       "Mozilla/5.0 (compatible; therapistsupport.org link check)"}


def verify_url(dom):
    for cand in (dom, "www." + dom):
        for scheme in ("https://", "http://"):
            try:
                req = urllib.request.Request(scheme + cand, headers=_UA)
                with urllib.request.urlopen(req, timeout=12,
                                            context=_CTX) as r:
                    if 200 <= r.status < 400:
                        return cand
            except Exception:
                pass
    return None


def fetch(url, fn):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, fn)
    if not os.path.exists(p):
        print("  fetching %s ..." % url)
        req = urllib.request.Request(url, headers={"User-Agent":
            "Mozilla/5.0 (compatible; therapistsupport.org data refresh)"})
        with urllib.request.urlopen(req, timeout=120) as r, open(p, "wb") as f:
            f.write(r.read())
    return p


def zcta_county():
    p = fetch(ZCTA_URL, "zcta_county.txt")
    best = {}
    for r in csv.DictReader(open(p, encoding="utf-8-sig"), delimiter="|"):
        z, c = r["GEOID_ZCTA5_20"], r["GEOID_COUNTY_20"]
        if not z or not c:
            continue
        a = int(r["AREALAND_PART"] or 0)
        if z not in best or a > best[z][1]:
            best[z] = (c, a)
    return {z: c for z, (c, a) in best.items()}


def refresh():
    zc = zcta_county()
    p = fetch(EO_URL, "eo_ca.csv")
    orgs = []
    for r in csv.DictReader(open(p, encoding="utf-8", errors="replace")):
        b = bucket(r.get("NTEE_CD"))
        if not b:
            continue
        fips = zc.get((r.get("ZIP") or "")[:5], "")
        county = CA_FIPS_COUNTY.get(fips)
        orgs.append({
            "name": pretty(r["NAME"]),
            "city": pretty(r.get("CITY") or ""),
            "county": county,
            "ntee": (r.get("NTEE_CD") or "").strip().upper()[:3],
            "bucket": b,
            "revenue": int(r.get("REVENUE_AMT") or 0),
        })
    orgs.sort(key=lambda o: (-o["revenue"], o["name"]))

    # verify curated URLs; a candidate that does not answer ships as no link
    dead = []
    for o in orgs:
        cand = CURATED_URLS.get(o["name"])
        if cand:
            ok = verify_url(cand)
            o["url"] = ("https://" + ok) if ok else None
            if not ok:
                dead.append(o["name"])
        else:
            o["url"] = None
    if dead:
        print("  candidate URL did not answer (shipping unlinked): %s"
              % ", ".join(dead))

    from datetime import date
    n_bay = sum(1 for o in orgs if o["county"] in BAY)
    counts = {b: sum(1 for o in orgs if o["bucket"] == b)
              for b in ("clinical", "substance", "support")}
    bayc = {b: sum(1 for o in orgs
                   if o["bucket"] == b and o["county"] in BAY)
            for b in ("clinical", "substance", "support")}
    with open(OUT, "w", encoding="utf-8") as f:
        f.write('#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n')
        f.write('"""California NTEE-F exempt organizations. WRITTEN BY '
                '_dev/nonprofits.py.\n\nDo not edit by hand - rerun the ETL. '
                'Source: IRS EO BMF California extract,\ncounty via the '
                'Census 2020 ZCTA relationship file (largest land share).\n'
                'NTEE is self-reported; the bucket rule is documented in '
                'the ETL.\n"""\n\n')
        f.write("CHECKED = %r\n\n" % date.today().strftime("%-d %B %Y"))
        f.write("TOTAL = %d\nBAY_TOTAL = %d\n" % (len(orgs), n_bay))
        f.write("BY_BUCKET = %r\nBAY_BY_BUCKET = %r\n" % (counts, bayc))
        f.write("BAY_COUNTIES = %r\n\n" % BAY)
        f.write("ORGS = [\n")
        for o in orgs:
            f.write(" %r,\n" % o)
        f.write("]\n")
    print("nonprofits: %d orgs (%d Bay Area) -> %s"
          % (len(orgs), n_bay, os.path.relpath(OUT, HERE)))
    print("  statewide", counts)
    print("  bay area ", bayc)


def check():
    import importlib.util
    spec = importlib.util.spec_from_file_location("nonprofit_data", OUT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    bad = []
    if m.TOTAL != len(m.ORGS):
        bad.append("TOTAL %d != len(ORGS) %d" % (m.TOTAL, len(m.ORGS)))
    for b, n in m.BY_BUCKET.items():
        real = sum(1 for o in m.ORGS if o["bucket"] == b)
        if real != n:
            bad.append("bucket %s: %d recorded, %d real" % (b, n, real))
    baireal = sum(1 for o in m.ORGS if o["county"] in m.BAY_COUNTIES)
    if baireal != m.BAY_TOTAL:
        bad.append("BAY_TOTAL %d != %d" % (m.BAY_TOTAL, baireal))
    for o in m.ORGS:
        if o["bucket"] not in ("clinical", "substance", "support"):
            bad.append("unknown bucket %r" % o["bucket"]); break
    if bad:
        for b in bad:
            print("GUARD nonprofit_data: %s" % b)
        sys.exit(1)
    print("nonprofits --check: %d orgs, %d Bay Area, buckets reconcile"
          % (m.TOTAL, m.BAY_TOTAL))


if __name__ == "__main__":
    (check if "--check" in sys.argv else refresh)()
