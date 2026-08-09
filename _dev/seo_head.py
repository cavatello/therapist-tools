#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every published page gets a canonical and a lang, because four did not.

WHAT THIS FIXES

`_dev/seo_rules.py` was run for the first time against the whole site and its
very first finding was that four real pages carry no `<link rel="canonical">`:
about.html, contact.html, newsletter.html and rates.html. Two of them are among
the most linked pages on the site.

A missing canonical is not a small thing here. This site has already been
deindexed once by a canonical problem - during the domain move, pages carried a
canonical pointing at the old GitHub host, and nothing else about the site
mattered until that was found. A page with no canonical at all is the milder
version of the same failure: any URL variant that reaches it (a tracking
parameter, a trailing slash, an http link, a syndicated copy) can be treated as
a separate document.

WHY A PASS RATHER THAN FOUR EDITS

Because four edits fix four pages and this fixes the class. The canonical for a
page on this site is a pure function of its path - there is nothing to decide -
so it should be derived, not typed. The next page anyone adds gets one whether
or not they remembered.

The same argument applies to `<html lang>`, which is one attribute and is what
tells a crawler and a screen reader what language this is.

WHAT IT WILL NOT DO

It will not overwrite a canonical that is already there. If a page deliberately
points its canonical somewhere else - a syndicated copy, a variant that should
consolidate onto its parent - that is a real editorial decision and this pass
leaves it alone and reports it. It only fills in what is missing.

Idempotent, guarded. Run before extract_css, and before discovery.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
BASE = "https://therapistsupport.org/"
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")
MARK = "<!-- _dev/seo_head.py -->"

# Not published, so not canonicalised. Kept in step with discovery.py's own
# exclusion list by the guard at the bottom.
EXCLUDE = {"tools.html", "concepts.html", "tycoon.html"}
ARTEFACTS = ("_chrome.html",)


def pages():
    out = [f for f in sorted(os.listdir(SITE))
           if f.endswith(".html") and not f.endswith(ARTEFACTS)]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html") and not f.endswith(ARTEFACTS)]
    return out


def canonical_for(rel):
    """A directory index canonicalises to the directory, not to index.html."""
    if rel == "index.html":
        return BASE
    if rel.endswith("/index.html"):
        return BASE + rel[:-len("index.html")]
    return BASE + rel


def main():
    added_c = added_l = 0
    elsewhere = []

    for rel in pages():
        if rel in EXCLUDE:
            continue
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()
        orig = s

        # ------------------------------------------------------------- lang
        m = re.search(r"<html\b([^>]*)>", s, re.I)
        if m and not re.search(r"\slang=", m.group(1), re.I):
            s = s[:m.start()] + '<html lang="en"%s>' % m.group(1) + s[m.end():]
            added_l += 1

        # -------------------------------------------------------- canonical
        cur = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', s, re.I)
        want = canonical_for(rel)
        if cur:
            if cur.group(1) != want:
                # Left alone on purpose. A canonical naming a different page is
                # either a deliberate consolidation or the copy-paste bug, and
                # only a person can tell which - so it is reported, not rewritten.
                elsewhere.append((rel, cur.group(1)))
        else:
            i = s.lower().find("</head>")
            if i < 0:
                print("SKIP %s: no </head>" % rel)
                continue
            s = (s[:i] + '%s<link rel="canonical" href="%s">\n' % (MARK, want)
                 + s[i:])
            added_c += 1

        if s != orig:
            open(p, "w", encoding="utf-8").write(s)

    print("%d canonical(s) added, %d lang attribute(s) added" % (added_c, added_l))
    if elsewhere:
        print("\n%d canonical(s) point somewhere other than their own URL. Not "
              "changed - check each one is deliberate:" % len(elsewhere))
        for rel, got in elsewhere[:20]:
            print("  %-46s -> %s" % (rel[:46], got[:60]))

    # ------------------------------------------------------------- guards
    bad = 0
    checked = 0
    for rel in pages():
        if rel in EXCLUDE:
            continue
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        checked += 1
        n = len(re.findall(r'<link\s+rel="canonical"', s, re.I))
        if n == 0:
            print("GUARD %s: still no canonical" % rel); bad += 1
        elif n > 1:
            # Two canonicals is worse than none: the crawler picks one and you
            # do not know which.
            print("GUARD %s: %d canonicals" % (rel, n)); bad += 1
        if not re.search(r"<html[^>]*\slang=", s, re.I):
            print("GUARD %s: no lang" % rel); bad += 1
        if s.count(MARK) > 1:
            print("GUARD %s: %d copies of this pass" % (rel, s.count(MARK)))
            bad += 1

    # The exclusion list must agree with discovery.py's, or a page ends up
    # canonicalised but absent from the sitemap, or the reverse.
    try:
        d = open(os.path.join(HERE, "discovery.py"), encoding="utf-8").read()
        theirs = set(re.findall(r'^\s*"([a-z0-9._-]+\.html)":\s*"', d, re.M))
        if theirs and theirs != EXCLUDE:
            print("GUARD: exclusion lists disagree with discovery.py")
            print("       here: %s" % ", ".join(sorted(EXCLUDE)))
            print("       there: %s" % ", ".join(sorted(theirs)))
            bad += 1
    except Exception:
        pass

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - all %d published page(s) have exactly one canonical "
          "and a lang" % checked)


if __name__ == "__main__":
    main()
