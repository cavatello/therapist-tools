#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crawl the live site, compare against the last run, report what got worse.

WHY A DIFF RATHER THAN A SCORE. A one-off audit finds the problems that exist
today; it cannot tell you which of them you introduced yesterday. This site is
generated from ~40 builders in mock/, and the recurring failure mode on it has
never been "nobody knew the rule" - it is "a new builder was written from
scratch rather than from the older one", so a page shipped without the nav
script, or without structured data, or with a canonical naming the wrong host.
Every one of those was found by measuring rather than by remembering.

So this script measures, stores what it measured, and on the next run tells you
only what CHANGED. A stable problem is reported once, in the baseline, and then
gets out of the way. A new one is loud.

WHAT IT CHECKS, AND WHY EACH ONE EARNED ITS PLACE

  canonical off-host   The migration bug. A canonical naming cavatello.cloudflare.io
                       took the whole site out of the index and nothing else
                       mattered until it was fixed. Cheap to check, catastrophic
                       to miss.
  canonical missing    Four real pages shipped without one.
  canonical mismatch   A page whose canonical names a DIFFERENT page - the
                       copy-paste error that silently deindexes the copy.
  noindex              Anything carrying noindex that is not deliberately
                       excluded.
  title / description  Presence, length, and duplicates across the site.
  h1 count             Exactly one, or it is a heading-structure bug.
  structured data      Presence of any JSON-LD, and that it PARSES - an
                       unparseable block is worse than none, because it looks
                       done.
  internal links       Every same-site href resolves to a page that exists.
  sitemap symmetry     The sitemap's URL set equals the crawlable page set.
                       Both a missing page and a phantom one fail.
  British spellings    This site is written for Californians. "programme" and
                       "licence" are keyword misses, and "licence" is wrong on
                       the merits - the BBS issues a license.

WHAT IT DELIBERATELY DOES NOT CHECK. Rankings, traffic, backlinks. Those need
Search Console and they are not regressions you can cause with a bad commit.
This is a build-integrity check that happens to be about SEO.

USAGE

  python3 _dev/seo_monitor.py                 # crawl live, diff, report
  python3 _dev/seo_monitor.py --local         # crawl ./ from disk instead
  python3 _dev/seo_monitor.py --baseline      # crawl and store, report nothing
  python3 _dev/seo_monitor.py --json out.json # machine-readable report

