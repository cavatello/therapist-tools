#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What San Francisco pays its behavioral health clinicians, from the city's file.

WHY THIS PASS EXISTS

`_dev/county_pay.py` reads the State Controller's county files and reports 55 of
California's 58 counties. San Francisco is one of the three missing, and it is
not under-counted - it is **absent**. There is no employer named San Francisco
anywhere in the county file, because San Francisco is a consolidated city and
county and files in the Controller's *cities* dataset instead.

That is not a footnote. San Francisco employs around 440 people in the clinical
titles this site cares about, which would place it among the largest public
behavioral health employers in the Bay Area, and the page said nothing about it.

WHY THIS DOES NOT JUST READ THE CONTROLLER'S CITY FILE

The Controller's bulk download sits behind Cloudflare and cannot be fetched by a
script - the county files are placed in `_dev/_cache` by hand. San Francisco
publishes the same information itself, through DataSF, over an open API with no
key. That is a better source for this one employer: it is first-party, it is
refreshed continuously, and it can be re-run by anybody.

THE MEASURE IS NOT THE SAME AS THE COUNTY TABLE'S, AND THAT IS THE WHOLE PROBLEM

The county page leads with the **published salary range** - what each county
advertised for a position. San Francisco's compensation file does not carry a
published range at all. It carries what each person was actually paid.

So these two numbers cannot go in the same column, and this pass does not
pretend otherwise. It computes actual base salary for full-time staff, the page
gives San Francisco its own section, and the difference in basis is stated in
the same breath as the figure rather than in a footnote. Putting a derived
"range" for San Francisco into a table of published ranges would be the kind of
quiet apples-to-oranges that makes every other number on the page less
trustworthy.

FULL-TIME ONLY, AND WHY

Actual pay includes people who started in November, took leave, or worked half
a year, and their salaries drag a median down for reasons that have nothing to
do with what the job pays. Rows are kept only where the file records at least
1,800 paid hours. The county page's actual-wages column does NOT filter this
way, which is one more reason the two sit in separate sections.

PRIVACY

