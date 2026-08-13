#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every place a California clinical supervisor list is supposed to be, fetched.

WHY THIS PASS EXISTS

The Board of Behavioral Sciences does not certify supervisors and publishes no
roster of them. It never has. So the question every registered associate asks
first - where do I find a supervisor - has no official answer, and what fills
the void is a scatter of chapter pages, one association list, two commercial
directories and a lot of dead domains that search engines still rank.

A page that just linked to all of them would be worse than nothing, because
several of the most-cited addresses do not resolve at all and two of the
chapters that carry them no longer exist. This pass fetches every candidate
and records what answered, so the page can say which lists are real on a date
rather than which lists were real when somebody last wrote a blog post.

WHAT IS RECORDED AND WHAT IS NOT

Status, final URL after redirects, and the entry count that the research pass
read off each source's own page. **No listing is retained.** These are other
people's membership directories; the site links to them and reports how big
they are, and reproducing them would be both a copyright problem and a
maintenance burden nobody wants. The counts are the finding - the coverage map
is wildly uneven and that is what the reader needs to know before spending an
evening on it.

THE 403 CONVENTION, SAME AS THE COUNTY PORTALS

A membership site answering 403 to a script is not a dead site; several of
these run bot protection that a browser sails through. Those are recorded as
reachable, with the code, exactly as `_dev/county_portals.py` does. A domain
that does not resolve at all is a different finding and is the one worth
publishing loudly.
"""
import json, os, socket, ssl, sys, time
import urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "supervisor_lists_data.py")
CHECKED = "12 August 2026"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/127.0 Safari/537.36")

# A site behind bot protection answers these to a script and renders normally
# in a browser. Recorded as reachable rather than dead - see the docstring.
REACHABLE_ERRORS = {401, 402, 403, 405, 406, 408, 409, 429, 500, 502, 503}

# kind: chapter | association | commercial | negative | dead
# n:    entries the research pass read off the source's own page, or None
# free: can a person browse it today without an account
LISTS = [
    # ---------------------------------------------------------- association
    dict(key="camft", kind="association", name="CAMFT Certified Supervisors",
         url="https://www.camft.org/Resources/CAMFT-Certified-Supervisors/Directory",
         n=302, ca=284, free=True,
         fields="Name, city, state",
         note="The only statewide list run by the profession itself. The "
              "contact column is empty for every row and there is no license "
              "type, no specialty and no indication whether anybody is taking "
              "supervisees, so it is a list of names to search for."),
    dict(key="aamft", kind="association", name="AAMFT Approved Supervisor search",
         url="https://www.aamft.org/AAMFT/web/Approved-Supervisor/Approved-Supervisor-Search.aspx",
         n=None, ca=None, free=True,
         fields="Search form",
         note="The page loads, and every search returns no content. Listing is "
              "opt-in and almost nobody has opted in, so it is a search box "
              "over an empty set rather than a directory."),

    # -------------------------------------------------------------- chapters
    dict(key="lacamft", kind="chapter", name="LA-CAMFT, Supervision Offered",
         url="https://www.lacamft.org/page-829807", n=314, ca=314, free=True,
         fields="Name, phone, address, city, free-text note",
         note="The largest chapter list in the state, filterable by about "
              "forty Los Angeles cities."),
    dict(key="ebcamft", kind="chapter", name="East Bay CAMFT Supervision Finder",
         url="https://ebcamft.org/supervision-finder", n=150, ca=150, free=True,
         fields="Name, phone, website, city, ZIP, supervision type",
         note="The best-built of them. It is the only chapter list that says "
              "whether a person offers individual, group or "
              "supervision-of-supervision, and flags CAMFT and AAMFT "
              "credentials."),
    dict(key="marincamft", kind="chapter", name="Marin CAMFT Supervisor Directory",
         url="https://marincamft.org/supervisor-directory", n=116, ca=116,
         free=True, fields="Name, phone, supervision type, certifications",
         note="Much larger than the county's population implies - it covers "
              "most of the North Bay."),
    dict(key="recamft", kind="chapter", name="Redwood Empire CAMFT",
         url="https://www.recamft.org/supervision-directory", n=99, ca=99,
         free=True, fields="Name, phone, address, city, supervision type, site",
         note="Sonoma and the North Coast. The chapter publishes the same list "
              "at two addresses in two layouts."),
    dict(key="occamft", kind="chapter", name="Orange County CAMFT",
         url="https://www.occamft.org/supervision-directory", n=63, ca=63,
         free=True, fields="Name, phone, website, address, supervision type",
         note="Orange County, and the only real list south of Los Angeles."),
    dict(key="cccamft", kind="chapter", name="Central Coast CAMFT",
         url="https://www.centralcoastcamft.org/supervision-directory/", n=39,
         ca=39, free=True,
         fields="Name, phone, website, address, supervision type",
         note="San Luis Obispo and Santa Maria."),
    dict(key="sgvcamft", kind="chapter", name="San Gabriel Valley CAMFT",
         url="https://www.sgvcamft.org/Supervision", n=30, ca=30, free=True,
         fields="Name, phone, website, address, city, supervision type",
         note="Overlaps heavily with the Los Angeles list."),
    dict(key="swrccamft", kind="chapter",
         name="Southwest Riverside County CAMFT",
         url="https://www.swrc-camft.org/supervision-directory", n=15, ca=15,
         free=True, fields="First name only, phone, website, address, type",
         note="Last names are withheld, which makes it hard to check anybody "
              "against the license lookup before calling."),
    dict(key="desertcamft", kind="chapter", name="Desert CAMFT",
         url="https://www.desert-camft.org/Supervision-Directory", n=4, ca=4,
         free=True, fields="Name, phone, website, address, supervision type",
         note="Live, and functionally empty."),

    # ------------------------------------------------------------ commercial
    dict(key="psychtoday", kind="commercial",
         name="Psychology Today, clinical supervision category",
         url="https://www.psychologytoday.com/us/therapists/california?category=supervision-services",
         n=3875, ca=3875, free=True,
         fields="Name, license, city, ZIP, phone, bio, in-person or online",
         note="By a wide margin the largest list with contact details on it, "
              "and the category is self-declared and unverified - a paid "
              "profile with a box ticked. It is a starting list, not a "
              "credential."),
    dict(key="zencare", kind="commercial", name="Zencare, clinical supervision",
         url="https://zencare.co/us/california/therapists/specialty/clinical-supervision",
         n=49, ca=49, free=True,
         fields="Name, credentials, location, format, next consult time",
         note="Small, and the only source in California that shows live "
              "availability rather than a static roster."),
    dict(key="csd", kind="commercial", name="Clinical Supervision Directory",
         url="https://clinicalsupervisiondirectory.com/licensed-professional-counselor-supervisor-directory/",
         n=None, ca=None, free=False,
         fields="Behind a free signup",
         note="Nationwide and counselor-weighted. It carries an "
              "&ldquo;accepting supervisees&rdquo; field, which almost nothing "
              "else does, and you cannot see it without an account."),
    dict(key="motivo", kind="commercial", name="Motivo Health",
         url="https://motivohealth.com/clinical-supervision/california",
         n=None, ca=None, free=False,
         fields="Matching service, no browsable profiles",
         note="Paid matching, and increasingly sold to employers rather than "
              "to individuals. An associate cannot browse it."),
]

# Checked, and confirmed to publish no supervisor list at all. This half of the
# work is the half that saves somebody an evening, so it ships as data too.
NEGATIVE = [
    ("California Board of Behavioral Sciences",
     "https://www.bbs.ca.gov/licensees/supervisor.html",
     "Publishes the rules and the forms. The Board does not certify "
     "supervisors, keeps no roster, and the license lookup has no supervisor "
     "flag."),
    ("NASW California Chapter", "https://naswca.org/",
     "No LCSW supervisor directory. Other states' NASW chapters run one; "
     "California does not."),
    ("CALPCC", "https://www.calpcc.org/approved-supervisors",
     "Explains how to become an approved supervisor. There is no list of "
     "them, which leaves APCCs the worst served of the three registrations."),
    ("CalSWEC", "https://socialwelfare.berkeley.edu/",
     "Field placement for MSW students, not post-degree supervision."),
    ("TherapyDen", "https://www.therapyden.com/",
     "Has no clinical supervision filter at all."),
    ("Open Path Collective", "https://openpathcollective.org/",
     "A low-fee directory for clients. No supervisor list."),
    ("Alma and Headway", "https://helloalma.com/",
     "Insurance credentialing networks that require an independent license. "
     "Neither supplies a supervisor or runs a directory of them."),
    ("CounselingCalifornia", "https://www.counselingcalifornia.com/",
     "CAMFT's directory for clients. No supervisor filter."),
    ("CalMHSA statewide clinical supervision",
     "https://calmhsa.org/clinical-supervision/",
     "Buys remote supervision in bulk and sells it to counties, not to "
     "people. Sixteen counties take part, and staff reach it through their "
     "employer."),
]

# Chapters checked that have no supervision directory. Names only - the value
# is knowing not to look.
NO_CHAPTER_LIST = [
    "Inland Empire", "Long Beach South Bay", "Monterey County",
    "Sacramento Valley", "San Diego", "San Diego North County",
    "San Fernando Valley", "San Francisco", "Santa Barbara",
    "Santa Clara Valley", "Santa Cruz County", "Ventura County",
]

# Addresses that search engines still rank and that no longer exist. Publishing
# these is the point: a reader who searches this question is sent to them.
DEAD = [
    ("Redding Regional CAMFT", "rrccamft.org",
     "The domain expired and was resold; it now redirects to an unrelated "
     "commercial site. CAMFT's own chapter list still points at it."),
    ("Sierra Foothills CAMFT", "sierrafoothillscamft.com",
     "Does not resolve. Also still on CAMFT's chapter list."),
    ("supervisiondirectory.com", "supervisiondirectory.com",
     "Does not resolve, and is still indexed."),
]


def fetch(url, tries=2):
    """Returns (status, final_url, note). Never raises."""
    for i in range(tries):
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9"})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.getcode(), r.geturl(), ""
        except urllib.error.HTTPError as e:
            return e.code, url, "http error"
        except urllib.error.URLError as e:
            reason = str(getattr(e, "reason", e))
            if isinstance(getattr(e, "reason", None),
                          (socket.gaierror,)) or "Name or service" in reason \
                    or "nodename nor servname" in reason:
                return 0, url, "does not resolve"
            if i == tries - 1:
                return -1, url, reason[:80]
        except (socket.timeout, TimeoutError):
            if i == tries - 1:
                return -2, url, "timed out"
        except ssl.SSLError as e:
            return -3, url, str(e)[:80]
        except Exception as e:
            if i == tries - 1:
                return -4, url, str(e)[:80]
        time.sleep(2 * (i + 1))
    return -1, url, "unknown"


def main():
    print("supervisor lists, fetched")
    rows = []
    for spec in LISTS:
        code, final, note = fetch(spec["url"])
        ok = 200 <= code < 300 or code in REACHABLE_ERRORS
        r = dict(spec)
        r["status"] = code
        r["final"] = final
        r["reachable"] = ok
        r["fetch_note"] = note
        rows.append(r)
        print("  %-13s %4s  %s%s" % (spec["key"], code,
                                     "ok " if ok else "UNREACHABLE ",
                                     note))

    # "Dead" has two shapes and they are not the same finding. A domain that
    # does not resolve is gone. A domain that resolves and lands somewhere
    # else entirely was sold, and that is the more dangerous one, because a
    # reader arrives at a working page and assumes the chapter moved.
    dead_rows = []
    for name, host, why in DEAD:
        try:
            socket.getaddrinfo(host, 443)
            resolves = True
        except Exception:
            resolves = False
        landed = ""
        if resolves:
            code, final, _ = fetch("https://" + host)
            base = final.split("/")[2].replace("www.", "") if "//" in final \
                else ""
            if base and not base.endswith(host.replace("www.", "")):
                landed = base
        dead_rows.append(dict(name=name, host=host, why=why,
                              resolves=resolves, landed=landed))
        print("  dead? %-28s %s%s"
              % (host, "resolves" if resolves else "does not resolve",
                 " -> " + landed if landed else ""))

    neg_rows = []
    for name, url, why in NEGATIVE:
        code, final, note = fetch(url)
        neg_rows.append(dict(name=name, url=url, why=why, status=code,
                             reachable=200 <= code < 300
                             or code in REACHABLE_ERRORS))
        print("  neg   %-42s %4s" % (name[:42], code))

    unreachable = [r["key"] for r in rows if not r["reachable"]]
    if unreachable:
        print("\nNOTE: %d list(s) did not answer and the builder will not "
              "publish them: %s" % (len(unreachable), ", ".join(unreachable)))

    b = ['#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n',
         '"""Where a California supervisor list actually is. WRITTEN BY '
         '_dev/supervisor_lists.py.\n\n',
         "Counts are what each source reports on its own page. No listing from\n",
         "any of these directories is stored here or published on the site -\n",
         "they are other people's membership lists. The finding is the\n",
         "coverage map, not the names.\n\"\"\"\n\n"]
    b.append("CHECKED = %r\n" % CHECKED)
    b.append("LISTS = %r\n" % rows)
    b.append("NEGATIVE = %r\n" % neg_rows)
    b.append("NO_CHAPTER_LIST = %r\n" % NO_CHAPTER_LIST)
    b.append("DEAD = %r\n" % dead_rows)
    open(OUT, "w", encoding="utf-8").write("".join(b))
    print("\n  wrote %s - %d lists, %d negatives, %d dead"
          % (os.path.basename(OUT), len(rows), len(neg_rows), len(dead_rows)))


if __name__ == "__main__":
    main()
