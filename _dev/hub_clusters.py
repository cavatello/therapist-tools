#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keep every topic hub's cluster sections identical to what the registry says.

WHY THIS EXISTS, AND WHY IT IS NOT A HAND-MAINTAINED INDEX

`mock/library/build_library.py` renders all the hubs from
`mock/library/registry.json`. It cannot simply be run against the live site:
its output is the *undecorated* hub, roughly 14KB per page smaller than what is
published, because forty-odd `_dev/` passes have since written into those
pages. Copying whole regenerated hubs over the live ones would silently delete
every one of those decorations - which is not hypothetical. It happened once,
to the "Key insights" block on all five hubs, and no guard noticed.

So this pass takes the narrowest possible slice. It lifts *only* the cluster
sections from the generator's output and syncs the live hub to them, replacing
sections that exist and inserting sections that do not, in the generator's
order. Everything outside a cluster section is left exactly as it was found.

Nothing is authored here. If a card's title, outcome or figure changes, or the
card format changes, the next run picks the change up. That is the whole point:
a hand-written card that drifts from the generator is exactly the failure the
registry was built to end. It supersedes `_dev/hub_assocpay_link.py`, which did
this for one section of one hub and is now a no-op.

WHAT IS NOT A CLUSTER, AND IS NEVER TOUCHED

  - `#tools`, written by `_dev/hub_hero.py` on the live page.
  - `#elsewhere`, the cross-topic footer.
  - The "Key insights" block from `_dev/hub_owid.py`, which sits between
    sections rather than inside one. The guard at the foot of this file counts
    it before and after, because that is the block this project has already
    lost once.

RUN ORDER

After the builders - the registry describes pages that must already exist - and
after `_dev/taxonomy_leaves.py`, which edits the registry. Before
`_dev/uplinks.py` and `_dev/breadcrumbs.py`, which read the hub's links. The
pass runs the generator itself rather than trusting whatever is on disk,
because taxonomy_leaves runs immediately before it.

Idempotent, guarded.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

REGISTRY = os.path.join(SITE, "mock", "library", "registry.json")
GENERATOR = os.path.join(SITE, "mock", "library", "build_library.py")
OUT = os.path.join(SITE, "mock", "library", "out")

# Emitted around the clusters by the generator, and owned elsewhere.
NOT_CLUSTERS = ("tools", "elsewhere")

SECT = r'<section class="sec[^"]*"><h2 id="%s">[\s\S]*?</section>'
ANY_SECT = (r'<section class="sec[^"]*"><h2 id="([a-z0-9-]+)">[\s\S]*?'
            r'</section>')

# The decoration this pass must not disturb. Counted before and after.
DECORATIONS = (("a Key insights card", r'<div class="ins">'),
               ("a what-you-should-know disclosure", r'<details class="ysk">'),
               ("an h1", r"<h1"))


def sections(html):
    """(id, markup) for every cluster section, in document order."""
    return [(m.group(1), m.group(0))
            for m in re.finditer(ANY_SECT, html)
            if m.group(1) not in NOT_CLUSTERS]


