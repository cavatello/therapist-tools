#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RETIRED on 10 August 2026 - the hubs are generated from registry.json now.

This pass existed as a bridge across a builder that could not be run against
the live site. `mock/library/build_library.py` was fixed, its output was
checked and copied over all nine library pages, and the licensure hub now
renders the "Counting the hours, and the job that banks them" cluster itself.
The bridge has nothing left to carry, and on the first run after the hubs were
regenerated it failed loudly rather than silently double-inserting - which is
the behaviour its anchor guard was written for.

`_dev/hub_clusters.py` now does this continuously, for every cluster on
every topic hub, on the same principle - lift the sections from the
generator's output, never author them - with the guard this one lacked: it
counts the decorations that live BETWEEN sections and refuses to write if a
sync would eat one. Losing the Key insights block from all five hubs is not
hypothetical; it happened, and nothing noticed.

Left in the tree rather than deleted, like the four `hub_*_link.py` passes
before it, because the reasoning is the useful part.

ORIGINAL HEADER FOLLOWS.

One cluster section onto the licensure hub, by hand, for one reason.

WHY THIS EXISTS WHEN THE HUBS ARE SUPPOSED TO BE GENERATED

They are. `mock/library/build_library.py` renders all nine index pages from
`mock/library/registry.json`, and the four `_dev/hub_*_link.py` passes that
predate it are all retired with a note saying so. This one is not a fifth
hand-maintained index; it is a bridge across a builder that cannot currently
be run against the live site.

The state of that builder, as of this pass:

  - Its `SITE` was `mock/../stage2`, left over from a layout the repo has since
    flattened, so **every run since the flattening died on a missing path.**
    That is now fixed, and it runs.
  - It writes to `mock/library/out/`, never to the site, so running it is safe.
  - But its output is the *undecorated* hub - about 14KB smaller per page than
    what is live, because forty-odd `_dev/` passes have since written into
    those pages. Copying nine regenerated hubs over the live ones and
    re-running the pipeline is a real change to five of the site's most
    important pages, and it cannot be checked in a browser from here while
    file staging is down.

So: the builder stays fixed and unused, this pass inserts the ONE section the
builder would have added, and the hub regeneration is a separate job with its
own verification. When that job happens, this pass becomes a no-op and should
be retired like its four predecessors.

WHAT IT INSERTS

Not authored markup - the exact section `build_library.py` emitted for this
page, lifted from `mock/library/out/licensure/index.html` at run time rather
than pasted in as a literal. That is the whole point: if the card format
changes, or the page's title, outcome or `ts:number` changes, this pass picks
the change up on the next run instead of freezing one day's rendering into a
Python string.

If the generated file is missing, the pass says how to regenerate it and stops.
It does not fall back to a hand-written card, because a hand-written card that
drifts from the generator is exactly the failure the registry was built to end.

Idempotent, guarded.
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
