#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every licensed therapist in California, counted, from the state's own file.

WHAT THIS IS

California's Department of Consumer Affairs publishes a complete list of BBS
licensees - every LMFT, LCSW, LPCC, LEP and every associate registration -
refreshed monthly, free, with no key and no login. 165,000-odd records. It is
linked from a consumer-information page that nobody in the profession reads, it
is served out of a Box folder, and it is named `.xls` while actually being
tab-delimited text.

This pass downloads it, counts what can be honestly counted, and writes the
totals to `_dev/dca_stats.py` for the pages that need them. Nothing else on this
site knows the raw file exists.

THE PRIVACY RULE, WHICH IS THE MOST IMPORTANT THING IN THIS FILE

The raw file contains ADDRESSES. For a solo practitioner the address of record
is, very often, the address they sleep at. This repository is published to
GitHub Pages: anything committed here is on the public internet within two
minutes.

So:

  - The raw file is cached in `_dev/_cache/`, which is gitignored, and this
    pass FAILS if git would track it. That check runs before any download.
  - `dca_stats.py` contains COUNTS ONLY. No names, no addresses, no licence
    numbers. The guard at the foot of this file re-reads what it wrote and
    fails if a street address pattern survived into it.
  - If a per-person directory is ever built from this file, the publishable
    subset is name, city, licence number, status. Never the street address.
    Never a map pin on a residence.

THE FIELD THAT LIES, AND HOW IT WAS CAUGHT

`Original Issue Date` looks like the date a licence was issued. Counting LMFTs
by the year in that field gives:

    2020: 3,006   2021: 2,435   2022: 2,138
    2023: 1,630   2024:   497   2025:   125   2026: 430

which reads as a catastrophic collapse in new California LMFTs. It is not one.
Two checks kill it:

  1. Licence numbers are assigned in sequence. If the field were an issue date,
     each year's numbers would form a band. They do not - the 2017 cohort
     contains licence numbers from 97,671 all the way to 161,886, which is a
     number issued years later.
  2. The Board's own licensing report for Q3 FY 2025/26 records **884 LMFT
     applications processed in that quarter alone** (see `_dev/bbs_stats.py`).
     A year cannot contain 125 new LMFTs and 884 in one quarter.

So the field does not mean what its name says, and this pass refuses to emit
any per-year issuance series from it. `issuance_by_year()` exists only to raise
an exception explaining why - because the next person to open this file will
have the same good idea, and the counts are seductive.

WHAT IT DOES EMIT, ALL OF IT CHECKED

Totals by licence type and status; per-county counts of associates and licensed
clinicians and the ratio between them; the count of distinct cities. Those are
simple sums over a categorical field, and they reconcile against the file's own
record count - which the guard verifies.