def regenerate():
    if not os.path.exists(GENERATOR):
        sys.exit("hub_clusters: mock/library/build_library.py is missing, and "
                 "this pass has nothing to lift from")
    r = subprocess.run([sys.executable, GENERATOR], cwd=SITE,
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.stdout.write(r.stdout)
        sys.stdout.write(r.stderr)
        sys.exit("hub_clusters: build_library.py failed, so the sections this "
                 "pass would insert are unknown. Nothing was written.")


def sync(topic):
    """Returns (replaced, inserted, problems)."""
    hub = os.path.join(SITE, topic, "index.html")
    gen = os.path.join(OUT, topic, "index.html")
    if not os.path.exists(hub):
        # A topic in the registry with no published hub is a registry problem,
        # not this pass's to fix - but it must not pass silently.
        return 0, 0, ["%s is in registry.json and %s/index.html does not exist"
                      % (topic, topic)]
    if not os.path.exists(gen):
        return 0, 0, ["the generator produced no %s hub" % topic]

    g = open(gen, encoding="utf-8").read()
    s = open(hub, encoding="utf-8").read()
    orig = s

    before = {label: len(re.findall(pat, s)) for label, pat in DECORATIONS}

    want = sections(g)
    if not want:
        return 0, 0, ["the generated %s hub has no cluster sections at all, "
                      "which means build_library.py changed its markup and "
                      "this pass is matching the wrong thing" % topic]

    have = dict(sections(s))
    replaced = inserted = 0

    for sid, markup in want:
        if sid in have and have[sid] != markup:
            s = re.sub(SECT % re.escape(sid), lambda m: markup, s, count=1)
            replaced += 1

    for i, (sid, markup) in enumerate(want):
        if sid in have:
            continue
        # Place a new cluster before the first following section that already
        # exists, so it lands where the registry puts it rather than wherever
        # is easiest to match.
        after = next((x for x, _ in want[i + 1:] if x in have), None)
        if after:
            anchor = re.search(SECT % re.escape(after), s)
            if not anchor:
                return replaced, inserted, [
                    "cannot place #%s on the %s hub - its follower #%s "
                    "vanished between two reads of the same file"
                    % (sid, topic, after)]
            s = s[:anchor.start()] + markup + s[anchor.start():]
        else:
            last = next((x for x, _ in reversed(want[:i]) if x in have), None)
            if not last:
                return replaced, inserted, [
                    "#%s would be the only cluster on the %s hub and the page "
                    "has none. Regenerate that hub properly instead."
                    % (sid, topic)]
            anchor = re.search(SECT % re.escape(last), s)
            s = s[:anchor.end()] + markup + s[anchor.end():]
        have[sid] = markup
        inserted += 1

    # ------------------------------------------------- check before writing
    problems = []
    after = {label: len(re.findall(pat, s)) for label, pat in DECORATIONS}
    for label, n in before.items():
        if after[label] != n:
            problems.append("%s: %d %s before, %d after - this pass has eaten "
                            "a decoration and will not write"
                            % (topic, n, label, after[label]))
    if problems:
        return 0, 0, problems

    if s != orig:
        open(hub, "w", encoding="utf-8").write(s)
    return replaced, inserted, []


def verify(topic, reg):
    problems = []
    hub = os.path.join(SITE, topic, "index.html")
    gen = os.path.join(OUT, topic, "index.html")
    if not os.path.exists(hub) or not os.path.exists(gen):
        return ["%s: nothing to verify" % topic]
    s = open(hub, encoding="utf-8").read()
    g = open(gen, encoding="utf-8").read()

    got = [x for x, _ in sections(s)]
    want = [x for x, _ in sections(g)]
    if got != want:
        problems.append("%s: the hub's clusters are %s, the registry says %s"
                        % (topic, got, want))
    for sid in want:
        n = len(re.findall(r'id="%s"' % re.escape(sid), s))
        if n != 1:
            problems.append("%s: %d sections with id=%r" % (topic, n, sid))
    if s.count("<h1") != 1:
        problems.append("%s: %d h1 on the hub" % (topic, s.count("<h1")))

    # A section nested inside another renders, and breaks the hub's
    # alternating background and its in-page navigation. Valid markup, wrong
    # place, no error - the failure this project has shipped before.
    if re.search(r'<section class="sec[^"]*">(?:(?!</section>).)*'
                 r'<section class="sec', s, re.S):
        problems.append("%s: a hub section is nested inside another" % topic)

    for c in reg["topics"][topic]["clusters"]:
        for f in c["files"]:
            if 'href="../%s"' % f not in s:
                problems.append("%s: %s is in the registry's clusters and is "
                                "not linked from the hub" % (topic, f))
    return problems


def main():
    if not os.path.exists(REGISTRY):
        sys.exit("hub_clusters: registry.json is missing")
    reg = json.load(open(REGISTRY, encoding="utf-8"))

    regenerate()

    topics = [t for t in reg["topics"]
              if os.path.exists(os.path.join(SITE, t, "index.html"))]
    if not topics:
        sys.exit("hub_clusters: the registry names %d topics and none of them "
                 "has a published hub" % len(reg["topics"]))

    total_r = total_i = 0
    problems = []
    for t in topics:
        r, i, p = sync(t)
        total_r += r
        total_i += i
        problems += p
        if r or i:
            print("  %-13s %d refreshed, %d inserted" % (t, r, i))

    for t in topics:
        problems += verify(t, reg)

    if total_r or total_i:
        print("%d cluster section(s) refreshed, %d inserted across %d hub(s)"
              % (total_r, total_i, len(topics)))
    else:
        print("%d hub(s) already current" % len(topics))

    if problems:
        for p in problems:
            print("GUARD:", p)
        sys.exit("\n%d problem(s)" % len(problems))

    n_clusters = sum(len(reg["topics"][t]["clusters"]) for t in topics)
    print("guards clean - %d hub(s), %d clusters, in the order registry.json "
          "defines, every file linked once, every decoration intact"
          % (len(topics), n_clusters))


if __name__ == "__main__":
    main()
