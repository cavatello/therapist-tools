#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove superseded stylesheets. Every page was carrying each pass twice.

THE BUG, WHICH COMPOUNDS

Each CSS-emitting pass in _dev/ is idempotent the way it was written: before it
inserts its block it strips its own previous one, matching

    <style>/* _dev/whatever.py */ ... </style>

But `extract_css.py` runs later in the pipeline and REPLACES that <style> with a
<link> to css/<sha>.css. On the next cycle the pass looks for its <style>, does
not find one — it is a <link> now — strips nothing, and appends a fresh block.
extract_css then hoists that too, and the page ends up linking two stylesheets
that both carry the same marker.

Run the pipeline again and it is three. Pages had reached seventeen stylesheets,
every one of them a separate request, and four passes were duplicated on
essentially every page:

    contrast_pass.py   134 pages
    footer_fix.py      132 pages
    pixel_concepts.py  131 pages
    hub_owid.py          5 pages

Nothing looked wrong, because the newest copy is last and wins. That is exactly
why it survived: the symptom is weight and request count, not appearance.

WHY THE FIX GOES HERE AND NOT IN EACH PASS

Teaching all six passes to also strip a <link> whose target contains their
marker means opening every file whenever any of them runs, six times over, and
means the next pass anyone writes has to remember. One step after extract_css,
which knows the rule — a page may link at most one stylesheet per marker, and
the LAST one wins because that is what the browser already does — fixes every
pass at once, including passes not written yet.

ORPHANS. Files in css/ that no page references any more are moved to
_to_delete/ rather than unlinked, because the bridge this repository is edited
through cannot delete.

Run after extract_css.py.
"""
import os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CSSDIR = os.path.join(SITE, "css")
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

LINK = re.compile(r'[ \t]*<link rel="stylesheet" href="((?:\.\./)*)css/'
                  r'([0-9a-f]{12})\.css">\n?')
MARKER = re.compile(r"/\* (_dev/[\w-]+\.py) \*/")


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def markers_of(h, cache):
    if h not in cache:
        p = os.path.join(CSSDIR, "%s.css" % h)
        try:
            cache[h] = set(MARKER.findall(open(p, encoding="utf-8").read()))
        except IOError:
            cache[h] = set()
    return cache[h]


def main():
    cache = {}
    cleaned, dropped = 0, collections.Counter()

    for rel in pages():
        p = os.path.join(SITE, rel)
        s = open(p, encoding="utf-8").read()

        hits = list(LINK.finditer(s))
        if not hits:
            continue

        # last occurrence of each marker wins, which is what the browser does
        last = {}
        for i, m in enumerate(hits):
            for mk in markers_of(m.group(2), cache):
                last[mk] = i

        kill = set()
        for i, m in enumerate(hits):
            mks = markers_of(m.group(2), cache)
            if mks and all(last[mk] != i for mk in mks):
                kill.add(i)
                for mk in mks:
                    dropped[mk] += 1

        if not kill:
            continue
        out, prev = [], 0
        for i, m in enumerate(hits):
            if i in kill:
                out.append(s[prev:m.start()])
                prev = m.end()
        out.append(s[prev:])
        s2 = "".join(out)
        if s2 != s:
            open(p, "w", encoding="utf-8").write(s2)
            cleaned += 1

    print("%d page(s) de-duplicated" % cleaned)
    for mk, n in dropped.most_common():
        print("  %-28s %3d superseded link(s) removed" % (mk, n))

    # ---- orphans
    live = set()
    for rel in pages():
        live |= set(m.group(2) for m in
                    LINK.finditer(open(os.path.join(SITE, rel),
                                       encoding="utf-8").read()))
    bin_ = os.path.join(SITE, "_to_delete")
    moved = 0
    for fn in sorted(os.listdir(CSSDIR)):
        if not fn.endswith(".css"):
            continue
        if fn[:-4] in live:
            continue
        os.makedirs(bin_, exist_ok=True)
        try:
            os.replace(os.path.join(CSSDIR, fn),
                       os.path.join(bin_, "orphan-%s" % fn))
            moved += 1
        except OSError as e:
            print("  could not move css/%s (%s)" % (fn, e))
    if moved:
        print("%d orphaned stylesheet(s) moved to _to_delete/" % moved)

    # ---- guards
    bad = 0
    worst = 0
    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        seen = collections.Counter()
        for m in LINK.finditer(s):
            for mk in markers_of(m.group(2), cache):
                seen[mk] += 1
        for mk, n in seen.items():
            if n > 1:
                print("GUARD %s: %s linked %d times" % (rel, mk, n))
                bad += 1
        worst = max(worst, len(LINK.findall(s)))
        for _u, h in LINK.findall(s):
            if not os.path.exists(os.path.join(CSSDIR, "%s.css" % h)):
                print("GUARD %s: links css/%s.css which is not there" % (rel, h))
                bad += 1
    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - at most %d stylesheet(s) on any page" % worst)


if __name__ == "__main__":
    main()
