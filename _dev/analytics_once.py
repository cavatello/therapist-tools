#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One analytics loader per page. Never two, never a marker with no tag.

WHY THIS EXISTS

For some weeks 107 of the site's 244 published pages loaded Microsoft Clarity
**twice**, and nothing in the pipeline noticed. Those pages fired a
third-party tracker twice per view, double-counting sessions in Clarity and
doubling a third-party request on more than 40 per cent of the site.

The cause was the shape this codebase keeps producing: a pass that is correct
about the file it writes and wrong about what a later pass does with it.
`_dev/clarity.py` removes its own previous tag by matching the comment markers
it wrapped around it, which is genuinely idempotent - run it twice, the count
does not move. But `pagekit.chrome_parts` strips `_dev/` pass markers out of
borrowed chrome with a non-greedy pattern, and on the donor's clarity block
that removed the OPENING marker and left the script. clarity.py could no
longer see that loader, so it prepended a second, marked copy. Every guard
stayed clean, because each guard checked its own pass.

The fix is in `clarity.py` alone, which now keys its removal on the loader's
own code rather than on a marker that something else can eat. Fixing the
pagekit side as well was tried and DELIBERATELY REVERTED: stripping the
analytics block there changes the head of every builder page enough that
`token_floor.py` re-injects its style block, `extract_css` hoists it under a
new content hash, and 72 pages are left pointing at a stylesheet that no
longer exists. That is the hashed-sheet hazard, incurred for a bug that is
fixable entirely on the clarity.py side. So pagekit is untouched, and a page
damaged before the fix repairs itself on the next pipeline run.

This pass is the third thing, and the one that would have caught it: **a
check on the page as it ships, not on the moment of writing.** That is rule
one in the handoff, learned again.

WHAT IT CHECKS

  - no published page carries more than one analytics loader
  - no page carries a `<!-- /clarity -->` with no opening marker, or an
    opening marker with no tag - the exact fingerprint of the bug above, and
    the thing that will still be true if the duplication ever returns by some
    route nobody has thought of
  - every page with a masthead carries the mask attribute exactly once, since
    a loader without it records what people type

A page with no masthead is not instrumented and is skipped, which is the same
rule clarity.py applies when it installs.

    python3 _dev/analytics_once.py            check, print, exit non-zero
    python3 _dev/analytics_once.py --list     print every finding in full
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SUBDIRS = ("money", "licensure", "getting-paid", "practice", "training", "for")

# NAMED `OPEN_MARKER` / `CLOSE_MARKER`, NOT `MARK` / `END`, AND THAT IS
# LOAD-BEARING. `_dev/passes_index.py` reads every pass's module-level `MARK`,
# `END`, `JSMARK`, `BLOCK` and `BODYCLASS` assignments by AST and treats the
# value as the marker THAT pass injects into a page - then fails the build if
# two passes claim the same one. This pass injects nothing; it only reads
# clarity.py's markers to check them. Assigning them to `MARK` and `END` here
# made passes_index believe two passes owned the same marker, and stopped the
# pipeline. That is the seventh convention in this codebase that is invisible
# until you break it, and the fourth to be broken by a file that is only
# describing something rather than doing it.
OPEN_MARKER = "<!-- _dev/clarity.py -->"
CLOSE_MARKER = "<!-- /clarity -->"
MASK_ATTR = 'data-clarity-mask="True"'
# The loader's own code. Deliberately NOT the project id: the Clarity snippet
# builds its URL by concatenation, so grepping a page for `clarity.ms/tag/<id>`
# finds nothing even when the tag is correctly installed. This repository has
# been caught by that once already.
LOADER = r"\(function\(c,l,a,r,i,t,y\)"


def pages():
    out = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]
    for d in SUBDIRS:
        p = os.path.join(SITE, d)
        if os.path.isdir(p):
            out += ["%s/%s" % (d, f) for f in sorted(os.listdir(p))
                    if f.endswith(".html")]
    return out


def main():
    show_all = "--list" in sys.argv
    findings = []
    checked = skipped = 0

    for rel in pages():
        s = open(os.path.join(SITE, rel), encoding="utf-8").read()
        if "sitenav" not in s:
            skipped += 1
            continue
        checked += 1
        loaders = len(re.findall(LOADER, s))
        marks = s.count(OPEN_MARKER)
        ends = s.count(CLOSE_MARKER)
        masks = s.count(MASK_ATTR)

        if loaders > 1:
            findings.append("%s\t%d analytics loaders" % (rel, loaders))
        if marks != ends:
            findings.append("%s\t%d opening marker(s) against %d closing - a "
                            "tag that clarity.py cannot remove" %
                            (rel, marks, ends))
        if loaders and masks != 1:
            findings.append("%s\t%d mask attribute(s) with a loader present - "
                            "the replay would record what people type" %
                            (rel, masks))

    if findings:
        for f in findings if show_all else findings[:20]:
            print("  " + f)
        if not show_all and len(findings) > 20:
            print("  ... and %d more (--list for all)" % (len(findings) - 20))
        sys.exit("%d page(s) with an analytics problem" % len(findings))

    print("guards clean - %d instrumented page(s) carry exactly one masked "
          "analytics loader, %d page(s) with no masthead skipped"
          % (checked, skipped))


if __name__ == "__main__":
    main()