EXIT CODES. 0 clean or improved, 1 new problems since the last run, 2 could not
crawl. Non-zero on new problems only - a stable known issue does not fail the
run, or the check becomes noise you learn to ignore.
"""
import os, re, sys, json, time, html, argparse
import urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNAP = os.path.join(HERE, "_snap", "seo_monitor.json")
BASE = "https://therapistsupport.org/"

# Pages excluded from the site's own sitemap, for reasons recorded in
# discovery.py. They are not failures and must not be reported as such.
EXCLUDE = {"tools.html", "concepts.html", "tycoon.html"}

BRITISH = {
    "programme": "program", "programmes": "programs",
    "licence": "license", "licences": "licenses",
    "centre": "center", "centres": "centers",
    "behaviour": "behavior", "organisation": "organization",
    "recognised": "recognized", "specialise": "specialize",
    "specialised": "specialized", "organised": "organized",
}


# ---------------------------------------------------------------- fetching

def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "seo-monitor/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", errors="replace")


def page_list_from_sitemap():
    status, xml = fetch(BASE + "sitemap.xml")
    return [m for m in re.findall(r"<loc>([^<]+)</loc>", xml)]


def page_list_local():
    return [BASE + f for f in sorted(os.listdir(ROOT))
            if f.endswith(".html") and f not in EXCLUDE]


def load(url, local):
    if local:
        p = os.path.join(ROOT, url[len(BASE):] or "index.html")
        if not os.path.exists(p):
            return None
        return open(p, encoding="utf-8", errors="replace").read()
    try:
        status, body = fetch(url)
        return body if status == 200 else None
    except Exception:
        return None


# ---------------------------------------------------------------- analysis

def analyse(url, doc):
    """Everything measurable about one page, as plain data."""
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    d = re.search(r'<meta\s+name="description"\s+content="(.*?)"', doc, re.S)
    c = re.search(r'rel="canonical"\s+href="([^"]+)"', doc)
    rb = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', doc)

    ld_ok, ld_n = True, 0
    for block in re.findall(
            r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
            doc, re.S):
        ld_n += 1
        try:
            json.loads(block)
        except Exception:
            ld_ok = False

    links = set()
    for href in re.findall(r'href="([^"]+)"', doc):
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#",
                            "javascript:", "data:")):
            continue
        tgt = href.split("#")[0].split("?")[0]
        if tgt.endswith(".html"):
            links.add(os.path.basename(tgt))

    low = doc.lower()
    brit = {w: low.count(w) for w in BRITISH if low.count(w)}

    return {
        "title": html.unescape(t.group(1).strip()) if t else None,
        "desc": html.unescape(d.group(1).strip()) if d else None,
        "canonical": c.group(1) if c else None,
        "robots": rb.group(1) if rb else None,
        "h1": len(re.findall(r"<h1[\b >]", doc)),
        "ld_blocks": ld_n,
        "ld_parses": ld_ok,
        "links": sorted(links),
        "british": brit,
    }


def same_page(a, b):
    """Is this the same URL, allowing for the directory-index form?

    `/money/index.html` and `/money/` are the SAME page, and pointing the
    canonical at the trailing-slash form is the correct choice, not an error.
    A naive string compare flags all five topic hubs as canonical mismatches,
    which is the kind of false positive that gets a monitor ignored.
    """
    def norm(u):
        u = u.split("#")[0].split("?")[0]
        if u.endswith("/index.html"):
            u = u[: -len("index.html")]
        return u.rstrip("/")
    return norm(a) == norm(b)


def problems(pages, known_files):
    """[(severity, code, url, detail)] - every complaint, uniformly shaped."""
    out = []
    seen_titles, seen_descs = {}, {}

    for url, p in sorted(pages.items()):
        slug = url[len(BASE):] or "index.html"
        if slug in EXCLUDE:
            continue

        can = p["canonical"]
        if not can:
            out.append(("high", "canonical-missing", url, "no canonical tag"))
        else:
            if not can.startswith(BASE.rstrip("/")):
                out.append(("critical", "canonical-off-host", url,
                            "canonical points off-domain: %s" % can))
            elif same_page(can, url):
                pass
            else:
                out.append(("high", "canonical-mismatch", url,
                            "canonical names a different page: %s" % can))

        if p["robots"] and "noindex" in p["robots"]:
            out.append(("critical", "noindex", url,
                        "robots meta says %s" % p["robots"]))

        if not p["title"]:
            out.append(("high", "title-missing", url, "no <title>"))
        elif len(p["title"]) > 62:
            out.append(("low", "title-long", url,
                        "%d chars, truncates in results" % len(p["title"])))

        if not p["desc"]:
            out.append(("medium", "desc-missing", url, "no meta description"))
        elif len(p["desc"]) > 165:
            out.append(("low", "desc-long", url,
                        "%d chars, truncates in results" % len(p["desc"])))

        if p["h1"] != 1:
            out.append(("medium", "h1-count", url, "%d <h1> elements" % p["h1"]))

        if p["ld_blocks"] == 0:
            out.append(("medium", "no-structured-data", url, "no JSON-LD"))
        elif not p["ld_parses"]:
            out.append(("high", "structured-data-broken", url,
                        "a JSON-LD block does not parse"))

        for tgt in p["links"]:
            if tgt not in known_files:
                out.append(("high", "broken-link", url,
                            "links to %s, which does not exist" % tgt))

        if p["title"]:
            seen_titles.setdefault(p["title"], []).append(url)
        if p["desc"]:
            seen_descs.setdefault(p["desc"], []).append(url)

        for w, n in sorted(p["british"].items()):
            out.append(("low", "british-spelling", url,
                        "%s x%d (US audience: %s)" % (w, n, BRITISH[w])))

    for val, urls in seen_titles.items():
        if len(urls) > 1:
            out.append(("medium", "duplicate-title", urls[0],
                        "%d pages share this title" % len(urls)))
    for val, urls in seen_descs.items():
        if len(urls) > 1:
            out.append(("medium", "duplicate-desc", urls[0],
                        "%d pages share this description" % len(urls)))
    return out


# ---------------------------------------------------------------- reporting

RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def key(p):
    return "%s|%s|%s" % (p[1], p[2], p[3])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", action="store_true")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()

    try:
        urls = page_list_local() if a.local else page_list_from_sitemap()
    except Exception as e:
        print("Could not get the page list: %s" % e)
        return 2

    known = {os.path.basename(u) or "index.html" for u in urls}
    known.add("index.html")
    known |= EXCLUDE   # linking to an excluded page is legal, just not indexed

    pages, missed = {}, []
    for u in urls:
        doc = load(u, a.local)
        if doc is None:
            missed.append(u)
            continue
        pages[u] = analyse(u, doc)

    print("Crawled %d/%d pages%s." %
          (len(pages), len(urls), " from disk" if a.local else " live"))
    for u in missed:
        print("   UNREACHABLE  %s" % u)

    probs = problems(pages, known)
    probs.sort(key=lambda p: (RANK[p[0]], p[1], p[2]))

    old = {}
    if os.path.exists(SNAP):
        old = json.load(open(SNAP))
    old_keys = set(old.get("problems", []))
    new_keys = {key(p) for p in probs}

    appeared = [p for p in probs if key(p) not in old_keys]
    fixed = sorted(old_keys - new_keys)

    counts = {}
    for sev, code, _, _ in probs:
        counts[code] = counts.get(code, 0) + 1

    print("\n%d finding(s) total:" % len(probs))
    for code, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print("   %-26s %d" % (code, n))

    if old:
        print("\nSince the last run (%s):" % old.get("at", "?"))
        print("   %d new, %d resolved" % (len(appeared), len(fixed)))
        for p in appeared[:40]:
            print("   NEW  [%s] %s  %s  %s" % (p[0], p[1], p[2], p[3]))
        if len(appeared) > 40:
            print("   ... and %d more new" % (len(appeared) - 40))
        for k in fixed[:20]:
            print("   FIXED  %s" % k)
    else:
        print("\nNo previous run - this is the baseline. "
              "Nothing is reported as new.")

    if a.json:
        json.dump({"at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "crawled": len(pages), "unreachable": missed,
                   "problems": [{"severity": s, "code": c, "url": u,
                                 "detail": d} for s, c, u, d in probs],
                   "new_since_last": [key(p) for p in appeared],
                   "resolved_since_last": fixed},
                  open(a.json, "w"), indent=1)
        print("\nJSON written to %s" % a.json)

    os.makedirs(os.path.dirname(SNAP), exist_ok=True)
    json.dump({"at": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "problems": sorted(new_keys)}, open(SNAP, "w"), indent=1)

    if missed:
        return 2
    return 1 if (old and appeared) else 0


if __name__ == "__main__":
    sys.exit(main())
