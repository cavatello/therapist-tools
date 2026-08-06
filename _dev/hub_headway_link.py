#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RETIRED - superseded by registry.json; see hub_psychedelic_link.py.

Add the Headway explainer to the hub's question index.

Same reasoning as hub_guide_link.py: the hub is indexed by the question a
reader arrives with, not by page title. The question here is the one people
actually type - "should I go through Headway or get on panels myself" - and it
sits next to the other getting-paid rows rather than with the licensure ones.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
HUB = "resources.html"
PAGE = "headway-for-california-therapists.html"

ROW = ('<a class="qread" href="' + PAGE + '"><div>'
       '<h3>Should I go through Headway, or get on panels myself?</h3>'
       '<div class="m"><span class="tag">Getting paid</span>'
       '<span class="g">Read &middot; Headway</span></div></div>'
       '<span class="ar">&rarr;</span></a>')

ANCHOR = '<a class="qread" href="become-an-mft-california.html">'


def main():
    import sys as _s
    print("hub_headway_link.py: retired - the hub is generated from registry.json")
    _s.exit(0)

    path = os.path.join(SITE, HUB)
    if not os.path.exists(os.path.join(SITE, PAGE)):
        sys.exit("hub_headway_link: %s does not exist - build it first" % PAGE)
    s = open(path, encoding="utf-8").read()

    if ('href="%s"' % PAGE) in s:
        print("%-44s already linked" % HUB)
    else:
        if s.count(ANCHOR) != 1:
            sys.exit("hub_headway_link: anchor matched %d times" % s.count(ANCHOR))
        s = s.replace(ANCHOR, ROW + ANCHOR, 1)
        open(path, "w", encoding="utf-8").write(s)
        print("%-44s Headway added to the question index" % HUB)

    s = open(path, encoding="utf-8").read()
    bad = 0
    if s.count('href="%s"' % PAGE) != 1:
        print("GUARD: %d links" % s.count('href="%s"' % PAGE)); bad += 1
    if re.search(r'<a class="q\w+"[^>]*>(?:(?!</a>).)*<a class="q', s, re.S):
        print("GUARD: an index row is nested inside another"); bad += 1
    if s.count("<h1") != 1:
        print("GUARD: %d h1" % s.count("<h1")); bad += 1
    if bad:
        sys.exit("hub_headway_link: %d guard failure(s)" % bad)
    print("guards clean · %d question rows" % len(re.findall(r'<a class="q\w+"', s)))


if __name__ == "__main__":
    main()
