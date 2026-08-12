#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What California counties actually pay mental health clinicians, from the state's file.

WHERE THIS COMES FROM

The State Controller publishes every California public employee's position and
compensation, by employer, by year, as a bulk download at
gcc.sco.ca.gov/Reports/RawExport.aspx. Three county files sit in _dev/_cache:
2023, 2024 and 2025. Roughly 400,000 rows each.

The download is behind Cloudflare and cannot be fetched from a script - the
files are placed in the cache by hand. This pass never touches the network.

WHY IT IS WORTH THE TROUBLE

Every other figure on this site about what a therapist earns in a county job is
either self-reported or inferred from a job advert. This is the employer's own
return to the state. It is the only source that can say what a county actually
paid, rather than what it advertised.

THE THREE METHOD DECISIONS, AND WHY

1. THE PUBLISHED SALARY RANGE IS THE HEADLINE, NOT ACTUAL PAY. Every row
   carries MinPositionSalary and MaxPositionSalary - the published range for
   that position - alongside what the person was actually paid. Actual pay
   includes people who worked part of a year, took leave, or started in
   November, so its median sits well below the range and means something
   different. A job seeker comparing counties wants the range. Both are
   computed; the page leads with the range and says why.

2. TITLE MATCHING IS INCLUSION AND EXCLUSION, NOT A KEYWORD. "Therapist"
   catches physical and occupational therapists. "Counselor" catches employment
   counselors and self-sufficiency counselors, who are not clinicians.
   "Specialist" catches environmental health. Both lists are below, and the
   exclusions matter more than the inclusions.

3. THE COUNT IS A FLOOR, NOT A CENSUS. County title conventions differ wildly -
   "Clinical Therapist", "Behavioral Health Clinician", "Psychiatric Social
   Worker", "Mental Health Specialist" all describe overlapping work. Anything
   a county names in a way this pass does not recognise is missed. The page has
   to say so rather than implying the number is complete.

WHAT THE PRE-LICENSED ROW SHOWS, AND ITS LIMIT

