#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add the psychedelic training section to the hub's question index.

The row is phrased as the question a reader actually arrives with. Not "learn
about psychedelic-assisted therapy training" - nobody types that - but the
thing they are really asking, which is whether a $10,000 certificate lets them
do anything they cannot already do. That is also the question the section is
built to answer, so the row and the page agree.

Idempotent: re-running is a no-op once the link is present.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
HUB = "resources.html"
PAGE = "psychedelic-therapy-training-california.html"

ROW = ('<a class="qread" href="' + PAGE + '"><div>'
       '<h3>What can I actually do with a psychedelic therapy certificate?</h3>'
       '<div class="m"><span class="tag">Training</span>'
       '<span class="g">Read &middot; 16 programmes compared</span></div></div>'
       '<span class="ar">&rarr;</span></a>')

# Sit directly above the programmes directory: both are "what should I train
# in" questions, and the graduate degree is the one that comes first.
ANCHOR = '<a class="qread" href="mft-programs-california.html">'


def main():
    path = os.path.join(SITE, HUB)
    if not os.path.exists(os.path.join(SITE, PAGE)):
        sys.exit("hub_psychedelic_link: %s missing" % PAGE)
    s = open(path, encoding="utf-8").read()
    # Look for OUR ROW, not for the href. By the time this runs, nav_rebuild
    # has already put the same page in the mega-panel and the footer, so a
    # bare href test is true before the question row exists - the script then
    # reports "already linked" and silently never adds the thing it exists to
    # add. The row is what is being checked for, so the row is what is tested.
    if ROW in s:
        print("%-44s already linked" % HUB)
    else:
        if s.count(ANCHOR) != 1:
            sys.exit("hub_psychedelic_link: anchor matched %d times"
                     % s.count(ANCHOR))
        s = s.replace(ANCHOR, ROW + ANCHOR, 1)
        open(path, "w", encoding="utf-8").write(s)
        print("%-44s psychedelic training added to the question index" % HUB)
    s = open(path, encoding="utf-8").read()
    bad = 0
    # Count only inside the body, for the same reason: the header and footer
    # legitimately carry their own link to this page and are not duplicates.
    body = re.sub(r"<header[\s\S]*?</header>|<footer[\s\S]*?</footer>", "", s)
    n = len(re.findall(r'<a class="qread" href="%s"' % re.escape(PAGE), body))
    if n != 1:
        print("GUARD: %d question rows for this page" % n)
        bad += 1
    # A row nested inside another row renders as one unclickable blob and is
    # invisible to every static check that only counts anchors.
    if re.search(r'<a class="q\w+"[^>]*>(?:(?!</a>).)*<a class="q', s, re.S):
        print("GUARD: nested index row")
        bad += 1
    if bad:
        sys.exit("hub_psychedelic_link: %d guard failure(s)" % bad)
    print("guards clean · %d question rows" % len(re.findall(r'<a class="q\w+"', s)))


if __name__ == "__main__":
    main()
