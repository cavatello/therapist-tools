#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""No page ships unreachable: every indexable page must have an inbound link.

The open-queue item this closes said a hand-maintained index "is wrong
within a month". The registry side is already safe - registry_sync
rebuilds the pages array from disk, and build_library emits the browse
indexes from the registry - but nothing verified the other direction:
that every indexable page actually has at least one inbound link from
another page. A page can be in the sitemap, carry perfect metadata, and
still be an orphan a reader can never reach by browsing.

This pass builds the full internal link graph and fails the build for
any page that is in the sitemap yet linked from nowhere. Read-only;
lives in VERIFY and on the /ops quality-gates board.

    python3 _dev/orphan_guard.py
"""
import os, re, sys
from urllib.parse import urljoin, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training",
           "for")


def pages():
    out = []
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html"):
            out.append(f)
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    sm = open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8").read()
    indexable = set()
    for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
        path = urlsplit(loc).path.lstrip("/")
        if not path or path.endswith("/"):
            path += "index.html"
        indexable.add(path)

    inbound = {}
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        base = rel
        for href in re.findall(r'href="([^"#]+)(?:#[^"]*)?"', s):
            if href.startswith(("http", "mailto:", "data:", "tel:")):
                continue
            tgt = urljoin(base, href)
            if tgt.endswith("/"):
                tgt += "index.html"
            if tgt != rel:
                inbound.setdefault(tgt, set()).add(rel)

    orphans = sorted(p for p in indexable
                     if p != "index.html" and not inbound.get(p))
    if orphans:
        for p in orphans:
            print("ORPHAN %s: in the sitemap, linked from nowhere" % p)
        sys.exit("%d orphan page(s)" % len(orphans))
    print("no orphans - all %d indexable pages have an inbound link"
          % len(indexable))


if __name__ == "__main__":
    main()