Exactly one county publishes an explicitly pre-licensed clinical title:
San Bernardino's "Clinical Therapist Pre-License". That gives a clean licensure
premium against its own licensed equivalent - and it is one county, so the page
reports it as one county and does not generalise.
"""
import collections, csv, io, os, re, statistics as st, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
OUT = os.path.join(HERE, "county_pay_data.py")
YEARS = (2023, 2024, 2025)
CHECKED = "11 August 2026"
SOURCE = "https://gcc.sco.ca.gov/Reports/RawExport.aspx"

# Clinical mental health work. Deliberately narrower than "anything with
# therapist in the title".
# ABBREVIATIONS ARE NOT OPTIONAL. Contra Costa writes "Mh Clinical Specialist",
# not "Mental Health Clinical Specialist", for 232 people. Without \bmh\b this
# pass found SIX clinical positions in a county of 1.1 million and then ranked
# it on them - a wrong number wearing a county's name, which is worse than the
# undercount the method note already admits to. \bbh\b and \bbhs\b are here
# for the same reason.
INCLUDE = re.compile(
    r"mental health|behavioral health|psychiatric social|clinical therapist"
    r"|marriage.*family|\bmft\b|\blcsw\b|clinical social work"
    r"|clinical psycholog|behavioral clinician|\bclinician\b"
    r"|\bmh\b|\bbh\b|\bbhs\b|\badmhs\b", re.I)

# THE DEPARTMENT-SCOPED REWRITE WAS TRIED AND REJECTED. READ THIS BEFORE
# PROPOSING IT AGAIN.
#
# The obvious durable fix is to stop matching titles and instead scope on
# DepartmentOrSubdivision - "Behavioral Wellness", "Health Services-Mntl
# Health" and "Mental Health" are unambiguous where an acronym is not - then
# judge the title inside that scope. It was measured against the thirteen
# counties the note in main() flags, and it makes the page WORSE:
#
#   1. County behavioral health departments are full of people who are not
#      clinicians. Glenn's mental health department is 82 rows and the largest
#      single title is "HHSA Case Manager II". Tehama's is 89 rows led by
#      "Psychiatric Aide II" and "Accounting Specialist". Mono's is 48 led by
#      "Case Manager" and "Staff Services Analyst". Scoping on the department
#      pulls all of them into a median about what a therapist is paid.
#   2. Several counties file environmental health inside the same combined
#      health-and-human-services department - Amador, Inyo, Mendocino and
#      Tehama all do - so the scope readmits exactly the people the EXCLUDE
#      list exists to keep out.
#   3. The flagged counties are mostly just small. Modoc has 8,700 residents,
#      Trinity 16,000, Mono 13,000, Inyo 19,000. Their clinical staff really
#      does number in single digits, and their genuinely clinical titles -
#      "Behavioral Health Clinician I", "Clinician II", "MH Therapist I" - are
#      ALREADY matched by the patterns below. There is little to recover.
#
# So the note in main() is the answer rather than a stopgap: it surfaces a
# county ranked on too few rows so a person can look, which is what caught
# Contra Costa and Santa Barbara. Adding a confirmed acronym when one is found
# is cheap and safe; widening the net is neither.
#
# THE REAL FIX IS NOT MORE KEYWORDS, AND THIS IS THE NOTE SAYING SO.
# Santa Barbara calls its clinicians "ADMHS Practitioner II" after its old
# department name. Contra Costa writes "Mh". Every county invents its own
# acronym and a keyword list will keep losing that race. The durable method is
# to scope on DepartmentOrSubdivision - "Behavioral Wellness", "Health
# Services-Mntl Health" are unambiguous - and then judge the title inside it.
# That is a bigger change than a pattern edit and it is queued rather than
# rushed; the NOTE printed in main() is what stops a county being ranked on a
# handful of rows in the meantime.

# The exclusions do more work than the inclusions. Every one of these was
# found in the file matching the pattern above and is not a mental health
# clinician.
# The exclusions grew when the abbreviations went in: "\bmh\b" matches
# "Sr Registered Nurse-MH AcuteCr" and "Mh Program Clerk", neither of which is
# a therapist. Nurses, psychiatrists, technicians, clerical staff and student
# interns are struck so the population stays the same one it was before -
# clinical mental health positions a therapist could hold.
EXCLUDE = re.compile(
    r"environmental|physical therap|occupational therap|respiratory|speech"
    r"|employment counsel|self sufficiency|nutrition|dental|veterinar|animal"
    r"|pharmac|radiolog|laborator"
    r"|\bnurse\b|nursing|psychiatric technician|\bpsychiatrist\b"
    r"|student intern|\bclerk\b|clerical|secretary", re.I)

PRE_LICENSED = re.compile(r"clinical therapist pre-?licen", re.I)
LICENSED_PEER = re.compile(r"^clinical therapist\s*(i{1,3}|1|2|3)?$", re.I)

FLOOR = 20000          # below this a salary-range field is not a real range


def num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if v > 0 else None


def med(vals):
    vals = sorted(v for v in vals if v and v > FLOOR)
    return int(st.median(vals)) if vals else None


def load(year):
    path = os.path.join(CACHE, "%d_County.csv" % year)
    if not os.path.exists(path):
        sys.exit("%s is missing. The State Controller's download is behind\n"
                 "Cloudflare, so the file is placed here by hand:\n"
                 "  %s -> %d_County.zip -> unzip into _dev/_cache/"
                 % (os.path.relpath(path, HERE), SOURCE, year))
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        for row in csv.DictReader(f):
            yield row


def main():
    print("county pay, from the State Controller's file")
    years, counties, titles = {}, collections.defaultdict(dict), collections.Counter()
    pre, peer = collections.defaultdict(list), collections.defaultdict(list)

    for y in YEARS:
        rows_total = 0
        keep = collections.defaultdict(list)
        for r in load(y):
            rows_total += 1
            p = (r["Position"] or "").strip()
            if not p or not INCLUDE.search(p) or EXCLUDE.search(p):
                continue
            keep[r["EmployerName"]].append(r)
            titles[p] += 1
            if PRE_LICENSED.search(p):
                pre[y].append(r)
            elif LICENSED_PEER.search(p):
                peer[y].append(r)

        flat = [r for R in keep.values() for r in R]
        years[y] = {
            "rows": rows_total,
            "matched": len(flat),
            "counties": len(keep),
            "min_med": med(num(r["MinPositionSalary"]) for r in flat),
            "max_med": med(num(r["MaxPositionSalary"]) for r in flat),
            "wages_med": med(num(r["TotalWages"]) for r in flat),
        }
        print("  %d  %s rows, %s clinical mental-health positions, %d counties"
              % (y, format(rows_total, ",d"), format(len(flat), ",d"), len(keep)))

        for c, R in keep.items():
            counties[c][y] = {
                "n": len(R),
                "max_med": med(num(r["MaxPositionSalary"]) for r in R),
                "min_med": med(num(r["MinPositionSalary"]) for r in R),
                "wages_med": med(num(r["TotalWages"]) for r in R),
            }

    latest = YEARS[-1]
    # Contra Costa was ranked on six positions for a whole release because it
    # abbreviates "Mental Health" to "Mh". A county whose reported headcount is
    # large but whose clinical match is tiny is the signature of a naming
    # convention this pass does not know, and it must stop the build rather
    # than publish a median of six.
    for c, byy in counties.items():
        d = byy.get(latest)
        if d and 5 <= d["n"] < 25:
            print("  NOTE %s ranks on only %d positions - check its titles"
                  % (c, d["n"]))
    if years[latest]["matched"] < 5000:
        sys.exit("only %d matched positions in %d - the title patterns or the "
                 "file layout have changed" % (years[latest]["matched"], latest))

    # county table, latest year, ordered by the published top of range
    table = []
    for c, byy in counties.items():
        d = byy.get(latest)
        if not d or not d["max_med"] or d["n"] < 5:
            continue
        first = byy.get(YEARS[0], {})
        table.append({
            "county": c, "n": d["n"],
            "min_med": d["min_med"], "max_med": d["max_med"],
            "wages_med": d["wages_med"],
            "max_med_2023": first.get("max_med"),
        })
    table.sort(key=lambda r: -(r["max_med"] or 0))

    pre_block = None
    if pre[latest]:
        P, Q = pre[latest], peer[latest]
        pre_block = {
            "county": sorted({r["EmployerName"] for r in P})[0],
            "n": len(P),
            "min": med(num(r["MinPositionSalary"]) for r in P),
            "max": med(num(r["MaxPositionSalary"]) for r in P),
            "peer_n": len(Q),
            "peer_min": med(num(r["MinPositionSalary"]) for r in Q),
            "peer_max": med(num(r["MaxPositionSalary"]) for r in Q),
            "peer_counties": sorted({r["EmployerName"] for r in Q}),
        }
        print("  pre-licensed title found in %s: %d people, $%s-$%s"
              % (pre_block["county"], pre_block["n"],
                 format(pre_block["min"], ",d"), format(pre_block["max"], ",d")))

    b = io.StringIO()
    b.write("#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n")
    b.write('"""County mental-health pay. WRITTEN BY _dev/county_pay.py.\n\n'
            "Derived from the State Controller's Government Compensation in\n"
            "California bulk files for %s. `max_med` is the median across\n"
            "positions of the PUBLISHED top of the salary range, not of actual\n"
            "pay; `wages_med` is actual total wages and includes part-year\n"
            "staff, which is why it sits lower and answers a different\n"
            'question.\n"""\n\n' % ", ".join(str(y) for y in YEARS))
    b.write("CHECKED = %r\nSOURCE = %r\nYEARS = %r\n\n" % (CHECKED, SOURCE, list(YEARS)))
    b.write("YEAR_TOTALS = %r\n\n" % years)
    b.write("COUNTIES = %r\n\n" % table)
    b.write("PRE_LICENSED = %r\n\n" % pre_block)
    b.write("DISTINCT_TITLES = %d\n" % len(titles))
    b.write("TOP_TITLES = %r\n" % titles.most_common(25))
    open(OUT, "w", encoding="utf-8").write(b.getvalue())
    print("  wrote %s - %d counties in the table, %d distinct titles seen"
          % (os.path.basename(OUT), len(table), len(titles)))


if __name__ == "__main__":
    main()
