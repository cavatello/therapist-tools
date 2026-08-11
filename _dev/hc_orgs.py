#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""California health center organizations, with every link actually checked.

WHAT THIS IS FOR

`_dev/hrsa_sites.py` reduces HRSA's bulk files to counts. This one does the
other half: it aggregates the 3,038 active California health center sites up to
the ~218 ORGANIZATIONS that run them, because a person looking for work applies
to an employer and not to a clinic address.

WHY THE LINK CHECKING IS THE POINT

The federal file carries a website for most sites and the field is dirty. Real
examples from the California rows: a domain with a zero in place of a letter o,
a domain truncated by a fixed-width field, and two rows where somebody typed an
email address into the website column. Shipping those as links would put ~30
dead or wrong links on a page whose whole claim is that its figures are
checkable.

So every candidate domain is fetched. The ones that answer become links. The
ones that do not are shipped as PLAIN TEXT with no link at all, and the page
says why - because "did not answer an automated request" is not the same as
"has no website", and several of these are simply behind bot protection. A
wrong link is worse than no link, which is the rule the citation pattern on the
rest of this site already follows.

Run it where there is network. It writes `_dev/hc_orgs_data.py`.
"""
import collections, concurrent.futures as cf, csv, io, json, os, re, ssl, sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
SRC = os.path.join(CACHE, "hc_sites.csv")
OUT = os.path.join(HERE, "hc_orgs_data.py")
CHECKED = "11 August 2026"

# Tokens that must survive title-casing of the file's upper-case names.
KEEP = {"INC": "Inc.", "INC.": "Inc.", "LLC": "LLC", "L.L.C.": "LLC",
        "CORP": "Corp.", "CORP.": "Corp.", "CO": "Co.", "USA": "USA",
        "II": "II", "III": "III", "AND": "and", "OF": "of", "THE": "the",
        "DE": "de", "DEL": "del", "LA": "la", "LAS": "las", "EL": "el",
        "A": "a", "AT": "at", "FOR": "for", "IN": "in", "ON": "on",
        "DBA": "dba", "MD": "MD", "DDS": "DDS", "PC": "PC",
        "AIDS": "AIDS", "HIV": "HIV", "YMCA": "YMCA", "UCSF": "UCSF",
        "UCLA": "UCLA", "UC": "UC", "SAC": "SAC", "AMH": "AMH",
        "DAP": "DAP", "OMNI": "Omni", "TCC": "TCC"}


def pretty(name):
    words = name.replace("’", "'").split()
    out = []
    for i, w in enumerate(words):
        bare, tail = w.strip(","), ("," if w.endswith(",") else "")
        up = bare.upper()
        if up in KEEP:
            v = KEEP[up]
            if i == 0 and v.islower():
                v = v.capitalize()
            out.append(v + tail)
        elif re.match(r"^[A-Z]\.([A-Z]\.)+$", bare):
            out.append(bare + tail)
        elif re.match(r"^\d+[A-Z]+$", bare):
            out.append(bare + tail)
        elif len(bare) <= 4 and not set(bare) & set("AEIOU"):
            out.append(bare + tail)
        elif len(bare) <= 4 and len(set(bare)) == 1:
            out.append(bare + tail)
        else:
            out.append(bare.capitalize() + tail)
    joined = " ".join(out)
    # "TULARE, COUNTY OF" is a sort-order artifact of the federal file.
    m = re.match(r"^(.*), (County) of$", joined, re.I)
    return "County of " + m.group(1) if m else joined


def norm(w):
    w = (w or "").strip().lower()
    if not w:
        return None
    w = re.sub(r"^https?://", "", w).rstrip("/")
    w = re.sub(r"^www\.", "", w).split("/")[0].strip()
    return w if ("." in w and " " not in w and "@" not in w) else None


def variants(dom):
    v = [dom, dom.replace("0rg", "org")]
    if re.search(r"\.or$", dom):
        v.append(dom + "g")
    if re.search(r"\.co$", dom):
        v.append(dom + "m")
    if re.search(r"\.ne$", dom):
        v.append(dom + "t")
    v.append("www." + dom)
    seen, out = set(), []
    for x in v:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (compatible; therapistsupport.org link check)"


def check(item):
    name, dom = item
    for cand in variants(dom):
        for scheme in ("https://", "http://"):
            try:
                req = urllib.request.Request(scheme + cand, method="GET",
                                             headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=12, context=CTX) as r:
                    if 200 <= r.status < 400:
                        return name, cand
            except Exception:
                pass
    return name, None


def main():
    if not os.path.exists(SRC):
        sys.exit("%s is missing - run _dev/hrsa_sites.py first, it fetches it"
                 % os.path.relpath(SRC, HERE))
    rows = [r for r in csv.DictReader(open(SRC, encoding="utf-8-sig",
                                           errors="replace"))
            if r.get("Site State Abbreviation") == "CA"
            and (r.get("Site Status Description") or "") == "Active"]
    org = collections.defaultdict(
        lambda: {"sites": 0, "counties": collections.Counter(),
                 "web": collections.Counter(), "type": set(),
                 "city": collections.Counter()})
    for r in rows:
        k = (r.get("Health Center Name") or "").strip()
        if not k:
            continue
        o = org[k]
        o["sites"] += 1
        c = (r.get("County Equivalent Name") or "").strip()
        if c:
            o["counties"][c] += 1
        w = norm(r.get("Site Web Address"))
        if w:
            o["web"][w] += 1
        o["type"].add((r.get("Health Center Type") or "").strip())
        ct = (r.get("Site City") or "").strip()
        if ct:
            o["city"][ct] += 1

    if len(org) < 100:
        sys.exit("only %d California health center organizations - the file "
                 "layout has changed" % len(org))

    cands = {k: v["web"].most_common(1)[0][0] for k, v in org.items() if v["web"]}
    print("  %d organizations, %d with a candidate domain" % (len(org), len(cands)))
    print("  checking every one of them over the network")
    good = {}
    with cf.ThreadPoolExecutor(max_workers=20) as ex:
        for name, dom in ex.map(check, sorted(cands.items())):
            if dom:
                good[name] = dom
    print("  %d answered, %d did not and will ship without a link"
          % (len(good), len(org) - len(good)))

    if len(good) < len(cands) * 0.6:
        sys.exit("fewer than 60%% of the domains answered - this looks like a "
                 "network problem here rather than %d dead sites, and writing "
                 "the module now would strip links that are fine"
                 % (len(cands) - len(good)))

    out = []
    for name in sorted(org):
        o = org[name]
        out.append({"name": pretty(name), "raw": name, "sites": o["sites"],
                    "counties": sorted(o["counties"]),
                    "lookalike": any("Look-Alike" in t for t in o["type"]),
                    "city": o["city"].most_common(1)[0][0] if o["city"] else "",
                    "url": ("https://" + good[name]) if name in good else None})

    b = io.StringIO()
    b.write("#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n")
    b.write('"""California health center organizations. WRITTEN BY '
            '_dev/hc_orgs.py.\n\n'
            "Do not edit by hand - rerun the ETL, which needs network because "
            "it fetches\nevery candidate domain before writing it as a link.\n\n"
            "`url` is None where the address in the federal file did not "
            "answer an\nautomated request. That is NOT the same as the "
            "organization having no\nwebsite - several are behind bot "
            "protection - so those rows ship as plain\ntext. A wrong link is "
            'worse than no link.\n"""\n\n')
    b.write("CHECKED = %r\n\n" % CHECKED)
    b.write("ORGS = [\n")
    for r in out:
        b.write("    %r,\n" % r)
    b.write("]\n\n")
    b.write("LINKED = %d\nUNLINKED = %d\nTOTAL_SITES = %d\nCOUNTIES = %d\n"
            % (sum(1 for r in out if r["url"]),
               sum(1 for r in out if not r["url"]),
               sum(r["sites"] for r in out),
               len({c for r in out for c in r["counties"]})))
    open(OUT, "w", encoding="utf-8").write(b.getvalue())
    print("  wrote %s" % os.path.basename(OUT))


if __name__ == "__main__":
    main()
