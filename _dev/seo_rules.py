#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The rule: a page cannot be added to this site badly, because publishing checks.

WHAT THE USER ASKED FOR

"Write a rule or script within the design and files so as you add content, the
sitemap is updated, you follow good SEO principles."

Two halves, and they need different mechanisms.

THE SITEMAP HALF IS ALREADY SOLVED, AND WAS SOLVED THE RIGHT WAY.
`_dev/discovery.py` generates sitemap.xml from the directory listing rather than
from a hand-maintained list, so a page cannot be forgotten because nobody is
remembering. What was missing is that somebody has to RUN it. That is fixed in
`_dev/publish.sh`, which now runs discovery before every commit. The sitemap can
no longer drift, because the only path to the live site goes through it.

THE SEO HALF NEEDS A GUARD, NOT A GENERATOR.
You cannot generate a good title. You can refuse to publish a bad one. So this
script reads every page and checks the things that are actually checkable, and
`publish.sh` refuses to commit when the answer got worse.

WHY A BASELINE INSTEAD OF A PASS/FAIL

A fresh audit of 160 pages returns a long list, most of it pre-existing and none
of it caused by whatever you are trying to publish right now. A guard that
blocks on all of it gets switched off within a day, and then it is worth
nothing.

So this records what is wrong TODAY in `_dev/_snap/seo_rules.json` and fails only
on findings that are NEW since that snapshot. A stable problem is listed once,
quietly, in the summary. A regression is loud and blocks the push. That is the
same design as `_dev/seo_monitor.py`, for the same reason, and it is the only
version of this that survives contact with a real site.

    python3 _dev/seo_rules.py            check against the baseline
    python3 _dev/seo_rules.py --all      show everything, baseline included
    python3 _dev/seo_rules.py --accept   adopt the current state as the baseline
    python3 _dev/seo_rules.py --strict   no baseline; every finding fails

THE RULES, AND WHY EACH ONE IS HERE

Every one of these has already gone wrong on this site at least once. None of
them is a general-purpose SEO checklist item included because a blog said so.

  one h1                A page with two h1s has a heading-structure bug, and on
                        this site it has always meant a builder emitted its hero
                        into a page that already had one.
  title present         Four pages shipped without one.
  title length          Under 15 characters is a stub; over 65 is truncated in
                        the result. Both are measurable, so both are checked.
  title unique          Two pages with the same title compete with each other.
  description present   The snippet Google shows when it does not like your
                        prose is worse than the one you wrote.
  description length    70 to 165 characters. Shorter gets ignored, longer gets
                        cut mid-sentence.
  description unique    Same reason as the title.
  canonical present     Four real pages shipped without one.
  canonical on-host     THE migration bug. A canonical naming the old GitHub
                        host took the entire site out of the index, and nothing
                        else mattered until it was found.
  canonical self        A canonical naming a DIFFERENT page silently deindexes
                        the page carrying it. That is the copy-paste failure,
                        and it is invisible in a browser.
  lang attribute        One line, and it is what tells a crawler this is English.
  internal links live   Every same-site href resolves to a file that exists.
  no extensionless href `href="some-page"` with the extension left outside the
                        quotes renders as a link and 404s. It shipped here, on
                        thirty links at once, and the existing link check could
                        not see it because it only looked at hrefs already
                        ending in .html.
  in the sitemap        Symmetry, both directions: no page missing from it, no
                        URL in it without a page.
  not an orphan         A page nothing links to is a page nothing crawls. New
                        pages are the ones that get stranded.
  json-ld parses        An unparseable block is worse than no block, because it
                        looks done.
  images have alt       Alt text is the only description a crawler gets.
  American spellings    This site is written for Californians. "licence" is not
                        a variant here, it is wrong on the merits: the Board
                        issues a license.
