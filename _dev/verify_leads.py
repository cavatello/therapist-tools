#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch every directory lead before it can ship as a link.

The site's rule (build_safetynet.py, county_portals.py): no external URL is
published unless it was fetched and the destination checked. This pass does
the FETCH half for the two banked lead files:

    RESEARCH/prelicensed-job-sites-leads.md      (232 statewide job sites)
    RESEARCH/ebcamft-practicum-sites-2026-08-14.md (22 East Bay practicum sites)

Like _dev/dca_licensees.py, the network half CANNOT run in the sandboxed
build environment - run it on a machine with outbound network (the Mac):

    python3 _dev/verify_leads.py            # fetch all, write results
    python3 _dev/verify_leads.py --limit 20 # smoke-test a batch

It writes RESEARCH/leads-verified-<date>.json (machine-readable, for the
directory builders) and a companion .md summary. Each row: url, final URL
after redirects, HTTP status, page <title>, and a verdict:

    ok        2xx and a real title
    redirect  2xx but landed on a different registrable domain (check by hand)
    dead      4xx/5xx, DNS failure, timeout
    empty     2xx but no title / tiny body (JS shell or parked page)

The builder rule stays: `dead` never ships; `redirect` and `empty` ship only
after a human look. Re-run any time; results are dated, not merged.
"""
import json, os, re, ssl, sys, time
import urllib.request
from datetime import date
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
RES = os.path.join(SITE, "RESEARCH")
UA = ("Mozilla/5.0 (Macintosh) TherapistSupport-linkcheck/1.0 "
      "(+https://therapistsupport.org/contact.html)")
TIMEOUT = 20
DELAY = 0.7  # polite

URL_RE = re.compile(r'https?://[^\s|)\]"<>]+')


class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.title = ""; self._in = False
    def handle_starttag(self, tag, attrs):
        if tag == "title": self._in = True
    def handle_endtag(self, tag):
        if tag == "title": self._in = False
    def handle_data(self, d):
        if self._in and len(self.title) < 200: self.title += d


def leads():
    seen, out = set(), []
    for fn in ("prelicensed-job-sites-leads.md",
               "ebcamft-practicum-sites-2026-08-14.md"):
        p = os.path.join(RES, fn)
        if not os.path.exists(p):
            print("  missing %s - skipped" % fn); continue
        for u in URL_RE.findall(open(p, encoding="utf-8").read()):
            u = u.rstrip(".,;")
            key = u.lower().rstrip("/")
            if key in seen: continue
            seen.add(key); out.append((fn, u))
    return out


def domain(u):
    m = re.match(r"https?://(?:www\.)?([^/:]+)", u.lower())
    return m.group(1) if m else ""


def check(u):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
            body = r.read(120000).decode("utf-8", "replace")
            tp = TitleParser()
            try: tp.feed(body)
            except Exception: pass
            title = re.sub(r"\s+", " ", tp.title).strip()
            final = r.geturl()
            if not title or len(body) < 800:
                verdict = "empty"
            elif domain(final) != domain(u):
                verdict = "redirect"
            else:
                verdict = "ok"
            return {"url": u, "final": final, "status": r.status,
                    "title": title[:160], "verdict": verdict}
    except Exception as e:
        return {"url": u, "final": None, "status": None,
                "title": "", "verdict": "dead", "error": str(e)[:120]}


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    rows, todo = [], leads()
    if limit: todo = todo[:limit]
    print("%d unique lead URL(s)" % len(todo))
    for i, (src, u) in enumerate(todo):
        r = check(u); r["source"] = src; rows.append(r)
        print("  %3d/%d %-8s %s" % (i + 1, len(todo), r["verdict"], u[:70]))
        time.sleep(DELAY)
    d = date.today().isoformat()
    jp = os.path.join(RES, "leads-verified-%s.json" % d)
    json.dump(rows, open(jp, "w", encoding="utf-8"), indent=1)
    counts = {}
    for r in rows: counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    mp = os.path.join(RES, "leads-verified-%s.md" % d)
    with open(mp, "w", encoding="utf-8") as f:
        f.write("# Lead URL verification - %s\n\n%s\n\n" % (
            d, " · ".join("%s %d" % kv for kv in sorted(counts.items()))))
        f.write("Machine-readable: leads-verified-%s.json. Builders: only "
                "`ok` ships unreviewed; `redirect`/`empty` need a human "
                "look; `dead` never ships.\n\n" % d)
        for v in ("dead", "redirect", "empty"):
            rs = [r for r in rows if r["verdict"] == v]
            if not rs: continue
            f.write("## %s (%d)\n\n" % (v, len(rs)))
            for r in rs:
                f.write("- %s%s\n" % (r["url"],
                        " -> %s" % r["final"] if r.get("final") and
                        r["final"] != r["url"] else ""))
            f.write("\n")
    print("wrote %s and %s" % (os.path.basename(jp), os.path.basename(mp)))
    print({k: v for k, v in sorted(counts.items())})


if __name__ == "__main__":
    main()