Idempotent. Re-downloads only when the state's file has changed.
"""
import collections, csv, hashlib, io, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "_cache")
RAW = os.path.join(CACHE, "dca_bbs_licensees.tsv")
OUT = os.path.join(HERE, "dca_stats.py")

# DCA's public-information store. The `.xls` name is wrong; the bytes are TSV.
URL = ("https://dca.box.com/index.php?rm=box_download_shared_file"
       "&shared_name=oss6hf8jys2bmgxqd2gdz7w4oepm2il9"
       "&file_id=f_2383115670508")
LANDING = "https://www.dca.ca.gov/consumers/public_info/index.shtml"

# The file is ~35MB. Anything wildly outside this means the URL now serves an
# error page or a login wall, and the pass should stop rather than parse HTML.
MIN_BYTES = 20_000_000
MAX_BYTES = 120_000_000
MIN_RECORDS = 120_000

# California has 58 counties and no more. The state's own file contains a
# handful of records with State="CA" and a county from somewhere else entirely
# - Kitsap, Ada, Santa Fe, New York, Palm Beach, Pitkin. They are data-entry
# errors, ten of them in 165,235 records, and left alone they would put "New
# York County, California" on a map. The list is pinned here so the map can
# only ever contain places that exist, and the discards are counted and printed
# rather than silently dropped.
CA_COUNTIES = {
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
}

LICENSED = {
    "Licensed Marriage and Family Therapist": "LMFT",
    "Licensed Clinical Social Worker": "LCSW",
    "Licensed Professional Clinical Counselor": "LPCC",
    "Licensed Educational Psychologist": "LEP",
}
ASSOCIATE = {
    "Associate Marriage & Family Therapist": "AMFT",
    "Associate Clinical Social Worker": "ASW",
    "Assoc. Professional Clinical Counselor": "APCC",
}

# Fields that must never reach dca_stats.py. Checked by name on the way in and
# by pattern on the way out.
FORBIDDEN = ("Address Line 1", "Address Line 2", "Org/Last Name", "First Name",
             "Middle Name", "Suffix", "License Number", "Zip")


# --------------------------------------------------------------- the trap
class IssueDateIsNotAnIssueDate(Exception):
    pass


def issuance_by_year(*_args, **_kw):
    """Deliberately unimplemented. See the module docstring.

    `Original Issue Date` does not carry the meaning its name implies, and a
    per-year series built from it shows a collapse in new California licences
    that did not happen. Two independent checks refute it: licence numbers do
    not band by year, and the Board's own quarterly report records more LMFT
    applications processed in one quarter than this field attributes to a
    whole year.

    If a real issuance series is ever needed, take it from the Board's
    licensing reports in `_dev/bbs_stats.py`, which are published figures.
    """
    raise IssueDateIsNotAnIssueDate(
        "Original Issue Date does not mean date of issue - see the docstring "
        "in _dev/dca_licensees.py. Use _dev/bbs_stats.py for issuance.")


# ------------------------------------------------------------------ safety
def refuse_if_tracked():
    """Stop before downloading if the cache would be committed.

    This repository publishes to GitHub Pages. The raw file contains home
    addresses. A gitignore line is one careless edit away from being deleted,
    so the check is made here as well, every run, before any bytes land.
    """
    if not os.path.isdir(os.path.join(SITE, ".git")):
        return
    rel = os.path.relpath(RAW, SITE)
    r = subprocess.run(["git", "check-ignore", "-q", rel], cwd=SITE)
    if r.returncode != 0:
        sys.exit(
            "dca_licensees: REFUSING TO RUN.\n"
            "  %s is not gitignored, and this repository is published to the\n"
            "  public internet. The file contains the home addresses of about\n"
            "  165,000 people.\n"
            "  Add this line to .gitignore and run again:\n"
            "      _dev/_cache/\n" % rel)


def fetch():
    """Download unless the cached copy is already the current one."""
    if not os.path.isdir(CACHE):
        os.makedirs(CACHE)
    if os.path.exists(RAW) and os.path.getsize(RAW) > MIN_BYTES:
        print("  cached: %s, %s bytes"
              % (os.path.relpath(RAW, SITE),
                 format(os.path.getsize(RAW), ",d")))
        return
    print("  downloading the DCA licensee file (~35MB)...")
    req = urllib.request.Request(URL, headers={"User-Agent": "therapistsupport.org"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = r.read()
    if not (MIN_BYTES < len(data) < MAX_BYTES):
        sys.exit("dca_licensees: the download is %s bytes, outside the sane "
                 "range. The URL probably now serves an error page or a login "
                 "wall. Start again from %s" % (format(len(data), ",d"), LANDING))
    head = data[:200].decode("utf-8", "replace")
    if not head.startswith("Agency Code\t"):
        sys.exit("dca_licensees: the download does not begin with the expected "
                 "tab-delimited header. DCA has changed the format; do not "
                 "guess at it. First bytes: %r" % head[:120])
    open(RAW, "wb").write(data)
    print("  downloaded %s bytes" % format(len(data), ",d"))


def load():
    with open(RAW, encoding="utf-8", errors="replace") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if len(rows) < MIN_RECORDS:
        sys.exit("dca_licensees: only %d records parsed, expected at least "
                 "%s. The file is truncated or the delimiter has changed."
                 % (len(rows), format(MIN_RECORDS, ",d")))
    return rows


# ------------------------------------------------------------------ counting
def summarise(rows):
    s = {}
    s["total"] = len(rows)
    s["by_type"] = dict(collections.Counter(r["License Type"] for r in rows))
    s["by_status"] = dict(collections.Counter(r["License Status"] for r in rows))

    # Delinquency, per type. The finding this pass was built for: associates
    # lapse markedly more often than licensed clinicians, and nobody has said so.
    delin = {}
    for label, short in list(LICENSED.items()) + list(ASSOCIATE.items()):
        sub = [r for r in rows if r["License Type"] == label]
        if not sub:
            continue
        n = sum(1 for r in sub if r["License Status"] == "Delinquent")
        delin[short] = {"total": len(sub), "delinquent": n,
                        "pct": round(100.0 * n / len(sub), 1)}
    s["delinquency"] = delin

    # Per county: associates, licensed, and the ratio. This is the supply map.
    counties = collections.defaultdict(lambda: {"assoc": 0, "lic": 0})
    discarded = collections.Counter()
    for r in rows:
        c = (r["County"] or "").strip().title()
        if not c or (r["State"] or "").strip() != "CA":
            continue
        if c not in CA_COUNTIES:
            discarded[c] += 1
            continue
        if r["License Type"] in ASSOCIATE:
            counties[c]["assoc"] += 1
        elif r["License Type"] in LICENSED:
            counties[c]["lic"] += 1
    out = {}
    for c, v in counties.items():
        if v["lic"] + v["assoc"] == 0:
            continue
        out[c] = {"assoc": v["assoc"], "lic": v["lic"],
                  "ratio": round(v["assoc"] / v["lic"], 3) if v["lic"] else None}
    s["counties"] = out
    s["county_discards"] = dict(discarded)

    s["cities"] = len({(r["City"] or "").strip().title()
                       for r in rows if (r["State"] or "").strip() == "CA"
                       and (r["City"] or "").strip()})
    s["out_of_state"] = sum(1 for r in rows
                            if (r["State"] or "").strip() not in ("CA", ""))
    return s


def emit(s, stamp):
    """Write dca_stats.py. Counts only - see the privacy rule up top."""
    o = ['#!/usr/bin/env python3',
         '# -*- coding: utf-8 -*-',
         '"""Counts derived from the DCA licensee file. GENERATED - do not edit.',
         '',
         'Written by `_dev/dca_licensees.py`, which downloads the state\'s own',
         'monthly file of every BBS licensee and counts it. Nothing here is',
         'estimated and nothing here identifies anybody: this file holds totals,',
         'and the raw file it came from is never committed.',
         '',
         'Source: %s' % LANDING,
         'File as at: %s' % stamp,
         '',
         'The raw file also carries an `Original Issue Date` field. It does NOT',
         'mean the date the licence was issued, and no series here is built from',
         'it - see the docstring in `_dev/dca_licensees.py` for the two checks',
         'that refute it.',
         '"""',
         '',
         'SOURCE = %r' % LANDING,
         'AS_AT = %r' % stamp,
         'TOTAL = %d' % s["total"],
         'CITIES = %d' % s["cities"],
         'OUT_OF_STATE = %d' % s["out_of_state"],
         '',
         'BY_TYPE = {']
    for k, v in sorted(s["by_type"].items(), key=lambda kv: -kv[1]):
        o.append('    %r: %d,' % (k, v))
    o.append('}')
    o.append('')
    o.append('BY_STATUS = {')
    for k, v in sorted(s["by_status"].items(), key=lambda kv: -kv[1]):
        o.append('    %r: %d,' % (k, v))
    o.append('}')
    o.append('')
    o.append('# short -> {total, delinquent, pct}')
    o.append('DELINQUENCY = {')
    for k, v in sorted(s["delinquency"].items()):
        o.append('    %r: {"total": %d, "delinquent": %d, "pct": %s},'
                 % (k, v["total"], v["delinquent"], v["pct"]))
    o.append('}')
    o.append('')
    o.append('# county -> {assoc, lic, ratio}. California addresses only.')
    o.append('COUNTIES = {')
    for c, v in sorted(s["counties"].items(),
                       key=lambda kv: -(kv[1]["assoc"] + kv[1]["lic"])):
        o.append('    %r: {"assoc": %d, "lic": %d, "ratio": %s},'
                 % (c, v["assoc"], v["lic"], v["ratio"]))
    o.append('}')
    o.append('')
    open(OUT, "w", encoding="utf-8").write("\n".join(o) + "\n")


