#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RETIRED. Superseded by `_dev/hub_clusters.py` on 10 August 2026.

This pass inserted one cluster section into one hub, lifted from
`mock/library/build_library.py`'s output, as a bridge across a generator that
could not be run against the live site. Its own docstring said it should be
retired once the hub regeneration was done properly.

`_dev/hub_clusters.py` does that job for every topic hub at once, on the same
principle - lift the cluster sections from the generator, never author them -
and adds the guard this one did not have: it counts the decorations that live
between sections, and refuses to write if a sync would eat one. That is the
failure this project has already had, when regenerating hubs silently deleted
the Key insights block from all five and nothing noticed.

Running this now would insert a section `hub_clusters.py` already maintains,
so it exits without touching anything. The original is kept below the exit for
the reasoning in it, which is still the reasoning behind its replacement.
"""
import sys

sys.exit("hub_assocpay_link: retired - _dev/hub_clusters.py maintains this "
         "section, and every other cluster section on every hub. Nothing was "
         "written.")

# --------------------------------------------------------------------------
# The original, kept for the argument it makes and not to be run.

"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

HUB = os.path.join(SITE, "licensure", "index.html")
GEN = os.path.join(SITE, "mock", "library", "out", "licensure", "index.html")
PAGE = "associate-therapist-pay-los-angeles-bay-area.html"
SECT_ID = "counting-the-hours-and-the-job-that-banks-them"

# The section this one goes before, so the hub's order matches the cluster
# order in registry.json rather than landing wherever is easiest to match.
BEFORE = '<section class="sec alt"><h2 id="where-the-degree-comes-from">'


def generated_section():
    """The section as build_library.py rendered it, read from its output."""
    if not os.path.exists(GEN):
        sys.exit("hub_assocpay_link: %s is missing.\n"
                 "  Regenerate it first:  python3 mock/library/build_library.py\n"
                 "  It writes only to mock/library/out/ and cannot touch the "
                 "live site." % os.path.relpath(GEN, SITE))
    g = open(GEN, encoding="utf-8").read()
    m = re.search(r'<section class="sec alt"><h2 id="%s">[\s\S]*?</section>'
                  % re.escape(SECT_ID), g)
    if not m:
        sys.exit("hub_assocpay_link: the generated hub has no #%s section. "
                 "Either the cluster was renamed in registry.json - update "
                 "SECT_ID - or registry_sync.py has not run since the page "
                 "was built." % SECT_ID)
    sect = m.group(0)
    if PAGE not in sect:
        sys.exit("hub_assocpay_link: the generated section does not link %s, "
                 "so it is not the section this pass is for" % PAGE)
    return sect


def main():
    print("hub_assocpay_link.py: retired - the licensure hub is generated "
          "from registry.json and carries this cluster itself")
    sys.exit(0)

    if not os.path.exists(os.path.join(SITE, PAGE)):
        sys.exit("hub_assocpay_link: %s does not exist - run "
                 "_dev/build_assocpay.py first" % PAGE)
    if not os.path.exists(HUB):
        sys.exit("hub_assocpay_link: the licensure hub is missing")

    sect = generated_section()
    s = open(HUB, encoding="utf-8").read()
    orig = s

    # Remove any previous copy of this section before re-inserting, so a
    # changed title or figure replaces the old card rather than joining it.
    s = re.sub(r'<section class="sec alt"><h2 id="%s">[\s\S]*?</section>'
               % re.escape(SECT_ID), "", s)

    if s.count(BEFORE) != 1:
        sys.exit("hub_assocpay_link: the anchor section matched %d times, "
                 "expected 1. The hub's structure has changed; do not guess a "
                 "new insertion point - regenerate the hub properly instead."
                 % s.count(BEFORE))
    s = s.replace(BEFORE, sect + BEFORE, 1)

    if s != orig:
        open(HUB, "w", encoding="utf-8").write(s)
        print("licensure hub: the cluster section inserted, %d bytes, lifted "
              "from the generator" % len(sect))
    else:
        print("licensure hub: already current")

    # --------------------------------------------------------------- guards
    bad = 0
    s = open(HUB, encoding="utf-8").read()

    n = s.count('href="../%s"' % PAGE)
    if n != 1:
        print("GUARD: %d links to the page on the hub, expected 1" % n)
        bad += 1
    if s.count('id="%s"' % SECT_ID) != 1:
        print("GUARD: %d sections with id=%r"
              % (s.count('id="%s"' % SECT_ID), SECT_ID))
        bad += 1
    if s.count("<h1") != 1:
        print("GUARD: %d h1 on the hub" % s.count("<h1"))
        bad += 1

    # A section nested inside another would render but would break the hub's
    # alternating background and its in-page navigation. This is the failure
    # this project has shipped before: valid markup, wrong place, no error.
    if re.search(r'<section class="sec[^"]*">(?:(?!</section>).)*'
                 r'<section class="sec', s, re.S):
        print("GUARD: a hub section is nested inside another")
        bad += 1

    # The card must sit inside a card grid, or it renders full-bleed and
    # unlike every one of its neighbours.
    m = re.search(r'<section class="sec alt"><h2 id="%s">[\s\S]*?</section>'
                  % re.escape(SECT_ID), s)
    if m and '<div class="lcg">' not in m.group(0):
        print("GUARD: the section has no .lcg card grid")
        bad += 1

    # And the order the hub presents its clusters in has to match the order
    # registry.json defines them in, or the pass has quietly reordered the
    # page while adding to it.
    order = [x for x in re.findall(r'<h2 id="([a-z0-9-]+)"', s)
             if x in ("tools", "the-route-and-what-it-costs", SECT_ID,
                      "where-the-degree-comes-from")]
    want = ["tools", "the-route-and-what-it-costs", SECT_ID,
            "where-the-degree-comes-from"]
    if order != want:
        print("GUARD: the hub's sections are in the order %s, expected %s"
              % (order, want))
        bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - one card, one section, in the order registry.json "
          "defines")


if __name__ == "__main__":
    main()

"""
