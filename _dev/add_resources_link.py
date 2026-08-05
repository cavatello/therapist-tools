#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Put resources.html in the footer of every page.

resources.html ships without a top-nav entry: every item in that menu carries
its own inline pixel-art icon (claude/pixel-art-system.md) and this page has no
icon drawn yet. Reusing another page's art would make the menu lie, so the nav
entry waits and the footer carries the link in the meantime.

The footer's Learn column is plain text links with no icons, so this is a
one-line insertion per page. Idempotent, and it asserts the column exists
rather than silently doing nothing if the footer is ever restructured.

SCOPED TO THE FOOTER. There are TWO `<h5>Learn</h5>` headings on every page -
one in the top nav's mega-menu (inside `.np-col`, with pixel-art icons beside
each link) and one in the footer (plain text). A naive replace on the heading
hit the nav first and would have inserted an icon-less text link into a menu of
icon rows. Find the balanced <footer> element and work only inside it.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
LINK = '<a href="resources.html">Resources</a>'
ANCHOR = "<h5>Learn</h5>"

SKIP = {"tycoon.html", "concepts.html"}


def footer_span(s):
    """Byte span of the balanced <footer> element, or None."""
    i = s.find("<footer")
    if i < 0:
        return None
    d = 0
    for m in re.finditer(r"<footer\b|</footer>", s[i:]):
        d += 1 if m.group(0).startswith("<footer") else -1
        if d == 0:
            return (i, i + m.end())
    return None


def main():
    added = already = nofoot = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in SKIP:
            continue
        path = os.path.join(SITE, f)
        s = open(path, encoding="utf-8").read()
        fspan = footer_span(s)
        if not fspan:
            print("%-44s no <footer>" % f)
            nofoot += 1
            continue
        fs, fe = fspan
        foot = s[fs:fe]
        if ANCHOR not in foot:
            print("%-44s no Learn column" % f)
            nofoot += 1
            continue
        if LINK in foot:
            already += 1
            continue
        n = foot.count(ANCHOR)
        if n != 1:
            sys.exit("%s: %d Learn columns in the footer, refusing to guess" % (f, n))
        foot = foot.replace(ANCHOR, ANCHOR + LINK, 1)
        s = s[:fs] + foot + s[fe:]
        open(path, "w", encoding="utf-8").write(s)
        added += 1
        print("%-44s linked" % f)

    bad = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html") or f in SKIP:
            continue
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        fspan = footer_span(s)
        if not fspan:
            continue
        foot = s[fspan[0]:fspan[1]]
        if ANCHOR in foot and foot.count(LINK) != 1:
            print("GUARD %s: %d resources links in footer" % (f, foot.count(LINK))); bad += 1
    if bad:
        sys.exit("add_resources_link: %d guard failure(s)" % bad)
    print("%d linked, %d already, %d without a footer" % (added, already, nofoot))


if __name__ == "__main__":
    main()
