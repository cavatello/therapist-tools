#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sitemap and structured data, derived from the pages that actually exist.

TWO GAPS, both found by measuring rather than by remembering.

THE SITEMAP LISTED 15 OF 59 PAGES. It was hand-written when the site had
fifteen, and every page added since - the three articles, the licensure guide,
the programmes directory, the Headway explainer and all thirty-seven school
pages - was invisible to it. Forty-four pages, including every piece of work
from the last two days.

It also listed tools.html at priority 0.9. That is a zero-delay meta refresh to
resources.html. A redirect in a sitemap is a soft error in Search Console and,
worse, it was ranked above the page it redirects to.

So the sitemap is now GENERATED from the directory listing, with lastmod taken
from each file's own modification time. A page cannot be forgotten, because
nobody is remembering.

THIRTY-NINE PAGES HAD NO STRUCTURED DATA. The older articles carry Article and
BreadcrumbList blocks; every page built in the last two days carries none,
because each new builder was written from scratch rather than from the older
one. Same class of omission as the missing nav script, and found the same way.

WHAT IS EMITTED, AND WHAT IS NOT. Only facts already on the page:

  - Article for the guide, the directory, the Headway explainer.
  - EducationalOccupationalProgram for each school page - the precise type, and
    honestly applicable. `provider` and `name` always; `timeToComplete` and
    `offers` ONLY where the institution published them. Inventing an ISO-8601
    duration for a programme that publishes no length would be a lie in a
    format designed to be parsed rather than read, which is worse than a lie in
    prose because nothing about it looks uncertain.
  - BreadcrumbList wherever the page renders a breadcrumb, built by reading
    that breadcrumb rather than by assuming a trail.

No aggregateRating anywhere. There are no ratings, and a review-rich snippet
on a page that ranks nothing would be a fabrication.

Idempotent: previous blocks from this pass are stripped and rewritten.
"""
import os, re, sys, json, html, time

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
BASE = "https://therapistsupport.org/"
MARK = "<!-- discovery -->"

# Pages that must never appear in the sitemap, and why.
EXCLUDE = {
    "tools.html": "a zero-delay redirect - a soft error in Search Console",
    "concepts.html": "layout scratchpad, already disallowed in robots.txt",
    "tycoon.html": "illustrative mockup with no real calculations behind it",
}

# priority, changefreq
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")


ARTEFACTS = ("_chrome.html",)


def html_files():
    """Every page, root and one level down, as paths relative to SITE.

    Build artefacts are excluded by name: a builder that lifts chrome writes it
    beside its output, and a blanket *.html copy has swept it into the site
    once already. It has no canonical and no title, so it would be indexed as a
    duplicate of the page it was lifted from."""
    out = [f for f in sorted(os.listdir(SITE))
           if f.endswith(".html") and not f.startswith(".")
           and f not in ARTEFACTS]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def rank(f, s):
    if f == "index.html":
        return 1.0, "weekly"
    if f == "resources.html":
        return 0.9, "weekly"
    if f.endswith("-mft.html"):
        return 0.6, "yearly"
    if f in ("privacy.html", "terms.html"):
        return 0.2, "yearly"
    if 'class="artbody"' in s:
        return 0.8, "monthly"
    if len(re.findall(r"<input|<select|<textarea", s)) > 6:
        return 0.85, "monthly"
    return 0.7, "monthly"


def text(x):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x))).strip()


def crumbs(s, url):
    """Read the page's own breadcrumb rather than assuming its trail."""
    m = re.search(r'<ol class="bcr"[^>]*>([\s\S]*?)</ol>', s)
    if not m:
        return None
    items, pos = [], 0
    for li in re.finditer(r"<li>([\s\S]*?)</li>", m.group(1)):
        inner = li.group(1)
        a = re.search(r'<a href="([^"]+)"[^>]*>([\s\S]*?)</a>', inner)
        pos += 1
        if a:
            href = a.group(1)
            items.append({"@type": "ListItem", "position": pos,
                          "name": text(a.group(2)),
                          "item": BASE + ("" if href == "index.html" else href)})
        else:
            cur = re.search(r"<span[^>]*>([\s\S]*?)</span>", inner)
            items.append({"@type": "ListItem", "position": pos,
                          "name": text(cur.group(1)) if cur else "", "item": url})
    return ({"@context": "https://schema.org", "@type": "BreadcrumbList",
             "itemListElement": items} if len(items) > 1 else None)


def iso_duration(length):
    """ISO-8601 for a published length, or None. Never a guess.

    "2.5-3 years, cohort, mandatory summers" is a real string on a real page
    and it does not have one duration in it. Where the text is not
    unambiguously a single number of years, this returns None and the property
    is omitted - which is the correct representation of "they did not say".
    """
    if not length:
        return None
    m = re.match(r"^\s*(\d+(?:\.\d+)?)\s*years?\b", length.strip(), re.I)
    if not m:
        return None
    yrs = float(m.group(1))
    return "P%dM" % round(yrs * 12)


