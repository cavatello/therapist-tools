#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RETIRED - superseded by registry.json; see hub_psychedelic_link.py.

Put the licensure guide into the hub's question index.

The hub is organised as questions rather than as a list of pages, which is the
right shape for it: a reader arrives with "can I set up as an LLC", not with
"show me your article about entity structure". A new page that is not phrased
as a question the hub already answers is invisible there no matter how good it
is.

So the guide enters as the question it actually answers, in the same markup as
its neighbours, immediately before the existing BBS-fees row - because fees are
one section of the route and the route is the larger question, so the general
should precede the specific.

Idempotent, and guarded on the count of index rows so a double insertion cannot
survive a run.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
HUB = "resources.html"
GUIDE = "become-an-mft-california.html"

ROW = ('<a class="qread" href="' + GUIDE + '"><div>'
       '<h3>What does it actually take to become an MFT here?</h3>'
       '<div class="m"><span class="tag">Licensure</span>'
       '<span class="g">Read &middot; The whole route</span></div></div>'
       '<span class="ar">&rarr;</span></a>')

ANCHOR = '<a class="qread" href="bbs-fees-california-2026.html">'


def main():
    import sys as _s
    print("hub_guide_link.py: retired - the hub is generated from registry.json")
    _s.exit(0)

    path = os.path.join(SITE, HUB)
    s = open(path, encoding="utf-8").read()

    if not os.path.exists(os.path.join(SITE, GUIDE)):
        sys.exit("hub_guide_link: %s does not exist - build it first" % GUIDE)

    before = s.count('href="%s"' % GUIDE)
    if before:
        print("%-44s already linked (%d)" % (HUB, before))
    else:
        if s.count(ANCHOR) != 1:
            sys.exit("hub_guide_link: anchor matched %d times, expected 1"
                     % s.count(ANCHOR))
        s = s.replace(ANCHOR, ROW + ANCHOR, 1)
        open(path, "w", encoding="utf-8").write(s)
        print("%-44s guide added to the question index" % HUB)

    # ---- guards
    s = open(path, encoding="utf-8").read()
    bad = 0
    n = s.count('href="%s"' % GUIDE)
    if n != 1:
        print("GUARD: %d links to the guide, expected 1" % n); bad += 1
    # the row must be a sibling of the others, not nested inside one
    if s.count(ROW) != 1:
        print("GUARD: the row markup is not intact"); bad += 1
    if re.search(r'<a class="q\w+"[^>]*>(?:(?!</a>).)*<a class="q', s, re.S):
        print("GUARD: an index row is nested inside another"); bad += 1
    if s.count("<h1") != 1:
        print("GUARD: %d h1" % s.count("<h1")); bad += 1
    if bad:
        sys.exit("hub_guide_link: %d guard failure(s)" % bad)
    print("guards clean · %d question rows in the index" % len(re.findall(r'<a class="q\w+"', s)))


if __name__ == "__main__":
    main()