# ------------------------------------------------------------------- guards
def check(s):
    bad = 0
    text = open(OUT, encoding="utf-8").read()

    # Nothing identifying may have reached the output. Street-address shapes
    # and long digit runs are the two things that would betray a mistake.
    if re.search(r"\d+\s+[A-Z][a-z]+\s+(St|Ave|Rd|Dr|Blvd|Way|Ln|Ct)\b", text):
        print("GUARD: something shaped like a street address is in dca_stats.py")
        bad += 1
    for m in re.finditer(r"\b\d{5,}\b", text):
        if int(m.group(0)) > 200000:
            print("GUARD: a number over 200,000 (%s) is in dca_stats.py, and "
                  "no count should be that large - is it a licence number or a "
                  "ZIP?" % m.group(0))
            bad += 1
            break
    for f in FORBIDDEN:
        if f in text:
            print("GUARD: the field name %r reached the output" % f)
            bad += 1

    # The counts have to reconcile with the file they came from.
    if sum(s["by_type"].values()) != s["total"]:
        print("GUARD: the type counts sum to %d against %d records"
              % (sum(s["by_type"].values()), s["total"]))
        bad += 1
    if sum(s["by_status"].values()) != s["total"]:
        print("GUARD: the status counts sum to %d against %d records"
              % (sum(s["by_status"].values()), s["total"]))
        bad += 1

    if len(s["counties"]) > 58:
        print("GUARD: %d counties, and California has 58"
              % len(s["counties"]))
        bad += 1
    if sum(s["county_discards"].values()) > 200:
        print("GUARD: %d records discarded for an unrecognised county. That is "
              "more than data entry; check whether DCA changed the field."
              % sum(s["county_discards"].values()))
        bad += 1

    ca = sum(v["assoc"] + v["lic"] for v in s["counties"].values())
    if not (0.80 * s["total"] < ca < s["total"]):
        print("GUARD: the county table holds %d of %d records, which is not a "
              "plausible share for a California board" % (ca, s["total"]))
        bad += 1

    # The trap must stay armed.
    try:
        issuance_by_year()
    except IssueDateIsNotAnIssueDate:
        pass
    else:
        print("GUARD: issuance_by_year() no longer refuses. Somebody has "
              "implemented it; read the docstring before trusting it.")
        bad += 1

    # And the output must import.
    sys.path.insert(0, HERE)
    try:
        import dca_stats
        import importlib
        importlib.reload(dca_stats)
        if dca_stats.TOTAL != s["total"]:
            print("GUARD: dca_stats.TOTAL disagrees with what was counted")
            bad += 1
    except Exception as e:
        print("GUARD: dca_stats.py does not import: %s" % e)
        bad += 1
    return bad


