#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RETIRED - superseded by registry.json; see hub_psychedelic_link.py.

Give About an inbound link from somewhere a reader would actually follow.

A link audit found about.html with ZERO inbound body-copy links. It sits in the
nav and in the footer of every page, so it is not unreachable - but nothing in
the reading flow ever sends anyone there. On a site whose whole argument is
"every figure is computed or cited", the page explaining who computed them
should be reachable from the moment a reader starts wondering.

The hub is the right place and the question index is the right shape, so it
enters as the question people actually have at that moment - not "About", which
is a label rather than a question.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
HUB, PAGE = "resources.html", "about.html"

ROW = ('<a class="qref" href="' + PAGE + '"><div>'
       '<h3>Who made this, and why should I trust the numbers?</h3>'
       '<div class="m"><span class="tag">About</span>'
       '<span class="g">Reference &middot; What this is</span></div></div>'
       '<span class="ar">&rarr;</span></a>')
ANCHOR = '<a class="qread" href="mft-programs-california.html">'


def main():
    import sys as _s
    print("hub_about_link.py: retired - the hub is generated from registry.json")
    _s.exit(0)

    path = os.path.join(SITE, HUB)
    s = open(path, encoding="utf-8").read()
    body = re.sub(r"<header[\s\S]*?</header>|<footer[\s\S]*?</footer>", "", s)

    if ('class="qref" href="%s"' % PAGE) in s:
        print("%-44s already linked from the index" % HUB)
    else:
        if s.count(ANCHOR) != 1:
            sys.exit("hub_about_link: anchor matched %d times" % s.count(ANCHOR))
        s = s.replace(ANCHOR, ROW + ANCHOR, 1)
        open(path, "w", encoding="utf-8").write(s)
        print("%-44s About added to the question index" % HUB)

    s = open(path, encoding="utf-8").read()
    body = re.sub(r"<header[\s\S]*?</header>|<footer[\s\S]*?</footer>", "", s)
    bad = 0
    if body.count('href="%s"' % PAGE) < 1:
        print("GUARD: About still has no body-copy link from the hub"); bad += 1
    if s.count('class="qref" href="%s"' % PAGE) != 1:
        print("GUARD: %d rows" % s.count('class="qref" href="%s"' % PAGE)); bad += 1
    if re.search(r'<a class="q\w+"[^>]*>(?:(?!</a>).)*<a class="q', s, re.S):
        print("GUARD: nested index row"); bad += 1
    if bad:
        sys.exit("hub_about_link: %d guard failure(s)" % bad)
    print("guards clean · %d question rows" % len(re.findall(r'<a class="q\w+"', s)))


if __name__ == "__main__":
    main()