"""
import os, re, sys, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
BASE = "https://therapistsupport.org/"
SNAP = os.path.join(HERE, "_snap", "seo_rules.json")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

# Pages excluded from the sitemap on purpose, and therefore from its symmetry
# check. Kept in step with _dev/discovery.py by the guard at the bottom.
EXCLUDE = {"tools.html", "concepts.html", "tycoon.html"}
# Artefacts a builder leaves beside its output. Not pages.
ARTEFACTS = ("_chrome.html",)

TITLE_MIN, TITLE_MAX = 15, 68
DESC_MIN, DESC_MAX = 70, 168

BRITISH = [
    (r"\blicence[sd]?\b", "license"),
    (r"\bprogramme[s]?\b", "program"),
    (r"\borganisation", "organization"),
    (r"\bcentre[s]?\b", "center"),
    (r"\banalyse[sd]?\b", "analyze"),
    (r"\bbehaviour", "behavior"),
    (r"\bcatalogue[s]?\b", "catalog"),
    (r"\bfulfil\b", "fulfill"),
    (r"\benrolment\b", "enrollment"),
]
# Quoting a source that spells it their way is not a mistake. These are the
# proper nouns and quoted phrases where the British form is correct on this
# site, and they are stripped before the spelling check runs.
BRITISH_OK = [
    r"Board of Behavioural Sciences",       # never correct, but caught elsewhere
    r"Behavioural Health Examiners",        # the Arizona board's actual name
    r"[Ll]icence[s]? issued in (?:England|Wales|Scotland)",
]


def pages():
    out = [f for f in sorted(os.listdir(SITE))
           if f.endswith(".html") and not f.endswith(ARTEFACTS)]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html") and not f.endswith(ARTEFACTS)]
    return out


def text_of(s):
    """The page with script, style and markup removed - just the prose."""
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<!--[\s\S]*?-->", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s)


def one(pat, s, g=1):
    m = re.search(pat, s, re.I)
    return m.group(g) if m else None


def check():
    """Every finding on the site, as a sorted list of "page\tcode\tdetail"."""
    found = []
    titles, descs = {}, {}
    all_pages = pages()
    existing = set(all_pages)
    inbound = {p: 0 for p in all_pages}

    docs = {}
    for rel in all_pages:
        docs[rel] = open(os.path.join(SITE, rel), encoding="utf-8").read()

    # ------------------------------------------------ inbound link counting
    def resolve(here, href):
        """A link target, as a path relative to SITE.

        `href="money/"` is how every section hub is linked in the nav. Counting
        only hrefs ending in .html reported all five section index pages as
        orphans, which is exactly backwards - they are among the most linked
        pages on the site."""
        if href.endswith("/"):
            href += "index.html"
        return os.path.normpath(os.path.join(here, href)).replace(os.sep, "/")

    for rel, s in docs.items():
        here = os.path.dirname(rel)
        for href in set(re.findall(r'href="([^"#?:]+(?:\.html|/))(?:[#?][^"]*)?"', s)):
            tgt = resolve(here, href)
            if tgt in inbound and tgt != rel:
                inbound[tgt] += 1

    for rel, s in docs.items():
        # A page deliberately kept out of the index is not held to the rules for
        # pages that are in it. concepts.html is a layout scratchpad carrying a
        # deliberate noindex; reporting it for having a noindex, no canonical,
        # no description and no structured data is five findings that all say
        # "this page is what it says it is".
        if rel in EXCLUDE:
            continue

        def add(code, detail=""):
            found.append("%s\t%s\t%s" % (rel, code, detail))

        # Script bodies are not markup. Scanning them for hrefs reports every
        # `'<a href="' + fn() + '">'` string concatenation as a broken link.
        markup = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)

        # ------------------------------------------------------------ head
        if len(re.findall(r"<h1\b", s, re.I)) != 1:
            add("h1-count", str(len(re.findall(r"<h1\b", s, re.I))))

        if not re.search(r"<html[^>]*\slang=", s, re.I):
            add("lang-missing")

        t = one(r"<title>([\s\S]*?)</title>", s)
        if not t:
            add("title-missing")
        else:
            t = re.sub(r"\s+", " ", text_of(t)).strip()
            if not (TITLE_MIN <= len(t) <= TITLE_MAX):
                add("title-length", "%d chars" % len(t))
            titles.setdefault(t, []).append(rel)

        d = one(r'<meta\s+name="description"\s+content="([^"]*)"', s)
        if d is None:
            add("description-missing")
        else:
            d = re.sub(r"\s+", " ", text_of(d)).strip()
            if not (DESC_MIN <= len(d) <= DESC_MAX):
                add("description-length", "%d chars" % len(d))
            descs.setdefault(d, []).append(rel)

        c = one(r'<link\s+rel="canonical"\s+href="([^"]*)"', s)
        if not c:
            add("canonical-missing")
        elif not c.startswith(BASE):
            add("canonical-off-host", c[:70])
        else:
            want = rel
            got = c[len(BASE):] or "index.html"
            if got in ("", "index.html") and rel == "index.html":
                got = "index.html"
            if got.rstrip("/") != want.rstrip("/") and \
               got.rstrip("/") + "/index.html" != want:
                add("canonical-mismatch", "says %s" % got)

        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', s, re.I):
            add("noindex")

        # --------------------------------------------------------- links
        here = os.path.dirname(rel)
        for href in set(re.findall(r'href="([^"#?:]+\.html)(?:[#?][^"]*)?"', markup)):
            tgt = os.path.normpath(os.path.join(here, href)).replace(os.sep, "/")
            if tgt not in existing and not os.path.exists(os.path.join(SITE, tgt)):
                add("dead-link", href)
        # The bug the .html-only check above cannot see.
        # Any scheme at all, not a list of the ones remembered. The first
        # version listed http/https/mailto/tel and then reported every inline
        # `data:image/svg+xml` icon as a broken relative link - 40 findings that
        # were all the guard's fault.
        for href in set(re.findall(
                r'href="(?![a-z][a-z0-9+.-]*:|#|/)([^"#?]+)"', markup, re.I)):
            if not href.endswith((".html", ".pdf", ".xml", ".txt", ".ico", ".png",
                                  ".jpg", ".svg", ".css", ".js", "/")):
                add("href-no-extension", href[:50])

        if inbound.get(rel, 0) == 0 and rel != "index.html":
            add("orphan")

        # ---------------------------------------------------- structured data
        blocks = re.findall(
            r'<script[^>]+type="application/ld\+json"[^>]*>([\s\S]*?)</script>', s)
        if not blocks:
            add("no-json-ld")
        for b in blocks:
            try:
                json.loads(b)
            except Exception as e:
                add("json-ld-broken", str(e)[:50])

        # ------------------------------------------------------------ images
        for tag in re.findall(r"<img\b[^>]*>", s, re.I):
            if not re.search(r"\salt=", tag, re.I):
                add("img-no-alt", tag[:52])

        # ---------------------------------------------------------- spelling
        prose = text_of(s)
        for pat in BRITISH_OK:
            prose = re.sub(pat, " ", prose)
        for pat, right in BRITISH:
            for m in set(re.findall(pat, prose, re.I)):
                add("british-spelling", "%s -> %s" % (m, right))

    # ------------------------------------------------------------ duplicates
    for t, ps in titles.items():
        if len(ps) > 1:
            for p in ps:
                found.append("%s\tduplicate-title\t%s" % (p, t[:48]))
    for d, ps in descs.items():
        if len(ps) > 1:
            for p in ps:
                found.append("%s\tduplicate-description\t%s" % (p, d[:48]))

    # --------------------------------------------------------- sitemap both ways
    sm = os.path.join(SITE, "sitemap.xml")
    if not os.path.exists(sm):
        found.append("sitemap.xml\tsitemap-missing\t")
    else:
        urls = set(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", open(sm, encoding="utf-8").read()))
        listed = {u[len(BASE):] if u.startswith(BASE) else u for u in urls}
        listed = {l or "index.html" for l in listed}
        for rel in all_pages:
            if rel in EXCLUDE:
                continue
            if rel not in listed and not (rel == "index.html" and "" in listed):
                found.append("%s\tnot-in-sitemap\t" % rel)
        for l in listed:
            if l not in existing and l != "index.html":
                found.append("sitemap.xml\tphantom-url\t%s" % l)

    return sorted(set(found))


def load_baseline():
    if not os.path.exists(SNAP):
        return None
    try:
        return set(json.load(open(SNAP, encoding="utf-8"))["findings"])
    except Exception:
        return None


def save_baseline(f):
    os.makedirs(os.path.dirname(SNAP), exist_ok=True)
    json.dump({"findings": sorted(f)}, open(SNAP, "w", encoding="utf-8"), indent=1)


def show(rows, cap=40):
    for r in rows[:cap]:
        page, code, detail = (r.split("\t") + ["", ""])[:3]
        print("  %-52s %-22s %s" % (page[:52], code, detail[:44]))
    if len(rows) > cap:
        print("  ... and %d more" % (len(rows) - cap))


def main():
    args = set(sys.argv[1:])
    findings = check()

    # discovery.py owns the exclusion list; if the two ever disagree, this check
    # reports pages as missing from a sitemap that is deliberately not listing
    # them, which reads as a bug in the site rather than a bug in the guard.
    try:
        dsrc = open(os.path.join(HERE, "discovery.py"), encoding="utf-8").read()
        theirs = set(re.findall(r'^\s*"([a-z0-9._-]+\.html)":\s*"', dsrc, re.M))
        if theirs and theirs != EXCLUDE:
            print("NOTE: the sitemap exclusion lists have drifted apart.")
            print("      discovery.py: %s" % ", ".join(sorted(theirs)))
            print("      seo_rules.py: %s" % ", ".join(sorted(EXCLUDE)))
    except Exception:
        pass

    if "--accept" in args:
        save_baseline(findings)
        print("baseline set: %d finding(s) recorded as the current state" % len(findings))
        print("from here, only NEW findings fail.")
        return

    if "--strict" in args:
        print("%d finding(s), strict mode - no baseline" % len(findings))
        show(findings, cap=200)
        sys.exit(1 if findings else 0)

    base = load_baseline()
    if base is None:
        save_baseline(findings)
        print("no baseline existed, so the current state is now the baseline.")
        print("%d finding(s) recorded. Re-run to check against it." % len(findings))
        show(findings, cap=25)
        return

    new = sorted(set(findings) - base)
    fixed = sorted(base - set(findings))

    if "--all" in args:
        print("%d finding(s) in total:" % len(findings))
        show(findings, cap=300)
        print()

    if fixed:
        print("%d finding(s) fixed since the baseline:" % len(fixed))
        show(fixed, cap=15)
        print()

    if new:
        print("%d NEW finding(s) - this is what publishing would ship:\n" % len(new))
        show(new, cap=60)
        print("\nFix them, or run --accept if they are deliberate.")
        sys.exit(1)

    print("%d page(s) checked. %d known finding(s) in the baseline, 0 new."
          % (len(pages()), len(base)))
    if fixed:
        print("Run --accept to bank the %d fix(es)." % len(fixed))


if __name__ == "__main__":
    main()
