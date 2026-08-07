#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add the display face, sitewide, in one place.

The brief was "much bolder typography". Fraunces at 700 is as far as Fraunces
goes and it is still a soft, optical-size serif; the direction that was picked
out of the ten mockups uses Bricolage Grotesque at 800, tracked to -.032em.

Two things have to happen together or the page shows a fallback:

  1. the font has to be REQUESTED - every page carries its own copy of the
     Google Fonts <link>, so the family has to be added to each one;
  2. the font has to be USED - the rule that applies it rides along in
     nav_rebuild's stylesheet, which is appended last on every page and so
     wins on source order without touching the content-hashed shared sheet.

This pass does (1) only. It is deliberately narrow: it edits one query string
and nothing else, so if the typography has to be reverted it is one line.

Fraunces STAYS, and is still loaded, because it is doing a different job now -
it sets the figures. A serif numeral at 40px reads as a quantity; a grotesque
one reads as a headline. Do not remove it from the request thinking it is dead.

Idempotent. Run any time; it is order-independent with respect to the other
passes because it touches nothing they touch.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training")

FAM = "family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800"
# The href is a css2 query. Insert before &display so the parameter order stays
# the conventional one; Google does not care, but a diff is easier to read.
HREF = re.compile(r'href="(https://fonts\.googleapis\.com/css2\?[^"]*?)"')


def pages():
    out = [f for f in sorted(os.listdir(SITE))
           if f.endswith(".html") and not f.startswith(".")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def patch(url):
    if "Bricolage" in url:
        return url
    if "&display=" in url:
        i = url.index("&display=")
        return url[:i] + "&" + FAM + url[i:]
    return url + "&" + FAM


def main():
    changed = 0
    for rel in pages():
        path = os.path.join(SITE, rel)
        s = open(path, encoding="utf-8").read()
        new = HREF.sub(lambda m: 'href="%s"' % patch(m.group(1)), s)
        if new != s:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1
    print("font request patched on %d pages" % changed)

    # ---- guard. A page that uses the family but never asks for it renders in
    # the fallback, which on macOS is Helvetica and looks close enough to pass
    # a screenshot review. Check the request, not the appearance.
    bad = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        asks = "family=Bricolage" in s
        uses = "Bricolage Grotesque" in s or "css/" in s
        if uses and not asks:
            print("GUARD %s: uses the display face without requesting it" % rel)
            bad += 1
    if bad:
        sys.exit("typeface: %d guard failure(s)" % bad)
    print("guards clean")


if __name__ == "__main__":
    main()
