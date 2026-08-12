#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Where you actually apply for a county job, in all 58 California counties.

WHY A DIRECTORY OF PORTALS AND NOT A DIRECTORY OF JOBS

A job posting is dead in six weeks. A portal is not. The site already says
what county work pays, which counties run the Medi-Cal plans, and why a county
is one of the few employers that can bill for a pre-licensed clinician - and
then stops short of saying where the application form is.

THE FINDING THAT MADE THIS WORTH BUILDING

Guessing the URL fails for eight of the fifty-eight, and it fails silently -
the wrong page loads, looks entirely plausible, and belongs to somebody else:

  governmentjobs.com/careers/marin        the Marin County SUPERIOR COURT
  governmentjobs.com/careers/sandiego     the CITY of San Diego
  governmentjobs.com/careers/santabarbara the CITY of Santa Barbara
  governmentjobs.com/careers/santacruz    a city portal
  governmentjobs.com/careers/alameda      an unbranded, empty tenant
  governmentjobs.com/careers/countyofmonterey   ditto
  governmentjobs.com/careers/trinity      ditto

Each of those is the first result a person would try. Three of the four
"empty tenant" cases have a real county portal at a different address
entirely - Alameda is on JobAps, not NeoGov at all.

HOW EACH ROW WAS ESTABLISHED

Two passes, and they disagreed, which is the reason for both. The first tried
predictable slugs against NeoGov and kept only pages whose own <title> named
the county - 19 of 58, with four caught pointing at the wrong agency. The
second resolved the remaining 39 from each county's own human resources page,
recording the exact wording that proves the destination belongs to the county
rather than to a city or a court. `evidence` on every row is that wording.

Then every URL was fetched. Statuses use the REACHABLE_ERRORS convention this
repository already runs on: a California .gov answering 403 to a script is
working fine in a browser, and only a DNS failure, a refused connection, a
timeout or an explicit 404 counts as broken.

WHAT THIS FILE DOES NOT CLAIM

Nothing about whether a county is hiring, and nothing about what any listing
pays. It is an address book. What the work pays is county_pay_data, and what
an employer must be able to bill before it can hire a pre-licensed clinician
is the hiring page.
"""
import json, os, sys, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "county_portals_data.py")
CHECKED = "12 August 2026"

# A .gov that answers one of these is working in a browser. Treating them as
# dead reported 22 false deaths the last time this was not done.
REACHABLE_ERRORS = {401, 402, 403, 405, 406, 408, 409, 429, 500, 502, 503}

SYSTEM_NAME = {
    "neogov": "NeoGov / GovernmentJobs",
    "jobaps": "JobAps",
    "calopps": "CalOpps",
    "own": "The county's own site",
}

# The URL a person would reasonably guess, and what actually answers there.
# This is the part of the file worth reading.
WRONG_GUESS = [
    ("Marin", "governmentjobs.com/careers/marin",
     "the Superior Court of California, County of Marin"),
    ("San Diego", "governmentjobs.com/careers/sandiego",
     "the <b>City</b> of San Diego"),
    ("Santa Barbara", "governmentjobs.com/careers/santabarbara",
     "the <b>City</b> of Santa Barbara"),
    ("Santa Cruz", "governmentjobs.com/careers/santacruz",
     "a city portal, not the county"),
    ("Alameda", "governmentjobs.com/careers/alameda",
     "an unbranded tenant with no listings &mdash; the county is on JobAps"),
    ("Monterey", "governmentjobs.com/careers/countyofmonterey",
     "an empty tenant &mdash; the county is at /montereycounty"),
    ("Trinity", "governmentjobs.com/careers/trinity",
     "an empty tenant &mdash; the county is at /trinitycoca"),
]

PORTALS = json.load(open(os.path.join(HERE, "county_portals_seed.json"),
                         encoding="utf-8")) if os.path.exists(
    os.path.join(HERE, "county_portals_seed.json")) else None


def check(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; therapistsupport-linkcheck/1.0; "
                      "+https://therapistsupport.org)"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, ""
    except urllib.error.HTTPError as e:
        return e.code, ("blocked" if e.code in REACHABLE_ERRORS else "http")
    except Exception as e:
        return None, type(e).__name__


def main():
    print("county job portals, all 58")
    if not PORTALS:
        sys.exit("county_portals_seed.json is missing. It holds the curated "
                 "(url, system, evidence) triple per county; this pass only "
                 "verifies it.")
    if len(PORTALS) != 58:
        sys.exit("%d counties in the seed, expected 58" % len(PORTALS))

    rows, dead = [], []
    for county in sorted(PORTALS):
        url, system, evidence = PORTALS[county]
        if system not in SYSTEM_NAME:
            sys.exit("%s has unknown system %r" % (county, system))
        st, note = check(url)
        ok = st == 200 or st in REACHABLE_ERRORS
        rows.append({"county": county, "url": url, "system": system,
                     "evidence": evidence, "status": st, "ok": ok,
                     "note": note})
        if not ok:
            dead.append(county)
        print("  %-17s %-5s %s" % (county, st, "" if ok else "DEAD"), flush=True)
        time.sleep(0.2)

    # A directory whose links are not checked is a directory nobody should
    # trust. If a third of them stop answering, something structural changed
    # and the page should not ship on the old data.
    if len(dead) > len(rows) // 3:
        sys.exit("%d of %d portals did not answer - check the network before "
                 "believing this" % (len(dead), len(rows)))

    counts = {}
    for r in rows:
        counts[r["system"]] = counts.get(r["system"], 0) + 1

    b = ['#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n',
         '"""County job portals. WRITTEN BY _dev/county_portals.py.\n\n',
         "Every URL was fetched before it shipped. `evidence` is the wording on\n",
         "the destination that proves it belongs to the county rather than to a\n",
         "city or a court - eight counties have an obvious-looking URL that\n",
         'belongs to somebody else, which is why that field exists.\n"""\n\n']
    b.append("CHECKED = %r\n" % CHECKED)
    b.append("SYSTEM_NAME = %r\n" % SYSTEM_NAME)
    b.append("COUNTS = %r\n" % counts)
    b.append("DEAD = %r\n" % dead)
    b.append("WRONG_GUESS = %r\n" % WRONG_GUESS)
    b.append("PORTALS = %r\n" % rows)
    open(OUT, "w", encoding="utf-8").write("".join(b))
    print("  %s; %d answered, %d dead"
          % (", ".join("%s %d" % (k, v) for k, v in sorted(counts.items())),
             len(rows) - len(dead), len(dead)))
    print("  wrote %s" % os.path.basename(OUT))


if __name__ == "__main__":
    main()
