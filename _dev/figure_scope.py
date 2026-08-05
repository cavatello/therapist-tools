#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stop figure styling leaking onto prose in the same block.

The live cost-of-living hero styles its three figures with a bare descendant
selector, `.clbig b`. The same block also holds the worked-example caption:

    <p class="cleg" id="bigeg">Worked example: California statewide, one adult,
    an $85,000 AGI on RAP and a $6,000 monthly take-home.
    <b>Change anything below and all three move.</b></p>

That `<b>` is prose. `.clbig b` caught it, so on the live site a 41-character
sentence renders in **Fraunces at 36px** on desktop and 26px on a phone - larger
than the labels beside the figures, and reading as a fourth headline in a block
that is supposed to have three numbers and a footnote. The author had already
written `.cleg b{color:#DCEAE3;font-weight:600}`, which only sets colour and
weight, so nothing ever contradicted the size.

This is the same defect as `claude/cola-hero-overflow.md`, wearing different
clothes. There the shared rule also carried `white-space:nowrap`, so the symptom
was a 406px sentence in a 390px viewport and it showed up as overflow. Here
there is no nowrap, the sentence wraps, and nothing overflows - so
`nowrap-audit.mjs` passes the page cleanly while the bug is plainly visible.
Overflow was never the defect. **The defect is a figure selector that also
matches prose**, and it has to be detected as that.

The fix is the one `build_cola.py` already applies to the Option 3 build:
scope the figure rules to the row, `.clbig > div > b`. Applied here as a pass
because the deployed cost-of-living page is NOT the current builder's output -
Option 3 has never shipped - so patching the builder alone would leave the live
page wrong indefinitely.

Table-driven and explicit: it will not go looking for selectors to rewrite.

Idempotent. Run before linkcheck.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

# page -> [(bare selector as written, scoped replacement)]
REWRITES = {
    "therapist-cost-of-living-california.html": [
        (".clbig b{", ".clbig > div > b{"),
        (".clbig em{", ".clbig > div > em{"),
    ],
}


def main():
    changed = 0
    for slug, pairs in sorted(REWRITES.items()):
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            print("%-44s MISSING" % slug)
            continue
        s = open(path, encoding="utf-8").read()
        did = []
        for bare, scoped in pairs:
            if scoped in s and bare not in s:
                continue                      # already done
            n = s.count(bare)
            if n == 0:
                print("%-44s %r not present - skipped" % (slug, bare))
                continue
            if n > 1:
                sys.exit("%s: %r appears %d times; refusing to guess" % (slug, bare, n))
            s = s.replace(bare, scoped, 1)
            did.append(bare)
        if did:
            open(path, "w", encoding="utf-8").write(s)
            changed += 1
            print("%-44s scoped %s" % (slug, ", ".join(did)))
        else:
            print("%-44s already scoped" % slug)

    bad = 0
    for slug, pairs in REWRITES.items():
        path = os.path.join(SITE, slug)
        if not os.path.exists(path):
            continue
        s = open(path, encoding="utf-8").read()
        for bare, scoped in pairs:
            if bare in s:
                print("GUARD %s: bare %r survives" % (slug, bare)); bad += 1
    if bad:
        sys.exit("figure_scope: %d guard failure(s)" % bad)
    print("%d page(s) rescoped" % changed)


if __name__ == "__main__":
    main()
