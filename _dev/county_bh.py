#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The county behavioral health plans, with every link on the state's own page checked.

WHERE THE LIST COMES FROM

DHCS publishes the county mental health plans at dhcs.ca.gov/CMHP, with a
website for each. That is the authoritative list - these are the agencies the
state contracts with to run Medi-Cal specialty mental health, which is the
system that employs registered associates in volume.

WHY IT STILL NEEDS CHECKING

A published government directory is not a working one. County websites move,
and the state page is not regenerated when they do. Every URL below is fetched
before it is allowed to ship, the final URL after redirects is recorded, and
anything that does not answer is shipped with NO link and counted - because
"the state's own directory has N dead links" is a finding worth publishing, and
a dead link on this site is not.

WHAT THIS LIST IS NOT

It is not a list of open jobs, and it is not a claim that any of these agencies
qualifies anyone for anything. A county is a local government entity, which is
the shape PSLF's employer definition asks for - but that is a question for the
federal employer search, not for this page.
"""
import concurrent.futures as cf, io, json, os, ssl, sys
import urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "county_bh_data.py")
CHECKED = "11 August 2026"
SOURCE = "https://www.dhcs.ca.gov/CMHP"

# Transcribed from dhcs.ca.gov/CMHP. The county names are DHCS's, including
# the two that are not one county each: Sutter and Yuba share a single plan,
# and Alameda's entry covers the City of Berkeley.
PLANS = [
    ("Alameda, and the City of Berkeley", "http://www.acbhcs.org/"),
    ("Alpine", "http://www.alpinecountyca.gov/Index.aspx?NID=192"),
    ("Amador", "http://www.co.amador.ca.us/services/behavioral-health/mental-health"),
    ("Butte", "https://www.buttecounty.net/159/Behavioral-Health"),
    ("Calaveras", "https://mentalhealth.calaverasgov.us/"),
    ("Colusa", "http://www.countyofcolusa.org/index.aspx?nid=325"),
    ("Contra Costa", "http://cchealth.org/mentalhealth/"),
    ("Del Norte", "http://www.co.del-norte.ca.us/departments/health-human-services/Behavioral-Health-Branch"),
    ("El Dorado", "https://www.eldoradocounty.ca.gov/Health-Well-Being/Behavioral-Health"),
    ("Fresno", "https://www.co.fresno.ca.us/departments/behavioral-health"),
    ("Glenn", "http://www.countyofglenn.net/dept/health-human-services/behavioral-health/welcome"),
    ("Humboldt", "http://www.humboldtgov.org/329/Mental-Health"),
    ("Imperial", "https://bhs.imperialcounty.org/"),
    ("Inyo", "https://www.inyocounty.us/services/health-human-services/behavioral-health-division"),
    ("Kern", "https://www.kernbhrs.org/"),
    ("Kings", "http://www.kcbh.org/"),
    ("Lake", "http://lcbh.lakecountyca.gov/"),
    ("Lassen", "http://www.lassencounty.org/node/142"),
    ("Los Angeles", "https://dmh.lacounty.gov/"),
    ("Madera", "https://www.maderacounty.com/government/behavioral-health-services"),
    ("Marin", "https://www.marinhhs.org/mental-health-services"),
    ("Mariposa", "http://www.mariposacounty.org/index.aspx?nid=250"),
    ("Mendocino", "https://www.co.mendocino.ca.us/hhsa/mentalhealth.htm"),
    ("Merced", "http://www.co.merced.ca.us/index.aspx?nid=78"),
    ("Modoc", "http://www.co.modoc.ca.us/departments/health-services"),
    ("Mono", "http://www.monocounty.ca.gov/behavioral-health/page/about-us"),
    ("Monterey", "http://www.co.monterey.ca.us/government/departments-a-h/health/behavioral-health"),
    ("Napa", "https://www.countyofnapa.org/3730/Behavioral-Health-Services-BHS"),
    ("Nevada", "https://www.mynevadacounty.com/430/Behavioral-Health"),
    ("Orange", "http://www.ochealthinfo.com/bhs/"),
    ("Placer", "https://www.placer.ca.gov/2166/Mental-Health-Services"),
    ("Plumas", "http://www.countyofplumas.com/mentalhealth/"),
    ("Riverside", "http://www.rcdmh.org/"),
    ("Sacramento", "http://www.dhs.saccounty.net/BHS/Pages/BHS-Home.aspx"),
    ("San Benito", "https://www.cosb.us/departments/behavioral-health"),
    ("San Bernardino", "http://wp.sbcounty.gov/dbh/"),
    ("San Diego", "http://www.sandiegocounty.gov/hhsa/programs/bhs/"),
    ("San Francisco", "https://www.sf.gov/information/mental-health-and-substance-use-resources"),
    ("San Joaquin", "https://www.sjcbhs.org/index.aspx"),
    ("San Luis Obispo", "https://www.slocounty.ca.gov/departments/health-agency/behavioral-health"),
    ("San Mateo", "http://www.smchealth.org/mentalhealth"),
    ("Santa Barbara", "https://www.countyofsb.org/behavioral-wellness"),
    ("Santa Clara", "https://bhsd.sccgov.org/home"),
    ("Santa Cruz", "http://www.santacruzhealth.org/HSAHome/HSADivisions/BehavioralHealth.aspx"),
    ("Shasta", "http://www.co.shasta.ca.us/index/hhsa_index/mental_wellness.aspx"),
    ("Sierra", "http://www.sierracounty.ca.gov/index.aspx?NID=181"),
    ("Siskiyou", "https://www.co.siskiyou.ca.us/behavioralhealth"),
    ("Solano", "https://www.solanocounty.gov/government/health-social-services-hss/behavioral-health"),
    ("Sonoma", "https://sonomacounty.ca.gov/health-and-human-services/health-services/divisions/behavioral-health/services"),
    ("Stanislaus", "http://www.stancounty.com/bhrs/"),
    ("Sutter and Yuba", "https://www.co.sutter.ca.us/doc/government/depts/hs/mh/hs_behavioral_health"),
    ("Tehama", "https://www.tehamacohealthservices.net/"),
    ("Trinity", "https://www.trinitycounty.org/Behavioral-Health"),
    ("Tulare", None),
    ("Tuolumne", "http://www.co.tuolumne.ca.us/Index.aspx?NID=220"),
    ("Ventura", "https://vcbh.org/en/"),
    ("Yolo", "https://www.yolocounty.org/government/general-government-departments/health-human-services/mental-health/mental-health-services"),
]

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (compatible; therapistsupport.org link check)"


# A .gov site behind bot protection answers 403 to an automated request and
# is perfectly fine in a browser. Treating that as a dead link would have this
# page telling readers that twenty county websites are down when they are not,
# which is a worse error than any it is trying to prevent. So: an HTTP status
# means the server answered and the address is real. Only a DNS failure, a
# refused connection, a timeout, or an explicit 404/410 is a broken link.
REACHABLE_ERRORS = {401, 402, 403, 405, 406, 408, 409, 429, 500, 502, 503}


def check(item):
    county, url = item
    if not url:
        return county, None, "not listed by DHCS", False
    tries = [url]
    if url.startswith("http://"):
        tries.insert(0, "https://" + url[7:])
    blocked = None
    for u in tries:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15, context=CTX) as r:
                if 200 <= r.status < 400:
                    return county, r.geturl(), None, False
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                continue
            if e.code in REACHABLE_ERRORS:
                blocked = u
        except Exception:
            pass
    if blocked:
        return county, blocked, None, True
    return county, None, "did not answer", False


def main():
    print("county behavioral health plans")
    print("  %d plans on the state page, checking every link" % len(PLANS))
    rows, dead, moved = [], 0, 0
    with cf.ThreadPoolExecutor(max_workers=16) as ex:
        for county, final, why, blocked in ex.map(check, PLANS):
            listed = dict(PLANS)[county]
            if final:
                # normalise for comparison: a bare scheme upgrade is not a move
                same = (final.rstrip("/") == (listed or "").rstrip("/")
                        or final.rstrip("/") == (listed or "").replace(
                            "http://", "https://").rstrip("/"))
                if not same:
                    moved += 1
                rows.append({"county": county, "url": final,
                             "listed": listed, "moved": not same,
                             "blocked": blocked, "note": None})
            else:
                dead += 1
                rows.append({"county": county, "url": None, "listed": listed,
                             "moved": False, "blocked": False, "note": why})
    print("  %d answered, %d did not, %d resolved somewhere other than the "
          "address DHCS prints" % (len(PLANS) - dead, dead, moved))

    if dead > len(PLANS) * 0.4:
        sys.exit("more than 40%% of county links failed - that is a network "
                 "problem here, not %d dead county websites" % dead)

    b = io.StringIO()
    b.write("#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n")
    b.write('"""County behavioral health plans. WRITTEN BY _dev/county_bh.py.\n\n'
            "Transcribed from DHCS's county mental health plan page, then every\n"
            "link fetched. `url` is the address that actually answered, after\n"
            "redirects; `listed` is what the state page prints; `moved` is True\n"
            "where those differ. A plan with url None is shipped without a link.\n"
            '"""\n\n')
    b.write("CHECKED = %r\nSOURCE = %r\n\n" % (CHECKED, SOURCE))
    b.write("PLANS = [\n")
    for r in rows:
        b.write("    %r,\n" % r)
    b.write("]\n\n")
    b.write("TOTAL = %d\nLINKED = %d\nDEAD = %d\nMOVED = %d\nBLOCKED = %d\n"
            % (len(rows), len(rows) - dead, dead, moved,
               sum(1 for r in rows if r.get("blocked"))))
    open(OUT, "w", encoding="utf-8").write(b.getvalue())
    print("  wrote %s" % os.path.basename(OUT))
    for r in rows:
        if r["note"] or r["moved"]:
            print("    %-34s %s" % (r["county"],
                                    r["note"] or ("-> " + r["url"][:64])))


if __name__ == "__main__":
    main()