The source table carries an `employee_identifier` column containing individual
names. **This pass never selects that column**, so no name enters the
repository, the cache, or this container - the same discipline the DCA licensee
pass runs under, where the underlying file holds home addresses for 165,000
people and only counts are ever committed.
"""
import json, os, statistics as st, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sf_pay_data.py")
CHECKED = "12 August 2026"
RES = "https://data.sfgov.org/resource/88g8-5mnd.json"
PAGE = "https://data.sfgov.org/City-Management-and-Ethics/Employee-Compensation/88g8-5mnd"
YEARS = ("2023", "2024", "2025")
FT_HOURS = 1800
FLOOR = 20000

# The city's own job titles, read off its classification list. Deliberately
# enumerated rather than pattern-matched: "Counselor, Juvenile Hall",
# "Counselor, Family Court Svc" and "Environmental Health Inspector" all match
# a sensible-looking regular expression and none of them is a clinician.
TITLES = [
    "Behavioral Health Clinician",
    "Sr Behavioral Health Clinicn",
    "Clinical Psychologist",
    "Behavioral Health Team Leader",
    "Marriage, Family & Child Cnslr",
]

# Titles considered and deliberately left out, so the next person does not have
# to rediscover why. Each one matches a keyword search for clinical work and is
# not a licensed-therapist role in San Francisco's classification.
EXCLUDED = [
    ("Counselor, Juvenile Hall", "custody staff in the juvenile justice system, "
                                 "not a clinical classification"),
    ("Counselor, Family Court Svc", "court mediation, under the Superior Court"),
    ("Environmental Health Inspector", "matches on &ldquo;health&rdquo; and is "
                                       "an inspector"),
    ("Sr Employee Asst Counselor", "internal employee assistance, two people"),
    ("Rehabilitation Counselor", "vocational rehabilitation, one person"),
]


def fetch(select, where, limit=50000, tries=4):
    u = "%s?$select=%s&$where=%s&$limit=%d" % (
        RES, urllib.parse.quote(select), urllib.parse.quote(where), limit)
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(u, timeout=120))
        except Exception as e:
            print("  retry %d: %s" % (i + 1, e))
            time.sleep(3 * (i + 1))
    sys.exit("DataSF did not answer after %d tries. This pass needs the "
             "network; %s is the committed artifact and the builder reads "
             "that." % (tries, os.path.basename(OUT)))


def pctile(v, p):
    return int(v[min(len(v) - 1, int(len(v) * p))]) if v else None


def main():
    print("San Francisco clinical pay, from the city's own compensation file")
    inlist = ",".join("'%s'" % t.replace("'", "''") for t in TITLES)
    years, titles = {}, []

    for y in YEARS:
        rows = fetch("job,salaries,hours,department",
                     "year_type='Calendar' AND year='%s' AND job in(%s)"
                     % (y, inlist))
        if not rows:
            sys.exit("no rows for %s - the job titles or the dataset layout "
                     "have changed. Check %s." % (y, PAGE))
        ft = [r for r in rows
              if float(r.get("hours") or 0) >= FT_HOURS
              and float(r.get("salaries") or 0) > FLOOR]
        sal = sorted(float(r["salaries"]) for r in ft)
        years[y] = {"n_all": len(rows), "n_ft": len(ft),
                    "median": int(st.median(sal)) if sal else None,
                    "p10": pctile(sal, .10), "p90": pctile(sal, .90),
                    "top": int(sal[-1]) if sal else None}
        print("  %s  %d people in these titles, %d full-time, median base $%s"
              % (y, len(rows), len(ft),
                 format(years[y]["median"], ",d")))

        if y == YEARS[-1]:
            by = {}
            for r in ft:
                by.setdefault(r["job"], []).append(float(r["salaries"]))
            for j, v in sorted(by.items(), key=lambda kv: -len(kv[1])):
                v = sorted(v)
                titles.append({"job": j, "n": len(v),
                               "median": int(st.median(v)),
                               "p10": pctile(v, .10), "p90": pctile(v, .90)})
            deps = {}
            for r in ft:
                deps[r["department"]] = deps.get(r["department"], 0) + 1
            top_dep = max(deps.items(), key=lambda kv: kv[1])

    latest = YEARS[-1]
    if years[latest]["n_ft"] < 100:
        sys.exit("only %d full-time rows in %s - that is too few for a city "
                 "this size and means the titles have been renamed"
                 % (years[latest]["n_ft"], latest))

    b = ['#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n',
         '"""San Francisco clinical pay. WRITTEN BY _dev/sf_pay.py.\n\n',
         "San Francisco is absent from the State Controller's COUNTY file - it\n",
         "is a consolidated city and county and files in the cities dataset -\n",
         "so `_dev/county_pay.py` cannot see it. These figures come from the\n",
         "city's own compensation file over DataSF, and are ACTUAL BASE SALARY\n",
         "for full-time staff, not a published salary range. They are not\n",
         "comparable with `county_pay_data.COUNTIES` and must never be put in\n",
         'the same table.\n"""\n\n']
    b.append("CHECKED = %r\nSOURCE = %r\nPAGE = %r\n" % (CHECKED, RES, PAGE))
    b.append("YEARS = %r\nFT_HOURS = %d\n" % (list(YEARS), FT_HOURS))
    b.append("TITLES = %r\n" % TITLES)
    b.append("EXCLUDED = %r\n" % EXCLUDED)
    b.append("YEAR_TOTALS = %r\n" % years)
    b.append("BY_TITLE = %r\n" % titles)
    b.append("TOP_DEPARTMENT = %r\n" % (top_dep,))
    open(OUT, "w", encoding="utf-8").write("".join(b))

    print("  %s employs %d of the %d in %s"
          % (top_dep[0], top_dep[1], years[latest]["n_ft"], latest))
    print("  wrote %s - %d titles, %d years"
          % (os.path.basename(OUT), len(titles), len(YEARS)))


if __name__ == "__main__":
    main()
