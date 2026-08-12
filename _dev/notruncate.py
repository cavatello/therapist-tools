#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""No published page may be implausibly small. Twice is a pattern.

WHAT HAPPENED, TWICE

`getting-paid/index.html` was once committed at **zero bytes** by two
concurrent `ship.py` runs racing on the same file. The rule that came out of it
was: never run the pipeline twice at once.

It happened again today to `therapynotes-vs-simplepractice-california.html`,
and the cause was different - a `ship.py` stage was killed by a command timeout
while a pass held the file open for writing. So the rule was necessary and not
sufficient: **anything that interrupts a pass mid-write can truncate a page**,
and the watcher commits it within the minute.

WHY NOTHING CAUGHT IT

`linkcheck.py` reads links, and an empty file has none. `seo_rules.py` skips
pages without the site chrome, and an empty file has none of that either. Both
reported clean on a run where a 215KB page had become 0 bytes. Every guard on
this site checks that something is *correct*; none checked that a page is
*there*.

WHAT THIS DOES

Reads every published HTML page and fails if one is implausibly small, or is
missing the three things every page on this site has: a `<title>`, an `<h1>`,
and the masthead. The floor is deliberately crude - 4KB - because this is not
a quality check. It is a smoke alarm for a file that has been emptied.

Redirect stubs are genuinely small and are listed by name rather than detected,
so that a stub shrinking to nothing still fails.

Runs in VERIFY, where it is read-only and cheap, and where a failure stops the
deploy rather than describing it afterwards.

RECOVERY, WRITTEN DOWN BECAUSE IT WAS NEEDED TWICE

    git log --oneline -- <file>          # find the last good commit
    git show <sha>:<file> > <file>       # restore it
    python3 _dev/ship.py --to american   # re-decorate

Check more than one commit back. The watcher commits every minute, so the
truncated version is usually already in HEAD and HEAD~1.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

FLOOR = 4096

# Genuinely small by design. Named, not detected - a stub that empties should
# still fail.
STUBS = {"tools.html"}

# Not published pages, and deliberately without the site chrome: two design
# mockups (both noindex, follow - see _dev/social_cards.py) and one redirect
# stub whose whole job is to be a single sentence pointing at resources.html.
# They still have to be non-empty and still have to have a title; they are only
# exempt from needing a masthead and an h1.
NO_CHROME = {"tycoon.html", "concepts.html", "tools.html"}


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    bad = []
    smallest = []
    n = 0
    for rel in pages():
        p = os.path.join(SITE, rel)
        size = os.path.getsize(p)
        base = os.path.basename(rel)
        s = open(p, encoding="utf-8", errors="replace").read()
        n += 1
        smallest.append((size, rel))

        if size == 0:
            bad.append("%s is EMPTY" % rel)
            continue
        if base not in STUBS and size < FLOOR:
            bad.append("%s is %d bytes, under the %d floor" % (rel, size, FLOOR))
        checks = [("<title>", "<title>" in s.lower())]
        if base not in NO_CHROME:
            checks += [("an <h1>", "<h1" in s.lower()),
                       ("a masthead", "sitenav" in s)]
        for what, ok in checks:
            if not ok:
                bad.append("%s has no %s" % (rel, what))

    smallest.sort()
    print("smoke test: %d published page(s), floor %d bytes" % (n, FLOOR))
    for size, rel in smallest[:3]:
        print("  smallest: %-52s %s bytes" % (rel[:50], format(size, ",d")))

    if bad:
        for b in bad:
            print("GUARD %s" % b)
        print("\nA page has been truncated or emptied. This is almost always a "
              "pass interrupted mid-write - a timeout, or two pipeline runs at "
              "once. Restore it before anything else:")
        print("  git log --oneline -- <file>")
        print("  git show <sha>:<file> > <file>      # check 2-3 commits back")
        print("  python3 _dev/ship.py --to american")
        sys.exit("\n%d problem(s)" % len(bad))
    print("guards clean - every published page has a title, an h1, the "
          "masthead, and real bytes behind it")


if __name__ == "__main__":
    main()