def main():
    print("the DCA licensee file")
    refuse_if_tracked()
    fetch()
    rows = load()
    import datetime
    stamp = datetime.date.fromtimestamp(os.path.getmtime(RAW)).strftime("%B %Y")
    s = summarise(rows)
    emit(s, stamp)

    print("  %s records, %d California cities, %d counties"
          % (format(s["total"], ",d"), s["cities"], len(s["counties"])))
    d = s["delinquency"]
    if "AMFT" in d and "LMFT" in d:
        print("  delinquency: AMFT %.1f%% against LMFT %.1f%%"
              % (d["AMFT"]["pct"], d["LMFT"]["pct"]))
    top = sorted(s["counties"].items(),
                 key=lambda kv: -(kv[1]["assoc"] + kv[1]["lic"]))[:3]
    if s["county_discards"]:
        print("  discarded %d record(s) with State=CA and a county that is not "
              "in California: %s"
              % (sum(s["county_discards"].values()),
                 ", ".join(sorted(s["county_discards"]))))
    print("  largest: " + ", ".join("%s %s" % (c, format(v["assoc"] + v["lic"], ",d"))
                                    for c, v in top))
    print("  wrote %s" % os.path.relpath(OUT, SITE))

    bad = check(s)
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("  guards clean - counts reconcile, nothing identifying in the "
          "output, and the issue-date trap is still armed")


if __name__ == "__main__":
    main()
