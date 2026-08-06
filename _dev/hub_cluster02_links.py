#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RETIRED - superseded by registry.json; see hub_psychedelic_link.py.

Add the two cluster-02 articles to the hub's question index.

Same rule as the other hub passes: a page enters as the question a reader
arrives with, not as its own title. "Cost of incorporating" is a label;
"what does incorporating actually cost me" is what someone types.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
HUB = "resources.html"

ROWS = [
    ("cost-of-incorporating-california-therapist.html",
     "What does incorporating actually cost me?", "Money",
     "Read &middot; Cost of incorporating"),
    ("quarterly-estimated-taxes-california-therapist.html",
     "When are my estimated taxes due, and how much?", "Money",
     "Read &middot; Estimated taxes"),
    ("backdoor-roth-pro-rata-therapist.html",
     "Can I still get money into a Roth?", "Money",
     "Read &middot; The backdoor Roth"),
]
ANCHOR = '<a class="qread" href="therapist-llc-california.html">'


def row(page, q, tag, g):
    return ('<a class="qread" href="%s"><div><h3>%s</h3>'
            '<div class="m"><span class="tag">%s</span><span class="g">%s</span>'
            "</div></div><span class=\"ar\">&rarr;</span></a>" % (page, q, tag, g))


def main():
    import sys as _s
    print("hub_cluster02_links.py: retired - the hub is generated from registry.json")
    _s.exit(0)

    path = os.path.join(SITE, HUB)
    s = open(path, encoding="utf-8").read()
    added = 0
    for page, q, tag, g in ROWS:
        if not os.path.exists(os.path.join(SITE, page)):
            sys.exit("hub_cluster02_links: %s does not exist" % page)
        if ('href="%s"' % page) in s:
            continue
        if s.count(ANCHOR) != 1:
            sys.exit("hub_cluster02_links: anchor matched %d times" % s.count(ANCHOR))
        s = s.replace(ANCHOR, row(page, q, tag, g) + ANCHOR, 1)
        added += 1
    if added:
        open(path, "w", encoding="utf-8").write(s)
    print("%-44s %d row(s) added" % (HUB, added))

    s = open(path, encoding="utf-8").read()
    # Count the QUESTION INDEX only. The first version counted every href in the
    # file and failed once nav_rebuild had also put these articles in the header
    # and the footer - three links, all correct, reported as a duplicate. A hub
    # pass is about the index; the chrome is another pass's business.
    body = re.sub(r"<header[\s\S]*?</header>|<footer[\s\S]*?</footer>", "", s)
    bad = 0
    for page, _q, _t, _g in ROWS:
        n = body.count('<a class="qread" href="%s">' % page)
        if n != 1:
            print("GUARD: %d index rows for %s" % (n, page)); bad += 1
    if re.search(r'<a class="q\w+"[^>]*>(?:(?!</a>).)*<a class="q', s, re.S):
        print("GUARD: nested index row"); bad += 1
    if s.count("<h1") != 1:
        print("GUARD: %d h1" % s.count("<h1")); bad += 1
    if bad:
        sys.exit("hub_cluster02_links: %d guard failure(s)" % bad)
    print("guards clean · %d question rows" % len(re.findall(r'<a class="q\w+"', s)))


if __name__ == "__main__":
    main()
