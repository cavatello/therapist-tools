#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bring the licensure hub's cluster sections back in line with the registry.

WHY THIS EXISTS, AND WHY IT IS NOT A HAND-MAINTAINED INDEX

`mock/library/build_library.py` renders all nine hubs from
`mock/library/registry.json`. It cannot be run against the live site: its
output is the *undecorated* hub, roughly 14KB per page smaller than what is
published, because forty-odd `_dev/` passes have since written into those
pages. Copying nine regenerated hubs over the live ones is a real change to
the site's most important pages and belongs in its own job with its own
verification.

`_dev/hub_assocpay_link.py` bridged that gap once, for one section. This is
the same idea widened to the whole licensure hub, and written to be run again:
it lifts every cluster section from the generator's output and syncs the live
hub to it - replacing sections that exist, inserting sections that do not, in
the generator's order.

Nothing is authored here. If a card's title, outcome or figure changes, or the
card format changes, the next run picks the change up. That is the whole point:
a hand-written card that drifts from the generator is exactly the failure the
registry was built to end.

RUN ORDER

After the builders (the pages must exist for the registry to describe them)
and before `_dev/uplinks.py` and `_dev/breadcrumbs.py`, which read the hub's
links. `mock/library/build_library.py` must have been run since the registry
last changed; this pass says so and stops if the output is missing.

Idempotent, guarded.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

TOPIC = "licensure"
HUB = os.path.join(SITE, TOPIC, "index.html")
GEN = os.path.join(SITE, "mock", "library", "out", TOPIC, "index.html")

# The generator emits these two around the clusters. They are not clusters and
# must not be touched: "tools" is built by _dev/hub_hero.py on the live page
# and "elsewhere" is the cross-topic footer.
NOT_CLUSTERS = ("tools", "elsewhere")

SECT = r'<section class="sec[^"]*"><h2 id="%s">[\s\S]*?</section>'


def sections(html):
    """(id, markup) for every cluster section, in document order."""
    out = []
    for m in re.finditer(r'<section class="sec[^"]*"><h2 id="([a-z0-9-]+)">'
                         r'[\s\S]*?</section>', html):
        if m.group(1) not in NOT_CLUSTERS:
            out.append((m.group(1), m.group(0)))
    return out


def main():
    if not os.path.exists(HUB):
        sys.exit("hub_clusters: the %s hub is missing" % TOPIC)
    if not os.path.exists(GEN):
        sys.exit("hub_clusters: %s is missing.\n"
                 "  Regenerate it first:  python3 mock/library/build_library.py\n"
                 "  It writes only to mock/library/out/ and cannot touch the "
                 "live site." % os.path.relpath(GEN, SITE))

    gen = open(GEN, encoding="utf-8").read()
    s = open(HUB, encoding="utf-8").read()
    orig = s

    want = sections(gen)
    if not want:
        sys.exit("hub_clusters: the generated hub has no cluster sections at "
                 "all, which means build_library.py changed its markup and "
                 "this pass is matching the wrong thing")

    have = dict(sections(s))
    replaced = inserted = 0

    # Replace what exists, in place, so the page's order is not disturbed.
    for sid, markup in want:
        if sid in have:
            if have[sid] != markup:
                s = re.sub(SECT % re.escape(sid), lambda m: markup, s, count=1)
                replaced += 1

    # Insert what does not, before the first following section that does
    # exist - so a new cluster lands where the registry puts it rather than
    # wherever is easiest to match.
    for i, (sid, markup) in enumerate(want):
        if sid in have:
            continue
        after = None
        for later_id, _ in want[i + 1:]:
            if later_id in have:
                after = later_id
                break
        if after:
            anchor = re.search(SECT % re.escape(after), s)
            if not anchor:
                sys.exit("hub_clusters: cannot place #%s - its follower #%s "
                         "vanished between two reads of the same file" % (sid, after))
            s = s[:anchor.start()] + markup + s[anchor.start():]
        else:
            # No following cluster on the page: put it after the last one.
            last = None
            for prev_id, _ in reversed(want[:i]):
                if prev_id in have:
                    last = prev_id
                    break
            if not last:
                sys.exit("hub_clusters: #%s is the only cluster and the hub "
                         "has none. Regenerate the hub properly instead." % sid)
            anchor = re.search(SECT % re.escape(last), s)
            s = s[:anchor.end()] + markup + s[anchor.end():]
        have[sid] = markup
        inserted += 1

    if s != orig:
        open(HUB, "w", encoding="utf-8").write(s)
        print("%s hub: %d cluster section(s) refreshed, %d inserted"
              % (TOPIC, replaced, inserted))
    else:
        print("%s hub: already current" % TOPIC)

    # --------------------------------------------------------------- guards
    bad = 0
    s = open(HUB, encoding="utf-8").read()
    got = sections(s)
    got_ids = [x for x, _ in got]
    want_ids = [x for x, _ in want]

    if got_ids != want_ids:
        print("GUARD: the hub's clusters are %s, the registry says %s"
              % (got_ids, want_ids))
        bad += 1

    for sid in want_ids:
        n = len(re.findall(r'id="%s"' % re.escape(sid), s))
        if n != 1:
            print("GUARD: %d sections with id=%r" % (n, sid))
            bad += 1

    if s.count("<h1") != 1:
        print("GUARD: %d h1 on the hub" % s.count("<h1"))
        bad += 1

    # A section nested inside another renders and breaks the hub's alternating
    # background and its in-page navigation. Valid markup, wrong place, no
    # error - the failure this project has shipped before.
    if re.search(r'<section class="sec[^"]*">(?:(?!</section>).)*'
                 r'<section class="sec', s, re.S):
        print("GUARD: a hub section is nested inside another")
        bad += 1

    # Every page the registry puts in this topic must be reachable from it.
    import json
    reg = json.load(open(os.path.join(SITE, "mock", "library",
                                      "registry.json"), encoding="utf-8"))
    for c in reg["topics"][TOPIC]["clusters"]:
        for f in c["files"]:
            if 'href="../%s"' % f not in s:
                print("GUARD: %s is in the registry's %s clusters and is not "
                      "linked from the hub" % (f, TOPIC))
                bad += 1

    if bad:
        sys.exit("\n%d problem(s)" % bad)
    print("guards clean - %d clusters, in the order registry.json defines, "
          "every file linked once" % len(got_ids))


if __name__ == "__main__":
    main()