def main():
    files = html_files()
    progs = {}
    pj = os.path.join(HERE, "..", "programs.json")
    slugs = {}
    for cand in ("school_slugs.json",):
        p = os.path.join(HERE, "..", cand)
        if os.path.exists(p):
            slugs = json.load(open(p, encoding="utf-8"))
    inv = {v: k for k, v in slugs.items()}
    if os.path.exists(pj):
        progs = {r["institution"]: r for r in json.load(open(pj, encoding="utf-8"))}

    # ---------------------------------------------------------- structured data
    added = 0
    for f in files:
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        before = s
        s = re.sub(re.escape(MARK) + r'<script type="application/ld\+json">[\s\S]*?</script>',
                   "", s)
        if f in EXCLUDE or "ld+json" in s:
            # already carries its own, hand-written or from an earlier builder
            if s != before:
                open(path, "w", encoding="utf-8").write(s)
            continue

        url = BASE + f
        h1 = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", s)
        desc = re.search(r'<meta name="description" content="([^"]*)"', s)
        if not (h1 and desc):
            continue
        blocks = []

        if f in inv and inv[f] in progs:
            p = progs[inv[f]]
            node = {"@context": "https://schema.org",
                    "@type": "EducationalOccupationalProgram",
                    "name": p.get("degree") or ("MFT programme, %s" % inv[f]),
                    "url": url,
                    "occupationalCategory": "Marriage and Family Therapist",
                    "programType": "Graduate degree",
                    "provider": {"@type": "CollegeOrUniversity",
                                 "name": inv[f], "url": p["url"]}}
            if p.get("city"):
                node["provider"]["address"] = {"@type": "PostalAddress",
                                               "addressLocality": p["city"],
                                               "addressRegion": "CA",
                                               "addressCountry": "US"}
            dur = iso_duration(p.get("length"))
            if dur:
                node["timeToComplete"] = dur
            if p.get("total"):
                node["offers"] = {"@type": "Offer", "price": int(p["total"]),
                                  "priceCurrency": "USD",
                                  "category": "Total published tuition"}
            blocks.append(node)
        else:
            blocks.append({"@context": "https://schema.org", "@type": "Article",
                           "headline": text(h1.group(1))[:110],
                           "description": html.unescape(desc.group(1)),
                           "url": url,
                           "dateModified": time.strftime(
                               "%Y-%m-%d", time.gmtime(os.path.getmtime(path))),
                           "isAccessibleForFree": True,
                           "author": {"@type": "Organization",
                                      "name": "Therapist Support"}})

        cb = crumbs(s, url)
        if cb:
            blocks.append(cb)

        tag = "".join(MARK + '<script type="application/ld+json">'
                      + json.dumps(b, separators=(",", ":")) + "</script>"
                      for b in blocks)
        s = s.replace("</head>", tag + "</head>", 1)
        open(path, "w", encoding="utf-8").write(s)
        added += 1

    # ------------------------------------------------------------- the sitemap
    urls = []
    for f in files:
        if f in EXCLUDE:
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        pr, cf = rank(f, s)
        loc = BASE + ("" if f == "index.html" else f)
        lm = time.strftime("%Y-%m-%d",
                           time.gmtime(os.path.getmtime(os.path.join(SITE, f))))
        urls.append((loc, lm, cf, pr))
    urls.sort(key=lambda x: (-x[3], x[0]))
    body = "".join(
        "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
        "    <changefreq>%s</changefreq>\n    <priority>%.1f</priority>\n  </url>\n"
        % u for u in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<!-- Generated by _dev/discovery.py from the pages that exist.\n'
           '     Do not hand-edit: the previous hand-written copy listed 15 of 59\n'
           '     pages and ranked a redirect stub above its own destination. -->\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + body + "</urlset>\n")
    open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write(xml)

    print("structured data added to %d page(s)" % added)
    print("sitemap: %d urls (%d html files, %d excluded)"
          % (len(urls), len(files), len(set(EXCLUDE) & set(files))))

    # ---- guards
    bad = 0
    live = {f for f in files if f not in EXCLUDE}
    listed = {u[0].replace(BASE, "") or "index.html" for u in urls}
    if listed != live:
        print("GUARD: sitemap and directory disagree: %s"
              % sorted(live ^ listed)[:4]); bad += 1
    for f in EXCLUDE:
        if f in files and (BASE + f) in xml:
            print("GUARD: %s is in the sitemap" % f); bad += 1
    for f in files:
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if s.count(MARK) and f in EXCLUDE:
            print("GUARD: %s got structured data it should not have" % f); bad += 1
        for m in re.finditer(re.escape(MARK)
                             + r'<script type="application/ld\+json">([\s\S]*?)</script>', s):
            try:
                node = json.loads(m.group(1))
            except ValueError:
                print("GUARD %s: invalid JSON-LD" % f); bad += 1; continue
            if node.get("@type") == "EducationalOccupationalProgram":
                inst = node["provider"]["name"]
                p = progs.get(inst, {})
                # a duration or a price may only appear if the institution published one
                if "timeToComplete" in node and not p.get("length"):
                    print("GUARD %s: invented a duration" % f); bad += 1
                if "offers" in node and not p.get("total"):
                    print("GUARD %s: invented a price" % f); bad += 1
            if "aggregateRating" in json.dumps(node):
                print("GUARD %s: emits a rating it does not have" % f); bad += 1
        # EXCLUDE is the list of pages this pass deliberately keeps out of the
        # sitemap - a redirect stub, a layout scratchpad, a visual mockup. None
        # of them is a published target, so holding them to a published page's
        # heading structure only produces a guard failure that must be ignored,
        # and a guard that must be ignored is a guard that gets ignored.
        if s.count("<h1") != 1 and f not in (
                "privacy.html", "terms.html") and f not in EXCLUDE:
            print("GUARD %s: %d h1" % (f, s.count("<h1"))); bad += 1
    if bad:
        sys.exit("discovery: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
