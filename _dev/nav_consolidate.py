#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collapse tools.html into the hub, and take Field Notes out of the top nav.

MEASURED FIRST, then decided. Counting what each page actually links to:

    tools.html      8 internal destinations
    resources.html 10 internal destinations
    overlap         6 - every calculator, plus rates.html

tools.html's only two unique links were `index.html` and `resources.html`
itself. It was not a third category; it was a strict SUBSET of the hub that
also linked to the page containing it. Two doors promising the same thing is
the duplication worth fixing - it was never about the blog.

So:

1. The nav's "All free tools" entry is REPOINTED at resources.html and
   relabelled, rather than removed. That keeps its pixel-art icon doing the
   same job (see claude/pixel-art-system.md - a new entry would need new art)
   and means the hub finally has a top-nav entry, which it shipped without.

2. tools.html itself becomes a redirect stub, written by build_redirect.py.
   GitHub Pages has no server-side redirects, so it is a zero-delay meta
   refresh plus rel=canonical - which Google treats as a redirect - plus a
   real visible link for anyone whose browser ignores both.

3. "Field Notes" leaves the TOP NAV. It is a document, not a destination, and
   it now has a prominent section inside the hub instead. It stays in the
   FOOTER, because a footer is an index of everything and a nav is a set of
   choices - Hick's law bites on the second, not the first.

Idempotent. Every edit asserts its match count.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SKIP = {"tycoon.html", "concepts.html", "tools.html"}   # tools.html is the stub now

NAV_TOOLS_OLD = ('<a href="tools.html"', '<b>All free tools</b>',
                 '<i>every calculator and widget, in one place</i>')
NAV_TOOLS_NEW_LABEL = '<b>Tools &amp; resources</b>'
NAV_TOOLS_NEW_SUB = '<i>every calculator, plus what the Board and the payers require</i>'


def header_span(s):
    i = s.find("<header")
    if i < 0:
        return None
    d = 0
    for m in re.finditer(r"<header\b|</header>", s[i:]):
        d += 1 if m.group(0).startswith("<header") else -1
        if d == 0:
            return (i, i + m.end())
    return None


def anchor_span(s, href, start=0):
    """Span of a whole <a href="..."> ... </a>, which carries an inline icon."""
    i = s.find('<a href="%s"' % href, start)
    if i < 0:
        return None
    j = s.find("</a>", i)
    if j < 0:
        return None
    return (i, j + 4)


def main():
    changed = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in SKIP:
            continue
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        hs = header_span(s)
        if not hs:
            print("%-44s no <header>" % f)
            continue
        nav = s[hs[0]:hs[1]]
        before = nav

        # --- 1. repoint the tools entry at the hub
        if 'href="tools.html"' in nav:
            n = nav.count('href="tools.html"')
            if n != 1:
                sys.exit("%s: %d tools links in nav" % (f, n))
            nav = nav.replace('<a href="tools.html"', '<a href="resources.html"', 1)
            nav = nav.replace("<b>All free tools</b>", NAV_TOOLS_NEW_LABEL, 1)
            nav = nav.replace("<i>every calculator and widget, in one place</i>",
                              NAV_TOOLS_NEW_SUB, 1)

        # --- 2. remove the Field Notes entry from the nav only
        sp = anchor_span(nav, "rates.html")
        if sp:
            block = nav[sp[0]:sp[1]]
            if "Field Notes" not in block:
                sys.exit("%s: the rates.html anchor is not the Field Notes card" % f)
            nav = nav[:sp[0]] + nav[sp[1]:]

        if nav == before:
            continue
        s = s[:hs[0]] + nav + s[hs[1]:]
        open(path, "w", encoding="utf-8").write(s)
        changed += 1
        print("%-44s nav updated" % f)

    # ---- guards
    bad = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in SKIP:
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        hs = header_span(s)
        if not hs:
            continue
        nav = s[hs[0]:hs[1]]
        foot = s[s.find("<footer"):]
        if 'href="tools.html"' in nav:
            print("GUARD %s: tools link survives in nav" % f); bad += 1
        if 'href="rates.html"' in nav:
            print("GUARD %s: Field Notes survives in nav" % f); bad += 1
        if nav.count('href="resources.html"') != 1:
            print("GUARD %s: %d hub links in nav (want 1)"
                  % (f, nav.count('href="resources.html"'))); bad += 1
        # the footer must still carry Field Notes - it is an index, not a choice
        if 'href="rates.html"' not in foot:
            print("GUARD %s: Field Notes lost from the footer too" % f); bad += 1
    if bad:
        sys.exit("nav_consolidate: %d guard failure(s)" % bad)
    print("%d page(s) updated" % changed)


if __name__ == "__main__":
    main()
